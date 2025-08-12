from sqlalchemy.orm import Session
from ..models.trade_models import Trade
from datetime import datetime

class TradeRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_trade(self, user, order_data, order_response, strategy: str):
        new_trade = Trade(
            user_identifier=user.username,
            symbol=order_data["symbol"],
            trade_type=order_data["order_type"],
            take_profit=order_data.get("take_profit"),
            stop_loss=order_data.get("stop_loss"),
            buy_price=order_data["price"],
            trade_time=datetime.now(),
            signal_time=datetime.now(),
            order_id=order_response["result"].get("orderId"),
            strategy=strategy # --- ZAPISUJEMY STRATEGIĘ ---
        )
        self.db.add(new_trade)
        self.db.commit()
        return new_trade