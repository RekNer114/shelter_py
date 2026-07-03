import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

SALT_SIZE=16
NONCE_SIZE=12
KEY_SIZE=32
KDF_ITERATIONS = 600_000


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    return kdf.derive(password.encode())


def encrypt(data: bytes, password: str) -> bytes:
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, data, None)
    return salt + nonce + ciphertext

def decrypt(token: bytes, password: str) -> bytes:
    salt = token[:SALT_SIZE]
    nonce = token[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
    ciphertext = token[SALT_SIZE + NONCE_SIZE:]
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)
