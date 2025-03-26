from flask import request
from config import SECRET_TOKEN, ALLOWED_IPS

def verify_ip():
    client_ip = request.remote_addr
    return client_ip in ALLOWED_IPS

def verify_token(data):
    return data.get("token") == SECRET_TOKEN