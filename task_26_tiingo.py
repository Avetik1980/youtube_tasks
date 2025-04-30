import requests
import logging
import time

TIINGO_API_KEY = ""

BASE_URL = "https://api.tiingo.com/tiingo/daily"
DELAY = 1.5

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_tiingo_price_data(tickers):
    data = []
    headers ={"Content-Type": "application/json"}

    for count, ticker in enumerate(tickers[:50]):
        try:
            url=f"{BASE_URL}/{ticker}/prices?token={TIINGO_API_KEY}"
            response =requests.get(url, headers=headers)
            response.raise_for_status()
            price_data=response.json()
            if price_data:
                price_entry=price_data[0]
                data.append({
                    "symbol": ticker,
                    "date": price_entry.get("date"),
                    "close": price_entry.get("close"),
                    "volume": price_entry.get("volume"),
                })
                logger.info(f"{ticker}: {price_entry.get('close')}")
            else:
                logger.warning(f"No data for {ticker}")
        except Exception as e:
            logger.warning(f"Error fetching {ticker}: {e}")
        time.sleep(DELAY)
    return data


if __name__=="__main__":
    stocks=['AAPL', 'MSFT', 'GOOGL']
    result = fetch_tiingo_price_data(stocks)

    for r in result:
        print(r)
