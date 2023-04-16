import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from sense_hat import SenseHat
import time

sense = SenseHat()

app = dash.Dash(__name__)
app.layout = html.Div([
    html.Button("Show on LED Matrix", id="button"),
    html.Div(id="output"),
    dcc.Interval(id="interval", interval=1*1000, n_intervals=0),
    dcc.Graph(id="live-update-graph")
])

def get_temperature():
    return sense.get_temperature_from_pressure() - 7.3

def get_pressure():
    return sense.get_pressure()

def get_humidity():
    return sense.get_humidity()

def interpolate_color(temp, temp_min=0, temp_max=30, color_min=(0, 0, 255), color_max=(255, 0, 0)):
    ratio = (temp - temp_min) / (temp_max - temp_min)
    r = int(color_min[0] + (color_max[0] - color_min[0]) * ratio)
    g = int(color_min[1] + (color_max[1] - color_min[1]) * ratio)
    b = int(color_min[2] + (color_max[2] - color_min[2]) * ratio)
    return r, g, b

def show_message(message, text_color, background_color):
    sense.show_message(message, text_colour=text_color, back_colour=background_color, scroll_speed=0.15)

@app.callback(Output("output", "children"), [Input("button", "n_clicks")])
def display_on_led_matrix(n_clicks):
    if n_clicks is not None:
        temp = round(get_temperature(), 2)
        message = f"{temp} C"
        color = interpolate_color(temp)
        show_message(message, (255, 255, 255), color)
    return n_clicks

@app.callback(Output("live-update-graph", "figure"), [Input("interval", "n_intervals")])
def update_graph_live(n):
    data = {
        "Time": time.time(),
        "Temperature": get_temperature(),
        "Pressure": get_pressure(),
        "Humidity": get_humidity()
    }

    data = [go.Scatter(x=list(data.keys()), y=list(data.values()), mode="lines+markers")]

    return {"data": data}

if __name__ == "__main__":
    app.run_server(debug=True)
