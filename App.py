import streamlit as st
import sqlite3



def login():
    import streamlit as st
    import sqlite3
    import streamlit_authenticator as authenticator

    if st.session_state.is_logged_in == True:
        st.success('You are already logged in')
    else:
        conn = sqlite3.connect('database/data.db')
        cursor = conn.cursor()

        st.write('Please enter your login details below')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        if st.button('Login'):
            conn = sqlite3.connect('database/data.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            if cursor.fetchone() is None:
                st.warning('Incorrect Username/Password')

            else:
                conn.close()
                st.success('Logged In as {}'.format(username))
                st.session_state.is_logged_in = True



# name, authentication_status, username = authenticator.login('Login', 'main')
# if authentication_status:
#     authenticator.logout('Logout', 'main')
#     st.write(f'Welcome *{name}*')
#     st.title('Some content')
# elif authentication_status == False:
#     st.error('Username/password is incorrect')
# elif authentication_status == None:
#     st.warning('P
#################################################

#################################################
# SIGNUP
def signup():
    import streamlit as st
    import sqlite3
    if st.session_state.is_logged_in == True:
        st.success('You are alreadt logged in')
    else:

        import re
        conn = sqlite3.connect('database/data.db')
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

#################################################
# MAIN WINDOW
#################################################

def app():
    # headerSection = st.container()
    # mainSection = st.container()
    # LeftNav = st.sidebar()


    # page setup has to be done before connection to the database??????
    # # with headerSection:
    #     st.title('Alek\'s Price Tracker')
    #
    # with LeftNav:
    #     st.button('Home')

    conn = sqlite3.connect('database/data.db')
    cursor = conn.cursor()

    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users (name TEXT, username VARCHAR(255) NOT NULL, '
        'password varchar(255) NOT NULL, PRIMARY KEY (username))')
    conn.close()

    choice = st.selectbox('Sign Up or Login', ['Sign Up', 'Login'])
    if choice == 'Home':
        st.subheader('Home')
        st.write('Please Sign Up or Login to continue')

    elif choice == 'Login':
        st.subheader('Login')
        if login():
            main_window()
    elif choice == 'Sign Up':
        st.subheader('Sign Up')
        if signup():
            main_window()



    st.image('Images/Hotpot.png', width=500)
def main_window():
    st.title('Main Window')
    # Display the main content of your application here




# def clear_inputs():
#     st.session_state.name = ""
#     st.session_state.user = ""
#     st.session_state.email = ""
#     st.session_state.passw = ""
#     st.session_state.con_pass = ""


def home():
    pass


if __name__ == '__main__':
    # st.set_page_config(page_title='Alek\'s Price Tracker', page_icon='Images/Hotpot.png', layout='wide')
    app()
    # if login():
    #     main()


#################################################
# LOGIN
