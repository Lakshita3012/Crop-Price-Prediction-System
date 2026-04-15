🌱 AgriPredict —  # Crop Price Prediction System

This project predicts vegetable prices (Onion, Tomato, Potato) across 5 Indian cities — Chennai, Mumbai, Delhi, Bangalore, and Hyderabad — using Machine Learning and real-time weather data from OpenWeatherMap.

It has 3 pages:

	∙	Dashboard → Select city & vegetable → fetches live weather → gives 7-day price forecast with a chart
	
	∙	Market → Shows dynamic prices for all city-vegetable combinations based on live weather
	
	∙	Analytics → 4 charts: price trend, price vs rainfall scatter, price vs demand bar, and price volatility

The ML model is a Random Forest Regressor trained on 1,500 records with features like temperature, rainfall, demand, and lag prices.

To run this file:

1. Install libraries
   
pip3 install flask scikit-learn pandas numpy requests

2. Add your OpenWeatherMap API key in app.py line 16
   
3. Retrain the model
python3 generate_data.py
python3 model.py

4. Start the app
python3 app.py

5. Open in browser
http://127.0.0.1:5000
