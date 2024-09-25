import yfinance as yf
import streamlit as st

ticker = 'AAPL'
stock_data=yf.Ticker(ticker)

st.title("Stock information for AAPL")
st.write("Company Information")

st.write(stock_data.info)
st.write("Earning Calendar")
st.write(stock_data.earnings)
