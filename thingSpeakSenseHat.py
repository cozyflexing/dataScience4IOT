import time
import requests
from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

nightRed = (64, 0, 0)
nightGreen = (0, 64, 0)
nightOrange = (255, 140, 0)
nightWhite = (64, 64, 64)

red = (255, 0, 0)
green = (0, 128, 0)
orange = (255, 100, 0)
white = (255, 255, 255)

writeAPIkey = "" # Input personal writeAPIkey
channelID = "" #Input personal channelID

url= "https://api.thingspeak.com/update"

def getTemperature():
    temp = round(sense.get_temperature_from_pressure()-7.3,3)
    return temp

def getPressure():
        press = round(sense.get_pressure(),3)
        return press

def getHumidity():
    hum = round(sense.get_humidity(),3)
    return hum

def updateQuery(writeAPIkey,temperature, pressure, humidity):
    queries = {"api_key": writeAPIkey,
                "field1": temperature,
                "field2": pressure,
                "field3": humidity}
    return queries

def updateAPI(url):
    requests.get(url, params=updateQuery(writeAPIkey, getTemperature(), getPressure(), getHumidity()))

def getLocalTimeHour():
    currentHour = time.localtime()
    return currentHour[3]

while True:
    if getLocalTimeHour() < 7 or getLocalTimeHour() > 20:
        sense.low_light = True
        
        if getTemperature() >= 20:
            sense.show_message(f"{round(getTemperature(),2)} C", text_colour=nightWhite, back_colour=nightGreen, scroll_speed=0.15)
            updateAPI(url)
            sense.clear()
            sleep(300)
            
        if 18 <= getTemperature() < 20:
            sense.show_message(f"{round(getTemperature(),2)} C", text_colour=nightWhite, back_colour=nightOrange, scroll_speed=0.15)
            updateAPI(url)
            sense.clear()
            sleep(300)
            
        if 0 < getTemperature() < 18:
            sense.show_message(f"{round(getTemperature(),2)} C", text_colour=nightWhite, back_colour=nightRed, scroll_speed=0.15)
            updateAPI(url)
            sense.clear()
            sleep(300)
            
    else:
        sense.low_light = False
        if getTemperature() >= 20:
            sense.show_message(f"{round(getTemperature(),2)} C", text_colour=white, back_colour=green, scroll_speed=0.15)
            updateAPI(url)
            
        if 18 <= getTemperature() < 20:
            sense.show_message(f"{round(getTemperature(),2)} C", text_colour=white, back_colour=orange, scroll_speed=0.15)
            updateAPI(url)
            
        if 0 < getTemperature() < 18:
            sense.show_message(f"{round(getTemperature(),2)} C", text_colour=white, back_colour=red, scroll_speed=0.15)
            updateAPI(url)
            
        
