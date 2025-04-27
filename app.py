from flask import Flask, render_template, request

app = Flask(__name__)

# Exchange rates (relative to USD)
exchange_rates = {
    "USD": 1.0,
    "EUR": 0.85,
    "INR": 83.0,
    "JPY": 151.0,
    "GBP": 0.75,
    "AUD": 1.52,
    "CAD": 1.36,
    "CNY": 7.24,
    "CHF": 0.91,
    "ZAR": 18.7
}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    currencies = list(exchange_rates.keys())

    if request.method == "POST":
        from_currency = request.form["from_currency"].upper()
        to_currency = request.form["to_currency"].upper()
        amount = request.form["amount"]

        try:
            amount = float(amount)
            if from_currency not in exchange_rates or to_currency not in exchange_rates:
                error = "Invalid currency code."
            elif amount < 0:
                error = "Amount cannot be negative."
            elif from_currency == to_currency:
                result = f"{amount:.2f} {from_currency} = {amount:.2f} {to_currency}"
            else:
                usd_amount = amount / exchange_rates[from_currency]
                converted = usd_amount * exchange_rates[to_currency]
                result = f"{amount:.2f} {from_currency} = {converted:.2f} {to_currency}"
        except ValueError:
            error = "Please enter a valid number for amount."

    return render_template("index.html", result=result, error=error, currencies=currencies)

if __name__ == "__main__":
    app.run(debug=True)
