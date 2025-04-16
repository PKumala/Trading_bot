from flask import Flask
from routes.users import users_bp
from routes.webhook import webhook_bp
from config import config
from models.database import db

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
app.register_blueprint(users_bp, url_prefix='/api')
app.register_blueprint(webhook_bp, url_prefix='/api')


if __name__ == "__main__":
    app.run(debug=True)