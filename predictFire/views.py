import geocoder
import requests
import pickle
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import os

def predictor():
    # Define a function to predict forest fire occurrence based on location, oxygen level, temperature, and humidity
    def predict_forest_fire(oxygen, temperature, humidity, model_path):
        # Load the trained model
        with open(model_path, 'rb') as file:
            forest_model = pickle.load(file)
        
        # Create test input with provided parameters
        test_input = pd.DataFrame({
            'Oxygen': [oxygen],
            'Temperature': [temperature],
            'Humidity': [humidity]
        })

        # Predicting fire occurrence using the trained model
        predicted_output = forest_model.predict(test_input)
        return predicted_output[0]

    # Define a function to predict flood occurrence based on rainfall
    def predict_flood(rainfall, model_path):
        # Load the trained model
        with open(model_path, 'rb') as file:
            flood_model = pickle.load(file)

        # Predicting flood occurrence using the trained model
        test_input = [[rainfall]]  # Model expects a 2D array
        predicted_output = flood_model.predict(test_input)
        return predicted_output[0]

    # Get current location
    def get_current_location():
        g = geocoder.ip('me')
        return g.latlng

    # Fetch weather data
    def fetch_weather_data(latitude, longitude, api_key):
        url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}'
        response = requests.get(url)
        data = response.json()
        return data

    # Main function to fetch all data and make predictions
    def fetch_and_predict(api_key, forest_model_path, flood_model_path):
        # Fetch weather data
        latitude, longitude = get_current_location()
        weather_data = fetch_weather_data(latitude, longitude, api_key)
        
        # Extract relevant weather parameters
        temperature = weather_data.get('main', {}).get('temp')
        humidity = weather_data.get('main', {}).get('humidity')
        # You may need to adjust the keys based on the structure of the response data
        
        # Predict forest fire occurrence
        forest_prediction = predict_forest_fire(21, temperature, humidity, forest_model_path)  # Provide default oxygen level
        
        # Predict flood occurrence
        rainfall = weather_data.get('rain', {}).get('1h', 0)  # Get 1-hour rainfall, default to 0 if not available
        flood_prediction = predict_flood(rainfall, flood_model_path)
        
        return forest_prediction, flood_prediction

    
    # Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
    api_key = '4bdbf886dc42be393258bcc3034b85c1'
    # Replace 'forest_model.pkl' and 'flood_model.pkl' with the paths to your model files
    current = os.path.dirname(os.path.abspath(__file__))
    forest_model_path = os.path.join(current,'forest1_pickle' )
    
    flood_model_path = os.path.join(current,'flood1_pickle' )
    
    forest_result, flood_result = fetch_and_predict(api_key, forest_model_path, flood_model_path)

    predictions = [forest_result, flood_result]

    return predictions



print(predictor())