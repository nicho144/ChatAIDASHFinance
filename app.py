import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import streamlit as st

# Your code logic goes here
st.title("Financial Dashboard")

# Example: Fetching historical data for SPY (S&P 500 ETF)
ticker = "SPY"
data = yf.download(ticker, start="2020-01-01", end=datetime.datetime.today().strftime('%Y-%m-%d'))

# Display the stock data
st.write(f"Stock data for {ticker}:", data.tail())

# Example: Plotting a simple line chart for SPY
st.write("Stock Price Trend:")
fig, ax = plt.subplots()
ax.plot(data.index, data['Close'])
st.pyplot(fig)

# Example: Calculate the 7-day moving average
data['7-day MA'] = data['Close'].rolling(window=7).mean()

st.write("7-Day Moving Average:")
st.line_chart(data[['Close', '7-day MA']])

# Example: Calculate Real Interest Rate (using a fixed formula for simplicity)
inflation_rate = 2  # Example: 2% inflation
nominal_interest_rate = 5  # Example: 5% nominal interest rate
real_interest_rate = nominal_interest_rate - inflation_rate

st.write(f"Real Interest Rate: {real_interest_rate}%")
