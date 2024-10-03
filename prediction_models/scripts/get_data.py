import pandas as pd
import yfinance as yf
import os

base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_file_path=os.path.join(base_dir, 'sp500_stocks.csv')
sp500_stocks=pd.read_csv(csv_file_path)

data_dir=os.path.join(base_dir, 'data')
os.makedirs(data_dir, exist_ok=True)

def download_stock_data(symbol, start_date='2021-01-01', end_date='2024-09-30'):
    try:
        stock_data=yf.download(symbol, start=start_date, end=end_date)
        stock_data.to_csv(os.path.join(data_dir, f"{symbol}.csv"))
        print(f'Successfully downloaded data for {symbol}')
    except Exception as e:
        print(f"Failed to download data for {symbol}")

for symbol in sp500_stocks['Symbol']:
    download_stock_data(symbol)
