# app.py

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="Financial Sentiment Dashboard", layout="wide")
st.title("📊 Daily Financial Market Dashboard")

# === Helper Functions ===

@st.cache_data
def fetch_yfinance_data(tickers, start, end):
    data = yf.download(tickers, start=start, end=end)
    return data['Adj Close'] if 'Adj Close' in data else data

def calc_real_interest(nominal_yield, inflation_rate):
    return nominal_yield - inflation_rate

def get_sentiment(gold_change, dxy_change, spx_change, yield_slope_change):
    risk_off_score = 0
    if gold_change > 0: risk_off_score += 1
    if dxy_change > 0: risk_off_score += 1
    if spx_change < 0: risk_off_score += 1
    if yield_slope_change < 0: risk_off_score += 1
    return "🟥 Risk-Off" if risk_off_score >= 3 else "🟩 Risk-On"

# === Dates ===
today = datetime.today()
yesterday = today - timedelta(days=2)
two_days_ago = today - timedelta(days=3)

# === Fetch Market Data ===
tickers = {
    'Gold': 'GC=F',
    'DXY': 'DX-Y.NYB',
    'S&P Futures': 'ES=F',
    '2Y Treasury': '^IRX',
    '10Y Treasury': '^TNX',
    'Fed Funds Futures': 'ZQ=F'
}

prices_today = fetch_yfinance_data(list(tickers.values()), start=yesterday, end=today)
prices_prev = fetch_yfinance_data(list(tickers.values()), start=two_days_ago, end=yesterday)

def pct_change(symbol):
    return ((prices_today[tickers[symbol]].iloc[-1] - prices_prev[tickers[symbol]].iloc[-1])
            / prices_prev[tickers[symbol]].iloc[-1]) * 100

gold_ch = pct_change('Gold')
dxy_ch = pct_change('DXY')
spx_ch = pct_change('S&P Futures')
irx = prices_today[tickers['2Y Treasury']].iloc[-1] / 100
tnx = prices_today[tickers['10Y Treasury']].iloc[-1] / 100
slope_change = tnx - irx

# === Real Interest Rate ===
# Assume US CPI YoY ~ 3.2% (update via API if needed)
real_rate = calc_real_interest(tnx, 0.032)

# === Fed Funds Implied Rate ===
zq_price = prices_today[tickers['Fed Funds Futures']].iloc[-1]
implied_fed_rate = 100 - zq_price

# === Display Results ===
col1, col2, col3 = st.columns(3)
col1.metric("Gold %", f"{gold_ch:.2f}%")
col2.metric("DXY %", f"{dxy_ch:.2f}%")
col3.metric("S&P Futures %", f"{spx_ch:.2f}%")

col4, col5, col6 = st.columns(3)
col4.metric("10Y Yield", f"{tnx*100:.2f}%")
col5.metric("2Y Yield", f"{irx*100:.2f}%")
col6.metric("Yield Curve", f"{slope_change*100:.2f} bps", "Flattener" if slope_change < 0 else "Steepener")

st.markdown("---")

col7, col8, col9 = st.columns(3)
col7.metric("Real Rate", f"{real_rate*100:.2f}%")
col8.metric("Fed Funds Futures", f"{zq_price:.2f}")
col9.metric("Implied Fed Rate", f"{implied_fed_rate:.2f}%")

st.subheader("📈 Market Sentiment")
sentiment = get_sentiment(gold_ch, dxy_ch, spx_ch, slope_change)
st.success(f"Market Sentiment: {sentiment}")
