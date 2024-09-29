import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import joblib
import os
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from tensorflow.keras.models import load_model

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_file_path = os.path.join(base_dir, 'sp500_stocks.csv')
sp500_stocks = pd.read_csv(csv_file_path)


def calculate_moving_averages(data, window_size):
    return data.rolling(window=window_size).mean()


def create_dataset(data, look_back=100):
    X, Y = [], []
    for i in range(len(data) - look_back):
        Y.append(data[i + look_back])
    return np.array(X), np.array(Y)

def main():
    st.sidebar.title("Stock Forecast")
    st.sidebar.markdown("Select stock and date range")
    stock_symbol=st.sidebar.selectbox("Select Ticker",sp500_stocks['Symbol'])
    start_date=st.sidebar.date_input("Select Start date", datetime.now()-timedelta(days=365))
    end_date=st.sidebar.date_input("Select End date", datetime.now())
    selected_model=st.sidebar.radio(("Select Model", ("Neural Network", "Random Forest", "Linear Regression")))
    if stock_symbol:
        try:
            stock_data=yf.download(stock_symbol, start=start_date, end=end_date)
            st.subheader(f"Stock Data for {stock_symbol}")
            st.write(stock_data.head(50))
            st.write("...")

            stock_data["MA100"]=calculate_moving_averages(stock_data['Close'],100)
            stock_data["MA200"]=calculate_moving_averages(stock_data['Close'],200)

            st.header('Price vs MA100')
            fig1=go.Figure()
            fig1.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Close Price'))
            fig1.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MA100'], mode='lines', name='MA100'))
            st.plotly_chart(fig1)

            st.header('Price vs MA100 & MA200')
            fig2=go.Figure()
            fig2.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Close Price'))
            fig2.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MA100'], mode='lines', name='MA100'))
            fig2.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MA200'], mode='lines', name='MA200'))
            st.plotly_chart(fig1)

            candlestick=go.Candlestick(x=stock_data.index, open=stock_data['Open'],close=stock_data['Close'],
                                       high=stock_data['High'],low=stock_data['Low'], name='Candlestick')
            candlestick_layout=go.Layout(title='Candlestick Chart')
            candlestick_fig=go.Figure(data=candlestick, layout=candlestick_layout)
            st.plotly_chart(candlestick_fig)

            volume_fig=go.Figure()
            volume_fig.add_trace(go.Bar(x=stock_data.index, y=stock_data['Volume'], name='Trade Volume'))
            volume_fig.update_layout(title='Volume Plot')
            st.plotly_chart(volume_fig)

            if selected_model=="Neural Network":
                model_path=os.path.join(base_dir, 'models', 'neural_network', f'{stock_symbol} _nn.keras')
                model=load_model(model_path)
                expected_input_shape=model.input_shape
                st.write(f"Model input shape: {expected_input_shape}")
            elif selected_model == "Random Forest":
                model_path=os.path.join(base_dir, 'models', 'random_forest', f'{stock_symbol} _rf.pkl')
                model=joblib.load(model_path)
            elif selected_model== 'Linear Regression':
                model_path = os.path.join(base_dir, 'models', 'linear_regression', f'{stock_symbol} lr.pkl')
                model=joblib.load(model_path)

            scaler=MinMaxScaler(feature_range=(0,1))
            scaled_data=scaler.fit_transform(stock_data['Close'].values.reshape(-1, 1))
            x_pred, y_true=create_dataset(scaled_data)
            st.write(f" x_pred shapre before reshape: {x_pred.shape}")

            if selected_model=="Neural Network":
                x_pred=x_pred.reshape(x_pred.shape[0], x_pred.shape[1], 1)
                st.write(f"x pred shape after reshape: {x_pred.shape}")
                y_pred=model.predict(x_pred)
                y_pred=scaler.inverse_transform(y_pred)
            elif selected_model in ["Random Forest", "Linear Regression"]:
                x_pred=x_pred.reshape(x_pred.shape[0], -1)
                st.write(f"x pred shape after reshape: {x_pred.shape}")
                y_pred=model.predict(x_pred)
                y_pred=scaler.inverse_transform(y_pred.reshape(-1, 1))

            st.subheader('Original vs Predicted Prices')
            fig3=go.Figure()
            fig3.add_trace(go.Scatter(x=stock_data.index[100:], y=stock_data['Close'][100:], mode='lines', name='Original Price'))
            fig3.add_trace(go.Scatter(x=stock_data.index[100:], y=y_pred.flatten(), mode='lines', name='Predicted Price'))
            st.plotly_chart(fig2)

            y_true=stock_data['Close'].values[100:]
            mae=mean_absolute_error(y_true, y_pred)
            mse=mean_squared_error(y_true,y_pred)

            st.subheader('Model Evaluation')
            st.write(f"Mean Absolute Error: {mae:.2f} ")
            st.write(f"Mean Squared Error: {mse:.2f} ")

            forecast_dates=[stock_data.index[-1]+timedelta(days=i) for i in range (1,31)]
            forecast=pd.DataFrame(index=forecast_dates, columns=['Forecast'])

            last_100_days=stock_data['Close'].tail(100)
            last_100_days_scaled=scaler.transform(last_100_days.values.reshape(-1,1))

            for i in range(30):
                x_forecast=last_100_days_scaled[-100::].reshape(1,-1)
                if selected_model=="Neural Network":
                    x_forecast=x_forecast.reshape(x_forecast.shape[0], x_forecast.shape[1], 1)
                else:
                    x_forecast=x_forecast.reshape(1, -1)
                y_forecast=model.predict(x_forecast)
                forecast.iloc[i]=scaler.inverse_transform(y_forecast.reshape(-1, 1))[0][0]
                last_100_days_scaled=np.append(last_100_days_scaled, y_forecast).reshape(-1, 1)

            st.subheader("30-Day Forecast")
            st.write(forecast)

        except Exception as e:
            st.error(f"Error{e}")

if __name__=="__main__":
    main()
