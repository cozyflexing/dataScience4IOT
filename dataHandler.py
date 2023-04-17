# sensor_handler.py
from sense_hat import SenseHat
from pymongo import MongoClient
from datetime import datetime
from time import sleep

# Replace 'your_mongodb_uri' with your actual MongoDB URI
client = MongoClient('your_mongodb_uri')
db = client['weather_data']
weather_collection = db['weather']

sense = SenseHat()

def get_temperature():
    temperature = round(sense.get_temperature() - 16.61, 2)
    return temperature

def get_pressure():
    pressure = round(sense.get_pressure(), 2)
    return pressure

def get_humidity():
    humidity = round(sense.get_humidity(), 2)
    return humidity

def save_data_to_mongodb(temperature, pressure, humidity):
    data = {
        'temperature': temperature,
        'pressure': pressure,
        'humidity': humidity,
        'timestamp': datetime.utcnow()
    }
    weather_collection.insert_one(data)

def update_and_save_values():
    temperature_value = round(get_temperature(), 2)
    pressure_value = round(get_pressure(), 2)
    humidity_value = round(get_humidity(), 2)
    
    save_data_to_mongodb(temperature_value, pressure_value, humidity_value)

if __name__ == "__main__":
    while True:
        update_and_save_values()
        sleep(30) # Save data every 60 seconds
