import yfinance as yf
import pandas as pd
import streamlit as st


def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    stock_data = {
        "Company Name": info.get('longName', "N/A"),
        "Sector": info.get("sector", "N/A"),
        "Market Capacity ($B)": round(info.get("marketCap", 0) / 1e9, 2),
        "52-W High Price": info.get("fiftyTwoWeekHigh", "N/A"),
        "52-W Low Price": info.get("fiftyTwoWeekLow", "N/A")
    }

    return stock_data


st.title("Interactive Stock Data Viewer (Yahoo Finance)")
ticker = st.text_input("Enter a stock Ticker (Example: AAPL, AMZN, META)", "AAPL")
if st.button("Get Stock Info"):
    stock_info = get_stock_info(ticker)
    df = pd.DataFrame.from_dict(stock_info, orient="index", columns=["Value"])
    st.dataframe(df)
