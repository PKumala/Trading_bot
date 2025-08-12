from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os
from dotenv import load_dotenv
load_dotenv()
# Załóżmy, że DATABASE_URL jest w konfiguracji
# np. "sqlite:///./trades.db"
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db_session():
    """
    Zapewnia sesję bazy danych w sposób bezpieczny wątkowo.
    Używać z `with get_db_session() as db:`
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()