import requests
import pandas as pd

API_KEY="iApEixsL6eBxxAB67vLGfncfN3n1xJaH"
BASE_URL="https://financialmodelingprep.com/api/v3"
ticker="AMZN"

url=f"{BASE_URL}/profile/{ticker}?apikey={API_KEY}"
response=requests.get(url)
if response.status_code == 200:
    data=response.json()
    df=pd.DataFrame(data)
    print(df.T)
else:
    print(f"Error fetching data: status code is {response.status_code}")
