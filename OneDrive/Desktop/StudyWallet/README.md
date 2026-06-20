# StudyWallet 💰 — v2.0

A web-based personal finance tracker built for college students. Track expenses, monitor your balance, and manage stock investments — all from a clean browser dashboard.

> **v1.0** was a Python CLI. **v2.0** is a full Flask web app with live stock prices.

## Features

- **Dashboard** — Visual overview with spending donut chart, live balance, and recent expenses
- **Expense Tracking** — Add and categorize expenses (food, snacks, medicine, etc.) with delete support
- **Two-Tier Balance Warnings** — Caution and danger alerts when funds run low
- **Stock Investment Tracker** — Log investments; live prices auto-fetched via Yahoo Finance
- **Investment Advisor** — Smart buy/sell suggestion based on portfolio P&L and balance
- **Monthly Budget Setup** — Set pocket money and minimum safety balance
- **Persistent Storage** — All data saved locally in JSON (no database needed)

## Project Structure

```
StudyWallet/
├── app.py              # Flask backend + API routes
├── tracker.py          # v1 CLI logic (kept for reference)
├── main.py             # v1 CLI entry point (kept for reference)
├── data.json           # Local data store
├── requirements.txt
└── templates/
    └── index.html      # Single-page web dashboard
```

## Getting Started

### Prerequisites

- Python 3.8+

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pratyushprakharojha-prog/StudyWallet.git
   cd StudyWallet
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python app.py
   ```

4. Open your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Tech Stack

| Layer     | Tech                              |
|-----------|-----------------------------------|
| Backend   | Python, Flask                     |
| Frontend  | HTML, CSS, Vanilla JS             |
| Charts    | Chart.js (CDN)                    |
| Icons     | Font Awesome (CDN)                |
| Storage   | JSON file                         |
| Live Data | yfinance (Yahoo Finance API)      |

## Stock Price Support

- Indian stocks: use NSE symbols (e.g. `RELIANCE`, `TCS`, `INFY`)
- US stocks: use standard tickers (e.g. `AAPL`, `TSLA`)
- Prices auto-fetched on the Stocks tab — no manual entry needed

## Author

**Pratyush Prakhar Ojha** — [@pratyushprakharojha-prog](https://github.com/pratyushprakharojha-prog)

---

*v1.0: Python CLI &nbsp;|&nbsp; v2.0: Flask Web App*
