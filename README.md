# 🤖 TradingView → Bybit Algorithmic Trading Bot

> Automated trading bot that bridges **TradingView** webhook alerts with live order execution on the **Bybit** crypto exchange.  
> Built with Python & Flask. Supports concurrent multi-user signal processing with encrypted API key storage.

---

## 🔍 How it works

```
TradingView Alert
      │
      ▼ HTTP POST (JSON)
 Flask Webhook
      │
      ├─ Token auth + Cloudflare IP check
      ├─ Decrypt user's Bybit API keys (AES-CFB)
      ├─ Calculate position size (risk %)
      │
      ▼ ThreadPoolExecutor (parallel per user)
 Bybit REST API (pybit)
      │
      ▼
 Execute Order + Log to DB
```

---

## 📁 Project Structure

```
Trading_bot/
├── app.py                # Flask application entry point
├── config.py             # Configuration loader
├── database_engine.py    # SQLAlchemy engine & session setup
├── example.env           # Environment variables template
├── requirements.txt      # Python dependencies
│
├── factory/              # Factory pattern — object construction
├── models/               # SQLAlchemy ORM models (users, transactions)
├── routes/               # Flask blueprints / webhook endpoints
├── services/             # Business logic (trading, encryption, risk)
└── utils/                # Helpers (IP verification, position sizing)
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Web framework | Python 3, Flask |
| Exchange API | Bybit REST API (`pybit`) |
| Concurrency | `ThreadPoolExecutor` |
| Encryption | AES-CFB (`cryptography`) |
| Database / ORM | SQLAlchemy |
| Security | Token auth, Cloudflare IP verification |

---

## ✨ Key Features

### 📡 Webhook → Order Execution
Flask endpoint receives JSON signals from TradingView strategy alerts and maps them to Bybit order actions:
- **Open Long / Open Short**
- **Modify Take Profit / Stop Loss**
- **Close position**

### ⚡ Concurrent Multi-User Processing
Signals from multiple users are processed in **parallel via `ThreadPoolExecutor`** — each user's order is executed independently without blocking others. Minimizes latency between signal receipt and order placement.

### 🔐 AES-CFB Encryption
Each user's Bybit API keys are stored **encrypted at rest** in the database using AES-CFB symmetric encryption (`cryptography` library). Keys are decrypted in memory only at the moment of trade execution.

### 🛡️ Security Layers
- **Token-based authorization** on all webhook endpoints
- **IP address verification** with support for Cloudflare proxy headers (`CF-Connecting-IP`)

### 📐 Dynamic Position Sizing
A dedicated algorithm in `utils/` calculates the safe order size for each trade based on:
- Live account balance fetched from Bybit
- User-configured risk percentage per trade

### 🗄️ Clean Architecture
Business logic is fully separated from routing via a **Services layer** (`services/`). The **Factory pattern** (`factory/`) handles object construction, keeping controllers thin and testable.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Bybit account with API keys *(use Testnet for development)*
- TradingView account with webhook access *(Pro plan or higher)*

### Installation

```bash
git clone https://github.com/PKumala/Trading_bot.git
cd Trading_bot
pip install -r requirements.txt
```

### Configuration

```bash
cp example.env .env
```

Fill in your values in `.env` — see `example.env` for all required variables.

### Run

```bash
python app.py
```

### TradingView Alert Payload

Set the webhook URL in your TradingView alert and use a JSON message body, for example:

```json
{
  "token": "your_webhook_token",
  "action": "long",
  "symbol": "BTCUSDT"
}
```

---

## 🔒 Security Notes

- `.env` is in `.gitignore` — **never commit real API keys**
- Use Bybit **Testnet** keys during development
- In production, run behind **nginx + HTTPS** and restrict access to TradingView IP ranges

---

## ⚠️ Disclaimer

This project is for **educational purposes only**.  
Cryptocurrency trading carries significant financial risk. The author assumes no responsibility for any losses incurred through use of this software. Always test on Testnet before using real funds.
