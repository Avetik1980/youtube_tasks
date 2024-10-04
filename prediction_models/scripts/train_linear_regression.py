import numpy as np
import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import joblib

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, 'data/')
model_dir = os.path.join(base_dir, 'models', 'linear_regression/')
os.makedirs(model_dir, exist_ok=True)

csv_file_path = os.path.join(base_dir, 'sp500_stocks.csv')
sp500_stocks = pd.read_csv(csv_file_path)


def train_linear_regression(symbol):
    data_path = os.path.join(data_dir, f'{symbol}.csv')
    if not os.path.exists(data_path):
        print(f'Data for {symbol} not found.')
        return

    stock_data = pd.read_csv(data_path)
    if stock_data.empty or 'Close' not in stock_data.columns:
        print(f'No valid data for {symbol}.')
        return

    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    stock_data.set_index('Date', inplace=True)

    if stock_data['Close'].isnull().all():
        print(f'No closing prices for {symbol}.')
        return

    scaler = MinMaxScaler(feature_range=(0, 1))
    try:
        scaled_data = scaler.fit_transform(stock_data['Close'].values.reshape(-1, 1))
    except ValueError as e:
        print(f'Error scaling data for {symbol}: {e}')
        return

    def create_dataset(data, look_back=100):
        X, Y = [], []
        for i in range(len(data) - look_back):
            X.append(data[i:(i + look_back), 0])
            Y.append(data[i + look_back, 0])
        return np.array(X), np.array(Y)

    look_back = 100
    x_train, y_train = create_dataset(scaled_data)

    if len(x_train) == 0 or len(y_train) == 0:
        print(f'Not enough data to create training set for {symbol}.')
        return

    model = LinearRegression()
    model.fit(x_train, y_train)

    model_path = os.path.join(model_dir, f'{symbol}_lr.pkl')
    joblib.dump(model, model_path)
    print(f'Model for {symbol} saved as {symbol}_lr.pkl')


for symbol in sp500_stocks['Symbol']:
    train_linear_regression(symbol)
