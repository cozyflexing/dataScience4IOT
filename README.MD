# sensehat-monitor

## Introduction

This project demonstrates a monitor using the Sense-Hat add-on board for Raspberry Pi. It measures temperature, pressure, and humidity, and displays the data in real-time using a Dash web application. The sensor data is also stored in a MongoDB database for historical analysis.

![Sense-Hat Monitor Dashboard](https://github.com/cozyflexing/dataScience4IOT/blob/5ee03c3dadeccccaeafba74fd92b79e41e329919/Dashboard.png)

## Parts

![Sense-Hat Monitor Separate](https://github.com/cozyflexing/dataScience4IOT/blob/9587aad39beb7e2d4f7242eac818a00f9f5c5997/separateParts.JPG)

![Sense-Hat Monitor Combined 4](https://github.com/cozyflexing/dataScience4IOT/blob/7ff92f0e6689487a3c03aa7619acabae37a6884b/combined4.JPG)

The Sense-Hat is put directly on top of the Raspberry Pi 4 and is held in place with 4 scews at each corner.

## IoT Pipeline

![Data Pipeline](https://github.com/cozyflexing/dataScience4IOT/blob/d819b91ca998dedd4bbcfb8e8a57db1b7d942161/Pipeline.jpeg)

### Sensor Data Collection

The `sensor_handler.py` script periodically collects data from the SenseHAT board and stores it in a MongoDB database. The data collected includes temperature, pressure, and humidity.

### Database

A MongoDB database is used to store the sensor data. The sensor data is stored in a collection named `weather`.

### Web Application

The web application is built using the Dash framework, which is a Python library for creating analytical web applications. The application consists of the following components:

- Temperature, pressure, and humidity gauges
- 4-hour historical line charts for each parameter

The web application updates the displayed data every 30 seconds.

### Dash Application Layout

The Dash application layout consists of a Bootstrap container with three main sections:

1. Header with the title "SenseHat Monitor"
2. Row with three columns for displaying the current temperature, pressure, and humidity
3. Two rows, each containing three columns with graphs for displaying the historical data

### Updating the Data

The `update_values` function is triggered by the interval component every 30 seconds. This function fetches the latest data from the MongoDB database and updates the gauges and historical line charts in the web application.
### Requirements
- Python 3.7 or higher
- Dash
- Dash Bootstrap Components
- Dash Core Components
- Dash HTML Components
- Plotly
- PyMongo
- Certifi
- Sense-HAT library

### Installation
1. Set up a Raspberry Pi with the Sense-HAT add-on board.
2. Install the required Python packages:
```bash
pip install dash dash_bootstrap_components dash_core_components dash_html_components plotly pymongo certifi sense-hat
```
3. Clone the repository:
```bash
git clone https://github.com/username/sensehat-weather-monitor.git
```
4. Replace your_mongodb_uri in sensor_handler.py with your actual MongoDB URI.
5. Run the sensor_handler.py script to start collecting data.
6. Run the app.py script to start the Dash web application.

### Features
1. Real-time monitoring of temperature, pressure, and humidity
2. 4-hour historical data visualization for temperature, pressure, and humidity
3. Gauge charts for each weather parameter
4. Line charts for historical data
5. Automatic red LED flashing on the Sense-HAT when high temperature is detected
6. Mobile and desktop friendly web application

### Running the Application

To run the application, execute the `app.py` script.

```bash
python app.py
```

The web application will be accessible at http://127.0.0.1:8050/.

### Sensor Data Collection Script

The sensor_handler.py script collects data from the SenseHAT board and stores it in the MongoDB database. It is executed independently of the Dash web application.

To run the data collection script, execute the sensor_handler.py script.

```bash
python sensor_handler.py
```

The script will collect and store sensor data every 30 seconds.

### Usage
1. Open the web application in a browser, either on the Raspberry Pi itself or on another device within the same network by using the Raspberry Pi's IP address.
2. Monitor the real-time temperature, pressure, and humidity data displayed on the gauges.
3. Observe the historical data in the line charts below the gauges, which displays the last 4 hours of sensor data.

### Customization
You can customize the application by modifying the following parameters:

- Data collection interval: Adjust the interval between sensor readings by changing the sleep duration in the sensor_handler.py script.
- Web application update interval: Modify the update interval in the app.py script by changing the value of the interval component.
- Chart time range: Change the duration of the historical data displayed in the line charts by adjusting the time range in the app.py script.

### Resources

- [SenseHAT Documentation](https://pythonhosted.org/sense-hat/api/)
- [Dash Documentation](https://dash.plotly.com/)
- [MongoDB Python Driver](https://pymongo.readthedocs.io/en/stable/)
