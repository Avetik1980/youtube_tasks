import requests
import json
import os

# API Configuration
FMP_API_KEY = ""
BASE_URL = "https://financialmodelingprep.com/api/v3/"


# Function to fetch data
def fetch_fmp_data(endpoint, stock_symbol):
    # Fetching Financial data from FMP API for a given stock (Stock symbol)
    # Endpoints will be defined later, so we introduce them as variables to form final API endpoint URL

    url = f"{BASE_URL}{endpoint}/{stock_symbol}?apikey={FMP_API_KEY}"
    response = requests.get(url)

    # check if response was successful
    if response.status_code == 200:
        return response.json()
    else:
        print("Not possible to fetch data")
        return None


# Save received data to a JSON file
def save_to_json(data, filename):
    # Saves the data to a JSON file
    # first we are accessing a file in write mode
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")


#Main function
if __name__=="__main__":
    #Stock symbol to be declared for data
    stock_symbol="AMZN"

    #Defining endpoints to get data for
    endpoints=["profile", "ratios", "financials"]

    #Create folders to save files to
    output_dir="fmp_data"
    os.makedirs(output_dir, exist_ok=True)

    #Going over iteration for each of elements of endpoints list
    for endpoint in endpoints:
        print(f"Fetching data for endpoint {endpoint}")
        data=fetch_fmp_data(endpoint, stock_symbol)
        if data:
            filename=os.path.join(output_dir, f"{stock_symbol}_{endpoint}.json")
            save_to_json(data, filename)
