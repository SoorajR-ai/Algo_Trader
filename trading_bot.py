from algomojo.pyapi import *
import yfinance as yf
import time
import threading
import numpy as np
import pandas as pd

excel_file = 'trading_log.xlsx'

# Function to initialize the DataFrame
def initialize_trades_df():
    columns = ["Stock", "Buy Price", "Buy Position", "Invested Amount", "Short EMA Angle", "Sell Price", "Sell Position", "Credited Amount", "Profit"]
    try:
        # Try to read the existing Excel file
        df = pd.read_excel(excel_file)
    except FileNotFoundError:
        # If the file doesn't exist, create a new DataFrame
        df = pd.DataFrame(columns=columns)
    return df

trades_df = initialize_trades_df()

# Set the StrategyName, broker code, Trading symbol, exchange
strategy = "EMA Crossover"
broker = "an"
exchange = "NSE"
quantity = 1

# Initialize global variables
Position = [0] * 30
Buy_price = [0] * 30
Invested = [0] * 30
Credited = [0] * 30
Profit = [0] * 30
i = 0

stock_list = [
    "WIPRO.NS","ONGC.NS","LT.NS","HINDALCO.NS","MARUTI.NS","TCS.NS","ADANIENT.NS","KOTAKBANK.NS","HDFCLIFE.NS",
    "BHARTIARTL.NS","LTIM.NS","TITAN.NS","BAJAJFINSV.NS","BRITANNIA.NS","BAJFINANCE.NS","NTPC.NS","RELIANCE.NS",
    "ITC.NS","TATASTEEL.NS","ULTRACEMCO.NS","NESTLEIND.NS","HEROMOTOCO.NS","COALINDIA.NS","APOLLOHOSP.NS","BAJAJ-AUTO.NS",
    "TATACONSUM.NS","SHRIRAMFIN.NS","INDUSINDBK.NS","M&M.NS","CIPLA.NS"
]

print(len(stock_list))

# Function to calculate the angle of an EMA line
def calculate_ema_angle(ema_series):
    time_interval = 1  # Interval in minutes, adjust as per your data
    if len(ema_series) < 2:
        return 0
    slope = (ema_series.iloc[-1] - ema_series.iloc[-2]) / time_interval
    angle = np.arctan(slope) * (180 / np.pi)  # Convert from radians to degrees
    return angle

# Define function to run the strategy
def main():
    global i, trades_df
    # Main loop
    while True:
        # Get historical data for the current stock using Yahoo Finance API
        stock = yf.Ticker(stock_list[i])
        EMA_cross_scanner(stock, i)

        

        # Move to the next stock in the list
        i += 1
        if i >= len(stock_list):
            i = 0
            time.sleep(30)

def EMA_cross_scanner(stock, index):
    global Buy_price, Position, Invested, Credited, Profit, trades_df
    # Get historical price data from 1min timeframe 
    df = stock.history(period="1d", interval="1m")
    close = df.Close.round(2)

    # Calculate short-term and long-term EMAs
    shortEMA = df.Close.ewm(span=30, adjust=False).mean().round(2)
    longEMA = df.Close.ewm(span=500, adjust=False).mean().round(2)

    # Determine the crossover point
    positive_crossover = shortEMA.iloc[-2] > longEMA.iloc[-2] and shortEMA.iloc[-3] < longEMA.iloc[-3]
    negative_crossover = shortEMA.iloc[-2] < longEMA.iloc[-2] and shortEMA.iloc[-3] > longEMA.iloc[-3]

    # Calculate the angles of the EMA lines
    short_ema_angle = abs(calculate_ema_angle(shortEMA))
    long_ema_angle = calculate_ema_angle(longEMA)

    # Print debug information
    #print(f"Stock: {stock.ticker}  LTP: {close.iloc[-1]}  Short EMA Angle: {short_ema_angle}")

    if positive_crossover and short_ema_angle > 45 and Position[index] <= 0:
        Buy_price[index] = close.iloc[-1]
        Position[index] = 5
        Invested[index] = Buy_price[index] * Position[index]
        print(f"Stock: {stock.ticker}  Buy Price: {Buy_price[index]}  Position: {Position[index]}  Invested: {Invested[index]}  Short EMA Angle: {short_ema_angle}")
        # Update the DataFrame
        new_trade = pd.DataFrame({
            "Stock": [stock.ticker],
            "Buy Price": [Buy_price[index]],
            "Buy Position": [Position[index]],
            "Invested Amount": [Invested[index]],
            "Short EMA Angle": [short_ema_angle],
            "Sell Price": [np.nan],
            "Sell Position": [np.nan],
            "Credited Amount": [np.nan],
            "Profit": [np.nan]
        })
        trades_df = pd.concat([trades_df, new_trade], ignore_index=True)
        write_to_excel()

    elif negative_crossover and short_ema_angle > 10 and Position[index] > 0:
        sell_price = close.iloc[-1]
        Credited[index] = sell_price * Position[index]
        Profit[index] = (sell_price - Buy_price[index]) * Position[index]
        print(f"Stock: {stock.ticker}  Sell Price: {sell_price}  Position: {Position[index]}  Credited: {Credited[index]}")
        print("========================================")
        print(f"Profit: {Profit[index]}")
        print("========================================")
        # Update the DataFrame
        new_trade = pd.DataFrame({
            "Stock": [stock.ticker],
            "Buy Price": [Buy_price[index]],
            "Buy Position": [Position[index]],
            "Invested Amount": [Invested[index]],
            "Short EMA Angle": [short_ema_angle],
            "Sell Price": [sell_price],
            "Sell Position": [Position[index]],
            "Credited Amount": [Credited[index]],
            "Profit": [Profit[index]]
        })
        trades_df = pd.concat([trades_df, new_trade], ignore_index=True)
        write_to_excel()
        Position[index] = 0

def write_to_excel():
    global trades_df
    trades_df.to_excel(excel_file, index=False)
    print("Excel file updated.")

# Create and start a new thread to run the strategy
t = threading.Thread(target=main)
t.start()
