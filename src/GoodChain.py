# Standard library imports
import os
import sqlite3

# Third-party imports
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.exceptions import InvalidSignature

# Local application imports
import menuMaker
import User
import userMenu
import database
import Transaction
import TransactionPool

def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    pbc_ser = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)

    return private_key, pbc_ser

def sign_password(private_key, password):
    signature = private_key.sign(
        password.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature

def verify_password(public_key, password, signature):
    try:
        public_key.verify(
            signature,
            password.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False

def sign_up():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    private_key, public_key = generate_keys()
    private_key_str = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Sign the password
    signature = sign_password(private_key, password)

    # Hash the password using the private key
    hashed_password = private_key.sign(
        password.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Connect to the SQLite database
    db_path = "../data/user_database.db"
    if not os.path.exists("../data"):
        os.makedirs("../data")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password BLOB, private_key TEXT, public_key TEXT)''')

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
              (username, hashed_password, private_key_str.decode(), public_key.decode()))
    conn.commit()

    # Close database connection
    conn.close()

    print("Sign up successful.")
    userMenu.UserMenu(User.User(username, hashed_password, private_key_str.decode(), public_key.decode()))

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Connect to the SQLite database
    db_path = "../data/user_database.db"
    if not os.path.exists("../data"):
        print("No users registered yet. Please sign up first.")
        return

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Fetch user data from the database
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user_data = c.fetchone()

    if not user_data:
        print("Incorrect username or password. Please try again.")
        conn.close()
        return

    # Extract data from the fetched row
    _, username, password_db, private_key, public_key = user_data

    private_key = serialization.load_pem_public_key(
        public_key.encode()
    )
    # Deserialize public key
    public_key = serialization.load_pem_public_key(
        public_key.encode()
    )
    # Verify the password using the public key
    if not verify_password(public_key, password, password_db):
        print("Incorrect username or password. Please try again.")
        conn.close()
        return

    print("Login successful.")
    userMenu.UserMenu(User.User(username, password_db, private_key, public_key))

    # Close database connection
    conn.close()

def explore_blockchain():
    input()
    print("Explore the blockchain function called.")

def exit_program():
    print("Exiting...")

def public_menu():
    options = ["Login", "Sign up", "Explore the blockchain", "Exit"]
    actions = [login, sign_up, explore_blockchain, exit_program]  # Define your action functions here

    index = menuMaker.select_menu_option(None, options)
    if index < len(actions):
        actions[index]()

if __name__ == "__main__":
    public_menu()
