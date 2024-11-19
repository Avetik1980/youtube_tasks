import yfinance as yf
import streamlit as st

# Define Buffett's investment criteria
CRITERIA = {
    "Debt/Equity Ratio": {"max": 0.5, "description": "Low financial leverage"},
    "Current Ratio": {"min": 1.5, "max": 2.5, "description": "Adequate liquidity"},
    "Price/Book Ratio": {"max": 1.5, "description": "Potentially undervalued stock"},
    "Return on Equity (ROE)": {"min": 8, "description": "Efficient profitability"},
    "Return on Assets (ROA)": {"min": 6, "description": "Operational efficiency"},
    "Interest Coverage Ratio": {"min": 5, "description": "Ability to cover debt interest"},
}


# get list of stocks
def load_stock_symbols():
    try:
        with open('stocks.txt', 'r') as file:
            symbols = [line.strip() for line in file if line.strip()]
            return symbols
    except FileNotFoundError:
        st.error("File not found")
        return []


# fetch financial data
def fetch_fundamental_data(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    info = stock.info
    financials = stock.financials
    metrics = {
        "Debt/Equity Ratio": info.get("debtToEquity", "N/A"),
        "Current Ratio": info.get("currentRatio", "N/A"),
        "Price/Book Ratio": info.get("priceToBook", "N/A"),
        "Return on Equity (ROE)": info.get("returnOnEquity", "N/A") * 100 if info.get("returnOnEquity") else "N/A",
        "Return on Assets (ROA)": info.get("returnOnAssets", "N/A") * 100 if info.get("returnOnAssets") else "N/A",
        "Interest Coverage Ratio": calculate_interest_ratio(financials),
    }
    return metrics


# create helper method for Interest coverage Ratio
def calculate_interest_ratio(financials):
    try:
        ebit = financials.loc['Operating Income'].iloc[0]
        interest_expense = financials.loc['Interest Expense'].iloc[0]
        return ebit / interest_expense
    except (KeyError, IndexError, ZeroDivisionError):
        return "N/A"


# evaluate stocks as per criteria
def evaluate_metrics(metrics):
    evaluation = {}
    for metric, value in metrics.items():
        if value == "N/A":
            evaluation[metric] = "N/A"
            continue
        criteria = CRITERIA.get(metric)
        meet_criteria = True
        if "min" in criteria and value < criteria["min"]:
            meet_criteria = False
        if "max" in criteria and value > criteria["max"]:
            meet_criteria = False
        evaluation[metric] = "Pass" if meet_criteria else "Fail"

    return evaluation


# display results
st.title("Stock Dashboard by Buffet's criteria")

stock_symbols = load_stock_symbols()
if not stock_symbols:
    st.warning("No stock names found")
else:
    selected_stock = st.sidebar.selectbox("Select a stock", stock_symbols)
    if selected_stock:
        st.header(f"Evaluating {selected_stock}")
        metrics = fetch_fundamental_data(selected_stock)
        evaluation = evaluate_metrics(metrics)
        for metric, value in metrics.items():
            result = evaluation[metric]
            description = CRITERIA[metric]["description"]
            color = "green" if result == "Pass" else "red"
            st.metric(
                label=f"{metric} ({description})",
                value=value if value != "N/A" else "N/A",
                delta=result,
                delta_color="inverse" if result == "Fail" else "normal"
            )
