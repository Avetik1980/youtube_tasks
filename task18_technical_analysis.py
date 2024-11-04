import streamlit as st
import yfinance as yf


# Load stock symbols from a file
@st.cache_data
def load_stock_symbols():
    try:
        with open('stocks.txt', 'r') as file:
            symbols = [line.strip() for line in file if line.strip()]
            return symbols
    except FileNotFoundError:
        st.error("The 'stocks.txt' file was not found. Please make sure it is in the same directory.")
        return []

# Calculate technical indicators
def calculate_indicators(data):
    # SMA50 and SMA200
    data['SMA50'] = data['Close'].rolling(window=50).mean()
    data['SMA200'] = data['Close'].rolling(window=200).mean()

    # MACD
    exp12 = data['Close'].ewm(span=12, adjust=False).mean()
    exp26 = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp12 - exp26
    data['Signal Line'] = data['MACD'].ewm(span=9, adjust=False).mean()

    # RSI
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Bollinger Bands
    data['Upper Band'] = data['Close'].rolling(20).mean() + (data['Close'].rolling(20).std() * 2)
    data['Lower Band'] = data['Close'].rolling(20).mean() - (data['Close'].rolling(20).std() * 2)
    return data

# Fetch and prepare stock data
@st.cache_data
def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period='1y')
    if data.empty:
        return None
    data = calculate_indicators(data)
    return data

# Sidebar to select stock from the list in stocks.txt
st.sidebar.title("Technical Analysis")
stock_symbols = load_stock_symbols()

if not stock_symbols:
    st.write("No stock symbols loaded. Please check 'stocks.txt' file.")
else:
    stock_symbol = st.sidebar.selectbox("Select Stock:", stock_symbols)
    data = get_stock_data(stock_symbol)

    if data is not None:
        st.title(f"{stock_symbol} - Technical Analysis")
        st.line_chart(data[['Close', 'SMA50', 'SMA200', 'MACD', 'Signal Line', 'RSI', 'Upper Band', 'Lower Band']])

        data = data.reset_index()
        data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
        df_metrics = data[['Date', 'Close', 'RSI', 'Upper Band', 'Lower Band', 'MACD', 'Signal Line', 'SMA50', 'SMA200']]

        def color_row(row, prev_row):
            colors = {}
            if prev_row is not None and row['Close'] > prev_row['Close']:
                colors['Close'] = 'color: green'
            elif prev_row is not None and row['Close'] < prev_row['Close']:
                colors['Close'] = 'color: red'

            colors['RSI'] = 'color: green' if 30 <= row['RSI'] <= 70 else 'color: red'
            colors['MACD'] = 'color: green' if row['MACD'] > row['Signal Line'] else 'color: red'
            colors['SMA50'] = 'color: green' if row['SMA50'] > row['SMA200'] else 'color: red'

            return colors

        color_mapping = []
        for i in range(len(df_metrics)):
            if i == 0:
                color_mapping.append(color_row(df_metrics.iloc[i], None))
            else:
                color_mapping.append(color_row(df_metrics.iloc[i], df_metrics.iloc[i - 1]))

        def apply_color(row):
            color_dict = color_mapping[row.name]
            return [color_dict.get(col, '') for col in row.index]

        styled_df = df_metrics.style.apply(apply_color, axis=1)

        st.subheader(f"{stock_symbol} - Key Metrics")
        st.dataframe(styled_df)

        st.subheader("Indicator Explanations")
        st.write("""
        - **Close Price**: Last recorded stock price and is Green if today's close is higher than yesterda, red otherwise.
        - **RSI**: Value in range 30 - 70 is normal and colored Green, red otherwise.
        - **Bollinger Bands**: volatility based on 20-day SMA.
        - **MACD**: is Green/bullish if MACD > Signal line, red / bearish otherwise
        - **SMA50 and 200**: Green/Bullish if SMA50 > SMA200, red / bearish otherwise
        """)
