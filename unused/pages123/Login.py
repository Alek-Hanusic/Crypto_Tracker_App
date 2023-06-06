import streamlit as st
import sqlite3
import streamlit_authenticator as authenticator
def login():
    if st.session_state.is_logged_in == True:
        st.success('You are already logged in')
    else:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        st.write('Please enter your login details below')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        if st.button('Login'):
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            if cursor.fetchone() is None:
                st.warning('Incorrect Username/Password')

            else:
                conn.close()
                st.success('Logged In as {}'.format(username))
                st.session_state.is_logged_in = True
name, authentication_status, username = authenticator.login('Login', 'main')
if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    st.title('Some content')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')