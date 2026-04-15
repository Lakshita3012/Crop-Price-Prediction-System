import pandas as pd
import random

vegetables = ["Onion", "Tomato", "Potato"]
cities = ["Chennai", "Mumbai", "Delhi", "Bangalore", "Hyderabad"]

data = []

for i in range(1500):

    veg = random.choice(vegetables)
    city = random.choice(cities)

    temperature = random.randint(25, 35)
    rainfall = random.randint(0, 30)
    demand = random.randint(180, 300)

    current_price = random.randint(10, 40)

    # Future price logic (important for realism)
    future_price = current_price + (demand * 0.05) - (rainfall * 0.1) + random.randint(-3, 5)

    data.append([
        veg, city, temperature, rainfall,
        demand, current_price, round(future_price, 2)
    ])

df = pd.DataFrame(data, columns=[
    "vegetable", "city", "temperature", "rainfall",
    "demand", "current_price", "future_price"
])

df.to_csv("crop_data.csv", index=False)

print("✅ 1500 dataset created: crop_data.csv")