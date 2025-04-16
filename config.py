import os
from dotenv import load_dotenv

load_dotenv()
class Config:

    AUTHORIZE_TOKEN = os.getenv("AUTHORIZE_TOKEN")
    ALLOWED_IPS = os.getenv("ALLOWED_IPS").split(",")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_URL = os.getenv("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://flask_user:password@localhost/trading_db")
    CLOUDFLARE = os.getenv("CLOUDFLARE", "False")
config = Config()