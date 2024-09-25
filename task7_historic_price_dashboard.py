import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt

ticker = 'AAPL'
stock_data=yf.Ticker(ticker)
historical_data=stock_data.history(period='1y')

st.title(f"Historical data for {ticker}")
st.line_chart(historical_data['Close'])

st.write("Stock Price Chart")
fig, ax = plt.subplots()
ax.plot(historical_data.index, historical_data['Close'], label="Close Price")
ax.set_xlabel("Date")
ax.set_ylabel("Price in USD")
ax.set_title (f"{ticker} Stock Closure price over last 1 year")
ax.legend()
st.pyplot(fig)
