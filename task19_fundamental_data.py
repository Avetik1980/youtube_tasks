import streamlit as st
import yfinance as yf
import os

def load_stock_symbol():
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'stockname.txt')
        with open (file_path, 'r') as file:
            symbols=[line.strip() for line in file if line.strip()]
            return symbols
    except FileNotFoundError:
        st.error("Stockname.txt file cannot be found")
        return []

def fetch_fundamental_data(stock_symbol):
    stock=yf.Ticker(stock_symbol)
    info=stock.info
    return {
        'Market Capitalization': info.get('marketCap'),
        'P/E Ratio': info.get('trailingPE'),
        'EPS' : info.get('trailingEps'),
        'EBITDA': info.get('ebitda'),
        'Revenue': info.get('totalRevenue'),
        'Debt-to-Equity': info.get('debtToEquity'),
        'Current Ratio': info.get('currentRatio'),
        'Quick Ratio': info.get('quickRatio')
    }

st.sidebar.title("Fundamental Analysis Dahsboard")
stock_symbols=load_stock_symbol()

if stock_symbols:
    stock_symbol = st.sidebar.selectbox("Select a stock", stock_symbols)
    st.title(f'{stock_symbol} : Fundamental Analysis')

    fundamental_Data = fetch_fundamental_data(stock_symbol)
    if fundamental_Data:
        for metric, value in fundamental_Data.items():
            st.metric(label=metric, value=value if value is not None else 'N/A')

    else:
        st.warning(f"No fundamental data for {stock_symbol}")
else:
    st.warning("No symbols found, check your file")
