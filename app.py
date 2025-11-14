from flask import Flask, jsonify

app = Flask(__name__)

# Static currency mapping
NAME_TO_ISO = {
    "dollar": "USD",
    "usd": "USD",
    "rupee": "INR",
    "inr": "INR",
    "euro": "EUR",
    "eur": "EUR"
}

# Static exchange rate table
STATIC_RATES = {
    ("USD", "INR"): 83.0,
    ("INR", "USD"): 1/83.0,
    ("USD", "EUR"): 0.92,
    ("EUR", "USD"): 1/0.92,
    ("INR", "EUR"): 0.011,
    ("EUR", "INR"): 1/0.011,
}

def name_to_iso(name: str):
    key = name.strip().lower()
    return NAME_TO_ISO.get(key, key.upper())

@app.route("/")
def root():
    return jsonify({"message": "Use /<from>/<to>/<amount> for static currency conversion"}), 200

@app.route("/<from_cur>/<to_cur>/<amount>", methods=["GET"])
@app.route("/<from_cur>/<to_cur>/<amount>", methods=["GET"])
def convert(from_cur, to_cur, amount):
    try:
        amt = float(amount)
    except ValueError:
        return jsonify({"error": "Amount must be numeric"}), 400

    from_iso = name_to_iso(from_cur)
    to_iso_code = name_to_iso(to_cur)

    key = (from_iso, to_iso_code)
    rate = STATIC_RATES.get(key)

    if rate is None:
        return jsonify({
            "error": "Conversion rate not available",
            "from": from_iso,
            "to": to_iso_code
        }), 404

    converted_amount = amt * rate

    return jsonify({
        "from": from_iso,
        "to": to_iso_code,
        "amount": amt,
        "rate": rate,
        "converted_amount": converted_amount,
        "mode": "static_conversion"
    }), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)