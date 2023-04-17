# app.py
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pymongo import MongoClient
import datetime
import plotly.graph_objs as go
from db import client

db = client['weather_data']
weather_collection = db['weather']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    html.H1("SenseHat Weather Monitor", style={"text-align": "center"}),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H4("Temperature"),
            html.P(id="temperature")
        ]),
        dbc.Col([
            html.H4("Pressure"),
            html.P(id="pressure")
        ]),
        dbc.Col([
            html.H4("Humidity"),
            html.P(id="humidity")
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="temperature-graph")
        ]),
        dbc.Col([
            dcc.Graph(id="pressure-graph")
        ]),
        dbc.Col([
            dcc.Graph(id="humidity-graph")
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="temperature-4h-graph")
        ]),
        dbc.Col([
            dcc.Graph(id="pressure-4h-graph")
        ]),
        dbc.Col([
            dcc.Graph(id="humidity-4h-graph")
        ])
    ]),
    dcc.Interval(id="interval", interval=1*30000, n_intervals=0)
])

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
    Input("interval", "n_intervals")
)

def update_values(n):
    latest_data = weather_collection.find_one(sort=[("timestamp", -1)])
    
    if latest_data:
        temperature_value = latest_data['temperature']
        pressure_value = latest_data['pressure']
        humidity_value = latest_data['humidity']
    else:
        temperature_value, pressure_value, humidity_value = None, None, None

    # Fetch the last 4 hours data
    now = datetime.datetime.now()
    start_time = now - datetime.timedelta(hours=4)
    query = {"timestamp": {"$gte": start_time}}
    historical_data = weather_collection.find(query).sort("timestamp", 1)

    timestamps, temperatures, pressures, humidities = [], [], [], []

    for data in historical_data:
        timestamps.append(data['timestamp'])
        temperatures.append(data['temperature'])
        pressures.append(data['pressure'])
        humidities.append(data['humidity'])

    temperature_figure = go.Figure(go.Indicator(
        mode="gauge+number",
        value=temperature_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Temperature"},
    ))

    pressure_figure = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pressure_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Pressure"},
    ))

    humidity_figure = go.Figure(go.Indicator(
        mode="gauge+number",
        value=humidity_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Humidity"},
    ))

    # Separate figures for each parameter
    temperature_history_figure = go.Figure()
    pressure_history_figure = go.Figure()
    humidity_history_figure = go.Figure()

    temperature_history_figure.add_trace(go.Scatter(
        x=timestamps, y=temperatures, mode="lines", name="Temperature"
    ))
    pressure_history_figure.add_trace(go.Scatter(
        x=timestamps, y=pressures, mode="lines", name="Pressure"
    ))
    humidity_history_figure.add_trace(go.Scatter(
        x=timestamps, y=humidities, mode="lines", name="Humidity"
    ))

    temperature_history_figure.update_layout(
        title="4 Hours Temperature Data",
        xaxis_title="Time",
        yaxis_title="Temperature"
    )

    pressure_history_figure.update_layout(
        title="4 Hours Pressure Data",
        xaxis_title="Time",
        yaxis_title="Pressure"
    )

    humidity_history_figure.update_layout(
        title="4 Hours Humidity Data",
        xaxis_title="Time",
        yaxis_title="Humidity"
    )

    return (temperature_value, pressure_value, humidity_value,
            temperature_figure, pressure_figure, humidity_figure,
            temperature_history_figure, pressure_history_figure, humidity_history_figure)


if __name__ == "__main__":
    app.run_server(debug=True)
