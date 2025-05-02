import streamlit as st
import pandas as pd
from fredapi import Fred
import datetime

# Initialize FRED API
fred = Fred(api_key='YOUR_FRED_API_KEY')

# Set date range
end_date = datetime.datetime.today()
start_date = end_date - datetime.timedelta(days=30)

# Fetch data
cpi = fred.get_series('CPIAUCSL', start_date, end_date)
dgs10 = fred.get_series('DGS10', start_date, end_date)
dgs3mo = fred.get_series('DGS3MO', start_date, end_date)
gold = fred.get_series('GOLDAMGBD228NLBM', start_date, end_date)
dxy = fred.get_series('DTWEXBGS', start_date, end_date)
sp500 = fred.get_series('SP500', start_date, end_date)

# Calculate real interest rate
latest_cpi = cpi.iloc[-1]
latest_dgs10 = dgs10.iloc[-1]
real_rate = latest_dgs10 - latest_cpi

# Yield curve analysis
yield_curve_change = dgs10.iloc[-1] - dgs3mo.iloc[-1]
previous_yield_curve = dgs10.iloc[-2] - dgs3mo.iloc[-2]
curve_movement = "Steepening" if yield_curve_change > previous_yield_curve else "Flattening"

# Market sentiment
gold_change = gold.iloc[-1] - gold.iloc[-2]
dxy_change = dxy.iloc[-1] - dxy.iloc[-2]
sp500_change = sp500.iloc[-1] - sp500.iloc[-2]

if sp500_change > 0 and gold_change < 0 and dxy_change > 0:
    sentiment = "Risk-On"
elif sp500_change < 0 and gold_change > 0 and dxy_change < 0:
    sentiment = "Risk-Off"
else:
    sentiment = "Neutral"

# Streamlit dashboard
st.title("Financial Dashboard")

st.subheader("Real Interest Rate")
st.metric(label="Real Interest Rate (%)", value=round(real_rate, 2))

st.subheader("Yield Curve Movement")
st.metric(label="Current Spread (10Y - 3M)", value=round(yield_curve_change, 2))
st.write(f"Yield Curve is {curve_movement}")

st.subheader("Market Sentiment")
st.write(f"Market Sentiment: **{sentiment}**")
