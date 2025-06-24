from sortedcontainers import SortedKeyList
import time

  
class Order:
  def __init__(self, price, size: int, timestamp):
    self.timestamp = timestamp
    self.price = price
    self.initial_size = size
    self.size = size
    self.fulfilled = False
    self.trades = [] #To be implemented
  
  def trade_order(self, trade_size: int):
    self.size = self.size - trade_size
    return self.size
  
  
  
class BuyOrder(Order):
  def __init__(self, price, size: int, timestamp):
    super().__init__(price, size, timestamp)
    self.order_type = "buy"
    
class SellOrder(Order):
  def __init__(self, price, size: int, timestamp):
    super().__init__(price, size, timestamp)
    self.order_type = "sell"
    
class Trade():
  def __init__(self, price, size) -> None:
    self.timestamp = time.time()
    self.price = price
    self.size = size
    
  

#Order book class holds orders
class OrderBook:
  def __init__(self, stock: str, initial_price: float):
    self.stock = stock
    self.buy_orders = SortedKeyList(key = lambda x: (-x.price, x.timestamp))
    self.sell_orders = SortedKeyList(key = lambda x: (x.price, x.timestamp))
    self.trade_history = SortedKeyList(key = lambda x: -x.timestamp)
    self.order_history = []
    self.initial_price = initial_price
  
  
  
  def add_sell_order(self, order: SellOrder):
    top_buy_order: BuyOrder | None = self.get_priority_buy()
    
    if top_buy_order: 
      if top_buy_order.price >= order.price:
        self.trade_orders(top_buy_order, order)
        
    if not order.fulfilled:   
      self.sell_orders.add(order)
    
    self.order_history.append(order)
    
    
    
  def add_buy_order(self, order: BuyOrder):
    top_sell_order: SellOrder | None = self.get_priority_sell()
    
    if top_sell_order: 
      if top_sell_order.price <= order.price:
        self.trade_orders(order, top_sell_order)
        
    if not order.fulfilled:   
      self.buy_orders.add(order)
    
    self.order_history.append(order)
    
  
  
  def get_priority_sell(self) -> SellOrder | None:
    top = None
    if len(self.sell_orders) > 0:
      top = self.sell_orders[0]
      
    if isinstance(top, SellOrder):
      return top
    return None
  
  
  
  def get_priority_buy(self):
    top = None
    if len(self.buy_orders) > 0:
      top = self.buy_orders[0]
      
    if isinstance(top, BuyOrder):
      return top
    return None
  
  
  
  #Get price of latest trade
  def get_price(self): #Something iffy about the return type of SortedKeyList
    last_trade = self.trade_history[0] if self.trade_history else Trade(self.initial_price, 0)
    if isinstance(last_trade, Trade):
      return float(last_trade.price)
    return float(self.initial_price)
  
  
  
  #Get tick data
  def get_tick(self, start_time, end_time=time.time):
    print("start time: ", start_time, "end time: ", end_time)
    if len(self.trade_history) == 0:
      return None
    trades = list(self.trade_history.irange_key(-end_time, -start_time))
    
    '''
    for t in self.trade_history:
      print("--------")
      print(vars(t))
    '''
    
    min_price = min(trades, key = lambda x: x.price).price if trades else self.initial_price
    max_price = max(trades, key = lambda x: x.price).price if trades else self.initial_price
    open_price = min(trades, key = lambda x: x.timestamp).price if trades else self.initial_price
    close_price = self.get_price()
    
    volume = sum(trade.size for trade in trades)
    
    return {
      "low": min_price,
      "high": max_price,
      "open": open_price,
      "close": close_price,
      "volume": volume
    }
    
    
  
  #Trade two matching orders
  def trade_orders(self, buy_order: BuyOrder, sell_order: SellOrder):
    print(sell_order.price, buy_order.price)
    print(sell_order.size, buy_order.size)
    self.print_book()
    
    print("===========================")
    
    #Check that the orders are matching
    if buy_order.price < sell_order.price or buy_order.size <= 0 or sell_order.size <= 0:
      print("fail!")
      raise Exception("Matching failed")
    
    #Find largest possible trade
    trade_size = min(buy_order.size, sell_order.size)
    resting_order = min(buy_order, sell_order, key = lambda x: x.timestamp)
    trade_price = resting_order.price
    
    buy_order.trade_order(trade_size)
    sell_order.trade_order(trade_size)

    trade_info = Trade(trade_price, trade_size)
    
    buy_order.trades.append(trade_info)
    self.trade_history.add(trade_info)

    #Order is fulfilled if size == 0
    if buy_order.size == 0:
      buy_order.fulfilled = True
      #Order is removed from book
      if buy_order in self.buy_orders:
        self.buy_orders.remove(buy_order)
    
    sell_order.trades.append(trade_info)
    
    #Order is fulfilled if size == 0
    if sell_order.size == 0:
      sell_order.fulfilled = True
      #Order is removed from book
      if sell_order in self.sell_orders:
        self.sell_orders.remove(sell_order)
        
        
        
  #Function for printing the orderbook
  def print_book(self):
    print("-------Sell orders-------")
    for order in self.sell_orders:
      print(order.price, order.size)
    print("-------------------------\n")
    
    print("-------Buy orders-------")
    for order in self.buy_orders:
      print(order.price, order.size)
    print("-------------------------\n")
    
  
  


    
  