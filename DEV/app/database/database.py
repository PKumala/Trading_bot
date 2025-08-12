from flask_sqlalchemy import SQLAlchemy

# Tworzymy instancję SQLAlchemy, ale jeszcze nie wiążemy jej z żadną aplikacją.
# Zrobimy to w fabryce aplikacji.
db = SQLAlchemy()