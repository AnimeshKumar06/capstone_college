import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc

# Streamlit UI
st.title("📈 Stock Candlestick Chart")

# Sidebar for symbol and date selection
symbol = st.sidebar.text_input("Enter Stock Symbol", value="AAPL")
days = st.sidebar.slider("Select Time Frame (days)", 7, 90, 30)
start_date = datetime.datetime.now() - datetime.timedelta(days=days)
end_date = datetime.datetime.now()

# Fetch stock data
st.sidebar.write(f"Fetching data for *{symbol}* from *{start_date.date()}* to *{end_date.date()}*")
try:
    df = yf.download(symbol, start=start_date, end=end_date, interval="1d")

    if df.empty:
        st.warning("No data available. Please try a different symbol or time frame.")
    else:
        # Prepare data
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()
        df.reset_index(inplace=True)
        df['Date'] = df['Date'].map(mdates.date2num)

        # Prepare OHLC data for candlestick chart
        ohlc = df[['Date', 'Open', 'High', 'Low', 'Close']].values

        # Plotting
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, days // 15)))
        plt.xticks(rotation=45)

        candlestick_ohlc(ax, ohlc, width=0.6, colorup='green', colordown='red', alpha=0.8)

        plt.xlabel('Date')
        plt.ylabel('Stock Price')
        plt.title(f"{symbol} Candlestick Chart (Daily)")
        plt.grid(True, linestyle='--', alpha=0.5)

        st.pyplot(fig)

except Exception as e:
    st.error(f"An error occurred: {e}")