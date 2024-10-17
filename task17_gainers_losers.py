import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

@st.cache_data
def load_stock_data():
    import os
    current_dir=os.path.dirname(os.path.abspath(__file__))
    file_path=os.path.join(current_dir, 'stockdata.txt')
    with open(file_path, 'r') as file:
        return [line.strip() for lines in file]

def fetch_stock_data(symbol):
    stock=yf.Ticker(symbol)
    today=datetime.now()
    one_week_ago=today-timedelta(day=7)

    data=stock.history(period='1d', start=one_week_ago.strftime('%y-%m-%d'), end=today.strftime('%y-%m-%d'))

    if data.empty:
        return None

    yesterday_price=data['Close'].iloc[-1]
    week_ago_price=data['Close'].iloc[0]

    return {
        'symbol': symbol,
        'yesterday_price': round(yesterday_price, 2),
        'week_ago_price': round(week_ago_price, 2),
        'price difference': round(yesterday_price-week_ago_price, 2)
        'price_change_percentage': round((yesterday_price-week_ago_price)/week_ago_price*100, 2)
    }

def plot_stock_chart(symbol):
    stock=yf.Ticker(symbol)
    stock_data=stock.history(period='1mo')

    if not stock_data.empty:
        st.subheader(f'Stock price for {symbol} for Last 1 Month')
        st.line_chart(stock_data['Close'])
    else:
        st.write(f'No data for symbol {symbol}')

def display_stock_table(df):
    def highlight_changes(val):
        color='green' if val > 0 else 'red'
        return f'color: {color}'

    styled_df=df.style.applymap(highlight_changes, subset=['price_diff'])
    st.write(styled_df)
