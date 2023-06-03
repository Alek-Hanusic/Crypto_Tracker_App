import streamlit as st
from database_helper import login
headerApp = st.container()
mainApp = st.container()
loginApp = st.container()
logoutApp = st.container()

def Login_CLick(username, password):
    if login(username, password):
        st.session_state['loggedIn'] = True
    else:
        st.session_state['loggedIn'] = False;
        st.error("Invalid user name or password")

def login_page():
    with loginApp:
        if st.session_state['loggedIn'] == False:
            st.title('Login')
            st.text('You are not logged in, you must login to continue')
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            st.button("Login", on_click= Login_CLick(username, password))
        else:
            st.success('You are already logged in')

def default():
    with mainApp:
        pass
        # st.title("Alek\'s Price Tracker")
        # st.title('Welcome')
        # st.text('Please login or signup to continue')
    with headerApp:
        st.title("Alek\'s Price Tracker")
        # first run will have nothing in session_state
        if 'loggedIn' not in st.session_state:
            st.session_state['loggedIn'] = False

            login_page()
        else:
            if st.session_state['loggedIn']:
                # show_logout_page()
                default()
            else:
                login_page()


if __name__ == '__main__':
    # st.set_page_config(page_title='Alek\'s Price Tracker', page_icon='Images/Hotpot.png', layout='wide')
    default()