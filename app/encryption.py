import hashlib

from cryptography.fernet import Fernet

from .config import SECRET_KEY


class Encryptor:
    """Uses a fernet authentication suite to encrypt and decrypt
    content of stored secrets.
    """

    def __init__(self):
        self.cipher_suite = Fernet(SECRET_KEY)

    def encrypt(self, data: str) -> bytes:
        return self.cipher_suite.encrypt(data.encode())

    def decrypt(self, data: bytes) -> str:
        return self.cipher_suite.decrypt(data).decode()


def hash_passphrase(passphrase: str) -> bytes:
    """Hashes a passphrase."""
    byte_passphrase = passphrase.encode()
    hashed = hashlib.pbkdf2_hmac('sha256', byte_passphrase, SECRET_KEY, 100000)

    return hashed
