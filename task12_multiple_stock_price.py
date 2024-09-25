import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz

def get_stock_data(symbol, date):
    stock=yf.Ticker(symbol)
    tz=pytz.timezone('America/New_York')
    start_date=tz.localize(datetime.strptime(date, '%y-%m-%d'))
    hist=stock.history(start=start_date, end=start_date+timedelta(days=1))

    if not hist.empty:
        last_row=hist.iloc[-1]
        return {
            'Symbol': symbol,
            'Open': round(last_row['Open'], 2),
            'Close': round(last_row['Close'], 2),
            'High': round(last_row['High'], 2),
            'Low': round(last_row['Low'], 2)
        }
    else:
        return {'Symbol': 'N/a','Open': 'N/a','Close': 'N/a','High': 'N/a','Low': 'N/a'}

def last_5_business_days():
    today=datetime.today().date()
    last_5_days=[today-timedelta(days=x) for x in range(1,8)]
    business_days=[day for day in last_5_days if day.weekday() <5][:5]
    return business_days

st.title("Stock Dashboard")

dates=last_5_business_days()
date_strings=[date.strftime('%y-%m-%d') for date in dates]
selected_dates=st.selectbox('Select date', date_strings)

stocks=['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
stocks_data=[]
for stock in stocks:
    stock_data=get_stock_data(stock, selected_dates)
    stocks_data.append(stock_data)

df=pd.DataFrame(stocks_data)
st.write(f"Stock data for set of Stocks and for {selected_dates}")
st.dataframe(df)
