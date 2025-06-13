# live_candlestick.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from graphs import candlestick_graph
from db import *
from simulator import *

app = dash.Dash(__name__)
server = app.server

ticker_data = {
  "AAA": []
}

db_setup()

#Layout
app.layout = html.Div([
    html.H1("Live stock chart", style={"textAlign": "center"}),
    dcc.Graph(id='candlestick-graph'),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0)  # update every 3s
])

@app.callback(
  Output('candlestick-graph', 'figure'),
  Input('interval-component', 'n_intervals')
)
def new_tick(n):
  global ticker_data

  #last_close = ticker_data[-1]["close"] if ticker_data else None
  
  new_data = simulate_tick(n)
  
  for ticker, data_list in ticker_data.items():
    data_list.append(new_data[ticker])
    ticker_data[ticker] = data_list[-100:]

  fig = candlestick_graph(ticker_data["AAA"])
  
  return fig

if __name__ == '__main__':
    app.run(debug=True)
