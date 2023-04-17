# app.py
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pymongo import MongoClient
from datetime import datetime
import plotly.graph_objs as go

# Replace 'your_mongodb_uri' with your actual MongoDB URI
client = MongoClient('your_mongodb_uri')
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
    dcc.Interval(id="interval", interval=1*1000, n_intervals=0)
])

@app.callback(
    Output("temperature", "children"),
    Output("pressure", "children"),
    Output("humidity", "children"),
    Output("temperature-graph", "figure"),
    Output("pressure-graph", "figure"),
    Output("humidity-graph", "figure"),
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

    return temperature_value, pressure_value, humidity_value, temperature_figure, pressure_figure, humidity_figure

if __name__ == "__main__":
    app.run_server(debug=True)
