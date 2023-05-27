import streamlit as st
import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()
try:
    cursor.execute(
    'CREATE TABLE users (name TEXT, username TEXT NOT NULL, '
    'password TEXT NOT NULL, email TEXT NOT NULL, PRIMARY KEY (username))')
except:
    pass

def app():
    st.title("Alek's Price Tracker")
    st.divider()
    menu = ['Home', 'Login', 'Sign Up']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.subheader('Home')
        st.write('Please Sign Up or Login to continue')

    elif choice == 'Login':
        st.subheader('Login')
        login()
    elif choice == 'Sign Up':
        st.subheader('Sign Up')
        signup()
    # choice = st.selectbox('Sign Up or Login', ['Sign Up', 'Login'])
    st.image('Images/Hotpot.png', width=500)
def login():
        st.write('Please enter your login details below')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        if st.button('Login'):
            if password == '':
                st.success('Logged In as {}'.format(username))
            else:
                st.warning('Incorrect Username/Password')

def signup():
        st.write('Please enter your details below')
        name = st.text_input('First and Last Name')
        username = st.text_input('Username')
        email = st.text_input('Email')
        password = st.text_input('Password', type='password')
        confirm_password = st.text_input('Confirm Password', type='password')
        if st.button('Sign Up'):
            cursor.execute('SELECT username FROM users WHERE username=?', (username,))
            if cursor.fetchone() is not None:
                st.warning('Username already exists')
            elif password != confirm_password:
                st.warning('Passwords do not match')
            else:
                st.success('Welcome {}'.format(username))
                cursor.execute('INSERT INTO users (name, username, password, email) VALUES (?, ?, ?, ?)',
                               (name, username, password, email))
                conn.commit()
                conn.close()


def main():
    pass

def register():

    pass




if __name__ == '__main__':
    app()