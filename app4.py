import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Financial Dashboard", layout="wide")
st.title("📊 Daily Macro & Futures Sentiment Dashboard")

# Define the instruments and their Yahoo tickers
tickers = {
    "S&P 500 Futures": "ES=F",
    "Fed Funds Futures": "ZQ=F",
    "10Y Treasury Yield": "^TNX",
    "Gold Futures": "GC=F",
    "Dollar Index": "DX-Y.NYB",
    "VIX": "^VIX"
}

# Download the past 2 days of data
data = yf.download(list(tickers.values()), period="2d")

# Extract last and previous close
df_close = data["Close"]
last_close = df_close.iloc[-1]
prev_close = df_close.iloc[-2]

# Calculate changes
result_data = []
for name, symbol in tickers.items():
    change = last_close[symbol] - prev_close[symbol]
    percent = (change / prev_close[symbol]) * 100
    result_data.append({
        "Instrument": name,
        "Last Close": round(last_close[symbol], 2),
        "Prev Close": round(prev_close[symbol], 2),
        "Change": round(change, 2),
        "Percent Change": f"{round(percent, 2)}%"
    })

df = pd.DataFrame(result_data)

# Sentiment classification logic
def determine_sentiment(row):
    if row['Instrument'] in ["S&P 500 Futures", "Gold Futures"]:
        return "Risk-On" if row["Change"] > 0 else "Risk-Off"
    elif row['Instrument'] in ["VIX", "10Y Treasury Yield"]:
        return "Risk-Off" if row["Change"] > 0 else "Risk-On"
    return "Neutral"

df["Sentiment"] = df.apply(determine_sentiment, axis=1)

# Yield Curve Analysis (Steepener vs Flattener)
try:
    spread_today = last_close["^TNX"] - last_close["ZQ=F"]  # Proxy for 10Y - Fed Funds
    spread_yesterday = prev_close["^TNX"] - prev_close["ZQ=F"]
    curve_shape = "Steepener" if spread_today > spread_yesterday else "Flattener"
except:
    curve_shape = "N/A"

# Display Results
st.subheader("Market Instruments Performance")
st.dataframe(df, use_container_width=True)

# Risk Sentiment Summary
risk_on = df[df["Sentiment"] == "Risk-On"].shape[0]
risk_off = df[df["Sentiment"] == "Risk-Off"].shape[0]
st.metric("📈 Risk-On Signals", risk_on)
st.metric("📉 Risk-Off Signals", risk_off)
st.metric("📊 Yield Curve Movement", curve_shape)

# Optional: Line Chart of Prices
st.subheader("Price Trends (Past 2 Days)")
st.line_chart(df_close)

st.caption("Data from Yahoo Finance. Consider augmenting with CBOE or FRED for critical production-grade accuracy.")





