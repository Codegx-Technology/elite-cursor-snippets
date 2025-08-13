import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import logging

# Adjust path for imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import SessionLocal, Base, engine
from auth.user_models import User, Tenant, AuditLog
from logging_setup import setup_logging, get_audit_logger, DatabaseAuditHandler

# --- Fixtures ---

@pytest.fixture(scope="module")
def db_session():
    """Create a test database session."""
    # Use an in-memory SQLite database for testing
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=test_engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine) # Clean up after tests

@pytest.fixture(scope="function")
def setup_audit_logger(db_session):
    """Set up the audit logger to use the test database."""
    # Clear existing handlers to prevent interference
    audit_logger = logging.getLogger('audit')
    audit_logger.handlers = []
    audit_logger.propagate = False # Ensure it doesn't send to root logger

    # Add our custom DatabaseAuditHandler
    db_handler = DatabaseAuditHandler()
    audit_logger.addHandler(db_handler)
    audit_logger.setLevel(logging.INFO) # Set level for testing

    # Ensure the global _last_audit_log_hash is reset for each test
    with patch('logging_setup._last_audit_log_hash', "0" * 64):
        yield audit_logger
    
    # Clean up handler after test
    audit_logger.removeHandler(db_handler)

@pytest.fixture(scope="function")
def test_user(db_session):
    """Create a dummy user for testing audit logs."""
    tenant = Tenant(name="test_tenant")
    db_session.add(tenant)
    db_session.commit()
    db_session.refresh(tenant)

    user = User(username="audit_user", email="audit@example.com", hashed_password="hashed_password", tenant_id=tenant.id)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

# --- Tests for AuditLog Model ---

def test_audit_log_hash_calculation():
    """Test that the hash calculation is consistent and changes with data."""
    log1 = AuditLog(
        timestamp=datetime(2023, 1, 1, 10, 0, 0),
        user_id=1,
        event_type="login",
        message="User logged in."
    )
    log1.set_hash("0" * 64)
    hash1 = log1.current_hash

    log2 = AuditLog(
        timestamp=datetime(2023, 1, 1, 10, 0, 0),
        user_id=1,
        event_type="login",
        message="User logged in."
    )
    log2.set_hash("0" * 64)
    hash2 = log2.current_hash

    assert hash1 == hash2 # Same data, same previous hash -> same current hash

    log3 = AuditLog(
        timestamp=datetime(2023, 1, 1, 10, 0, 1), # Different timestamp
        user_id=1,
        event_type="login",
        message="User logged in."
    )
    log3.set_hash("0" * 64)
    hash3 = log3.current_hash

    assert hash1 != hash3 # Different data -> different hash

def test_audit_log_chaining(db_session):
    """Test that audit logs are chained correctly."""
    log1 = AuditLog(
        timestamp=datetime.utcnow(),
        user_id=1,
        event_type="event1",
        message="First event."
    )
    log1.set_hash("0" * 64)
    db_session.add(log1)
    db_session.commit()
    db_session.refresh(log1)

    log2 = AuditLog(
        timestamp=datetime.utcnow(),
        user_id=1,
        event_type="event2",
        message="Second event."
    )
    log2.set_hash(log1.current_hash)
    db_session.add(log2)
    db_session.commit()
    db_session.refresh(log2)

    assert log2.previous_hash == log1.current_hash
    assert log2.current_hash != log1.current_hash # Should be different as data is different

# --- Tests for DatabaseAuditHandler ---

def test_database_audit_handler_writes_to_db(db_session, setup_audit_logger, test_user):
    """Test that DatabaseAuditHandler writes log records to the database."""
    audit_logger = setup_audit_logger
    
    message = "User logged in successfully."
    audit_logger.info(message, extra={'user_id': test_user.id})

    # Verify log entry in DB
    logs = db_session.query(AuditLog).all()
    assert len(logs) == 1
    assert logs[0].message == message
    assert logs[0].user_id == test_user.id
    assert logs[0].event_type == "INFO"
    assert logs[0].previous_hash == "0" * 64 # First log, so initial hash

def test_database_audit_handler_chains_hashes(db_session, setup_audit_logger, test_user):
    """Test that subsequent log entries have correct previous_hash."""
    audit_logger = setup_audit_logger

    # First log
    audit_logger.info("First audit event.", extra={'user_id': test_user.id})
    first_log = db_session.query(AuditLog).filter_by(message="First audit event.").first()
    assert first_log is not None
    assert first_log.previous_hash == "0" * 64

    # Second log
    audit_logger.warning("Second audit event.", extra={'user_id': test_user.id})
    second_log = db_session.query(AuditLog).filter_by(message="Second audit event.").first()
    assert second_log is not None
    assert second_log.previous_hash == first_log.current_hash

def test_database_audit_handler_handles_no_user_id(db_session, setup_audit_logger):
    """Test that logs without user_id are handled."""
    audit_logger = setup_audit_logger
    audit_logger.error("System error occurred.")

    logs = db_session.query(AuditLog).all()
    assert len(logs) == 1
    assert logs[0].message == "System error occurred."
    assert logs[0].user_id is None

def test_database_audit_handler_integrity_check(db_session, setup_audit_logger, test_user):
    """
    Test a basic integrity check by re-calculating hashes.
    This simulates a tamper detection mechanism.
    """
    audit_logger = setup_audit_logger

    # Log a few entries
    audit_logger.info("Event A.", extra={'user_id': test_user.id})
    audit_logger.info("Event B.", extra={'user_id': test_user.id})
    audit_logger.info("Event C.", extra={'user_id': test_user.id})

    # Retrieve logs in order
    logs = db_session.query(AuditLog).order_by(AuditLog.id).all()
    assert len(logs) == 3

    # Verify chain integrity
    is_tampered = False
    calculated_hash = "0" * 64
    for log_entry in logs:
        if log_entry.previous_hash != calculated_hash:
            is_tampered = True
            break
        calculated_hash = log_entry.calculate_hash(log_entry.previous_hash)
        if calculated_hash != log_entry.current_hash:
            is_tampered = True
            break
    
    assert not is_tampered, "Audit log chain appears to be tampered!"

    # Simulate tampering: modify a message in the middle and re-check
    tampered_log = db_session.query(AuditLog).filter_by(message="Event B.").first()
    tampered_log.message = "Event B. (TAMPERED)"
    db_session.add(tampered_log)
    db_session.commit() # Commit the "tampered" change

    # Re-retrieve logs and re-verify
    logs_after_tamper = db_session.query(AuditLog).order_by(AuditLog.id).all()
    is_tampered_recheck = False
    calculated_hash_recheck = "0" * 64
    for log_entry in logs_after_tamper:
        if log_entry.previous_hash != calculated_hash_recheck:
            is_tampered_recheck = True
            break
        calculated_hash_recheck = log_entry.calculate_hash(log_entry.previous_hash)
        if calculated_hash_recheck != log_entry.current_hash:
            is_tampered_recheck = True
            break
    
    assert is_tampered_recheck, "Audit log chain should be detected as tampered!"