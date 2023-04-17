# sensehat-weather-monitor

## Introduction

This project demonstrates a weather monitor using the SenseHAT add-on board for Raspberry Pi. It measures temperature, pressure, and humidity, and displays the data in real-time using a Dash web application. The sensor data is also stored in a MongoDB database for historical analysis.

![SenseHAT Weather Monitor](https://raw.githubusercontent.com/username/sensehat-weather-monitor/main/sensehat-weather-monitor-screenshot.png)

## Architecture

![SenseHAT Weather Monitor Architecture](https://raw.githubusercontent.com/username/sensehat-weather-monitor/main/sensehat-weather-monitor-architecture.png)

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