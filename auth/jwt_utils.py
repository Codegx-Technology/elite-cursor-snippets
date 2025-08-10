import jwt
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from logging_setup import get_logger
from config_loader import get_config

logger = get_logger(__name__)
config = get_config()

# --- JWT Key Management (Placeholder/Conceptual) ---
# In a real application, these keys would be securely loaded from
# environment variables, a secrets manager, or a key management service.

# For demonstration, we'll generate a pair if not found, but DO NOT use in production.
_private_key = None
_public_key = None

def _generate_rsa_keys():
    """
    // [TASK]: Generate RSA private and public keys
    // [GOAL]: Provide cryptographic keys for JWT signing
    """
    global _private_key, _public_key
    if _private_key is None or _public_key is None:
        logger.warning("Generating RSA keys for JWT. DO NOT USE IN PRODUCTION.")
        _private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        _public_key = _private_key.public_key()

        # You would typically save these to secure locations
        # private_pem = _private_key.private_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PrivateFormat.PKCS8,
        #     encryption_algorithm=serialization.NoEncryption()
        # )
        # public_pem = _public_key.public_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PublicFormat.SubjectPublicKeyInfo
        # )

_generate_rsa_keys() # Generate keys on module import for demonstration

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
