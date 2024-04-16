import menuMaker
import User
import userMenu
import database
import sqlite3
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import hashlib  # Add this line for SHA256 hashing

import Transaction, TransactionPool


# Function to generate keys
def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    pbc_ser = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)

    return private_key, pbc_ser


# Function to handle user sign-up
def sign_up():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Hash the password using SHA256
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    private_key, public_key = generate_keys()
    private_key_str = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Connect to the SQLite database
    db_path = "../data/user_database.db"
    if not os.path.exists("../data"):
        os.makedirs("../data")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, private_key TEXT, public_key TEXT)''')

    # Check if username already exists
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    existing_user = c.fetchone()
    if existing_user:
        print("Username already exists. Please choose a different username.")
        conn.close()
        sign_up()
        return

    # Insert user data into the database
    c.execute("INSERT INTO users (username, password, private_key, public_key) VALUES (?, ?, ?, ?)",
              (username, password_hash, private_key_str, public_key))
    conn.commit()

    # Close database connection
    conn.close()

    print("Sign up successful.")
    userMenu.UserMenu(User.User(username,password_hash,private_key_str,public_key))


def login():
    # Get user input
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Hash the password using SHA256
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Retrieve user data from the database
    user_data = database.fetch_user_data(username, password_hash)
    if not user_data:
        print("Incorrect username or password.")
        return

    print("Login successful.")
    print(user_data)
    userMenu.UserMenu(User.User(user_data[1],user_data[2],user_data[3],user_data[4]))
    # Call the UserMenu function here if it's defined elsewhere


def explore_blockchain():
    input()
    print("Explore the blockchain function called.")


def exit_program():
    print("Exiting...")

from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives import serialization

def public_menu():
    options = ["Login", "Explore the blockchain", "Sign up", "Exit"]
    actions = [login, explore_blockchain, sign_up, exit_program]  # Define your action functions here

    index = menuMaker.select_menu_option(None, options)
    if index < len(actions):
        actions[index]()


if __name__ == "__main__":
    # public_menu()
    test_transaction_pool()