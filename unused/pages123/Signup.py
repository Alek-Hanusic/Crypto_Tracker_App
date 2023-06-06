import streamlit as st
import sqlite3
def signup():
    if st.session_state.is_logged_in == True:
        st.success('You are alreadt logged in')
    else:

        import re
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        st.write('Please enter your details below')

        # NAME CHECK
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
        #
        # # EMAIL CHECK
        # email = st.text_input('Email', key='email')
        # if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        #     st.warning('Email address is invalid')
        #     email_valid = False
        # else:
        #     st.success('Email address is valid')
        #     email_valid = True

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
            if name_valid and username_valid and password_valid and confirm_password_valid:
                cursor.execute('SELECT username FROM users WHERE username=?', (username.lower(),))

                cursor.execute('SELECT username FROM users WHERE username = ?', (username.lower(),))
                existing_username = cursor.fetchone()

                if existing_username is None:
                    cursor.execute('INSERT INTO users (name, username, password) VALUES (?, ?, ?)',
                                   (name, username.lower(), password))
                    st.success('Welcome {}'.format(username))
                    return True
                else:
                    st.warning('Username already exists')
                    return False

                conn.commit()
                conn.close()
                return True
                # clear_inputs()
            else:
                st.warning('Fix the above errors to sign up')
                return False
