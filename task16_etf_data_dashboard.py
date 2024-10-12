import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

st.title("ETF Performance Dashboard")

etf_list = ['SPY', 'IVY', 'VOO', 'QQQ', 'VTI', 'BND', 'VEA', 'IEMG', 'VWO', 'VIG',
            'VYM', 'DIA', 'EFA', 'LQD', 'AGG', 'SCHD', 'IJH', 'XLK', 'XLF', 'ARKK']


def fetch_etf_data(etf):
    stock = yf.Ticker(etf)
    hist = stock.history(period='1y')

    hist['MA50'] = hist['Close'].rolling(window=50).mean()
    hist['MA200'] = hist['Close'].rolling(window=200).mean()

    info = stock.info
    metrics = {
        'Name': info.get('shortName', 'N/A'),
        'Current Price': round(hist['Close'].iloc[-1], 2),
        '52W Max': round(info.get('fiftyTwoWeekHigh', 0), 2),
        '52W Min': round(info.get('fiftyTwoWeekLow', 0), 2)
    }
    return hist, metrics


for etf in etf_list:
    try:
        hist_data, etf_metrics = fetch_etf_data(etf)
        st.subheader(f"{etf} - {etf_metrics['Name']}")
        st.write(f"52 Week High: {etf_metrics['52W Max']}")
        st.write(f"52 Week Low: {etf_metrics['52W Min']}")
        st.write(f" Current Price: {etf_metrics['Current Price']}")

        ratio_to_52W_Max = round((etf_metrics['Current Price'] / etf_metrics['52W Max']) * 100, 2)
        ratio_to_52W_Min = round((etf_metrics['Current Price'] / etf_metrics['52W Min']) * 100, 2)

        st.write(f"Ratio Current to 52W Max: {ratio_to_52W_Max}")
        st.write(f"Ratio Current to 52W Min: {ratio_to_52W_Min}")

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=hist_data.index, y=hist_data['Close'], mode='lines', name='Close Price'))
        fig1.add_trace(go.Scatter(x=hist_data.index, y=hist_data['MA50'], mode='lines', name='MA 50-Day '))
        fig1.add_trace(go.Scatter(x=hist_data.index, y=hist_data['MA200'], mode='lines', name='MA 200-Day '))
        fig1.update_layout(title=f"{etf} Price trend and Moving Avg.", xaxis_title='Date', yaxis_title='Price')

        st.plotly_chart(fig1)

    except Exception as e:
        st.error(f"Impossible to fetch data for ETF {etf} : {e}")
