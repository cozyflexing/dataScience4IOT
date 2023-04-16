import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from sense_hat import SenseHat
import requests

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
    dbc.Button("Show on LED Matrix", id="show-button", color="primary", className="mr-1"),
    dcc.Interval(id="interval", interval=5*60*1000, n_intervals=0)
])

@app.callback(
    Output("temperature", "children"),
    Output("pressure", "children"),
    Output("humidity", "children"),
    Input("interval", "n_intervals")
)
def update_values(n):
    temperature = f"{round(get_temperature(), 2)} °C"
    pressure = f"{round(get_pressure(), 2)} hPa"
    humidity = f"{round(get_humidity(), 2)} %"
    return temperature, pressure, humidity

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
    return 0

if __name__ == "__main__":
    app.run_server(debug=True)
