import streamlit as st
from pages import commodities, cryptos, etfs_value, underpriced_stocks

pages = {
   "Commodities": commodities,
   "Cryptos": cryptos,
   "ETFs ": etfs_value,
   "Stocks": underpriced_stocks
}

st.sidebar.title("Navigation")
choice = st.sidebar.radio("Choose a page to display", list(pages.keys()))

page=pages[choice]
page.app()
