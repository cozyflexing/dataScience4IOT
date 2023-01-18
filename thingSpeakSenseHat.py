import time
import requests
from sense_hat import SenseHat
from time import sleep

sense = SenseHat() # Hier initialiseren je de SenseHat library.

# Kleuren voor de nachtmodus.
nightRed = (64, 0, 0)
nightGreen = (0, 64, 0)
nightOrange = (255, 140, 0)
nightWhite = (64, 64, 64)

# Kleuren voor de dagmodus.
red = (255, 0, 0)
green = (0, 128, 0)
orange = (255, 100, 0)
white = (255, 255, 255)

writeAPIkey = "" # Vul hier je eigen writeAPIkey in. 
channelID = "" # Vul hier je eigen channelID in.


url= "https://api.thingspeak.com/update"

# Geeft een float temperatuur terug.
def getTemperature():
    temperature = sense.get_temperature_from_pressure() - 7.3 
    # De '-7.3' is voor juiste calibratie, de temperatuur sensor geeft een te hooge waarde, 
    # dus die heb ik aangepast aan de hand van een preciezere temperatuur sensor. 
    return temperature

# Geeft een float luchtdruk terug.
def getPressure():
        pressure = sense.get_pressure()
        return pressure

# Geeft een float luchtvochtigheid terug. 
def getHumidity():
    humidity = sense.get_humidity()
    return humidity

# Geeft een dictionary met daarin de juiste waardes voor de verschillende fields op het Thingspeak dashboard.
def updateQuery(writeAPIkey,temperature, pressure, humidity):
    queries = {"api_key": writeAPIkey,
                "field1": temperature,
                "field2": pressure,
                "field3": humidity}
    return queries

# Deze functie stuurt de dictionary naar de update url om zo het dashboard te updaten.
def updateAPI(url):
    requests.get(url, params=updateQuery(writeAPIkey, getTemperature(), getPressure(), getHumidity()))

# Geeft een integer terug die de uur van de dag heeft als waarde.
def getLocalTimeHour():
    currentHour = time.localtime()
    return currentHour[3]

# Verlaagd felheid van ledmatrix.
def setLowLight():
    sense.low_light = True

# Verhoogd felheid van ledmatrix.
def setBrightLight():
    sense.low_light = False

# Laat informatie zien op de ledmatrix.
def showMessage(message, textColour, backgroundColour):
    sense.show_message(message, text_colour=textColour, back_colour=backgroundColour, scroll_speed=0.15)

# Start infinite loop.
while True:
    if getLocalTimeHour() < 7 or getLocalTimeHour() > 20: # We checken hier hoe laat het is zodat we dagmodus of nachtmodus kunnen activeren.
        setLowLight() # Nachtmodus aan.
        if getTemperature() >= 20: # Temperatuur check.
            showMessage(f"{round(getTemperature(),2)} C", nightWhite, nightGreen)
            updateAPI(url)
            sense.clear() # Zet scherm uit.
            sleep(300) # Wacht 5 minuten voordat het scherm weer aan kan.
            
        if 18 <= getTemperature() < 20: # Temperatuur check.
            showMessage(f"{round(getTemperature(),2)} C", nightWhite, nightOrange)
            updateAPI(url)
            sense.clear() # Zet scherm uit.
            sleep(300) # Wacht 5 minuten voordat het scherm weer aan kan.
            
        if 0 < getTemperature() < 18: # Temperatuur check.
            showMessage(f"{round(getTemperature(),2)} C", nightWhite, nightRed)
            updateAPI(url)
            sense.clear() # Zet scherm uit.
            sleep(300) # Wacht 5 minuten voordat het scherm weer aan kan.
            
    else:
        setBrightLight() # Dagmodus aan.
        if getTemperature() >= 20: # Temperatuur check.
            showMessage(f"{round(getTemperature(),2)} C", white, green)
            updateAPI(url)
            
        if 18 <= getTemperature() < 20: # Temperatuur check.
            showMessage(f"{round(getTemperature(),2)} C", white, orange)
            updateAPI(url)
            
        if 0 < getTemperature() < 18: # Temperatuur check.
            showMessage(f"{round(getTemperature(),2)} C", white, red)
            updateAPI(url)
            
        
