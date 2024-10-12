import websocket
import json
import pandas as pd
import threading

endpoint = 'wss://stream.binance.com:9443/ws'

our_message = json.dumps({
    "method": "SUBSCRIBE",
    "params": [
        "btcusdt@ticker",
    ],
    "id": 1
})

# global variable to store the data
df = pd.DataFrame() 
in_position = False
sma_7 = 0
sma_25 = 0
prev_sma_7 = 0
prev_sma_25 = 0
buy_orders, sell_orders = [], []
time_in_seconds = 120

def on_open(ws):
    print('opened connection')
    ws.send(our_message)
    
def on_message(ws, message):
    # import the global variables
    global df, in_position, sma_7, sma_25, prev_sma_7, prev_sma_25, buy_orders, sell_orders
    
    # receive the message and store it in a df
    out = json.loads(message)
    out = pd.DataFrame({'price': float(out['c'])}, index=[pd.to_datetime(out['E'], unit='ms')])
    df = pd.concat([df, out], axis=0)
    # print(df.tail(1))
    
    # calculate the indicator
    df = df.tail(25)
    
    prev_sma_7 = sma_7
    prev_sma_25 = sma_25
  
    
    last_price = df.tail(1)['price'].values[0]
    sma_7 = df.price.rolling(window=7).mean().tail(1).values[0]
    sma_25 = df.price.rolling(window=25).mean().tail(1).values[0]
    
    # trading logic
    if (sma_7 > sma_25) and in_position == False:
        in_position = True
        buy_orders.append(last_price)
        print(f'-----> Buy order: {last_price}')
    elif (sma_7 < sma_25) and in_position == True:
        
        in_position = False
        sell_orders.append(last_price)
        print(f'-----> Sell order: {last_price} & Profit_pct: {(last_price - buy_orders[-1])/buy_orders[-1]} %')
    else:
        if sma_7 > sma_25:
            symbol = '>'
        elif sma_7 < sma_25:
            symbol = '<'
        else:
            symbol = '='    
            
        print(f'Price: {last_price} in_position: {in_position}, {sma_7} {symbol} {sma_25}')
        
def stop_websocket(ws):
    global time_in_seconds
    print(f"Closing WebSocket after {time_in_seconds/60} minutes")
    if in_position:
        sell_orders.append(df.tail(1)['price'].values[0])
    print(f"Buy Orders: {buy_orders}")
    print(f"Sell Orders: {sell_orders}")
    ws.close()

ws = websocket.WebSocketApp(endpoint, on_open=on_open, on_message=on_message)

timer = threading.Timer(time_in_seconds, stop_websocket, args=[ws])

timer.start()
ws.run_forever()