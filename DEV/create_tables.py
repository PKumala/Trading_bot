from app import create_app
from app.database.database import db

# Tworzymy instancję aplikacji, aby mieć dostęp do jej kontekstu
app = create_app()

def reset_database():
    """
    UWAGA: Używa kontekstu aplikacji do usunięcia i utworzenia tabel.
    """
    print("Usuwanie istniejących tabel...")
    # Operacje na bazie danych muszą być wykonane wewnątrz kontekstu aplikacji
    with app.app_context():
        db.drop_all()
        print("Tworzenie nowych tabel...")
        db.create_all()
    print("Baza danych została zresetowana pomyślnie.")

if __name__ == "__main__":
    choice = input("Czy na pewno chcesz usunąć WSZYSTKIE dane i zresetować tabele? (tak/nie): ")
    if choice.lower() == 'tak':
        reset_database()
    else:
        print("Operacja anulowana.")