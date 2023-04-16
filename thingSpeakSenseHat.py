import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from sense_hat import SenseHat
import requests
import plotly.graph_objs as go

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

sense = SenseHat()

def get_temperature():
    temperature = sense.get_temperature_from_pressure() - 7.3
    return temperature

def get_pressure():
    pressure = sense.get_pressure()
    return pressure

def get_humidity():
    humidity = sense.get_humidity()
    return humidity

def show_message(message, text_colour, background_colour):
    sense.show_message(message, text_colour=text_colour, back_colour=background_colour, scroll_speed=0.15)

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
    dbc.Button("Show on LED Matrix", id="show-button", color="primary", className="mr-1"),
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
    temperature = f"{round(get_temperature(), 2)} °C"
    pressure = f"{round(get_pressure(), 2)} hPa"
    humidity = f"{round(get_humidity(), 2)} %"
    
    temperature_figure = go.Figure(go.Indicator(
        mode="gauge+number",
        value=get_temperature(),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Temperature"}
    ))

    pressure_figure = go.Figure(go.Indicator(
        mode="gauge+number",
        value=get_pressure(),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Pressure"}
    ))

    humidity_figure = go.Figure(go.Indicator(
        mode="gauge+number",
        value=get_humidity(),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Humidity"}
    ))
    
    return temperature, pressure, humidity, temperature_figure, pressure_figure, humidity_figure

@app.callback(
    Output("show-button", "n_clicks"),
    Input("show-button", "n_clicks")
)
def display_on_led_matrix(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from sense_hat import SenseHat
import requests
import plotly.graph_objs as go

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

sense = SenseHat()

def get_temperature():
    temperature = sense.get_temperature_from_pressure() - 7.3
    return temperature

def get_pressure():
    pressure = sense.get_pressure()
    return pressure

def get_humidity():
    humidity = sense.get_humidity()
    return humidity

def show_message(message, text_colour, background_colour):
    sense.show_message(message, text_colour=text_colour, back_colour=background_colour, scroll_speed=0.15)

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
    dbc.Button("Show on LED Matrix", id="show-button", color="primary", className="mr-1"),
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
    temperature = f"{round(get_temperature(), 2)} °C"
    pressure = f"{round(get_pressure(), 2)} hPa"
    humidity = f"{round(get_humidity(), 2)} %"
    
    temperature_figure = go.Figure(go.Indicator(
        mode="gauge+number",
        value=get_temperature(),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Temperature"}
    ))

    pressure_figure = go.Figure(go.Indicator(
        mode="gauge+number",
        value=get_pressure(),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Pressure"}
    ))

    humidity_figure = go.Figure(go.Indicator(
        mode="gauge+number",
        value=get_humidity(),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Humidity"}
    ))
    
    return temperature, pressure, humidity, temperature_figure, pressure_figure, humidity_figure

@app.callback(
    Output("show-button", "n_clicks"),
    Input("show-button", "n_clicks")
)
def display_on_led_matrix(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        temp = round(get_temperature(), 2)
        message = f"{temp} C"
        if temp >= 20:
            show_message(message, (255, 255, 255), (0, 128, 0))
        elif 18 <= temp < 20:
            show_message(message, (255, 255, 255), (255, 100, 0))
        else:
            show_message(message, (255, 255, 255), (255, 0, 0))
    return n_clicks

if __name__ == "__main__":
    app.run_server(debug=True)
