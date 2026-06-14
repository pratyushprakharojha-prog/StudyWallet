import json
import datetime
import os
from colorama import Fore, Style, init

init(autoreset=True)

DATA_FILE = "data.json"

# ── Helpers ──────────────────────────────────────────────────────────

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def section_header(title):
    # Prints a clean colored header for every section
    print(Fore.CYAN + f"\n{'='*40}")
    print(Fore.CYAN + f"  {title}")
    print(Fore.CYAN + f"{'='*40}")

# ── Budget Setup ──────────────────────────────────────────────────────

def setup_budget():
    data = load_data()
    section_header("💰 BUDGET SETUP")

    print(Fore.WHITE + f"Current budget: Rs.{data['total_amount']}")
    amount = float(input(Fore.GREEN + "Enter your monthly pocket money: Rs."))
    min_bal = float(input(Fore.GREEN + "Enter your minimum balance (safety limit): Rs."))

    data["total_amount"] = amount
    data["new_month_money"] = amount
    data["minimum_balance"] = min_bal

    save_data(data)
    print(Fore.GREEN + f"\n✅ Budget set! You have Rs.{amount} for this month.")
    print(Fore.YELLOW + f"⚠️  You will be warned if balance drops below Rs.{min_bal}")

# ── Warning Logic ─────────────────────────────────────────────────────

def check_warnings(data):
    total = data["total_amount"]
    minimum = data["minimum_balance"]
    new_month = data["new_month_money"]
    cutdown = (new_month - minimum) / 3

    if total <= minimum:
        print(Fore.RED + "\n🚨 DANGER: EXPENDITURE EXCEEDS MINIMUM BALANCE! 🚨")
        print(Fore.RED + f"   Remaining: Rs.{total} | Minimum: Rs.{minimum}")

    elif total <= cutdown:
        print(Fore.YELLOW + "\n⚠️  CAUTION: Approaching minimum balance!")
        print(Fore.YELLOW + f"   Remaining: Rs.{total:.2f} | Cutdown threshold: Rs.{cutdown:.2f}")

# ── Add Expense ───────────────────────────────────────────────────────

CATEGORIES = [
    "Nutrition/Gym Food",
    "Relationship",
    "Stationery/Academic",
    "Outside Food/Snacks",
    "Medicine",
    "Miscellaneous"
]

def add_expense():
    data = load_data()
    section_header("➕ ADD EXPENSE")

    print(Fore.CYAN + "Categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(Fore.YELLOW + f"  {i}. {cat}")

    choice = int(input(Fore.GREEN + "Choose category (1-6): ")) - 1
    category = CATEGORIES[choice]
    description = input(Fore.GREEN + "What did you buy? ")
    amount = float(input(Fore.GREEN + "Amount spent: Rs."))

    new_expense = {
        "category": category,
        "description": description,
        "amount": amount,
        "datetime": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    }

    data["expenses"].append(new_expense)
    data["total_amount"] -= amount

    save_data(data)
    print(Fore.GREEN + f"\n✅ Expense added!")
    print(Fore.WHITE + f"   Remaining balance: Rs.{data['total_amount']:.2f}")

    check_warnings(data)

# ── Stock Tracker ─────────────────────────────────────────────────────

def add_stock():
    data = load_data()
    section_header("📈 ADD STOCK INVESTMENT")

    name = input(Fore.GREEN + "Stock name (e.g. TCS, INFY): ").upper()
    quantity = float(input(Fore.GREEN + "How many shares did you buy? "))
    buy_price = float(input(Fore.GREEN + "Buy price per share: Rs."))
    amount_invested = quantity * buy_price

    new_stock = {
        "name": name,
        "quantity": quantity,
        "buy_price": buy_price,
        "date": str(datetime.datetime.now().strftime("%Y-%m-%d"))
    }

    data["stocks"].append(new_stock)
    data["total_amount"] -= amount_invested

    save_data(data)
    print(Fore.GREEN + f"\n✅ Logged {quantity} shares of {name} at Rs.{buy_price} each")
    print(Fore.YELLOW + f"   Total invested: Rs.{amount_invested:.2f}")
    print(Fore.WHITE + f"   Remaining balance: Rs.{data['total_amount']:.2f}")

def check_stocks():
    data = load_data()
    section_header("📊 STOCK PROFIT / LOSS")

    if not data["stocks"]:
        print(Fore.YELLOW + "No stocks logged yet!")
        return

    total_invested = 0
    total_current = 0

    for stock in data["stocks"]:
        print(Fore.CYAN + f"\n{stock['name']} — {stock['quantity']} shares @ Rs.{stock['buy_price']} (bought {stock['date']})")
        current_price = float(input(Fore.GREEN + f"Current price of {stock['name']}: Rs."))

        invested = stock["quantity"] * stock["buy_price"]
        current_value = stock["quantity"] * current_price
        profit_loss = current_value - invested
        percentage = (profit_loss / invested) * 100

        total_invested += invested
        total_current += current_value

        if profit_loss >= 0:
            print(Fore.GREEN + f"   ✅ PROFIT: Rs.{profit_loss:.2f} (+{percentage:.1f}%)")
        else:
            print(Fore.RED + f"   ❌ LOSS: Rs.{profit_loss:.2f} ({percentage:.1f}%)")

    overall_pl = total_current - total_invested
    balance_left = data["total_amount"]

    section_header("💡 INVESTMENT ADVICE")
    if overall_pl >= 0:
        print(Fore.GREEN + f"Overall Portfolio: Rs.{overall_pl:.2f} PROFIT ✅")
    else:
        print(Fore.RED + f"Overall Portfolio: Rs.{overall_pl:.2f} LOSS ❌")

    print(Fore.WHITE + f"Balance remaining: Rs.{balance_left:.2f}")

    if balance_left < data["minimum_balance"]:
        print(Fore.RED + "\n❌ ADVICE: Do NOT invest — balance below minimum!")
    elif overall_pl < -500:
        print(Fore.YELLOW + "\n⚠️  ADVICE: Portfolio in loss — wait before investing more.")
    else:
        print(Fore.GREEN + "\n✅ ADVICE: Looks healthy — you can consider investing!")

# ── Monthly Report ────────────────────────────────────────────────────

def monthly_report():
    data = load_data()
    section_header("📋 MONTHLY REPORT")

    total_spent = data["new_month_money"] - data["total_amount"]

    print(Fore.WHITE + f"Monthly Budget:   Rs.{data['new_month_money']:.2f}")
    print(Fore.RED +   f"Total Spent:      Rs.{total_spent:.2f}")
    print(Fore.GREEN + f"Current Balance:  Rs.{data['total_amount']:.2f}")
    print(Fore.YELLOW + f"Minimum Balance:  Rs.{data['minimum_balance']:.2f}")

    print(Fore.CYAN + "\n--- Spending by Category ---")
    category_totals = {}
    for expense in data["expenses"]:
        cat = expense["category"]
        amt = expense["amount"]
        if cat in category_totals:
            category_totals[cat] += amt
        else:
            category_totals[cat] = amt

    if category_totals:
        for cat, total in category_totals.items():
            print(Fore.YELLOW + f"  {cat}: Rs.{total:.2f}")
    else:
        print(Fore.WHITE + "  No expenses logged yet!")

    print(Fore.CYAN + "\n--- Stock Summary ---")
    if data["stocks"]:
        for stock in data["stocks"]:
            invested = stock["quantity"] * stock["buy_price"]
            print(Fore.YELLOW + f"  {stock['name']}: {stock['quantity']} shares — Rs.{invested:.2f} invested")
    else:
        print(Fore.WHITE + "  No stocks logged yet!")

    print(Fore.CYAN + "\n" + "="*40)