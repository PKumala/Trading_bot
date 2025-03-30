import hashlib
import os

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def generate_token():
    return hashlib.sha256(os.urandom(24)).hexdigest()

def authorize_request(token_autoryzacyjny, token_użytkownika):
    from models.database import User
    user = User.query.filter_by(token_użytkownika_hash=token_użytkownika).first()
    if not user or token_autoryzacyjny != "globalny_hash":
        raise Exception("Błąd autoryzacji")
    return user
