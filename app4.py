import os
import sys
import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import requests

# Installation check for yfinance if not already installed
try:
    import yfinance as yf
except ImportError:
    os.system(f"{sys.executable} -m pip install yfinance")
    import yfinance as yf

# Load Treasury yield data from FRED API (You can replace with other sources)
def load_treasury_yield_data():
    # Placeholder for actual FRED API call (use the FRED API for daily treasury yields)
    # Example: Getting 10-year treasury yield
    url = 'https://api.stlouisfed.org/fred/series/observations?series_id=DGS10&api_key=YOUR_API_KEY&file_type=json'
    response = requests.get(url)
    data = response.json()
    dates = [item['date'] for item in data['observations']]
    values = [float(item['value']) if item['value'] != '.' else None for item in data['observations']]
    treasury_data = pd.DataFrame({'Date': pd.to_datetime(dates), 'Yield': values})
    return treasury_data

# Calculate real interest rates and implied rates
def calculate_interest_rates(treasury_yield_data, fed_funds_rate_data):
    # Example calculation based on treasury yield (simplified)
    real_interest_rate = treasury_yield_data['Yield'] - fed_funds_rate_data['Rate']
    implied_rate = fed_funds_rate_data['Rate'] + 0.5  # Example implied rate formula
    return real_interest_rate, implied_rate

# Analyze the yield curve: steepener vs. flattener
def analyze_yield_curve(treasury_yield_data):
    # We can determine whether the yield curve is steepening or flattening based on the change in yields.
    yield_diff = treasury_yield_data['Yield'].diff()
    if yield_diff.iloc[-1] > 0:
        return "Steepener"
    else:
        return "Flattener"

# Risk-On/Risk-Off Sentiment based on financial data
def risk_sentiment(implied_rate, real_interest_rate, gold_price, dxy, spx_futures):
    # Sentiment rules based on implied rate and other indicators
    if implied_rate > real_interest_rate and gold_price < 2000 and dxy > 95 and spx_futures > 4000:
        return "Risk-On"
    else:
        return "Risk-Off"

# Example of loading data using yfinance
def load_data():
    # Example: Fetch stock data for S&P500 index (SPX)
    spx = yf.download('^SPX', start='2022-01-01', end='2022-12-31')
    gold = yf.download('GC=F', start='2022-01-01', end='2022-12-31')  # Gold futures
    dxy = yf.download('DX-Y.NYB', start='2022-01-01', end='2022-12-31')  # US Dollar Index
    return spx, gold, dxy

# Streamlit UI to display results
st.title("Financial Sentiment Dashboard")

# Fetch market data
spx, gold, dxy = load_data()

# Load treasury yield curve data (simplified example)
treasury_data = load_treasury_yield_data()
fed_funds_rate_data = pd.DataFrame({'Date': pd.to_datetime(['2022-01-01', '2022-02-01', '2022-03-01']), 'Rate': [0.25, 0.5, 0.75]})

# Calculate real interest rates and implied rates
real_interest_rate, implied_rate = calculate_interest_rates(treasury_data, fed_funds_rate_data)

# Yield curve analysis
yield_curve_analysis = analyze_yield_curve(treasury_data)

# Assess the market sentiment
sentiment = risk_sentiment(implied_rate.iloc[-1], real_interest_rate.iloc[-1], gold['Close'][-1], dxy['Close'][-1], spx['Close'][-1])

# Display information on Streamlit
st.write("Real Interest Rates:", real_interest_rate.iloc[-1])
st.write("Implied Rates:", implied_rate.iloc[-1])
st.write("Yield Curve Analysis:", yield_curve_analysis)
st.write("Market Sentiment:", sentiment)

# Example: Display the dataframes
st.write("S&P 500 Data:")
st.write(spx.tail())

st.write("Gold Data:")
st.write(gold.tail())

st.write("Dollar Index Data:")
st.write(dxy.tail())

# Treasury Yield Data
st.write("Treasury Yield Data:")
st.write(treasury_data.tail())
