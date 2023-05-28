import streamlit as st
import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute(
    'CREATE TABLE IF NOT EXISTS users (name TEXT, username VARCHAR(255) NOT NULL, '
    'password varchar(255) NOT NULL, email TEXT NOT NULL, PRIMARY KEY (username))')


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
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            if cursor.fetchone() is None:
                st.warning('Incorrect Username/Password')
            else:
                conn.close()
                st.success('Logged In as {}'.format(username))


def signup():
    import re

    st.write('Please enter your details below')

    #NAME CHECK
    name = st.text_input('First Name', key='name')
    if name.isalpha() and len(name) > 1:
        st.success('Name is valid')
        name_valid = True
    else:
        st.warning('Name is not valid')
        name_valid = False

    # USERNAME CHECK
    username = st.text_input('Username', key='user')
    if cursor.fetchone() is not None:
        st.warning('Username already exists')
        username_valid = False
    if len(username) < 4:
        st.warning('Username should have at least 4 characters')
        username_valid = False
    else:
        st.success('Username is available')
        username_valid = True

    # EMAIL CHECK
    email = st.text_input('Email', key='email')
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.warning('Email address is invalid')
        email_valid = False
    else:
        st.success('Email address is valid')
        email_valid = True

    # PASSWORD CHECK
    password = st.text_input('Password', type='password', key='passw')
    if len(password) < 6:
        st.warning('Password should have at least 6 characters')
        password_valid = False
    elif not any(char.isdigit() for char in password):
        st.warning('Password should have at least one number')
        password_valid = False
    else:
        st.success('Password is valid')
        password_valid = True

    # CONFIRM PASSWORD CHECK
    confirm_password = st.text_input('Confirm Password', type='password', key='con_pass')
    if password != confirm_password:
        st.warning('Passwords do not match')
        confirm_password_valid = False
    else:
        st.success('Passwords match')
        confirm_password_valid = True

    # FUNCTIONALITY
    if st.button('Sign Up'):
        if name_valid and username_valid and email_valid and password_valid and confirm_password_valid:
            cursor.execute('SELECT username FROM users WHERE username=?', (username.lower(),))
            st.success('Welcome {}'.format(username))
            cursor.execute('INSERT INTO users (name, username, password, email) VALUES (?, ?, ?, ?)',
                           (name, username.lower(), password, email))
            conn.commit()
            conn.close()
            clear_inputs()
        else:
            st.warning('Fix the above errors to sign up')

def clear_inputs():
    st.session_state.name = ""
    st.session_state.user = ""
    st.session_state.email = ""
    st.session_state.passw = ""
    st.session_state.con_pass = ""
def main():
    pass

def register():
    pass



if __name__ == '__main__':
    app()