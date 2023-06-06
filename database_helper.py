import sqlite3
import hashlib
import pandas as pd
import streamlit as st


def connect():
    conn = sqlite3.connect("database/userdata.db")
    cursor = conn.cursor()
    return conn, cursor

def close_connection(conn, cursor):
    cursor.close()
    conn.close()
def hash_password(password):
    #Hashes the password using hashlib.sha256
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    #Verifies the provided password against the hashed password
    return hashed_password == hash_password(password)

def create_table():
    ########## CONNECT ##########
    conn, cursor = connect()

    query = (
        'CREATE TABLE IF NOT EXISTS users (username VARCHAR(255) NOT NULL, '
        'password varchar(255) NOT NULL,liked_coins TEXT[], PRIMARY KEY (username))')
    cursor.execute(query)
    conn.commit()

    close_connection(conn, cursor)

def username_correct(username):
    conn, cursor = connect()
    try:
        if cursor.fetchone() is not None:
            return False
        if len(username) < 4:
            return False
        else:
            return True
    finally:
        close_connection(conn, cursor)

def password_correct(password, confirm_password):
    pass
    conn, cursor = connect()
    if len(password) < 6 or not any(char.isdigit() for char in password) or password != confirm_password:
        return False
    else:
        return True
    #     st.warning('Password should have at least 6 characters')
    #     password_valid = False
    #     st.warning('Password should have at least one number')
    #     password_valid = False
    # else:
    #     st.success('Password is valid')
    #     password_valid = True
    #
    # # CONFIRM PASSWORD CHECK
    # confirm_password = st.text_input('Confirm Password', type='password', key='con_pass')
    # if password != confirm_password:
    #     st.warning('Passwords do not match')
    #     confirm_password_valid = False
    # else:
    #     st.success('Passwords match')
    #     confirm_password_valid = True
    #
    #
def signup(username, password):
    ########## CONNECT ##########
    conn, cursor = connect()
    cursor.execute('SELECT username FROM users WHERE username = ?', (username.lower(),))
    existing_username = cursor.fetchone()
    if existing_username is None:

        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    else:
        return False
# def login(username, password):
#     if check(username, password):
#         st.session_state['authenticated'] = True
#         st.session_state['username'] = username
#         return True
#     else:
#         st.session_state['authenticated'] = False
#         return False


# def enter(username, password):
#     ########## CONNECT ##########
#     conn, cursor = connect()
#
#     if check(username, password):
#         close_connection(conn, cursor)
#         return False
#     else:
#         query = "INSERT INTO users (username, password) VALUES (?, ?)"
#         cursor.execute(query, (username, password))
#         conn.commit()
#         close_connection(conn, cursor)
#         return True
#
#         return True

def login(username, password):
    ########## CONNECT ##########
    conn, cursor = connect()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    # IF IT EXISTS
    if result:
        hash_password = result[0]
        if verify_password(password, hash_password):
            conn.commit()
            close_connection(conn, cursor)
            return True
        else:
            conn.commit()
            close_connection(conn, cursor)
            return False

    # IF DOESNT EXIST
    else:
        conn.commit()
        close_connection(conn, cursor)
        # st.error('CHECK NOT WORK')
        return False

def add_liked_coin(username, coin_symbol):
    conn, cursor = connect()

    # Fetch the current list of liked coins for the user
    query = 'SELECT liked_coins FROM users WHERE username = ?'
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    # st.success(result)
    liked_coins = list()
    for i in result:
        liked_coins.append(i)
        # st.success(i)
    # Append the new coin symbol to the list of liked coins
    liked_coins.append(coin_symbol)

    # Convert the list to a string
    liked_coins = [coin for coin in liked_coins if coin is not None]
    liked_coins_str = ','.join(liked_coins)

    # Update the liked_coins column for the user
    query = 'UPDATE users SET liked_coins = ? WHERE username = ?'
    cursor.execute(query, (liked_coins_str, username))
    conn.commit()

    close_connection(conn, cursor)
def display_liked_coins():
    conn, cursor = connect()

    username = st.session_state['username']
    # Fetch the liked coins for the user
    query = 'SELECT liked_coins FROM users WHERE username = ?'
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    liked_coins = result[0] if result else []

    # Create a DataFrame with the liked coins
    series = pd.Series(liked_coins, name='symbol')

    close_connection(conn, cursor)

    return series
# --- main ---

conn, cursor = connect()


create_table() # called create table to create 'users'
# enter('alek', '1234')
# enter('bob', '1234')


close_connection(conn, cursor)
