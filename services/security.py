from flask import request
from config import config

def verify_ip():
    if config.CLOUDFLARE ==True:
        client_ip =  request.headers.get('CF-Connecting-IP')
    else:
        client_ip = request.remote_addr

    return client_ip in config.ALLOWED_IPS


def verify_token(data):
    return data.get("token") == config.AUTHORIZE_TOKEN
