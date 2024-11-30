import requests
import json

API_KEY = ""
BASE_URL = "https://eodhd.com/api/fundamentals/"


def fetch_and_save_data(stock_symbol):
    url = f"{BASE_URL}{stock_symbol}?api_token={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        file_name = f"{stock_symbol}_fundamentals.json"
        with open(file_name, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Data saved succesfully for the stock {stock_symbol}")
    else:
        print(f"Failed to fetch data for stock{stock_symbol}")


stock_symbol = input("Enter stock symbol, for example AAPL.US: ")
fetch_and_save_data(stock_symbol)
