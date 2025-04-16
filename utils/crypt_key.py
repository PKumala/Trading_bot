import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')


def encrypt_api_key(api_key: str) -> str:
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(ENCRYPTION_KEY.encode()), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    encrypted_key = encryptor.update(api_key.encode()) + encryptor.finalize()
    encrypted_data = iv + encrypted_key

    return base64.b64encode(encrypted_data).decode()


def decrypt_api_key(encrypted_key: str) -> str:
    encrypted_data = base64.b64decode(encrypted_key)
    iv = encrypted_data[:16]
    encrypted_key = encrypted_data[16:]

    cipher = Cipher(algorithms.AES(ENCRYPTION_KEY.encode()), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_key = decryptor.update(encrypted_key) + decryptor.finalize()
    return decrypted_key.decode()
