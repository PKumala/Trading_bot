import logging
from flask import Flask


# === NAJWAŻNIEJSZA LINIA ===
# Upewnij się, że importujesz 'config' (małe 'c')
from .core.config import config
# ===========================

from .api.v1.webhook_routes import webhook_bp
from .api.v1.users import users_bp
from .database.database import db


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def create_app(config_name="default"):
    app = Flask(__name__)

    # Ta linia musi otrzymać SŁOWNIK o nazwie 'config', aby mogła zadziałać
    # Wyrażenie config[config_name] pobiera odpowiednią klasę konfiguracyjną (np. DevelopmentConfig)
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_DATABASE_URI'] = config[config_name].DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    configure_logging()

    # Rejestracja Blueprints
    app.register_blueprint(webhook_bp, url_prefix='/api/v1')
    app.register_blueprint(users_bp, url_prefix='/api/v1')

    return app