from sqlalchemy.orm import Session
from ..models.trade_models import User

class UserRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_active_traders(self):
        return self.db.query(User).filter_by(enabled_trading=True).all()