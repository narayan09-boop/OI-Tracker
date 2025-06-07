from flask import Flask, render_template, jsonify, request
from nsepython import nse_optionchain_scrapper

app = Flask(__name__)

def calculate_oi_change_percent(open_interest, change_in_oi):
    previous_oi = open_interest - change_in_oi
    if previous_oi == 0:
        return 0.0
    try:
        return round((change_in_oi / previous_oi) * 100, 2)
    except ZeroDivisionError:
        return 0.0

@app.route("/")
def index():
    symbol = "NIFTY"
    data = nse_optionchain_scrapper(symbol)
    expiries = data["records"]["expiryDates"]
    expiry = expiries[0] if expiries else None

    return render_template("index.html", expiries=expiries, expiry=expiry)

@app.route("/data/")
def get_option_data():
    symbol = "NIFTY"
    expiry = request.args.get('expiry')

    data = nse_optionchain_scrapper(symbol)
    expiries = data["records"]["expiryDates"]

    if not expiry or expiry not in expiries:
        expiry = expiries[0] if expiries else None

    options = [entry for entry in data["records"]["data"] if entry["expiryDate"] == expiry] if expiry else []

    # Pick current strike
    strike_prices = sorted({entry['strikePrice'] for entry in options})
    if not strike_prices:
        calls = []
        puts = []
    else:
        # Find closest strike to underlying price
        underlying = data["records"]["underlyingValue"]
        closest_strike = min(strike_prices, key=lambda x: abs(x - underlying))
        idx = strike_prices.index(closest_strike)

        # Take 3 strikes below, current, 3 strikes above (total 7)
        start = max(0, idx - 3)
        end = min(len(strike_prices), idx + 4)
        selected_strikes = strike_prices[start:end]

        calls = []
        puts = []
        for strike in selected_strikes:
            option_data = next((entry for entry in options if entry["strikePrice"] == strike), None)
            if option_data:
                if "CE" in option_data and option_data["CE"]:
                    ce = option_data["CE"]
                    oi = ce.get('openInterest', 0)
                    coi = ce.get('changeinOpenInterest', 0)
                    oi_chg_percent = calculate_oi_change_percent(oi, coi)
                    calls.append({
                        'strikePrice': ce.get('strikePrice', ''),
                        'lastPrice': ce.get('lastPrice', 0),
                        'openInterest': oi,
                        'changeinOpenInterest': coi,
                        'oiChangePercent': oi_chg_percent,
                        'openInterestLakh': round(oi / 100000, 2),
                        'totalTradedVolume': ce.get('totalTradedVolume', 0),
                        'impliedVolatility': ce.get('impliedVolatility', 0),
                    })
                else:
                    calls.append({})
                if "PE" in option_data and option_data["PE"]:
                    pe = option_data["PE"]
                    oi = pe.get('openInterest', 0)
                    coi = pe.get('changeinOpenInterest', 0)
                    oi_chg_percent = calculate_oi_change_percent(oi, coi)
                    puts.append({
                        'strikePrice': pe.get('strikePrice', ''),
                        'lastPrice': pe.get('lastPrice', 0),
                        'openInterest': oi,
                        'changeinOpenInterest': coi,
                        'oiChangePercent': oi_chg_percent,
                        'openInterestLakh': round(oi / 100000, 2),
                        'totalTradedVolume': pe.get('totalTradedVolume', 0),
                        'impliedVolatility': pe.get('impliedVolatility', 0),
                    })
                else:
                    puts.append({})
            else:
                calls.append({})
                puts.append({})

    return jsonify({
        "calls": calls,
        "puts": puts,
        "expiry": expiry,
        "underlying": data["records"]["underlyingValue"]
    })

if __name__ == "__main__":
    app.run(debug=True)
