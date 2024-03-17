from django.shortcuts import render
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import os
# Define a function to predict forest fire occurrence based on location, oxygen level, temperature, and humidity
current = os.path.dirname(os.path.abspath(__file__))
output = os.path.join(current,'forest1_pickle' )
with open(output,'rb') as file:
    mp=pickle.load(file)
# Create test input with only the columns specified in the model's column list
test_input = pd.DataFrame({
    'Oxygen': [21, 22, 23],
    'Temperature': [25, 26, 27],
    'Humidity': [40, 45, 50]
})

# Predicting fire occurrence using the trained model
predicted_output = mp.predict(test_input)
print(predicted_output)
# flood

output2 = os.path.join(current,'flood1_pickle' )
with open(output2,'rb') as file:
    mp2=pickle.load(file)
test_input=[[3248.6]]
predicted_output = mp2.predict(test_input)

print("Predicted Output:")
print(predicted_output)

