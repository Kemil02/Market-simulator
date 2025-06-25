# live_candlestick.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from graphs import candlestick_graph
from db import *
from simulator import *
from order_book import *

app = dash.Dash(__name__)
server = app.server

stock_data = {
  "AAA": {
    "price_data": [],
    "order_data": {} 
    }
}

db_setup()

simulator = Simulator()

#Layout
app.layout = html.Div([
    html.H1("Live stock chart", style={"textAlign": "center"}),
    dcc.Graph(id='candlestick-graph'),
    html.H2("Order Book"),
    html.Div([
        html.Div(id="buy-orders"),
        html.Div(id="sell-orders"),
    ], style={"display": "flex", "gap": "40px"}),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0)  # update every 3s
])

@app.callback(
  Output('candlestick-graph', 'figure'),
  Output('buy-orders', 'children'),
  Output('sell-orders', 'children'),
  Input('interval-component', 'n_intervals')
)
def new_tick(n):
  global stock_data
  '''
  Format of new_data and stock_data
  
  {
    "AAA": {
      "price_data": [{
        "low"
        "high"
        "open"
        "close"
        "volume"
        }
        ...
        ],
      "order_data": {
        "sell_orders"
        "buy_orders"
      }
    },
    ...
  }
  
  '''

  new_data = simulator.run_epoch()
  
  #Update each stock
  for ticker, data_obj in stock_data.items():
    data_obj["price_data"].extend(new_data[ticker]["price_data"])
    data_obj["price_data"] = data_obj["price_data"][-100:]
    
    data_obj["order_data"] = new_data[ticker]["order_data"]

  fig = candlestick_graph(stock_data["AAA"]["price_data"])
  
  sell_orders = stock_data["AAA"]["order_data"]["sell_orders"]
  buy_orders = stock_data["AAA"]["order_data"]["buy_orders"]
  
  buy_list = html.Div([
    html.H4(f"Sell Orders ({len(sell_orders)})"),
    *[html.Div(order.stringify()) for order in sell_orders[:15]]
    ], style={"display": "inline-block", "verticalAlign": "top"})
  
  sell_list = html.Div([
    html.H4(f"Buy Orders ({len(buy_orders)})"),
    *[html.Div(order.stringify()) for order in buy_orders[:15]]
    ], style={"display": "inline-block", "verticalAlign": "top"})
  
  return fig, buy_list, sell_list

if __name__ == '__main__':
    app.run(debug=True)
