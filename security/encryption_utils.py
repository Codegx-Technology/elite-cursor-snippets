from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os
import logging

from config_loader import get_config

# Use standard logging to avoid circular import with logging_setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
config = get_config()

# --- Key Derivation (Conceptual) ---
# In a real application, the encryption key would be securely managed
# and not derived directly from a hardcoded string or simple environment variable.
# This is for demonstration purposes.

def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

# Use a key from config or environment variable
ENCRYPTION_PASSWORD = os.getenv("ENCRYPTION_PASSWORD") or getattr(getattr(config, 'security', {}), 'encryption_password', None)
_salt_val = os.getenv("ENCRYPTION_SALT") or getattr(getattr(config, 'security', {}), 'encryption_salt', None)
ENCRYPTION_SALT = _salt_val.encode() if isinstance(_salt_val, str) else _salt_val

if not ENCRYPTION_PASSWORD or not ENCRYPTION_SALT:
    logger.error("Encryption password or salt not configured. Encryption utilities will not function.")
    _fernet = None
else:
    try:
        _key = _derive_key(ENCRYPTION_PASSWORD, ENCRYPTION_SALT)
        _fernet = Fernet(_key)
        logger.info("Encryption utilities initialized.")
    except Exception as e:
        logger.error(f"Failed to initialize encryption utilities: {e}")
        _fernet = None

def encrypt_data(data: str) -> str:
    """
    // [TASK]: Encrypt a string using AES-256
    // [GOAL]: Secure sensitive input/output data
    """
    if not _fernet:
        logger.warning("Encryption not initialized. Returning unencrypted data.")
        return data
    try:
        encrypted_bytes = _fernet.encrypt(data.encode())
        return encrypted_bytes.decode()
    except Exception as e:
        logger.error(f"Failed to encrypt data: {e}")
        return data # Return original data on failure

def decrypt_data(encrypted_data: str) -> str:
    """
    // [TASK]: Decrypt an AES-256 encrypted string
    // [GOAL]: Retrieve original sensitive data
    """
    if not _fernet:
        logger.warning("Encryption not initialized. Returning original data.")
        return encrypted_data
    try:
        decrypted_bytes = _fernet.decrypt(encrypted_data.encode())
        return decrypted_bytes.decode()
    except Exception as e:
        logger.error(f"Failed to decrypt data: {e}")
        return encrypted_data # Return original data on failure

def encrypt_bytes(data: bytes) -> bytes:
    """
    // [TASK]: Encrypt bytes using AES-256 (via Fernet)
    // [GOAL]: Secure sensitive binary data
    """
    if not _fernet:
        logger.warning("Encryption not initialized. Returning unencrypted bytes.")
        return data
    try:
        encrypted_bytes = _fernet.encrypt(data)
        return encrypted_bytes
    except Exception as e:
        logger.error(f"Failed to encrypt bytes: {e}")
        return data # Return original bytes on failure

def decrypt_bytes(encrypted_data: bytes) -> bytes:
    """
    // [TASK]: Decrypt AES-256 encrypted bytes (via Fernet)
    // [GOAL]: Retrieve original sensitive binary data
    """
    if not _fernet:
        logger.warning("Encryption not initialized. Returning original bytes.")
        return encrypted_data
    try:
        decrypted_bytes = _fernet.decrypt(encrypted_data)
        return decrypted_bytes
    except Exception as e:
        logger.error(f"Failed to decrypt bytes: {e}")
        return encrypted_data # Return original bytes on failure

# Example usage (conceptual)
async def main():
    # Ensure ENCRYPTION_PASSWORD and ENCRYPTION_SALT are set in config.yaml or env
    if _fernet:
        original_data = "This is some sensitive data."
        encrypted = encrypt_data(original_data)
        decrypted = decrypt_data(encrypted)
        logger.info(f"Original: {original_data}")
        logger.info(f"Encrypted: {encrypted}")
        logger.info(f"Decrypted: {decrypted}")
        assert original_data == decrypted
    else:
        logger.warning("Encryption utilities not functional for example.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
