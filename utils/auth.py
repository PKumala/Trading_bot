import hashlib
import os

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def generate_token():
    return hashlib.sha256(os.urandom(24)).hexdigest()
