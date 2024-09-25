import yfinance as yf

ticker = 'AAPL'

stock_data=yf.Ticker(ticker)

major_holder=stock_data.major_holders

print(major_holder)
