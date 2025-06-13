import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import random
import datetime

def candlestick_graph(data):
  fig = go.Figure(data=[go.Candlestick(
      x=[i for i in range(1, len(data))],
      open=[c["open"] for c in data],
      high=[c["high"] for c in data],
      low=[c["low"] for c in data],
      close=[c["close"] for c in data],
      increasing_line_color='green',
      decreasing_line_color='red'
  )])

  fig.update_layout(
    xaxis_rangeslider_visible=False,
    xaxis_title="Time",
    yaxis_title="Price",
    title="Simulated Market Feed"
  )

  return fig