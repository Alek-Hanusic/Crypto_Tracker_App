import streamlit as st
import requests
import pandas as pd
import plotly.graph_objs as go

# Define the API endpoint and parameters
url = 'https://api.coingecko.com/api/v3/coins/markets'
params = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 100,
    'page': 1,
    'sparkline': True
}

# Make the API request and get the response
response = requests.get(url, params=params)
data = response.json()
# Create a DataFrame from the response data
df = pd.DataFrame(data, columns=['id', 'symbol', 'name', 'current_price', 'price_change_percentage_24h'])
print(data)