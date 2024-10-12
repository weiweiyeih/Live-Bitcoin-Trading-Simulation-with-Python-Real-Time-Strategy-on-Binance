# Live Bitcoin Trading Simulation with Python: Real-Time Strategy on Binance

This repository contains a simple trading bot simulation implemented using Python, WebSocket, and the Binance WebSocket API. The bot subscribes to the BTC/USDT ticker stream, calculates short-term and long-term Simple Moving Averages (SMA), and simulates buy/sell orders based on SMA crossovers. Instead of placing real orders on Binance, we simply record the buy and sell prices for later review and analysis.

📺 [Watch the demo on YouTube](https://www.youtube.com/watch?v=As9fOcn3Kvg) 🎥

## Features

- **Live WebSocket Connection:** Connects to Binance WebSocket stream to get real-time price updates for the BTC/USDT trading pair.
- **Simple Moving Averages (SMA):** Calculates two SMAs:
  - SMA-7 (Short-term, 7 periods)
  - SMA-25 (Long-term, 25 periods)
- **Trading Logic:**
  - **Buy Signal:** When the 7-period SMA crosses above the 25-period SMA (Golden Cross) and the bot is not in a position, it simulates a buy order.
  - **Sell Signal:** When the 7-period SMA crosses below the 25-period SMA (Death Cross) and the bot is in a position, it simulates a sell order.
  - **Profit Calculation:** On every sell order, the bot prints the profit percentage based on the last buy price.
- **Order Storage:** Buy and sell orders are stored in lists for tracking trade history.
- **Automatic Stop:** The WebSocket connection automatically stops after a user-defined time period (default: 120 seconds).

## How it Works

1. **WebSocket Connection:**  
   The bot connects to the Binance WebSocket server to receive live updates for the BTC/USDT trading pair.

2. **Price Storage:**  
   The bot stores incoming price data in a Pandas DataFrame and maintains a rolling window of the last 25 prices for SMA calculations.

3. **Trading Decisions:**  
   Based on the relationship between SMA-7 and SMA-25:

   - If the short-term SMA crosses above the long-term SMA, a buy order is simulated (if not already in a position).
   - If the short-term SMA crosses below the long-term SMA, a sell order is simulated (if already in a position).

4. **Stopping the Bot:**  
   After the predefined `time_in_seconds` period, the WebSocket connection closes, and a summary of buy and sell orders is printed for later review and analysis.

## Requirements

- Python 3.7+
- WebSocket client library (`websocket-client`)
- Pandas (`pandas`)

### Install Dependencies

You can install the required dependencies by running:

```bash
pip install websocket-client pandas
```

## Notes

**_Simulation Only:_**

This bot is for educational and simulation purposes only. It does not place real orders on the Binance exchange. Instead, it records the buy and sell prices for later review and analysis. Please use a proper exchange API and authentication method if you plan to implement real trades.
