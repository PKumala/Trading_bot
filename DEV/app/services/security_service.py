from flask import request
from ..core.config import config
from flask import Request
def verify_ip(req: Request) -> bool:
    if config.CLOUDFLARE ==True:
        client_ip =  request.headers.get('CF-Connecting-IP')
    else:
        client_ip = request.remote_addr

    return client_ip in config.ALLOWED_IPS


def verify_token(data: dict) -> bool:
    return data.get("token") == config.AUTHORIZE_TOKEN
