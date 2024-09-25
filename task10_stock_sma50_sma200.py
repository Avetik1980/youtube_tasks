import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt

stocks=["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "JPM", "V", "DIS"]

st.title("Top 10 Stock Analysis SMA 50 and SMA 200")

st.write("""
SMA = Simple Moving Average
50 Day SMA is Short term indicator
200 Day SMA is Long term indicator""")

for stock in stocks:
    stock_symbol = yf.Ticker(stock)
    hist = stock_symbol.history(period = "2y")

    hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
    hist['SMA_200'] = hist['Close'].rolling(window=200).mean()

    fig, ax = plt.subplots(figsize=(14,7))
    ax.plot(hist['Close'], label=f"{stock} Close", alpha = 0.5)
    ax.plot(hist['SMA_50'], label= f"{stock} SMA50", alpha = 0.75)
    ax.plot(hist['SMA_200'], label = f"{stock} SMA200", alpha = 0.75)

    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD")
    ax.set_title(f"{stock_symbol} - Close price and moving averages")

    st.pyplot(fig)

st.write("If 50 day SMA is above 200 day SMA - bull or upward, if below - bear or downtrend")
