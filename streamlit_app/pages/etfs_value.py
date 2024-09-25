import streamlit as st
import pandas as pd
import yfinance as yf

def format_assets(assets):
    if assets>=1e9:
        return f"{assets /1e9:.2f}B"
    elif assets>=1e6:
        return f"{assets /1e6:.2f}M"

def fetch_data(symbol):
    etf=yf.Ticker(symbol)
    info=etf.info
    return {
        "Name": info.get('longName', 'N/A'),
        "Latest Price": info.get('previousClose', 'N/A'),
        "52W High": info.get('fiftyTwoWeekHigh', 'N/A'),
        "52W Low": info.get('fiftyTwoWeekLow', 'N/A'),
        "Total assets": format_assets(info.get('totalAssets', 'N/A')),
    }

def app():
    st.title("ETF Analysis")

    file_path='etfs.txt'
    try:
        with open(file_path, 'r') as file:
            symbols =[line.strip().upper() for line in file.readlines()]
            data = [fetch_data(symbol) for symbol in symbols]
            df= pd.DataFrame(data)
            st.table(df)
    except FileNotFoundError:
        st.error("ETF Symbol File not accessible")

if __name__=="__main__":
    app()
