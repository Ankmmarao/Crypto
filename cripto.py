import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# Function to fetch cryptocurrency data from CoinGecko
def get_crypto_data(coin, vs_currency, days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency={vs_currency}&days={days}"
    response = requests.get(url)
    data = response.json()
     # Print the first few rows of the DataFrame


    # Check if 'prices' key exists in the received data
    if 'prices' in data:
        prices = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
        prices['date'] = pd.to_datetime(prices['timestamp'], unit='ms')
        prices.set_index('date', inplace=True)
        return prices

# Set Streamlit app configurations
st.set_page_config(
    page_title="Cryptocurrency Analysis",
    page_icon=":money_with_wings:",
    layout="wide"
)

# Custom CSS for beautiful headings and backgrounds
st.markdown(
    """
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #ffffff;
        padding: 20px;
        background-color: #0066CC;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
    .sidebar {
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app
st.markdown('<p class="title">Cryptocurrency Analysis</p>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar"><h2>Settings</h2></div>', unsafe_allow_html=True)

# Select cryptocurrency and currency
coin = st.sidebar.selectbox('Select Cryptocurrency', ['bitcoin', 'ethereum', 'ripple'])
vs_currency = st.sidebar.selectbox('Select Currency', ['usd', 'eur', 'gbp'])

# Get cryptocurrency data
days = 1  # Fetch data for the last 1 day
crypto_data = get_crypto_data(coin, vs_currency, days)
print(crypto_data.head())

# Display data
st.subheader(f'{coin.capitalize()} Price in {vs_currency.upper()}')
st.write(crypto_data)

# Live updating plot with seaborn
fig, ax = plt.subplots()
line, = ax.plot(crypto_data.index, crypto_data['price'], label='Price')

# Use Seaborn's set_style for better aesthetics
sns.set_style("whitegrid")

# Infinite loop for updating the plot
while True:
    # Fetch updated data every 10 seconds
    updated_data = get_crypto_data(coin, vs_currency, days)
    
    # Update the existing plot data
    line.set_data(updated_data.index, updated_data['price'])
    
    # Clear the previous plot in Streamlit
    plt.cla()
    
    # Redraw the updated plot using Seaborn and Matplotlib
    sns.lineplot(data=updated_data, x=updated_data.index, y='price', ax=ax, label='Price')
    
    # Display the plot in Streamlit
    st.pyplot(fig)
    
    # Wait for 10 seconds before fetching new data
    plt.pause(10)
