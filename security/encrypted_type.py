from sqlalchemy.types import TypeDecorator, TEXT
from .encryption_utils import encrypt_data, decrypt_data, _fernet
from logging_setup import get_logger

logger = get_logger(__name__)

class EncryptedType(TypeDecorator):
    """
    A SQLAlchemy TypeDecorator to transparently encrypt and decrypt data
    when storing and retrieving it from the database.
    
    It uses the Fernet encryption from encryption_utils.
    """
    impl = TEXT
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """
        Encrypt the value before sending it to the database.
        """
        if value is not None:
            if not _fernet:
                logger.error("Encryption key not available. Storing data unencrypted.")
                return value
            # The value from the model is already a string, no need for str()
            return encrypt_data(value)
        return value

    def process_result_value(self, value, dialect):
        """
        Decrypt the value after retrieving it from the database.
        """
        if value is not None:
            if not _fernet:
                logger.error("Encryption key not available. Returning raw data from DB.")
                return value
            try:
                # The value from the DB is already a string
                return decrypt_data(value)
            except Exception as e:
                logger.exception(f"Failed to decrypt data from database: {e}. Returning raw value.")
                return value
        return value
