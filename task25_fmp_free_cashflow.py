import streamlit as st
import requests
import pandas as pd

# Streamlit page configuration
st.set_page_config(page_title="FMP Statement")
st.title("Income Statement")
st.markdown("Analyze the recent income from FMP for a single stock")

# Input
ticker = st.text_input("Enter Stock Symbol", value="AAPL").upper()

# API Setup
API_KEY = "iApEixsL6eBxxAB67vLGfncfN3n1xJaH"
BASE_URL = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=10&apikey={API_KEY}"

# Getting the data
response = requests.get(BASE_URL)
if response.status_code != 200:
    st.error("Failed to fetch data")
else:
    income_data = response.json()
    if isinstance(income_data, list) and len(income_data) > 0:
        df_income = pd.DataFrame(income_data).iloc[::-1]
        df_income.set_index("date", inplace=True)
        numeric_cols = df_income.select_dtypes(include='number').columns
        st.dataframe(df_income.style.format({col: "{:,.0f}" for col in numeric_cols}), use_container_width=True)
    else:
        st.warning("No income statement")
