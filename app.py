import streamlit as st
import yfinance as yf
import datetime
import pandas as pd

# Helper Functions
def get_today_yield(symbol):
    data = yf.Ticker(symbol)
    hist = data.history(period="2d")
    if len(hist) >= 2:
        today_yield = hist['Close'].iloc[-1]
        yesterday_yield = hist['Close'].iloc[-2]
        delta = today_yield - yesterday_yield
        return today_yield, delta
    return None, None

def check_steepener():
    ten_year, ten_delta = get_today_yield("^TNX")
    two_year, two_delta = get_today_yield("^IRX")
    if ten_year and two_year:
        slope_today = ten_year - two_year
        slope_yesterday = slope_today - (ten_delta - two_delta)
        if slope_today > slope_yesterday:
            return "Steepener"
        else:
            return "Flattener"
    return "No Data"

def get_price(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")
    if not data.empty:
        return data['Close'].iloc[-1]
    return None

def infer_sentiment(gold, spx, dxy):
    if spx > 0 and gold < 0 and dxy < 0:
        return "Risk-On"
    elif gold > 0 and spx < 0:
        return "Risk-Off"
    else:
        return "Mixed / Neutral"

# Streamlit UI
st.set_page_config(page_title="Market Dashboard", layout="wide")
st.title("📊 Daily Financial Dashboard")

# Prices and indicators
st.header("📈 Market Prices")

gold = get_price("GC=F")
dxy = get_price("DX-Y.NYB")
spx = get_price("^GSPC")
bonds = get_price("ZB=F")
fed_futures = get_price("ZQ=F")

st.metric("Gold Futures", f"${gold:,.2f}" if gold else "N/A")
st.metric("DXY (USD Index)", f"{dxy:.2f}" if dxy else "N/A")
st.metric("S&P 500 Index", f"{spx:,.2f}" if spx else "N/A")
st.metric("30Y Bonds", f"{bonds:,.2f}" if bonds else "N/A")
st.metric("Fed Funds Futures", f"{fed_futures:,.2f}" if fed_futures else "N/A")

# Yield Curve Analysis
st.header("🧮 Yield Curve")

steepener = check_steepener()
st.write(f"Yield Curve Movement: **{steepener}**")

# Real Interest Rate Estimate (approximate)
inflation_estimate = 3.0  # Change as needed or connect to FRED
if fed_futures:
    implied_rate = fed_futures / 100
    real_rate = implied_rate - (inflation_estimate / 100)
    st.metric("Implied Fed Rate", f"{implied_rate:.2%}")
    st.metric("Estimated Real Interest Rate", f"{real_rate:.2%}")
else:
    st.write("Fed Futures data unavailable.")

# Sentiment Analysis
st.header("🔍 Market Sentiment")

sentiment = infer_sentiment(gold, spx, dxy)
st.success(f"Market Sentiment: **{sentiment}**")

st.caption("Data Source: Yahoo Finance. Rates are approximations.")
