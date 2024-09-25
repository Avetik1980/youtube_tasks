import yfinance as yf

ticker = 'AAPL'

stock_data=yf.Ticker(ticker)

earning_calendar=stock_data.calendar

print(earning_calendar)
