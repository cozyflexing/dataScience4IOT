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

def interpolate_color(minval, maxval, val, color_palette):
    max_index = len(color_palette) - 1
    v = float(val - minval) / float(maxval - minval) * max_index
    i1, i2 = int(v), min(int(v) + 1, max_index)
    (r1, g1, b1), (r2, g2, b2) = color_palette[i1], color_palette[i2]
    f = v - i1
    return int(r1 + f * (r2 - r1)), int(g1 + f * (g2 - g1)), int(b1 + f * (b2 - b1))

def get_temperature():
    temperature = sense.get_temperature() - 7.3
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
        color_palette = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]
        background_color = interpolate_color(0, 30, temp, color_palette)
        show_message(message, (255, 255, 255), background_color)
    return n_clicks


if __name__ == "__main__":
    app.run_server(debug=True)
