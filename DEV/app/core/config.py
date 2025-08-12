import os
from dotenv import load_dotenv

load_dotenv()

class Config:  # <-- To jest KLASA, której NIE CHCESZ importować bezpośrednio w __init__.py
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("Nie zdefiniowano zmiennej środowiskowej DATABASE_URL")

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# V-- To jest SŁOWNIK, który MUSISZ importować w __init__.py
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}