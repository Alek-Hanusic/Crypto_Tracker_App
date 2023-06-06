import streamlit as st
import requests
import pandas as pd
import plotly.graph_objs as plotly_go

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
df = pd.DataFrame(data, columns=['image', 'symbol', 'name', 'current_price', 'price_change_percentage_24h'])

# Define a function to get the HTML code for the image
def get_image_html(url):
    return f'<img src="{url}" width="35">'

# Apply the function to the 'image' column
df['image'] = df['image'].apply(lambda x: get_image_html(x))

# Rename the columns
df = df.rename(columns={
    'image': 'LOGO',
    'name': 'NAME',
    'symbol': 'SYMBOL',
    'current_price': 'PRICE($)',
    'price_change_percentage_24h': 'PRICE CHANGE 24H (%)',
})
st.write(data)
# Render the styled DataFrame
st.dataframe(df)


