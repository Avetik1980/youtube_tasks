"""
1. Create Streamlit Application +
2. Design Streamlit Application
3. Code the formula of calculation for best/worst stocks +
4. Code the calculation +
5. Display the calculation results

Scope: Stocks and ETF's

Formula: Year to Date Return % = ((End of the Year Price - Start of the Year Price)/Start of the Year Price)*100

"""

import streamlit as st
import yfinance as yf
import pandas as pd

# Configure Streamlit Page

st.set_page_config(page_title="Stock and ETF Performance for 2024", layout="wide")

st.sidebar.header("Dashboard Settings")
categories=st.sidebar.selectbox("Select Category", ["Stocks", "ETFs"])


@st.cache_data
def get_sp500_constituents():
    # Retrieve the list of SP500 tickers
    wiki_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    sp500_table = pd.read_html(wiki_url, header=0)[0]
    return sp500_table['Symbol'].tolist()


# Method to fetch stock data
@st.cache_data
def fetch_stock_data(tickers, start_date, end_date):
    data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            history = stock.history(start=start_date, end=end_date)
            if not history.empty:
                start_price = history['Close'].iloc[0]
                end_price = history['Close'].iloc[-1]
                ytd_return = ((end_price - start_price) / start_price) * 100
                data.append({
                    "Ticker": ticker,
                    "Start Price": start_price,
                    "End Price": end_price,
                    "Year to date return (%)": ytd_return
                })
        except Exception as e:
            st.error(f"Error fetching data for stock {ticker}: {e}")
    return pd.DataFrame(data)


# Main App logic
st.title("Market performance dashboard for 2024")

if categories == "Stocks":
    st.header("Top 10 Best and Worst performing stocks for 2024 among SP500 list")

    # Fetch SP500 Stock List
    sp500_tickers = get_sp500_constituents()

    # Fetch stock data for 2024
    start_date = "2024-01-01"
    end_date = "2024-12-31"
    stock_data = fetch_stock_data(sp500_tickers, start_date, end_date)

    if not stock_data.empty:
        # Sort by return per year
        sorted_data=stock_data.sort_values(by="Year to date return (%)", ascending=False)

        # Top and worst performers
        top_10_stock=sorted_data.head(10).reset_index(drop=True)
        worst_10_stock=sorted_data.tail(10).reset_index(drop=True)

        # Display tables in Streamlit
        st.subheader("Top 10 Best Performed stocks")
        st.dataframe(top_10_stock.style.format({"Year to date return (%)": "{:.2f}"}))

        st.subheader("Top 10 Worst Performed stocks")
        st.dataframe(worst_10_stock.style.format({"Year to date return (%)": "{:.2f}"}))
    else:
        st.error("No stock data to display")

elif categories == "ETFs":
    st.header("Top 10 best and worst ETF's")

    # Define ETF's
    etf_tickers=["SPY", "IVV", "VOO", "QQQ", "VTI", "VEA", "IWM", "VUG", "VTV", "BND", "SCHD", "XLF",
                 "XLE", "XLY", "XLI", "XLK", "XLV", "XLP", "XLC", "IEFF", "AGG"]

    # Fetch ETF data for 2024
    start_date = "2024-01-01"
    end_date = "2024-12-31"
    etf_data = fetch_stock_data(etf_tickers, start_date, end_date)

    if not etf_data.empty:
        # Sort by return per year
        sorted_data=etf_data.sort_values(by="Year to date return (%)", ascending=False)

        # Top and worst performers
        top_10_etfs=sorted_data.head(10).reset_index(drop=True)
        worst_10_etfs=sorted_data.tail(10).reset_index(drop=True)

        # Display tables in Streamlit
        st.subheader("Top 10 Best Performed ETF")
        st.dataframe(top_10_etfs.style.format({"Year to date return (%)": "{:.2f}"}))

        st.subheader("Top 10 Worst Performed ETFs")
        st.dataframe(worst_10_etfs.style.format({"Year to date return (%)": "{:.2f}"}))
    else:
        st.error("No ETF data to display")

