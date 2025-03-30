import os
from dotenv import load_dotenv

load_dotenv()
class Config:

    TOKEN_AUTORYZACYJNY = os.getenv("TOKEN_AUTORYZACYJNY", "globalny_hash")
    ALLOWED_IPS = os.getenv("ALLOWED_IPS").split(",")
    SECRET_KEY = os.getenv("SECRET_KEY", "super_secret")
    # Opcje
    ENABLE_BYBIT_TRADING = os.getenv("ENABLE_BYBIT_TRADING", "True").lower() == "true"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Baza danych
    DATABASE_URL = os.getenv("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://flask_user:password@localhost/trading_db")

config = Config()