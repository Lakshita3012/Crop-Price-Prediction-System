import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle

df = pd.read_csv("crop_data.csv")

le_veg = LabelEncoder()
le_city = LabelEncoder()

df["vegetable"] = le_veg.fit_transform(df["vegetable"])
df["city"] = le_city.fit_transform(df["city"])

df["lag1"] = df["current_price"].shift(1)
df["lag2"] = df["current_price"].shift(2)

df = df.dropna()

X = df[[
    "vegetable","city",
    "temperature","rainfall","demand",
    "lag1","lag2"
]]

y = df["future_price"]

model = RandomForestRegressor(n_estimators=100)
model.fit(X, y)

pickle.dump((model, le_veg, le_city), open("model.pkl", "wb"))

print("✅ Model trained")