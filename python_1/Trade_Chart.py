"""
Trade Chart

A simple python application that helps users understand the stock market.
It shows stock prices & market trends in an easy-to-read chart.

Requirements: pip install yfinance pandas matpotlib

Algorithm steps (see the matching comments in main()):
1. Start the application         6. Organize (clean) the data
2. Display a welcome message     7. Display the prices in a chart
3. Ask for a stock symbol        8. Analyze the trend
4. Get the price data            9. Ask to view another stock (loop)
5. Check the data is available   10. Close the application  
"""

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

# Variables (settings used across the program)
APP_NAME = "Trade Chart"
TIME_PERIOD = "1y" # how far back to pull prices
SHORT_WINDOW = 25 # short moving average (days)
LONG_WINDOW = 50 # long moving average (days)
TREND_THRESHOLD = 2.0 # % change needed to call a trend up or down
MAX_ATTEMPTS = 3 # tries allowed to enter a valid symbol


# Functions
def show_welcome():
    """Step 2: Display a welcome message."""
    print("=" * 50)
    print(f"Welcome to {APP_NAME}!")
    print("See stock prices & trends in easy-to-read charts.")
    print("=" * 50)


def get_stock_symbol():
    """Step 3: Ask the user for a stock symbol (such as AAPL for Apple)."""
    # Loop until the user types something that looks like a symbol.
    while True:
        symbol = input("\nEnter a stock symbol (e.g., AAPL for Apple): ")
        symbol = symbol.strip().upper()
        if symbol.isalpha() and len(symbol) <= 5:
            return symbol
        print("Please enter 1 - 5 letters only (no numbers or spaces).")


def get_stock_data(symbol):
    """Step 4. Get the stock's price data. Returns None if it falls."""
    try:
        return yf.download(symbol, period =TIME_PERIOD, progress = False,
                           auto_adjust=True)
    except Exception as error:
        print(f"Could not download data: {error}")
        return None


def clean_data(data):
    """Step 5: Check that the stock data is available."""
    return data is not None and not data.empty


def clean_data(data):
    """Step 6: Organize the data so it can be displayed."""
    # Newer yfinance versions return multi-level column names; flatten them.
    if isinstance(data.columns, pd.MultiIndex):
        datacolumns = data.columns.get_level_values(0)

        prices = data[["Close"]].dropna().copy() # remove missing prices
        prices["Short MA"] = prices["Close"].rolling(SHORT_WINDOW).mean()
        prices["Long MA"] = prices["Close"].rolling(LONG_WINDOW).mean()
        return prices


def display_chart(symbol, prices):
    """Step 7: Display the stock price in a chart."""
    plt.figure(figsize=(10, 5))
    plt.plot(prices.index, prices["Close"], label="Closing Price", linewidth = 2)
    plt.plot(prices.index, prices["Short MA"],
             label=f"")