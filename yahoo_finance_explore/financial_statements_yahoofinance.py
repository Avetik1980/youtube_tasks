import yfinance as yf
import pandas as pd
import streamlit as st

st.title("Financial statement Explorer")
ticker=st.text_input("Enter a stock Ticker, example: AAPL, AMZN, TSLA", "AMZN")

if st.button("Get Financial Statements"):
    stock = yf.Ticker(ticker)
    income_statement=stock.financials
    balance_sheet=stock.balance_sheet
    cash_flow=stock.cashflow

    st.subheader("Income Statement Display")
    st.dataframe(income_statement)

    st.subheader("Financial Balance Document")
    st.dataframe(balance_sheet)

    st.subheader("Cash Flow Statements")
    st.dataframe(cash_flow)
