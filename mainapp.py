
import streamlit as st
from database_helper import *
import matplotlib.pyplot as plt
from networking_helper import *
def main():
    # Initialize the session state variable
    st.session_state['selected_api'] = 'CoinRanking'
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'liked_page' not in st.session_state:
        st.session_state['liked_page'] = False
    if 'signup_page' not in st.session_state:
        st.session_state['signup_page'] = False

    # Check if the user is authenticated
    if st.session_state['authenticated']:
        if st.session_state['liked_page']:
            liked_page()
        else:
            dashboard()
    elif st.session_state['signup_page']:
        signup_page()
    else:
        login_page()


def login_page():
    st.title('Login')

    st.text('You are not logged in, you must login to continue')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        if login(username, password):
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            st.experimental_rerun()
        else:
            st.error('Incorrect username or password')
    st.markdown("---")
    st.text('Don\'t have an account? Signup below')
    if st.button('Signup'):
        st.session_state['signup_page'] = True
        # signup_page()
        st.experimental_rerun()


def signup_page():
    st.title('Sign Up')
    st.text('Enter your details below to signup')
    st.markdown("---")

    ### INPUTS ###
    st.text('Your username is unique and is stored in lowercase')
    username_signup = st.text_input('Username', key='username_input')
    st.text('Your password needs to be at least 6 characters long and must have one number')
    password_signup = st.text_input('Password', type='password',key='password_input')
    confirm_password_signup = st.text_input('Confirm Password', type='password', key='confirm_password_input')
    ### CHECK INPUTS ###

    if st.button('Sign Up', key='signup_page_button'):
        if username_correct(username_signup) and password_correct(password_signup, confirm_password_signup):
            if signup(username_signup, password_signup):
                st.session_state['authenticated'] = True
                st.session_state['signup_page'] = False
                st.session_state['username'] = username_signup
                st.experimental_rerun()
            else:
                st.error('Username already exists')
        else:
            st.error('Your password is either too short, does not contain a number or does not match the confirm password')
    st.markdown("---")
    st.text('Already have an account? Login below')
    if st.button('Login'):
        st.session_state['signup_page'] = False
        # login_page()
        st.experimental_rerun()


def dashboard():
    username = st.session_state.get('username', 'User')

    # API selection
    st.sidebar.markdown("---")
    st.sidebar.title('API Selection')
    selected_api = st.sidebar.selectbox('Choose an API', ['CoinRanking','CoinGecko'])
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
    if liked_page_button:
        st.session_state['liked_page'] = True
        st.experimental_rerun()

    # sort_by = st.sidebar.selectbox('Sort By', ['Name', 'Price', 'Price Change (24h)'])
    # st.session_state.sort_by = sort_by
    st.title(f"Dashboard - Welcome, {username}!")

    # Data fetching and display
    data = get_response(selected_api)
    if st.session_state.selected_api == 'CoinGecko':
        st.success('Data fetched from CoinGecko')
        df = pd.DataFrame(data, columns=['name', 'symbol', 'current_price', 'price_change_percentage_24h'])
        df.columns = ['Name', 'Symbol', 'Current Price ($)', 'Price Change Last 24h ($)']
    # elif st.session_state.selected_api == 'Binance':
    #     st.success('Data fetched from Binance')
    #
    #     df = pd.DataFrame(data, columns=['symbol', 'lastPrice', 'priceChangePercent'])
    #     df.columns = ['Symbol', 'Current Price ($)', 'Price Change Last 24h (%)']
    else:
        st.success('Data fetched from CoinRanking')
        df = pd.DataFrame(data, columns=['symbol','name', 'price', 'change'])
        df.columns = ['Symbol', 'Name', 'Current Price ($)', 'Price Change Last 24h (%)']


    filtered_df = df.copy()
    if search_symbol:
        filtered_df = filtered_df[filtered_df['Symbol'].str.contains(search_symbol, case=False)]

    # Dataframe styling options

    st.dataframe(filtered_df, width=1280, height=600)
    st.markdown("---")
    if st.button('Logout'):
        st.session_state['authenticated'] = False
        st.experimental_rerun()

def liked_page():
    username = st.session_state.get('username', 'User')
    st.title(f'Coins liked by you, {username}!')
    st.markdown("---")

    if st.sidebar.button('Dashboard'):
        st.session_state['liked_page'] = False
        st.session_state['dashboard'] = True
        st.experimental_rerun()

    # Data fetching and display
    st.subheader("Like a Coin")
    liked_symbol = st.text_input("Enter the symbol of the coin you want to like")
    st.markdown("---")
    if st.button("Like"):
        if liked_symbol.isalpha():
            add_liked_coin(username, liked_symbol)
            st.success(f"You liked {liked_symbol}!")
        else:
            st.warning("Please enter a valid symbol")
    st.markdown("---")
    st.subheader("Liked Coins")
    liked_coins = display_liked_coins()
    coinranking_data = get_response('CoinRanking')
    if not liked_coins.empty:
        found = False
        liked_coins = str(liked_coins.tolist())
        data_dict = liked_coins.split(',')
        data_dict = [x.strip("[]'") for x in data_dict]
        symbol_list = []
        for l_symbol in data_dict:
            l_symbol = l_symbol.upper()
            found = False
            for coin in coinranking_data:
                if coin['symbol'] == l_symbol:
                    symbol_list.append(coin)
                    found = True
            if not found:
                st.warning(f"{l_symbol} not found in CoinRanking API")

        if symbol_list:
            df = pd.DataFrame(symbol_list, columns=['symbol', 'name', 'price', 'change'])
            st.dataframe(df, width=1280, height=400)
        # df = pd.DataFrame([symbol, name, price, change], columns=['symbol', 'name', 'price', 'change'])
        # st.dataframe(df, width=1280, height=600)








    else:
        st.info("You have not liked any coins yet.")

    st.markdown("---")
    if st.button('Logout'):
        st.session_state['authenticated'] = False
        st.experimental_rerun()

if __name__ == '__main__':
    main()
