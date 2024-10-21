import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


@st.cache_data
def load_stock_data():
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'stockname.txt')
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]


def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    today = datetime.now()
    one_week_ago = today - timedelta(days=7)
    data = stock.history(period='1d', start=one_week_ago.strftime('%Y-%m-%d'), end=today.strftime('%Y-%m-%d'))

    if data.empty:
        return None

    yesterday_price = data['Close'].iloc[-1]
    week_ago_price = data['Close'].iloc[0]

    return {
        'symbol': symbol,
        'yesterday_price': round(yesterday_price, 2),
        'week_ago_price': round(week_ago_price, 2),
        'price difference': round(yesterday_price - week_ago_price, 2),
        'price_change_percentage': round((yesterday_price - week_ago_price) / week_ago_price * 100, 2)
    }


def plot_stock_chart(symbol):
    stock = yf.Ticker(symbol)
    stock_data = stock.history(period='1mo')

    if not stock_data.empty:
        st.subheader(f'Stock price for {symbol} for Last 1 Month')
        st.line_chart(stock_data['Close'])
    else:
        st.write(f'No data for symbol {symbol}')

def display_stock_table(df):
    def highlight_changes(val):
        color = 'green' if val > 0 else 'red'
        return f'color: {color}'

    styled_df = df.style.applymap(highlight_changes, subset=['price difference'])
    st.write(styled_df)

stock_symbols=load_stock_data()
st.sidebar.title("Stocks list")
selected_stock=st.sidebar.selectbox("Select a stock for the chart", stock_symbols)

all_stock_data=[]
for symbol in stock_symbols:
    stock_data=fetch_stock_data(symbol)
    if stock_data:
        all_stock_data.append(stock_data)

df=pd.DataFrame(all_stock_data)

top_gainers=df.nlargest(10, 'price_change_percentage')[['symbol', 'price difference', 'price_change_percentage']]
top_losers=df.nsmallest(10, 'price_change_percentage')[['symbol', 'price difference', 'price_change_percentage']]

st.header("Top Gainers")
st.table(top_gainers)
st.header("Top Losers")
st.table(top_losers)

st.header("Complete stock table")
display_stock_table(df)

if selected_stock:
    plot_stock_chart(selected_stock)
