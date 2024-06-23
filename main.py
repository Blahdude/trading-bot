import time
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
import config
import main
import scrape
import csv
import requests

# Initialize Alpaca Trading Client
trading_client = TradingClient(config.API_KEY, config.SECRET_KEY, paper=True)
data_client = CryptoHistoricalDataClient()

def write_to_csv(filename, timestamp, price):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, price])

# Function to fetch the latest BTC/USD price
def fetch_latest_price(symbol):
    request_params = CryptoBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe=TimeFrame.Minute,
        start=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        limit=1
    )
    bars = data_client.get_crypto_bars(request_params)
    latest_price = bars.df['close'].iloc[-1]
    return latest_price

# Function to create a market order
def create_market_order(symbol, qty, side):
    order_data = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=side,
        time_in_force=TimeInForce.GTC
    )
    try:
        order = trading_client.submit_order(order_data)
        print(f"Order created: {order}")
    except Exception as e:
        print(f"Error creating order: {e}")

# Main function to run the trading bot
def main():
    while True:
        symbol = 'BTCUSD'

        results = scrape.scrape("https://www.reddit.com/r/Bitcoin/new/")

        pos = False
        if "positive" in results[0]:
            pos = True

        # Fetch BTC price from Coinbase API
        url = 'https://api.coinbase.com/api/v3/brokerage/market/products/BTC-USD'
        response = requests.get(url)
        response.raise_for_status()  # Ensure we handle HTTP errors
        data = response.json()

        # Define the CSV file to write to
        file = 'btcdata.csv'

        if pos == True:
            writeme = float(results[0].replace("positive ", ""))
        else:
            writeme = float(results[1].replace("positive ", ""))


        # Writing to CSV file
        with open(file, 'a', newline='') as file:  # Use 'a' mode to append to the file
            writer = csv.writer(file)
            writer.writerow([datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), data['price'], writeme])  # Write a single row with timestamp and price

        # Wait for 10 minutes before making the next purchase
        time.sleep(60)  # 600 seconds = 10 minutes

if __name__ == "__main__":
    main()
