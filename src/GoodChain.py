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
import test_file

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

def verify_password(public_key_pem, password, signature):
    # Load the PEM-formatted public key string to an RSAPublicKey object
    public_key = serialization.load_pem_public_key(
        public_key_pem.encode(),
    )

    try:
        # Verify the signature
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

    #add sign up reward to pool
    tx_pool = TransactionPool.TransactionPool()
    tx1 = Transaction.Tx()
    tx1.set_type('reward')
    tx1.add_output(public_key.decode(), 50)
    tx_pool.add_transaction(tx1)
    tx_pool.print_transactions()

    print("Sign up successful.")
    # userMenu.UserMenu(User.User(username, hashed_password, private_key, public_key))

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    user_data = database.fetch_user_data(username)
    # Verify the password using the public key
    if not verify_password(user_data[4], password, user_data[2]):
        print("Incorrect username or password. Please try again.")
        return

    print("Login successful.")
    userMenu.UserMenu(User.User(user_data[1], user_data[2], user_data[3], user_data[4]))


def explore_blockchain():
    input()
    print("Explore the blockchain function called.")

def exit_program():
    print("Exiting...")

def onStartUp():
    print("Starting up...")
    #alle files hashen en checken of het overeenkomt met wat er in de files staat met behulp van hashing
def public_menu():
    options = ["Login", "Sign up", "Explore the blockchain", "Exit"]
    actions = [login, sign_up, explore_blockchain, exit_program]  # Define your action functions here

    index = menuMaker.select_menu_option(None, options)
    if index < len(actions):
        actions[index]()

if __name__ == "__main__":
    # test_file.test_transaction_pool()
    public_menu()

# een user moet info krijgen over transactions die door zijn gegaan of transactions die zijn afgekeurd
# aantal blokken in de blockchain en aantal transactions in de pool
# aangeven of een transactie gelukt is
# een blok word afgekeurd als hij eerder 3 invalid heeft dan 3 valid
