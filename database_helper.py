import sqlite3


def create_table():
    # query = "DROP TABLE IF EXISTS login"
    # cursor.execute(query)
    # conn.commit()
    query = (
        'CREATE TABLE IF NOT EXISTS users (username VARCHAR(255) NOT NULL, '
        'password varchar(255) NOT NULL, PRIMARY KEY (username))')
    cursor.execute(query)
    conn.commit()


def signup(username, password):
    cursor.execute()
    query = 'INSERT INTO users (name, username, password) VALUES (?, ?, ?)'
    cursor.execute(query,username.lower(), password)
    conn.commit()


def check(username, password):
    query = 'SELECT * FROM users WHERE username = ? AND password = ?'
    cursor.execute(query, (username, password))

    if cursor.fetchone():
        conn.commit()
        return True

    else:
        conn.commit()
        return False





def login(username,password):
    pass
    # if answer.lower() == "y":
    #     username = input("Username: ")
    #     password = input("Password: ")
    #     if check(username, password):
    #         print("Username correct!")
    #         print("Password correct!")
    #         print("Logging in...")
    #     else:
    #         print("Something wrong")


# --- main ---

conn = sqlite3.connect("pooptest123.db")
cursor = conn.cursor()

# create_table()

# Username = input("Create username: ")
# Password = input("Create password: ")

# enter(Username, Password)

# check(Username, Password)

# loginlol()

cursor.close()
conn.close()