# StudyWallet 💰

A Python CLI personal finance tracker built for college students. Track expenses, monitor your balance, and manage stock investments — all from the terminal.

## Features

- **Expense Tracking** — Add and categorize expenses (food, transport, entertainment, etc.)
- **Balance Warnings** — Two-tier alert system that warns you when funds are running low
- **Stock Investment Tracker** — Log investments and track profit/loss in real time
- **Investment Advisor** — Get simple buy/sell suggestions based on your portfolio
- **Monthly Report** — View a full summary of your spending by category
- **Persistent Storage** — All data saved locally using JSON (no database needed)
- **Colored Terminal Output** — Clean, readable interface using `colorama`

## Project Structure

```
StudyWallet/
├── main.py       # Entry point and menu logic
└── tracker.py    # Core logic: expenses, investments, reports
```

## Getting Started

### Prerequisites

- Python 3.x
- `colorama` library

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pratyushprakharojha-prog/StudyWallet.git
   cd StudyWallet
   ```

2. Install dependencies:
   ```bash
   pip install colorama
   ```

3. Run the app:
   ```bash
   python main.py
   ```

> **Note:** Run from Command Prompt (not VS Code terminal) for best experience on Windows.

## Usage

On launch, you'll see a menu to:
- Add an expense with a category
- View your current balance and warnings
- Add or view stock investments
- Generate a monthly spending report

## Tech Stack

- **Language:** Python
- **Storage:** JSON files
- **Libraries:** `colorama` for terminal colors

## What I Learned

- Structuring a Python project across multiple modules
- Designing data persistence with JSON
- Building a menu-driven CLI application
- Tracking financial data with dictionaries and lists

## Future Plans

- GUI version using Tkinter or a web version with Flask
- Budget goal setting per category
- Export reports to CSV

## Author

**Pratyush Prakhar Ojha** — [@pratyushprakharojha-prog](https://github.com/pratyushprakharojha-prog)

---

*Built as a portfolio project to practice Python fundamentals and software design.*
