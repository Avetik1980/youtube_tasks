import streamlit as st
import yfinance as yf
import pandas as pd


@st.cache_data
def load_stock_symbols():
    try:
        with open('stocks.txt', 'r') as file:
            symbols = [line.strip() for line in file if line.strip()]
            return symbols
    except FileNotFoundError:
        st.error("Your file wasn't found")
        return []


def calculate_indicators(data):
    # SMA50 and SMA200
    data['SMA50'] = data['Close'].rolling(window=50).mean()
    data['SMA200'] = data['Close'].rolling(window=200).mean()

    # MACD
    exp12 = data['Close'].ewm(span=12, adjust=False).mean()
    exp26 = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp12 - exp26
    data['Signal Line'] = data['MACD'].ewm(span=9, adjust=False).mean()

    # RSI
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Bollinger Bands
    data['Upper Band'] = data['Close'].rolling(20).mean() + (data['Close'].rolling(20).std() * 2)
    data['Lower Band'] = data['Close'].rolling(20).mean() - (data['Close'].rolling(20).std() * 2)

    return data


def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period='6m')
    if data.empty:
        return None
    data = calculate_indicators(data)
    return data


st.sidebar.title("Technical Analysis")
stock_symbols = load_stock_symbols
