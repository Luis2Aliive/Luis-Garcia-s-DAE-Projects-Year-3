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
search_history = [] # stores all stock symbols searched by the user


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


def is_data_available(data):
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
             label=f"{SHORT_WINDOW}-Day Average", linestyle="--")
    plt.plot(prices.index, prices["Long MA"],
             label=f"{LONG_WINDOW}-Day Average", linestyle="--")
    plt.title(f"{symbol} Stock Price ({TIME_PERIOD})")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    print("\nShowing chart... close the chart window to see the analysis.")
    plt.show()


def analyze_trend(symbol, prices):
    """Step 8: Analyze how the stock price changes over time."""

    closes = prices["Close"]

    # Handle stock data with multiple columns.
    if isinstance(closes, pd.DataFrame):
        closes = closes.iloc[:, 0]

    closes = closes.dropna()

    if closes.empty:
        print("No closing prices are available for analysis.")
        return

    start_price = float(closes.iloc[0])
    end_price = float(closes.iloc[-1])

    if start_price == 0:
        print("Cannot calculate percentage change from zero.")
        return

    percent_change = (
        (end_price - start_price) / start_price
    ) * 100

    if percent_change > TREND_THRESHOLD:
        trend = "UPTREND (price is rising)"
    elif percent_change < -TREND_THRESHOLD:
        trend = "DOWNTREND (price is falling)"
    else:
        trend = "SIDEWAYS (price is mostly flat)"

    print(f"\n--- {symbol} Trend Analysis ({TIME_PERIOD}) ---")
    print(f"Starting price: ${start_price:,.2f}")
    print(f"Latest price: ${end_price:,.2f}")
    print(f"Change: {percent_change:+.2f}%")
    print(f"Highest close: ${float(closes.max()):,.2f}")
    print(f"Lowest close: ${float(closes.min()):,.2f}")
    print(f"Overall trend: {trend}")

    latest = prices.iloc[-1]

    short_ma = latest["Short MA"]
    long_ma = latest["Long MA"]

    # Handle moving averages that may also contain multiple columns.
    if isinstance(short_ma, pd.Series):
        short_ma = short_ma.iloc[0]

    if isinstance(long_ma, pd.Series):
        long_ma = long_ma.iloc[0]

    if pd.notna(short_ma) and pd.notna(long_ma):
        if short_ma > long_ma:
            print("Signal: Short-term average is above long-term average (bullish).")
        elif short_ma < long_ma:
            print("Signal: Short-term average is below long-term average (bearish).")
        else:
            print("Signal: Both moving averages are equal.")


def ask_view_another():
    """Step 9: Ask the user if they want to view another stock."""
    while True:
        answer = input("\nView another stock? (yes/no): ").strip().lower()
        if answer in ("yes", "y"):
            return True
        if answer in ("no", "n"):
            return False
        print("Please type yes or no.")


def load_stock(symbol):
    """Steps 4-6 for one symbol. Returns clean prices, or None on failure."""
    data = get_stock_data(symbol) # Step 4
    if not is_data_available(data): # Step 5
        print (f"Sorry, no data found for '{symbol}'."
              "Check the symbol and your internet connection.")
        return None
    return clean_data(data) # Step 6


def main():
    """Run the Trade Chart application."""
    # Step 1: Start the application
    show_welcome() # Step 2

    view_another = True
    while view_another: # Loop for Step 9
        symbol = get_stock_symbol() # Step 3
    def record_search(symbol):
        """Save and display searched stock symbols."""


        search_history.append(symbol)

        print("\n--- Stock Search History ---")

        for index, stock in enumerate(search_history, start=1):
            print(f"{index}. {stock}")
        record_search(symbol) # Record and display the stock search history

        # Give the user a few tries if the symbol has no data.
        prices = None
        for attempt in range(1, MAX_ATTEMPTS + 1):
            prices = load_stock(symbol) # Steps 4-6
            if prices is not None:
                break
            if attempt < MAX_ATTEMPTS:
                symbol = get_stock_symbol() 

            # Step 7: Display the stock chart
        if prices is not None:
            display_chart(symbol, prices)

            # Step 8: Analyze the stock trend
            analyze_trend(symbol, prices)
        else:
            print("Too many failed attempts. Let's try again.")

        # Step 9: Ask whether to view another stock
        view_another = ask_view_another()

    # Step 10: Close the application
    print(f"\nThanks for using {APP_NAME}. Goodbye!")

#.

if __name__ == "__main__":
    main()