import plotly.graph_objs as go
import random
import datetime
from db import *

last_tick_list = {
  "AAA": dict(
    ticker="AAA",
    times=1,
    open=100,
    high=100,
    low=100,
    close=100,
    volume=0,
  )
}

def simulate_tick(tick: int):
  global last_tick_list
  
  for stock in last_tick_list.values():
    new_ticker = generate_ticker_data(stock, timestamp=tick)
    last_tick_list[new_ticker["ticker"]] = new_ticker
    db_insert_ticker_data(new_ticker)
  
  return last_tick_list
  
  

def generate_ticker_data(prev_tick: dict, timestamp: int):
  ticker: str = prev_tick["ticker"]
  prev_close = prev_tick["close"]
  
  base = prev_close if prev_close else 100
  open_price = base
  close = open_price + random.normalvariate(0, 10)
  high = max(open_price, close) + random.uniform(0, 5)
  low = min(open_price, close) - random.uniform(0, 5)
  volume = random.normalvariate(1000, 400)

  return {
    "ticker": ticker,
    "time": timestamp,
    "open": open_price,
    "high": high,
    "low": low,
    "close": close,
    "volume": volume
  }