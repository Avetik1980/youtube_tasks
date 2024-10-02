import numpy as np
import pandas as pd
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
import joblib

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, 'data/')
model_dir = os.path.join(base_dir, 'models', 'random_forest/')
os.makedirs(model_dir, exist_ok=True)


def create_dataset(data, look_back=100):
    X, Y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back), 0])
        Y.append(data[i + look_back, 0])
    return np.array(X), np.array(Y)

for file in os.listdir(data_dir):
    if file.endswith('.csv'):
        symbol=file.split('.')[0]
        print( f"Processing file for stock {symbol}")
        data=pd.read_csv(os.path.join(data_dir, file))

    if data.empty:
        print(f"No data available for {symbol}")
        continue

    data['Date']=pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    data.dropna(inplace=True)

    if data.empty or len(data) <100:
        print(f"Insufficient data for {symbol}")
        continue

    data["MA100"]=data['Close'].rolling(100).mean()
    data["MA200"]=data['Close'].rolling(200).mean()

    train_size=int(len(data)*0.8)
    train_data=data[:train_size]
    test_data=data[train_size]
    if train_data.empty or test_data.empty:
        print("Insufficient data to process")
        continue

    scaler=MinMaxScaler(feature_range=(0, 1))
    train_scaled=scaler.fit_transform((train_data[['Close']]))
    test_scaled=scaler.fit_transform((test_data[['Close']]))

    x_train, y_train=create_dataset(train_scaled)
    x_test, y_test=create_dataset(test_scaled)

    if x_train.size==0 or y_train.size==0:
        print("Skipping")
        continue

    rf_model=RandomForestRegressor(n_estimators=100)
    rf_model.fit(x_train, y_train)

    joblib.dump((rf_model, f"{model_dir}//{symbol}_rf.pkl"))
    print(f"Model for {symbol} saved as {symbol}_rf.pkl")
