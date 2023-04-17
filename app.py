# app.py
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pymongo import MongoClient
import datetime
import plotly.graph_objs as go
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
from sense_hat import SenseHat
import time

sense = SenseHat()


def flash_led_matrix_red():
    for i in range(5):
        sense.clear()
        time.sleep(0.5)
        sense.set_pixels([(255, 0, 0)] * 64)
        time.sleep(0.5)
    sense.clear()


uri = "mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"), tlsCAFile=certifi.where())


db = client["weather_data"]
weather_collection = db["weather"]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container(
    [
        html.H1("Sense-Hat Monitor", style={"text-align": "center"}),
        html.Br(),
        dbc.Row(
            [
                dbc.Col([html.H4("Temperature"), html.P(id="temperature")]),
                dbc.Col([html.H4("Pressure"), html.P(id="pressure")]),
                dbc.Col([html.H4("Humidity"), html.P(id="humidity")]),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id="temperature-graph")]),
                dbc.Col([dcc.Graph(id="pressure-graph")]),
                dbc.Col([dcc.Graph(id="humidity-graph")]),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id="temperature-4h-graph")]),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id="pressure-4h-graph")]),
            ]
        ),
        dbc.Row([dbc.Col([dcc.Graph(id="humidity-4h-graph")])]),
        dcc.Interval(id="interval", interval=1 * 30000, n_intervals=0),
        html.Div(id="alert-container"),
    ]
)


@app.callback(
    Output("temperature", "children"),
    Output("pressure", "children"),
    Output("humidity", "children"),
    Output("temperature-graph", "figure"),
    Output("pressure-graph", "figure"),
    Output("humidity-graph", "figure"),
    Output("temperature-4h-graph", "figure"),
    Output("pressure-4h-graph", "figure"),
    Output("humidity-4h-graph", "figure"),
    Output("alert-container", "children"),  # Add this line
    Input("interval", "n_intervals"),
)
def update_values(n):
    latest_data = weather_collection.find_one(sort=[("timestamp", -1)])

    if latest_data:
        temperature_value = latest_data["temperature"]
        pressure_value = latest_data["pressure"]
        humidity_value = latest_data["humidity"]
    else:
        temperature_value, pressure_value, humidity_value = None, None, None

    # Fetch the last 4 hours data
    now = datetime.datetime.utcnow()
    start_time = now - datetime.timedelta(hours=4)
    query = {"timestamp": {"$gte": start_time}}
    historical_data = weather_collection.find(query).sort("timestamp", 1)

    timestamps, temperatures, pressures, humidities = [], [], [], []

    for data in historical_data:
        timestamps.append(data["timestamp"])
        temperatures.append(data["temperature"])
        pressures.append(data["pressure"])
        humidities.append(data["humidity"])

    temperature_figure = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=temperature_value,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Temperature"},
            gauge={
                "axis": {"range": [None, 40]},
                "bar": {"color": "rgba(0, 0, 0, 0.5)"},
                "steps": [
                    {"range": [0, 10], "color": "lightblue"},
                    {"range": [10, 30], "color": "lightgreen"},
                    {"range": [30, 40], "color": "red"},
                ],
            },
        )
    )

    pressure_figure = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=pressure_value,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Pressure"},
            gauge={
                "axis": {"range": [None, 1200]},
                "bar": {"color": "rgba(0, 0, 0, 0.5)"},
                "steps": [
                    {"range": [0, 1000], "color": "lightgreen"},
                    {"range": [1000, 1100], "color": "yellow"},
                    {"range": [1100, 1200], "color": "red"},
                ],
            },
        )
    )

    humidity_figure = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=humidity_value,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Humidity"},
            gauge={
                "axis": {"range": [None, 100]},
                "bar": {"color": "rgba(0, 0, 0, 0.5)"},
                "steps": [
                    {"range": [0, 55], "color": "lightgreen"},
                    {"range": [55, 65], "color": "yellow"},
                    {"range": [65, 100], "color": "red"},
                ],
            },
        )
    )

    # Separate figures for each parameter
    temperature_history_figure = go.Figure()
    pressure_history_figure = go.Figure()
    humidity_history_figure = go.Figure()

    temperature_history_figure.add_trace(
        go.Scatter(x=timestamps, y=temperatures, mode="lines", name="Temperature")
    )
    pressure_history_figure.add_trace(
        go.Scatter(x=timestamps, y=pressures, mode="lines", name="Pressure")
    )
    humidity_history_figure.add_trace(
        go.Scatter(x=timestamps, y=humidities, mode="lines", name="Humidity")
    )

    temperature_history_figure.update_layout(
        title="4 Hours Temperature Data", xaxis_title="Time", yaxis_title="Temperature"
    )

    pressure_history_figure.update_layout(
        title="4 Hours Pressure Data", xaxis_title="Time", yaxis_title="Pressure"
    )

    humidity_history_figure.update_layout(
        title="4 Hours Humidity Data", xaxis_title="Time", yaxis_title="Humidity"
    )
    alert_list = []

    if temperature_value and temperature_value >= 30:
        alert_list.append("High temperature!")

    if pressure_value and pressure_value >= 1100:
        alert_list.append("High pressure!")

    if humidity_value and humidity_value >= 65:
        alert_list.append("High humidity!")

    if alert_list:
        flash_led_matrix_red()

    # Create alerts if any conditions are met
    alerts = []
    for alert_text in alert_list:
        alerts.append(
            dbc.Alert(alert_text, color="danger", duration=5000, dismissable=True)
        )
    return (
        temperature_value,
        pressure_value,
        humidity_value,
        temperature_figure,
        pressure_figure,
        humidity_figure,
        temperature_history_figure,
        pressure_history_figure,
        humidity_history_figure,
        alerts,
    )


if __name__ == "__main__":
    app.run_server(debug=True)
