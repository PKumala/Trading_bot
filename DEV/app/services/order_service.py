# app/services/order_service.py
import logging
from concurrent.futures import ThreadPoolExecutor
from .bybit_service import BybitService
from ..repositories.user_repository import UserRepository
from ..repositories.trade_repository import TradeRepository
from ..database.session import get_db_session
from ..utils.crypt_key import decrypt_api_key

logger = logging.getLogger(__name__)


class OrderProcessingService:

    def _process_order_for_single_user(self, webhook_data: dict, user):
        """Logika przetwarzania zlecenia dla jednego użytkownika w osobnym wątku."""
        webhook_strategy = webhook_data.get("strategy")

        if not isinstance(user.strategies, list) or webhook_strategy not in user.strategies:
            logger.info(f"User {user.username} is not subscribed to strategy '{webhook_strategy}'. Skipping.")
            return {"status": "skipped", "message": "User not subscribed to this strategy."}

        with get_db_session() as db:
            try:
                # --- KLUCZOWA ZMIANA: Konwersja ceny na float ---
                try:
                    entry_price = float(webhook_data["price"])
                except (ValueError, TypeError):
                    msg = f"Invalid price format in webhook data: {webhook_data.get('price')}"
                    logger.error(msg)
                    return {"status": "error", "message": msg}

                api_key = decrypt_api_key(user.bybit_api_key)
                api_secret = decrypt_api_key(user.bybit_api_secret_key)
                bybit_service = BybitService(api_key, api_secret)
                symbol = webhook_data["symbol"]

                leverage_response = bybit_service.set_leverage(symbol=symbol, leverage=user.leverage)
                if leverage_response.get("retCode") != 0:
                    msg = f"Failed to set leverage to {user.leverage}x for user {user.username}."
                    logger.error(f"{msg} Response: {leverage_response}")
                    return {"status": "error", "message": msg}

                logger.info(f"Successfully set leverage to {user.leverage}x for {user.username} on {symbol}.")

                for symbol_to_check in ["ETHUSDT", "BTCUSDT"]:
                    if bybit_service.position_is_open(symbol_to_check):
                        msg = f"Position for {symbol_to_check} is already open."
                        logger.warning(f"User {user.username}: {msg}")
                        return {"status": "error", "message": msg}

                # Teraz entry_price jest na pewno liczbą
                raw_qty = bybit_service.calculate_safe_qty(
                    entry_price,
                    user.balance,
                    risk_percent=7,
                    leverage=user.leverage
                )
                qty = round(raw_qty, 2) if symbol == "ETHUSDT" else round(raw_qty, 3)

                response = bybit_service.send_order(
                    symbol=symbol,
                    order_type=webhook_data["order_type"],
                    qty=qty,
                    take_profit=webhook_data.get("take_profit"),
                    stop_loss=webhook_data.get("stop_loss")
                )

                # if isinstance(response, dict) and response.get("retCode") == 0:
                #     trade_repo = TradeRepository(db)
                #     trade_repo.create_trade(user, webhook_data, response, strategy=webhook_strategy)
                #     logger.info(
                #         f"Successfully processed order for user {user.username} with strategy '{webhook_strategy}'.")
                #     return {"status": "success", "response": response}
                # else:
                #     logger.error(f"Failed to send order for user {user.username}: {response}")
                #     return {"status": "error", "message": "Failed to send order", "details": response}

            except Exception as e:
                # To jest ogólny 'catch-all', który złapał Twój błąd.
                logger.exception(f"An unexpected error occurred for user {user.username}")
                return {"status": "error", "message": str(e)}

    # ... reszta klasy bez zmian ...
    def process_webhook_for_all_users(self, webhook_data: dict):
        with get_db_session() as db:
            user_repo = UserRepository(db)
            active_users = user_repo.get_active_traders()

        if not active_users:
            logger.info("No active traders found.")
            return []

        responses = []
        with ThreadPoolExecutor(max_workers=len(active_users) or 1) as executor:
            future_to_user = {
                executor.submit(self._process_order_for_single_user, webhook_data, user): user
                for user in active_users
            }

            for future in future_to_user:
                user = future_to_user[future]
                try:
                    result = future.result()
                    responses.append({"user": user.username, "result": result})
                except Exception as e:
                    logger.error(f"Future for user {user.username} generated an exception: {e}")
                    responses.append(
                        {"user": user.username, "result": {"status": "error", "message": "Thread execution failed."}})

        return responses