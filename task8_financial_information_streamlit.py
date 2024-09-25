import yfinance as yf
import streamlit as st

ticker="AAPL"
stock_data=yf.Ticker(ticker)
balance_sheet = stock_data.balance_sheet
income_statement=stock_data.financials
info=stock_data.info

st.title(f"Useful financials for the {ticker} stock")

st.write("Balance sheet")
st.write(balance_sheet)

st.write("Income Statement")
st.write(income_statement)

st.write("Cash flow data")
st.write(info)
