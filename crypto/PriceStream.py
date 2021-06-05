'''
PriceStream.py 
Example websocket connection for price data
Author: Dan Wallace
Date: 6/5/2021

Notes: 
    -> This example script shows how to subscribe to binance websockets for multiple tickers
    -> The script handles each push from the websocket and prints out the price for each coin subscribed too

Example: response from Binance /@miniTicker websocket 
    {
    "e": "24hrMiniTicker",  // Event type
    "E": 123456789,         // Event time
    "s": "BNBBTC",          // Symbol
    "c": "0.0025",          // Close price
    "o": "0.0010",          // Open price
    "h": "0.0025",          // High price
    "l": "0.0010",          // Low price
    "v": "10000",           // Total traded base asset volume
    "q": "18"               // Total traded quote asset volume
    }
'''
import json
from websocket import create_connection

# Set coins to subscribe to and create appropriate websocket url
coins = ['btcusdt','ethusdt','dogeusdt']
url = 'wss://stream.binance.com:9443/ws'
for x in coins:
    url += '/'+x+'@miniTicker' 

# Parse websocket results
def parse_ws(result):
    msg = json.loads(result)
    print(msg['s']+' :: {:.2f}'.format(float(msg['c'])))

# Create connection
ws = create_connection(url)

# Main loop
while True:
    try:
        result = ws.recv()
        parse_ws(result)
    except Exception as e:
        print(e)
        break
