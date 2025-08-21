import jwt
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from logging_setup import get_logger
from config_loader import get_config

logger = get_logger(__name__)
config = get_config()

# --- JWT Key Management ---
# In a real application, these keys would be securely loaded from
# environment variables, a secrets manager, or a key management service.

_private_key = None
_public_key = None

def _load_jwt_keys():
    global _private_key, _public_key
    if _private_key is None or _public_key is None:
        jwt_private_key_pem = config.security.jwt_private_key_pem
        jwt_public_key_pem = config.security.jwt_public_key_pem

        if jwt_private_key_pem and jwt_public_key_pem:
            logger.info("Loading JWT keys from configuration.")
            _private_key = serialization.load_pem_private_key(
                jwt_private_key_pem.encode(),
                password=None, # Assuming no password for the key file
                backend=default_backend()
            )
            _public_key = serialization.load_pem_public_key(
                jwt_public_key_pem.encode(),
                backend=default_backend()
            )
        else:
            logger.warning("JWT keys not found in configuration. Generating RSA keys for demonstration. DO NOT USE IN PRODUCTION.")
            _generate_rsa_keys_for_demo() # Call a new demo function

def _generate_rsa_keys_for_demo(): # New function for demo key generation
    """
    // [TASK]: Generate RSA private and public keys for demonstration ONLY
    // [GOAL]: Provide cryptographic keys for JWT signing when not configured
    """
    global _private_key, _public_key
    _private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    _public_key = _private_key.public_key()

# Call the key loading function
_load_jwt_keys()

# --- JWT Utility Functions ---

def create_jwt(payload: dict, expiry_minutes: int = 30) -> str:
    """
    // [TASK]: Create a JWT token
    // [GOAL]: Generate signed tokens for authentication
    """
    to_encode = payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=expiry_minutes)
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, _private_key, algorithm="RS256")
    logger.info(f"JWT created for user: {payload.get('user_id')}")
    return encoded_jwt

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Compatibility wrapper: create an access token using the existing create_jwt.
    """
    minutes = 30
    if expires_delta is not None:
        try:
            minutes = max(1, int(expires_delta.total_seconds() // 60))
        except Exception:
            minutes = 30
    return create_jwt(data, expiry_minutes=minutes)

def verify_jwt(token: str) -> dict:
    """
    // [TASK]: Verify a JWT token
    // [GOAL]: Validate token authenticity and extract payload
    """
    try:
        decoded_payload = jwt.decode(token, _public_key, algorithms=["RS256"])
        logger.info(f"JWT verified for user: {decoded_payload.get('user_id')}")
        return decoded_payload
    except jwt.ExpiredSignatureError:
        log_and_raise(jwt.ExpiredSignatureError("Token has expired"), "JWT verification failed")
    except jwt.InvalidTokenError as e:
        log_and_raise(e, "Invalid JWT token")

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hashes a plain-text password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

# Example usage (conceptual)
async def main():
    # Create a dummy JWT
    user_payload = {"user_id": "test_user_123", "role": "admin", "tenant_id": "tenant_abc"}
    token = create_jwt(user_payload)
    logger.info(f"Generated JWT: {token}")

    # Verify the JWT
    try:
        decoded = verify_jwt(token)
        logger.info(f"Decoded JWT: {decoded}")
    except Exception as e:
        logger.error(f"JWT verification failed in example: {e}")

    # Test expired token (optional)
    # expired_token = create_jwt(user_payload, expiry_minutes=-1)
    # try:
    #     verify_jwt(expired_token)
    # except Exception as e:
    #     logger.info(f"Expected error for expired token: {e}")

if __name__ == "__main__":
    asyncio.run(main())
