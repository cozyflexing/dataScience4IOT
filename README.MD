# sensehat-weather-monitor

## Introduction

This project demonstrates a weather monitor using the SenseHAT add-on board for Raspberry Pi. It measures temperature, pressure, and humidity, and displays the data in real-time using a Dash web application. The sensor data is also stored in a MongoDB database for historical analysis.

![SenseHAT Weather Monitor Dashboard](https://github.com/cozyflexing/dataScience4IOT/blob/33a5886199d38828c2789780666378c04d29d8b9/Dashboard%20Part%201.png)

## Parts

![Sense-Hat Weather Monitor Separate](https://github.com/cozyflexing/dataScience4IOT/blob/9587aad39beb7e2d4f7242eac818a00f9f5c5997/separateParts.JPG)
![Sense-Hat Weather Monitor Combined 1]
(https://github.com/cozyflexing/dataScience4IOT/blob/7ff92f0e6689487a3c03aa7619acabae37a6884b/combined1.JPG)
![Sense-Hat Weather Monitor Combined 2]
(https://github.com/cozyflexing/dataScience4IOT/blob/7ff92f0e6689487a3c03aa7619acabae37a6884b/combined2.JPG)
![Sense-Hat Weather Monitor Combined 3]
(https://github.com/cozyflexing/dataScience4IOT/blob/7ff92f0e6689487a3c03aa7619acabae37a6884b/combined3.JPG)
![Sense-Hat Weather Monitor Combined 4]
(https://github.com/cozyflexing/dataScience4IOT/blob/7ff92f0e6689487a3c03aa7619acabae37a6884b/combined4.JPG)

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

1. Header with the title "SenseHat Weather Monitor"
2. Row with three columns for displaying the current temperature, pressure, and humidity
3. Two rows, each containing three columns with graphs for displaying the historical data

### Updating the Data

The `update_values` function is triggered by the interval component every 30 seconds. This function fetches the latest data from the MongoDB database and updates the gauges and historical line charts in the web application.

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

### Setup

1. Set up a Raspberry Pi with the SenseHAT add-on board.
2. Install the required Python packages:

```bash
pip install dash dash-bootstrap-components pymongo sense-hat
```

3. Clone the repository:

```bash
git clone https://github.com/username/sensehat-weather-monitor.git
```

4. Replace your_mongodb_uri in sensor_handler.py with your actual MongoDB URI.
5. Run the sensor_handler.py script to start collecting data.
6. Run the app.py script to start the Dash web application.

### Credits

This project was inspired by various weather monitoring projects using the SenseHAT add-on board.

### Resources

- SenseHAT Documentation
- Dash Documentation
- MongoDB Python Driver
