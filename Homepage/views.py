from django.shortcuts import render
import os
import json
import re
import requests
from bs4 import BeautifulSoup
import geocoder
import requests
import pickle
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import os


def scrape_and_save(url, output_file):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles_list = []

        # find all parent tags
        parent_tags = soup.find_all(class_="uwU81")

        # Iterate through parent tags
        for parent_tag in parent_tags:
            # Check if the parent tag has a child with class "fHv_i"
            article = parent_tag.find(class_="fHv_i")
            if article:
                title = article.text
                paragraph_elem = parent_tag.find(class_="oxXSK")
                paragraph = paragraph_elem.text if paragraph_elem else "No description available"

                # Check if the title contains specific words
                keywords = ["earthquake", "magnitude", "forest fire", "tsunami", "cyclone", "pandemic", "epidemic", "drought", "flood"]
                for keyword in keywords:
                    if keyword.lower() in title.lower():
                        articles_list.append({"title": title, "paragraph": paragraph})
                        break

        # Create JSON structure
        data = {"articles": articles_list}

        # Write data to JSON file
        with open(output_file, "w") as file:
            json.dump(data, file, indent=4)

        print("Scraping completed and data saved to", output_file)
    else:
        print("Failed to fetch data from the webpage")

# Example usage
current_dir = os.path.dirname(os.path.abspath(__file__))
json_file = os.path.join(current_dir, "sample.json")
print(json_file)

# json_file = 'E:\GoogleSolutionChallenge\Exodia\Exodia\Homepage\sample.json'


# Function to map earthquake intensity to common scale
def earthquake_scale(magnitude):
    if magnitude < 3:
        return 1  # Low
    elif magnitude < 4:
        return 2  # Moderate
    elif magnitude < 5:
        return 3  # Significant
    elif magnitude < 6:
        return 4  # Severe
    elif magnitude < 8:
        return 5  # extreme
    else:
        return 0  

# Function to map avalanche size to common scale
def avalanche_scale(size):
    if size == "small":
        return 1  # Low
    elif size == "medium":
        return 2  # Moderate
    elif size == "large":
        return 3  # Significant
    elif size == "very large":
        return 4  # Severe
    else:
        return 0  # Extreme

# Function to map tsunami magnitude scale to common scale
def tsunami_scale(magnitude):
    if magnitude < 3:
        return 1  # Low
    elif magnitude < 4:
        return 2  # Moderate
    elif magnitude < 5:
        return 3  # Significant
    elif magnitude < 6:
        return 4  # Severe
    elif magnitude < 7:
        return 5  # Extreme
    else:
        return 0

# Function to map cyclone category to common scale
def cyclone_scale(category):
    if category == 1:
        return 1  # Low
    elif category == 2:
        return 2  # Moderate
    elif category == 3:
        return 3  # Significant
    elif category == 4:
        return 4  # Severe
    elif category == 5:
        return 5  # Extreme
    else:
        return 0

# Function to map pandemic outbreak scale to common scale
def pandemic_scale(outbreak):
    if outbreak == "local":
        return 1  # Low
    elif outbreak == "regional":
        return 2  # Moderate
    elif outbreak == "national":
        return 3  # Significant
    elif outbreak == "international":
        return 4  # Severe
    else:
        return 0  # Extreme

# Function to map flood water level to common scale
def flood_scale(water_level):
    if water_level < 10:
        return 1  # Low
    elif water_level < 20:
        return 2  # Moderate
    elif water_level < 30:
        return 3  # Significant
    elif water_level < 40:
        return 4  # Severe
    else:
        return 0  # Extreme

# Function to extract disaster information from a paragraph
def extract_disaster_info(title, paragraph):
    disaster_types = ["earthquake", "avalanche", "tsunami", "cyclone", "pandemics", "floods"]
    location_regex = r'in \s*([^\.,]+)'
    intensity_regex = r'(\d+(\.\d+)?)\s*(magnitude|richter)?'
    water_level_regex = r'(\d+(\.\d+)?)\s*(cm|meters|meter|m)'
    shelter_keywords = ["shelter", "evacuation", "rescue"]

    # Find disaster type
    for disaster_type in disaster_types:
        if disaster_type in title.lower():
            disaster_name = disaster_type.capitalize()
            break
    else:
        return None  # Not a disaster article

    # Find location
    location_match = re.search(location_regex, paragraph, re.IGNORECASE)
    location = location_match.group(1).strip() if location_match else ""

    # Find intensity or water level based on disaster type
    if disaster_name == "Floods":
        water_level_match = re.search(water_level_regex, paragraph, re.IGNORECASE)
        intensity = float(water_level_match.group(1)) if water_level_match else 0
    else:
        intensity_match = re.search(intensity_regex, paragraph, re.IGNORECASE)
        intensity = float(intensity_match.group(1)) if intensity_match else 0

    # Find shelter information
    shelters = []
    for keyword in shelter_keywords:
        if keyword in paragraph.lower():
            shelter_matches = re.findall(r'\b' + keyword + r'\b\s*([^\.,]+)', paragraph, re.IGNORECASE)
            shelters.extend(shelter_matches)

    shelter_info = ', '.join(shelters) if shelters else "Not mentioned"

    # Determine common scale based on disaster type
    if disaster_name == "Earthquake":
        common_scale = earthquake_scale(intensity)
    elif disaster_name == "Avalanche":
        common_scale = avalanche_scale(location) 
    elif disaster_name == "Tsunami":
        common_scale = tsunami_scale(intensity)  
    elif disaster_name == "Cyclone":
        common_scale = cyclone_scale(intensity)  
    elif disaster_name == "Pandemics":
        common_scale = pandemic_scale(location)  
    elif disaster_name == "Floods":
        common_scale = flood_scale(intensity)  

    return {
        "name": disaster_name,
        "location": location,
        "scale (original)": intensity,
        "scale (common)": common_scale,
        "shelter": shelter_info
    }

# Function to process news articles JSON file
def process_news_articles(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    disaster_info_list = []
    for article in data['articles']:
        title = article['title']
        paragraph = article['paragraph']
        disaster_info = extract_disaster_info(title, paragraph)
        if disaster_info:
            disaster_info_list.append(disaster_info)

    return disaster_info_list

result = process_news_articles(json_file)
for info in result:
    print(info)



def create_list():
    result = process_news_articles(json_file)
    class Spots:
        def __init__(self):
            self.spots = []
            for info in result:
                self.spots.append({
                    'disaster': info['name'],
                    'location': info['location'],
                    'scale': info['scale (original)'],
                    'UniScale': info['scale (common)'],
                    'shelterlist': info['shelter']
                })

        def __iter__(self):
            return iter(self.spots)

    spots = Spots()
    return spots


# Predictor------------------------------------------------------------
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



# Base -----------------------------------------------------------------


# Create your views here.
def home_view(request, *args, **kwargs):
    # whatever function is fetching City and Country name of current location, should return here
    city = "Dehradun"
    country = "India"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_dir, "sample.json")
    scrape_and_save("https://timesofindia.indiatimes.com/topic/disaster-alert", output_file)

    hotspots = create_list()
    prediction = predictor()
    p1 = prediction[0]
    p2 = prediction[1]
    context = {
        'city' : city,
        'country' : country,
        'list' : hotspots,
        'p1' : p1,
        'p2': p2,
    }
    return render(request, 'home.html', context)


