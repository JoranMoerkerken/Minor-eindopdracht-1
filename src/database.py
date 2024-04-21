import sqlite3
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def fetch_user_data(username, db_path="../data/user_database.db"):
    """
    Retrieve user data from the database.
    """
    if not os.path.exists("../data"):
        return

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user_data = c.fetchone()

    conn.close()

    if user_data:
        user_data_list = list(user_data)

        # Deserialize private key
        private_key = serialization.load_pem_private_key(
            user_data[3].encode(), password=None, backend=default_backend()
        )
        user_data_list[3] = private_key

        return user_data_list
    else:
        return None

def fetch_all_users(db_path="../data/user_database.db"):
    """
    Retrieve all user data from the database.
    """
    if not os.path.exists("../data"):
        return []

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT * FROM users")
    users_data = c.fetchall()

    conn.close()

    users_list = []

    for user_data in users_data:
        user_dict = {
            "id": user_data[0],
            "username": user_data[1],
            "password": user_data[2],
            "public_key": user_data[4]
        }

        # Deserialize private key
        private_key = serialization.load_pem_private_key(
            user_data[3].encode(), password=None, backend=default_backend()
        )
        user_dict["private_key"] = private_key

        users_list.append(user_dict)

    return users_list

def get_username(public_key):
    db_path = "../data/user_database.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT username FROM users WHERE public_key=?", (public_key,))
    result = c.fetchone()
    conn.close()

    return result[0] if result else "Unknown"

def update_user_password(username, new_password_hash, db_path="../data/user_database.db"):
    """
    Update the user's password in the database.
    """
    if not os.path.exists("../data"):
        return False

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("UPDATE users SET password=? WHERE username=?", (new_password_hash, username))
    conn.commit()

    conn.close()

    return True





