import sqlite3

connection = sqlite3.connect("market_sim_dat.db", check_same_thread=False)
cursor = connection.cursor()

def db_setup():
  cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS tickers (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      ticker STRING
    )
    '''
  )
  
  cursor.executemany(
    '''
    INSERT OR IGNORE INTO tickers (ticker)
    VALUES (?)
    ''', [('AAA',), ('BBB',)]
  )
  
  cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS tickerdata (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      ticker TEXT,
      timestamp INTEGER,
      open REAL,
      close REAL,
      high REAL,
      low REAL,
      volume INTEGER
    )
    '''
    )
  
  connection.commit()
  
def db_insert_ticker_data(data: dict):
  cursor.execute(
    '''
    INSERT INTO tickerdata (ticker, timestamp, open, close, high, low)
    VALUES (?, ?, ?, ?, ?, ?)
    ''',
    (data["ticker"], 
     data["time"], 
     data["open"], 
     data["close"], 
     data["high"], 
     data["low"])
  ) 

def db_insert_multiple_ticker_data(datalist: list[dict]):
  for data in datalist: db_insert_ticker_data(data)
  
def db_get_ticker_data(ticker: str, start=1, interval=1, limit=100):
  cursor.execute(
    '''
    SELECT * FROM tickerdata
    WHERE ticker='?' AND timestamp >= ? AND timestamp % ? = 0
    ORDER BY timestamp DESC
    LIMIT ?
    ''', (ticker, start, interval, limit)
  )
  
  return cursor.fetchall()
