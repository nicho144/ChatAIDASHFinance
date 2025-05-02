import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="Financial Dashboard", layout="wide")

st.title("📈 Market Risk Dashboard")
st.caption("Data from Yahoo Finance. Last updated: " + str(datetime.now().date()))

# --- Fetch data
def fetch_data(ticker, period="5d", interval="1d"):
    data = yf.download(ticker, period=period, interval=interval)
    return data

# --- Get market data
tickers = {
    "S&P 500 Futures": "^GSPC",
    "10Y Treasury": "^TNX",
    "Fed Funds Rate Proxy": "^IRX",
    "Gold": "GC=F",
    "US Dollar Index (DXY)": "DX-Y.NYB"
}

market_data = {name: fetch_data(ticker) for name, ticker in tickers.items()}

# --- Calculate metrics
def calculate_real_rate(nominal_yield, inflation_rate):
    return nominal_yield - inflation_rate

def calculate_yield_curve_change(tnx_today, irx_today, tnx_yesterday, irx_yesterday):
    diff_today = tnx_today - irx_today
    diff_yesterday = tnx_yesterday - irx_yesterday
    change = diff_today - diff_yesterday
    return "Steepener" if change > 0 else "Flattener"

# --- Display
st.subheader("Market Overview")

for name, data in market_data.items():
    price = data['Close'].iloc[-1]
    change = price - data['Close'].iloc[-2]
    pct = (change / data['Close'].iloc[-2]) * 100
    st.metric(name, f"{price:.2f}", f"{pct:+.2f}%")

# --- Risk Sentiment Assessment
st.subheader("🧠 Risk Sentiment Analysis")

try:
    tnx_today = market_data["10Y Treasury"]['Close'].iloc[-1]
    irx_today = market_data["Fed Funds Rate Proxy"]['Close'].iloc[-1]
    tnx_yesterday = market_data["10Y Treasury"]['Close'].iloc[-2]
    irx_yesterday = market_data["Fed Funds Rate Proxy"]['Close'].iloc[-2]

    yield_slope = calculate_yield_curve_change(tnx_today, irx_today, tnx_yesterday, irx_yesterday)
    real_rate = calculate_real_rate(tnx_today, irx_today)

    st.write(f"Yield Curve Movement: **{yield_slope}**")
    st.write(f"Real Interest Rate: **{real_rate:.2f}%**")

    if yield_slope == "Steepener" and real_rate < 2:
        sentiment = "🟢 Risk-On"
    else:
        sentiment = "🔴 Risk-Off"
    st.success(f"Current Market Sentiment: {sentiment}")
except Exception as e:
    st.error("Error calculating sentiment. Please try again later.")
    st.exception(e)
