# import requests
# url = 'https://data.binance.com/api/v3/ticker/price'
# params = {
#             'symbol': 'coinrankingee8408d5b7c021e1a323d780d62b61d9db4145c28c17b60d',
#             'base': 'USD',
#         }
# response = requests.get(url)
# data = response.json()
# print(data)
import requests
import json

# Replace YOUR_API_KEY with your actual API key
api_key = 'coinrankingee8408d5b7c021e1a323d780d62b61d9db4145c28c17b60d'

# Make a request to the API to get the Bitcoin price in USD
response = requests.get(f'https://api.coinranking.com/v2/coins')

# Parse the JSON response
data = json.loads(response.text)

# Extract the Bitcoin price from the response


print(data)