from DEV.app import db
from app import create_app
import os

# Możesz wczytać konfigurację z zmiennych środowiskowych
# np. FLASK_ENV=development lub FLASK_ENV=production
app = create_app(os.getenv("FLASK_CONFIG") or "default")

if __name__ == "__main__":
    # Użyj Gunicorn/Uvicorn w produkcji zamiast app.run()

    app.run(host="0.0.0.0", port=5000)