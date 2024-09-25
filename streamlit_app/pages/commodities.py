import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define commodities, their measurement units, and names
commodities_info = {
    "CL=F": {"unit": "barrels", "name": "Crude Oil (WTI)"},
    "BZ=F": {"unit": "barrels", "name": "Brent Crude"},
    "NG=F": {"unit": "mmBtu", "name": "Natural Gas"},
    "HO=F": {"unit": "gallons", "name": "Heating Oil"},
    "RB=F": {"unit": "gallons", "name": "Gasoline (RBOB)"},
    "GC=F": {"unit": "troy ounces", "name": "Gold"},
    "SI=F": {"unit": "troy ounces", "name": "Silver"},
    "HG=F": {"unit": "pounds", "name": "Copper"},
    "PL=F": {"unit": "troy ounces", "name": "Platinum"},
    "PA=F": {"unit": "troy ounces", "name": "Palladium"},
    "ZC=F": {"unit": "bushels", "name": "Corn"},
    "ZS=F": {"unit": "bushels", "name": "Soybeans"},
    "ZW=F": {"unit": "bushels", "name": "Wheat"},
    "ZM=F": {"unit": "tons", "name": "Soybean Meal"},
    "ZL=F": {"unit": "pounds", "name": "Soybean Oil"},
    "ZO=F": {"unit": "bushels", "name": "Oats"},
    "ZR=F": {"unit": "cwt", "name": "Rice"},
    "CT=F": {"unit": "pounds", "name": "Cotton"},
    "KC=F": {"unit": "pounds", "name": "Coffee"},
    "SB=F": {"unit": "pounds", "name": "Sugar"},
    "CC=F": {"unit": "metric tons", "name": "Cocoa"},
    "OJ=F": {"unit": "pounds", "name": "Orange Juice"},
}

@st.cache
def fetch_commodity_data(tickers, period="6d", interval= "1d"):
    try:
        data = yf.download(tickers, period=period, interval=interval)
        return data
    except Exception as e:
        st.error(f"Failed to get commodity data: {str(e)}")
        return pd.DataFrame

def app():
    st.title("Comodities Dashboard")
    period = st.sidebar.selectbox("Select period", ["1d", "5d", "1mo", "3mo", "6mo", "1y"], index =3)
    interval = st.sidebar.selectbox("Select Granularity", ["1d", "5d", "1wk", "1mo"], index=0)
    selected_commodities = st.sidebar.multiselect("Select Commodities", list(commodities_info.keys()), default=list(commodities_info.keys()))

    if selected_commodities:
        data=fetch_commodity_data(selected_commodities, period=period, interval=interval)
        if not data.empty:
            st.success("Data Loaded successfully for select commodities")
            dashboard_data=[]
            for commodity in selected_commodities:
                commodity_data=data['Close'][commodity].dropna()
                if len(commodity_data) >=2:
                    last_close=commodity_data.iloc[-1]
                    prev_close=commodity_data.iloc[-2]
                    change=(last_close-prev_close)/prev_close*100
                    dashboard_data.append({
                        'Commodity': commodities_info[commodity]["name"],
                        'Ticker': commodity,
                        'Unit': commodities_info[commodity]["unit"],
                        'Last Close': last_close,
                        'Change': change
                    })

            dashboard_df =pd.DataFrame(dashboard_data)
            st.dataframe(dashboard_df)

            for commodity in selected_commodities:
                if 'Close' in data:
                    plot_price_data(data['Close'][commodity], commodities_info[commodity]['name'])
        else:
            st.warning("No data available for selected commodities")
    else:
        st.warning("Please select at least one of the commodities")

def plot_price_data(df, commodity_name):
    plt.figure(figsize=(10,5))
    plt.plot(df.index, df, marker='o', linestyle = '-')
    plt.title(f"Price movement for {commodity_name}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    st.pyplot

if __name__=='__main__':
    app()
