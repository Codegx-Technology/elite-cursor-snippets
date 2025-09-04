# utils/encryption.py

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os

class EncryptionUtil:
    def __init__(self, password: str, salt: str):
        # Derive a key from the password and salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt.encode('utf-8'),
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
        self.f = Fernet(key)

    def encrypt(self, data: str) -> str:
        return self.f.encrypt(data.encode('utf-8')).decode('utf-8')

    def decrypt(self, encrypted_data: str) -> str:
        return self.f.decrypt(encrypted_data.encode('utf-8')).decode('utf-8')


