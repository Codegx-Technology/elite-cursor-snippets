from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from config_loader import get_config

# Use standard logging to avoid circular import with logging_setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
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
