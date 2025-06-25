import plotly.graph_objs as go
from db import *
from order_book import *
from scipy import stats

class Simulator:
  def __init__(self) -> None:
    self.order_books = [OrderBook("AAA", 100)]
    self.epoch = 0
    self.previous_epoch_end = time.time()
  
  def run_epoch(self):
    tick_data = {}
    for book in self.order_books:
      self.run_orders(book)
      tick = book.get_tick(self.previous_epoch_end, time.time())
      
      tick_data[book.stock] = tick
      #db_insert_ticker_data(tick)
    
    self.previous_epoch_end = time.time()
    self.epoch = self.epoch +1
    
    return tick_data
    
    
  def run_orders(self, book: OrderBook):
    current_price: float = book.get_price()
    for i in range(0, 4):
      buy_price = abs(stats.norm.rvs(1 * current_price, 10))
      buy_size = abs(stats.norm.rvs(10, 10))
      sell_price = abs(stats.norm.rvs(1 * current_price, 10))
      sell_size = abs(stats.norm.rvs(10, 10))
      
      buy_order = BuyOrder(buy_price, buy_size, time.time())
      sell_order = SellOrder(sell_price, sell_size, time.time())
      
      book.add_sell_order(sell_order)
      book.add_buy_order(buy_order)
      


  '''def generate_ticker_data(self, prev_tick: dict, timestamp: int):
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
    }'''