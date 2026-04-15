from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd
import requests

app = Flask(__name__)

# ── Load model ──────────────────────────────────────────────────────────────
model, le_veg, le_city = pickle.load(open("model.pkl", "rb"))
df = pd.read_csv("crop_data.csv")

# ── PASTE YOUR KEY HERE ──────────────────────────────────────────────────────
WEATHER_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"

CITY_COORDS = {
    "Chennai":   {"lat": 13.0827, "lon": 80.2707},
    "Mumbai":    {"lat": 19.0760, "lon": 72.8777},
    "Delhi":     {"lat": 28.6139, "lon": 77.2090},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
}

BASE_DEMAND = {
    "Chennai":   {"Onion": 220, "Tomato": 240, "Potato": 200},
    "Mumbai":    {"Onion": 260, "Tomato": 270, "Potato": 210},
    "Delhi":     {"Onion": 230, "Tomato": 250, "Potato": 220},
    "Bangalore": {"Onion": 210, "Tomato": 230, "Potato": 190},
    "Hyderabad": {"Onion": 200, "Tomato": 220, "Potato": 180},
}

BASE_PRICE = {"Onion": 22, "Tomato": 19, "Potato": 26}


def get_weather(city):
    coords = CITY_COORDS.get(city, CITY_COORDS["Chennai"])
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={coords['lat']}&lon={coords['lon']}"
        f"&appid={WEATHER_API_KEY}&units=metric"
    )
    try:
        r = requests.get(url, timeout=5)
        data = r.json()
        temperature = round(data["main"]["temp"], 1)
        rainfall = round(data.get("rain", {}).get("1h", 0), 1)
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"].title()
        icon = data["weather"][0]["icon"]
        return {
            "temperature": temperature,
            "rainfall": rainfall,
            "humidity": humidity,
            "description": description,
            "icon": f"https://openweathermap.org/img/wn/{icon}@2x.png",
            "live": True,
        }
    except Exception as e:
        return {
            "temperature": 30,
            "rainfall": 5,
            "humidity": 65,
            "description": "Data unavailable",
            "icon": "",
            "live": False,
            "error": str(e),
        }


@app.route("/")
def home():
    cities = list(CITY_COORDS.keys())
    return render_template("dashboard.html", cities=cities)


@app.route("/get_data", methods=["POST"])
def get_data():
    data = request.json
    city = data["city"]
    vegetable = data["vegetable"]
    weather = get_weather(city)
    demand = BASE_DEMAND.get(city, {}).get(vegetable, 220)
    humidity_factor = weather["humidity"] / 100
    demand = int(demand * (0.9 + humidity_factor * 0.2))
    base = BASE_PRICE.get(vegetable, 20)
    price = round(base + (demand * 0.02) - (weather["rainfall"] * 0.15), 2)
    return jsonify({
        "temperature": weather["temperature"],
        "rainfall": weather["rainfall"],
        "humidity": weather["humidity"],
        "description": weather["description"],
        "icon": weather["icon"],
        "demand": demand,
        "price": price,
        "live": weather["live"],
    })


@app.route("/analytics")
def analytics():
    data = df.head(30)
    labels = list(range(1, len(data) + 1))
    prices = list(data["current_price"])
    demand = list(data["demand"])
    rainfall = list(data["rainfall"])
    future_prices = list(data["future_price"])
    return render_template(
        "analytics.html",
        labels=labels,
        prices=prices,
        demand=demand,
        rainfall=rainfall,
        future_prices=future_prices,
    )


@app.route("/market")
def market():
    market_data = []
    for city in CITY_COORDS:
        weather = get_weather(city)
        for veg in ["Onion", "Tomato", "Potato"]:
            demand = BASE_DEMAND[city][veg]
            base = BASE_PRICE[veg]
            price = round(base + (demand * 0.02) - (weather["rainfall"] * 0.15), 2)
            market_data.append({
                "city": city,
                "vegetable": veg,
                "price": price,
                "temperature": weather["temperature"],
                "rainfall": weather["rainfall"],
            })
    return render_template("market.html", market_data=market_data)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    veg = le_veg.transform([data["vegetable"]])[0]
    city = le_city.transform([data["city"]])[0]
    price = float(data["price"])
    temp = float(data["temperature"])
    rain = float(data["rainfall"])
    demand = float(data["demand"])
    lag1 = price
    lag2 = price - 2
    forecast = []
    history = [round(price - 5, 2), round(price - 2, 2), round(price, 2)]
    for i in range(7):
        inp = np.array([[veg, city, temp, rain, demand, lag1, lag2]])
        pred = round(float(model.predict(inp)[0]), 2)
        forecast.append(pred)
        lag2 = lag1
        lag1 = pred
    return jsonify({
        "predicted": forecast[0],
        "history": history,
        "forecast": forecast,
    })


if __name__ == "__main__":
    app.run(debug=True)
