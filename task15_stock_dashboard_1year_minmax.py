import streamlit as st
import pandas as pd
import yfinance as yf

sp500_stocks = pd.read_csv('sp500_stocks.csv')


def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    try:
        stock_history = stock.history(period='1d')
        if not stock_history.empty:
            data = {
                'Name': stock.info.get('shortName', 'N/A'),
                'Current Price': round(stock_history['Close'].iloc[-1], 2),
                '52W Max': round(stock.info.get('fiftyTwoWeekHigh', 0), 2),
                '52W Min': round(stock.info.get('fiftyTwoWeekLow', 0), 2)
            }
        return data
    except Exception:
        return None


stocks_data = []
for symbol in sp500_stocks['Symbol']:
    stock_data = fetch_stock_data(symbol)
    if stock_data:
        stocks_data.append(stock_data)

df = pd.DataFrame(stocks_data)

df['Ratio 52W Max'] = round((df['Current Price'] / df['52W Max']) * 100, 2)
df['Ratio 52W Min'] = round((df['Current Price'] / df['52W Min']) * 100, 2)


def highlight_ratio(val, col_type):
    if col_type == 'max' and 80 <= val <= 100:
        return 'background-color: green; color:white'
    elif col_type == 'min' and 100 <= val <= 120:
        return 'background-color: red; color:white'
    return ' '


styled_df = df.style.applymap(lambda x: highlight_ratio(x, 'max') if isinstance(x, (int, float)) else '',
                              subset=['Ratio 52W Max'])
styled_df = styled_df.applymap(lambda x: highlight_ratio(x, 'min') if isinstance(x, (int, float)) else '',
                               subset=['Ratio 52W Min'])

st.dataframe(styled_df)
