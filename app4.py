import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date

st.set_page_config(page_title="Daily Financial Dashboard", layout="wide")
st.title("📊 Daily Financial Sentiment Dashboard")

# Helper to safely fetch ticker price & percent change
def get_price(ticker):
    try:
        data = yf.download(ticker, period="5d", interval="1d", progress=False)
        if data.empty or "Close" not in data.columns:
            return None, None
        latest = data["Close"].dropna().iloc[-1]
        change = data["Close"].pct_change().dropna().iloc[-1]
        return round(latest, 2), round(change * 100, 2)
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None, None

# Pull necessary prices
with st.spinner("Fetching market data..."):
    fed_funds, fed_funds_chg = get_price("ZQ=F")        # Fed Funds Futures
    spx, spx_chg = get_price("^GSPC")                   # S&P 500
    dxy, dxy_chg = get_price("DX-Y.NYB")                # DXY
    gold, gold_chg = get_price("GC=F")                  # Gold Futures
    bond10, bond10_chg = get_price("^TNX")              # 10Y Yield (x10)
    bond2, bond2_chg = get_price("^IRX")                # 2Y Yield (x100)

# Yield spread
spread, spread_status = None, "N/A"
if bond10 is not None and bond2 is not None:
    y10 = bond10 / 10
    y2 = bond2 / 100
    spread = round(y10 - y2, 2)
    spread_status = "Steepener" if spread > 0 else "Flattener"

# Real interest rate (Fed Funds - CPI)
# For demo purposes, CPI is hardcoded — this could be automated via FRED
cpi_yoy = 3.4
real_rate = round((fed_funds or 0) - cpi_yoy, 2) if fed_funds else None

# Risk sentiment
sentiment = "Unknown"
if spx_chg is not None and dxy_chg is not None and gold_chg is not None:
    if spx_chg > 0 and dxy_chg < 0 and gold_chg < 0:
        sentiment = "🟢 Risk-On"
    elif spx_chg < 0 and (dxy_chg > 0 or gold_chg > 0):
        sentiment = "🔴 Risk-Off"

# Display
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Key Market Prices")
    st.metric("Fed Funds Futures (ZQ=F)", fed_funds, f"{fed_funds_chg}%")
    st.metric("S&P 500 (^GSPC)", spx, f"{spx_chg}%")
    st.metric("DXY", dxy, f"{dxy_chg}%")
    st.metric("Gold Futures (GC=F)", gold, f"{gold_chg}%")

with col2:
    st.subheader("💡 Yield & Rate Analysis")
    st.metric("10Y Treasury Yield", f"{y10:.2f}%" if bond10 else "N/A", f"{bond10_chg}%" if bond10_chg else "")
    st.metric("2Y Treasury Yield", f"{y2:.2f}%" if bond2 else "N/A", f"{bond2_chg}%" if bond2_chg else "")
    st.metric("Yield Spread (10Y - 2Y)", spread if spread is not None else "N/A", spread_status)
    st.metric("Real Interest Rate", f"{real_rate}%" if real_rate is not None else "N/A")

st.markdown("---")
st.subheader("📊 Market Sentiment")
st.markdown(f"### {sentiment}")

st.caption(f"Last updated: {date.today()}")
