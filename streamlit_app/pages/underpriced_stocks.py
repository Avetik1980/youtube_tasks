import streamlit as st
import yfinance as yf
import pandas as pd
import requests

BASE_URL = "https://financialmodelingprep.com/api/v3"
API_KEY = "8685dd75580791a73a4f689e161c183b"

@st.cache_resource
def fetch_sp500_tickers():
    url = f"{BASE_URL}/sp500_constituent?apikey={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            tickers = [item['symbol'] for item in data]
            return tickers
        else:
            st.error(f"Failed to fetch tickers: Status code is: {response.status_code}")
            return []
    except Exception as e:
        st.error("Request failed")
        return []

@st.cache_data
def fetch_stock_data(_tickers):
    data = []
    for symbol in _tickers:
        stock = yf.Ticker(symbol)
        try:
            info = stock.info
            if 'currentPrice' in info and 'trailingEps' in info:
                current_price = info['currentPrice']
                eps = info['trailingEps']
                pe_ratio = info.get('trailingPE', float('inf'))

                target_pe = 15
                fair_value_stock = eps * target_pe
                underpriced = current_price < fair_value_stock
                price_gap = ((fair_value_stock - current_price) / current_price) * 100 if current_price else 0

                data.append({
                    'Symbol': symbol,
                    'Current Price': current_price,
                    'EPS': eps,
                    'Fair Market Price': fair_value_stock,
                    'Underpriced': 'YES' if underpriced else 'NO',
                    'Price Gap %': price_gap
                })
        except Exception as e:
            print(f"Failed to fetch data for {symbol}: {e}")

    return pd.DataFrame(data)

def app():
    st.title("Underpriced Stocks in SP500 List")
    tickers = fetch_sp500_tickers()

    if tickers:
        st.write("Loading tickers for SP500")
        df = fetch_stock_data(tickers)
        if not df.empty:
            st.dataframe(df)
        else:
            st.write("No data is available for selected tickers")
    else:
        st.write("Unable to load stock tickers")

if __name__ == "__main__":
    app()
