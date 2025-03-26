import os
from dotenv import load_dotenv

load_dotenv()

SECRET_TOKEN = os.getenv("SECRET_TOKEN")
SECRET_KEY = os.getenv("SECRET_KEY")
ALLOWED_IPS = os.getenv("ALLOWED_IPS").split(",")

# Bybit API
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")

# Opcje
ENABLE_BYBIT_TRADING = os.getenv("ENABLE_BYBIT_TRADING", "True").lower() == "true"

# Baza danych
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///trading.db")