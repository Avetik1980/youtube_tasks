import yfinance as yf

ticker = 'AAPL'

stock_data=yf.Ticker(ticker)

historical_data=stock_data.history(period='1mo')

print(historical_data)
