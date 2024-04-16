import sqlite3

# the goal of this file is to place all read functions inside it,
# as these have a high chance of being used again and aren't specific as a read/write function is.

def fetch_user_data(username, password_hash, db_path="../data/user_database.db"):
    """
    Retrieve user data from the database.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password_hash))
    user_data = c.fetchone()

    conn.close()

    return user_data

def fetch_user_by_public_key(public_key, db_path="../data/user_database.db"):
    """
    Retrieve user data from the database based on the public key.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE public_key=?", (public_key,))
    user_data = c.fetchone()

    conn.close()

    return user_data