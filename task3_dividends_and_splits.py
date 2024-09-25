import yfinance as yf
ticker = "AAPL"

stock_data=yf.Ticker(ticker)
financial=stock_data.financials
html_file_path=f"{ticker}_financials.html"
financial.to_html(html_file_path)

