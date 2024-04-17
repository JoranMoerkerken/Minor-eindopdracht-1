import sqlite3

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


# the goal of this file is to place all read functions inside it,
# as these have a high chance of being used again and aren't specific as a read/write function is.

def fetch_user_data(username, db_path="../data/user_database.db"):
    """
    Retrieve user data from the database.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user_data = c.fetchone()

    conn.close()

    return user_data


def get_username( public_key):
    db_path = "../data/user_database.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE public_key=?", (public_key,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else "Unknown"




