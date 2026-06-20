from flask import Flask, jsonify, request, render_template
import json
import datetime
import os

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

CATEGORIES = [
    "Nutrition/Gym Food",
    "Relationship",
    "Stationery/Academic",
    "Outside Food/Snacks",
    "Medicine",
    "Miscellaneous"
]

# ── Data helpers ──────────────────────────────────────────────────────

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_warning_level(data):
    total = data["total_amount"]
    minimum = data["minimum_balance"]
    new_month = data["new_month_money"]
    cutdown = (new_month - minimum) / 3 if (new_month - minimum) > 0 else 0

    if total <= minimum:
        return "danger"
    elif total <= cutdown:
        return "caution"
    return "safe"

# ── Routes ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data", methods=["GET"])
def get_data():
    data = load_data()
    data["warning_level"] = get_warning_level(data)
    data["categories"] = CATEGORIES
    total_spent = data["new_month_money"] - data["total_amount"]
    data["total_spent"] = round(total_spent, 2)

    # Category breakdown
    category_totals = {}
    for expense in data["expenses"]:
        cat = expense["category"]
        amt = expense["amount"]
        category_totals[cat] = category_totals.get(cat, 0) + amt
    data["category_totals"] = {k: round(v, 2) for k, v in category_totals.items()}

    return jsonify(data)

@app.route("/api/budget", methods=["POST"])
def set_budget():
    body = request.get_json()
    amount = float(body["amount"])
    min_bal = float(body["min_balance"])

    data = load_data()
    data["total_amount"] = amount
    data["new_month_money"] = amount
    data["minimum_balance"] = min_bal
    save_data(data)

    return jsonify({"success": True, "message": f"Budget set to Rs.{amount:.2f}"})

@app.route("/api/expense", methods=["POST"])
def add_expense():
    body = request.get_json()
    category = body["category"]
    description = body["description"]
    amount = float(body["amount"])

    data = load_data()
    new_expense = {
        "category": category,
        "description": description,
        "amount": amount,
        "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    data["expenses"].append(new_expense)
    data["total_amount"] -= amount
    data["total_amount"] = round(data["total_amount"], 2)
    save_data(data)

    warning = get_warning_level(data)
    return jsonify({
        "success": True,
        "remaining": data["total_amount"],
        "warning_level": warning
    })

@app.route("/api/expense/<int:index>", methods=["DELETE"])
def delete_expense(index):
    data = load_data()
    if index < 0 or index >= len(data["expenses"]):
        return jsonify({"success": False, "message": "Invalid index"}), 400
    removed = data["expenses"].pop(index)
    data["total_amount"] = round(data["total_amount"] + removed["amount"], 2)
    save_data(data)
    return jsonify({"success": True, "remaining": data["total_amount"]})

@app.route("/api/stock", methods=["POST"])
def add_stock():
    body = request.get_json()
    name = body["name"].upper().strip()
    quantity = float(body["quantity"])
    buy_price = float(body["buy_price"])
    amount_invested = round(quantity * buy_price, 2)

    data = load_data()
    new_stock = {
        "name": name,
        "quantity": quantity,
        "buy_price": buy_price,
        "date": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    data["stocks"].append(new_stock)
    data["total_amount"] = round(data["total_amount"] - amount_invested, 2)
    save_data(data)

    return jsonify({
        "success": True,
        "invested": amount_invested,
        "remaining": data["total_amount"]
    })

@app.route("/api/stock/<int:index>", methods=["DELETE"])
def delete_stock(index):
    data = load_data()
    if index < 0 or index >= len(data["stocks"]):
        return jsonify({"success": False, "message": "Invalid index"}), 400
    removed = data["stocks"].pop(index)
    refund = round(removed["quantity"] * removed["buy_price"], 2)
    data["total_amount"] = round(data["total_amount"] + refund, 2)
    save_data(data)
    return jsonify({"success": True, "remaining": data["total_amount"]})

@app.route("/api/stocks/live", methods=["GET"])
def check_stocks_live():
    data = load_data()
    if not data["stocks"]:
        return jsonify({"stocks": [], "total_invested": 0, "total_current": 0, "overall_pl": 0})

    result = []
    total_invested = 0
    total_current = 0

    for stock in data["stocks"]:
        invested = round(stock["quantity"] * stock["buy_price"], 2)
        current_price = None
        current_value = None
        profit_loss = None
        percentage = None
        error = None

        if YFINANCE_AVAILABLE:
            try:
                # Try Indian exchange suffixes first, then raw
                ticker_variants = [
                    stock["name"] + ".NS",   # NSE
                    stock["name"] + ".BO",   # BSE
                    stock["name"]            # US or others
                ]
                fetched = False
                for ticker_str in ticker_variants:
                    ticker = yf.Ticker(ticker_str)
                    info = ticker.fast_info
                    price = getattr(info, "last_price", None)
                    if price and price > 0:
                        current_price = round(float(price), 2)
                        fetched = True
                        break
                if not fetched:
                    error = "Price unavailable"
            except Exception as e:
                error = str(e)
        else:
            error = "yfinance not installed"

        if current_price is not None:
            current_value = round(stock["quantity"] * current_price, 2)
            profit_loss = round(current_value - invested, 2)
            percentage = round((profit_loss / invested) * 100, 2) if invested else 0
            total_current += current_value

        total_invested += invested

        result.append({
            "name": stock["name"],
            "quantity": stock["quantity"],
            "buy_price": stock["buy_price"],
            "date": stock["date"],
            "invested": invested,
            "current_price": current_price,
            "current_value": current_value,
            "profit_loss": profit_loss,
            "percentage": percentage,
            "error": error
        })

    overall_pl = round(total_current - total_invested, 2)
    advice = ""
    balance_left = data["total_amount"]
    if balance_left < data["minimum_balance"]:
        advice = "Do NOT invest — balance is below your minimum!"
    elif overall_pl < -500:
        advice = "Portfolio in loss — wait before investing more."
    else:
        advice = "Portfolio looks healthy — you can consider investing!"

    return jsonify({
        "stocks": result,
        "total_invested": round(total_invested, 2),
        "total_current": round(total_current, 2),
        "overall_pl": overall_pl,
        "advice": advice,
        "balance_left": balance_left
    })

if __name__ == "__main__":
    app.run(debug=True)
