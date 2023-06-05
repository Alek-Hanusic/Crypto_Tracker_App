import sqlite3
import streamlit as st

def connect():
    conn = sqlite3.connect("database/userdata.db")
    cursor = conn.cursor()
    return conn, cursor

def close_connection(conn, cursor):
    cursor.close()
    conn.close()

def create_table():
    ########## CONNECT ##########
    conn, cursor = connect()

    query = (
        'CREATE TABLE IF NOT EXISTS users (username VARCHAR(255) NOT NULL, '
        'password varchar(255) NOT NULL,liked_coins TEXT[], PRIMARY KEY (username))')
    cursor.execute(query)
    conn.commit()

    close_connection(conn, cursor)


def signup(username, password):
    pass

def enter(username, password):
    ########## CONNECT ##########
    conn, cursor = connect()

    if check(username, password):
        close_connection(conn, cursor)
        return False
    else:
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        cursor.execute(query, (username, password))
        conn.commit()
        close_connection(conn, cursor)
        return True

        return True

def check(username, password):
    ########## CONNECT ##########
    conn, cursor = connect()

    query = 'SELECT * FROM users WHERE username = ? AND password = ?'
    cursor.execute(query, (username, password))

    # IF IT EXISTS
    if cursor.fetchone():
        conn.commit()
        close_connection(conn, cursor)
        # print("CHECK IS TRUE")
        return True

    # IF DOESNT EXIST
    else:
        conn.commit()
        close_connection(conn, cursor)
        # st.error('CHECK NOT WORK')
        return False



# --- main ---

conn, cursor = connect()


create_table() # called create table to create 'users'
enter('alek', '1234')
enter('bob', '1234')


close_connection(conn, cursor)
