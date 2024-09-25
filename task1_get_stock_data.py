import yfinance as yf

ticker = 'AAPL'
stock_data=yf.Ticker(ticker)

current_price = stock_data.history(period='1d')['Close'][0]

