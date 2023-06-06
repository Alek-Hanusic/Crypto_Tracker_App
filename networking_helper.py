import streamlit as st
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt


coin_gecko_api = "https://api.coingecko.com/api/v3/coins/markets"
binance_api = "https://data.binance.com/api/v3/ticker/24hr/"
coinranking_api = "https://api.coinranking.com/v2/coins"


def get_response(api):
    if api == 'CoinGecko':
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            # 'per_page': 10,
            # 'page': 1
        }
        response = requests.get(coin_gecko_api, params=params)
        data = response.json()
        return data
    # if api == 'Binance':
    #
    #     response = requests.get(binance_api)
    #     data = response.json()
    #     return data

    if api == 'CoinRanking':
        response = requests.get(coinranking_api)
        data = json.loads(response.text)
        data = data["data"]["coins"]
        # st.error(data)
        # for coin in data:
        #     name = coin["name"]
        #     symbol = coin["symbol"]
        #     price = float(coin["price"])
        #     price_change = float(coin["change"])
        #     data.append({"Name": name, "Symbol": symbol, "Price": price, "Price Change": price_change})
        return data
    else:
        return "Error"



# Plot settings
#     plt.style.use('seaborn')
# API endpoints

