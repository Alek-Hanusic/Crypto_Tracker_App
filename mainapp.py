
import streamlit as st
from database_helper import *
import pandas as pd
import matplotlib.pyplot as plt
from networking_helper import *
def main():
    # Initialize the session state variable
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'liked_page' not in st.session_state:
        st.session_state['liked_page'] = False

    # Check if the user is authenticated
    if st.session_state['authenticated']:
        if st.session_state['liked_page']:
            liked_page()
        else:
            dashboard()
    else:
        login_page()

def authenticate_user(username, password):
    if check(username, password):
        st.session_state['authenticated'] = True
        st.session_state['username'] = username
        return True
    else:
        st.session_state['authenticated'] = False
        return False

def login_page():
    st.title('Login')
    st.text('You are not logged in, you must login to continue')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login', on_click=lambda: authenticate_user(username, password)):
        if st.session_state['authenticated']:
            st.experimental_rerun()
        else:
            st.error('Incorrect username or password')
    st.text('Don\'t have an account? Signup below')
    if st.button('Signup', on_click=Signup_Page):
        st.experimental_rerun()


def Signup_Page():
    st.title('Signup')






def dashboard():
    username = st.session_state.get('username', 'User')
    if 'selected_api' not in st.session_state:
        st.session_state.selected_api = 'CoinRanking'

    # API selection
    st.sidebar.markdown("---")
    st.sidebar.title('API Selection')
    selected_api = st.sidebar.selectbox('Choose an API', ['CoinGecko','CoinRanking', 'Binance'])
    st.session_state.selected_api = selected_api

    # Sort options
    st.sidebar.markdown("---")
    st.sidebar.title('Filters')
    search_symbol = st.sidebar.text_input('Search Symbol')

    # Liked coins
    st.sidebar.markdown("---")
    st.sidebar.title('Liked Coins')
    st.sidebar.text('Track your coins')
    liked_page_button = st.sidebar.button(':yellow_heart: Liked Coins :yellow_heart:')
    st.sidebar.markdown("---")

    # sort_by = st.sidebar.selectbox('Sort By', ['Name', 'Price', 'Price Change (24h)'])
    # st.session_state.sort_by = sort_by
    st.title(f"Dashboard - Welcome, {username}!")

    # Data fetching and display
    data = get_response(selected_api)
    if st.session_state.selected_api == 'CoinGecko':
        st.success('Data fetched from CoinGecko')
        df = pd.DataFrame(data, columns=['name', 'symbol', 'current_price', 'price_change_percentage_24h'])
        df.columns = ['Name', 'Symbol', 'Current Price', 'Price Change (24h)']
    elif st.session_state.selected_api == 'Binance':
        st.success('Data fetched from Binance')
        df = pd.DataFrame(data, columns=['symbol', 'lastPrice', 'priceChangePercent'])
        df.columns = ['Symbol', 'Current Price ($)', 'Price Change Last 24h (%)']
    else:
        st.success('Data fetched from CoinRanking')
        df = pd.DataFrame(data, columns=['symbol','name', 'price', 'change'])
        df.columns = ['Symbol', 'Name', 'Current Price ($)', 'Price Change Last 24h (%)']





    filtered_df = df.copy()
    if search_symbol:
        filtered_df = filtered_df[filtered_df['Symbol'].str.contains(search_symbol, case=False)]

    # Dataframe styling options

    st.dataframe(filtered_df, width=1280, height=720)

    if st.button('Logout'):
        st.session_state['authenticated'] = False
        st.experimental_rerun()

def liked_page():
    st.title('Coins liked by you, {username}!')

    if st.sidebar.button('Dashboard'):
        st.session_state['liked_page'] = False
        st.session_state['dashboard'] = True
        st.experimental_rerun()
    if st.button('Logout'):
        st.session_state['authenticated'] = False
        st.experimental_rerun()

if __name__ == '__main__':
    main()
