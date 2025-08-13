from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from logging_setup import get_logger
from config_loader import get_config

logger = get_logger(__name__)
config = get_config()

# Use SQLite for simplicity in development
SQLALCHEMY_DATABASE_URL = f"sqlite:///./{config.app.database_name}.db"

# Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

def get_db():
    """
    // [TASK]: Dependency to get a database session
    // [GOAL]: Provide a database session for API endpoints
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

logger.info(f"Database engine created for: {SQLALCHEMY_DATABASE_URL}")
