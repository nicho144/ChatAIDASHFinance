import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys

# Function to check and install yfinance if missing
def check_and_install_yfinance():
    try:
        import yfinance as yf
    except ImportError:
        st.write("`yfinance` not found. Installing...")
        os.system(f"{sys.executable} -m pip install yfinance")
        import yfinance as yf

# Install yfinance if it's not found
check_and_install_yfinance()

# Function to get price data from Yahoo Finance
def get_price(ticker):
    try:
        data = yf.download(ticker, period="1d", interval="1d")
        return data["Close"].iloc[0] if not data.empty else None
    except Exception as e:
        st.write(f"Error fetching data for {ticker}: {e}")
        return None

# Fetch tickers
def fetch_data():
    try:
        fed_funds = get_price("ZQ=F")
        spx = get_price("^GSPC")
        dxy = get_price("DX-Y.NYB")
        gold = get_price("GC=F")
        ten_year = get_price("^TNX") / 10  # 10Y treasury yield in % (divide by 10)
        two_year = get_price("^IRX") / 100  # 2Y treasury yield in %

        return fed_funds, spx, dxy, gold, ten_year, two_year
    except Exception as e:
        st.write(f"Error fetching data: {e}")
        return None, None, None, None, None, None

# Check for CPI data, default 3.4%
def get_cpi():
    return 3.4  # Placeholder for CPI data

# Sentiment logic
def calculate_sentiment(spx_chg, dxy_chg, gold_chg):
    if spx_chg > 0 and dxy_chg < 0 and gold_chg < 0:
        return "🟢 Risk-On"
    elif spx_chg < 0 and (dxy_chg > 0 or gold_chg > 0):
        return "🔴 Risk-Off"
    else:
        return "⚪ Neutral"

# Streamlit Layout and Dashboard
def app():
    st.title("Financial Dashboard")
    st.write("Welcome to the financial market dashboard. This app calculates real interest rates, yield spreads, and more.")

    fed_funds, spx, dxy, gold, ten_year, two_year = fetch_data()

    if fed_funds is not None:
        cpi = get_cpi()
        real_interest_rate = fed_funds - cpi
        yield_spread = ten_year - two_year

        # Sentiment logic (price changes for simplification)
        spx_chg = spx - spx  # No price change logic implemented yet
        dxy_chg = dxy - dxy  # Same for DXY
        gold_chg = gold - gold  # Same for Gold
        
        sentiment = calculate_sentiment(spx_chg, dxy_chg, gold_chg)

        # Display Results
        st.subheader(f"Real Interest Rate: {real_interest_rate:.2f}%")
        st.subheader(f"Yield Spread (10Y - 2Y): {yield_spread:.2f}%")
        st.subheader(f"Market Sentiment: {sentiment}")
        
        # Additional Visuals (Placeholder for Future Expansion)
        st.write(f"Fed Funds Rate (Futures): {fed_funds:.2f}%")
        st.write(f"S&P 500 (SPX): {spx}")
        st.write(f"DXY (US Dollar Index): {dxy}")
        st.write(f"Gold (GC=F): {gold}")
        st.write(f"10-Year Treasury Yield: {ten_year}%")
        st.write(f"2-Year Treasury Yield: {two_year}%")
        
    else:
        st.write("Failed to retrieve financial data. Please check the connection.")

# Run the Streamlit app
if __name__ == "__main__":
    app()

