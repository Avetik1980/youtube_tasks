import streamlit as st
import pandas as pd
import requests

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params= {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 500,
        'page': 1,
        'sparkline': False,
        'price_change_percentage': '24h, 7d'
    }
    response = requests.get(url, params=params)
    data=response.json()
    return data


def prepare_data(data):
    cryptos=[]
    for item in data:
        symbol = item.get('symbol', ' ').upper()
        name = item.get('name', 'N/A')
        current_price = item.get('current_price', 'N/A')
        price_change_24h= item.get('price_change_percentage_24h_in_currency', 'N/A')
        price_change_7d= item.get('price_change_percentage_7d_in_currency', 'N/A')
        previous_price=(current_price/(1+price_change_24h/100)) if current_price != 'N/A' else 'N/A'

        cryptos.append({
            "Symbol": symbol,
            "Name": name,
            "Current Price USD": current_price,
            "Previous day Price": previous_price,
            "24H Change": price_change_24h,
            "7D Change": price_change_7d
        })
    return pd.DataFrame(cryptos)

def app():
    st.title("Streamlit Crypto Dashboard")
    with st.spinner("Fetching Crypto Data"):
        data=fetch_crypto_data()
        df=prepare_data(data)
        df.index += 1

    st.dataframe(
        df.style.apply(
            lambda x:['background-color: #90ee90' if v>=10 else '' for v in x],
            subset=['24H Change']
        )
    )
if __name__=='__main__':
    app()
