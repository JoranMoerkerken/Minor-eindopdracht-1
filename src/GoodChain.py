# Standard library imports
import os
import sqlite3
import hashlib

# Third-party imports
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.exceptions import InvalidSignature

# Local application imports
import Blockchain
import Transaction
import TransactionPool
import User
import database
import menuMaker
import userMenu

def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    pbc_ser = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)

    return private_key, pbc_ser

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
    check_file_integrity()
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
    create_hashes()

    #add sign up reward to pool
    tx_pool = TransactionPool.TransactionPool()
    tx1 = Transaction.Tx()
    tx1.set_type('reward')
    tx1.add_output(public_key.decode(), 50)
    tx_pool.add_transaction(tx1)

    print("Sign up successful.")
    input("Press Enter to continue...")
    userMenu.UserMenu(User.User(username, hashed_password, private_key, public_key))

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    user_data = database.fetch_user_data(username)
    # Verify the password using the public key
    if not verify_password(user_data[4], password, user_data[2]):
        print("Incorrect username or password. Please try again.")
        input("Press Enter to continue...")
        public_menu()
        return

    print("Login successful.")
    input("Press Enter to continue...")
    userMenu.UserMenu(User.User(user_data[1], user_data[2], user_data[3], user_data[4]))

def explore_blockchain():
    Blockchain.Blockchain().print_blockchain()
    public_menu()

def check_pool():
    TransactionPool.TransactionPool().print_transactions()
    public_menu()

def exit_program():
    print("Exiting...")

def check_file_integrity():
    files_to_check = [
        "../data/block.dat",
        "../data/TransactionPool.dat",
        "../data/user_database.db"
    ]

    hash_file_path = "../data/integrity.hash"

    if os.path.exists(hash_file_path):
        with open(hash_file_path, "r") as hash_file:
            stored_hashes = {line.split(":")[0]: line.split(":")[1].strip() for line in hash_file.readlines()}
    else:
        stored_hashes = {}

    for file_path in files_to_check:
        if os.path.exists(file_path):
            # Calculate the hash of the file
            current_hash = hashlib.sha256()
            with open(file_path, "rb") as file:
                for chunk in iter(lambda: file.read(4096), b""):
                    current_hash.update(chunk)

            current_hash_hex = current_hash.hexdigest()

            # Compare the hashes
            if file_path in stored_hashes:
                if current_hash_hex == stored_hashes[file_path]:
                    pass
                else:
                    print(f"Invalid data found in {file_path}.")
                    input("Press Enter to continue...")
            else:
                print(f"No hash found for {file_path}.")
                input("Press Enter to continue...")
        else:
            pass

def create_hashes():
    files_to_hash = [
        "../data/block.dat",
        "../data/TransactionPool.dat",
        "../data/user_database.db"
    ]

    hash_file_path = "../data/integrity.hash"

    file_hashes = {}

    for file_path in files_to_hash:
        if os.path.exists(file_path):
            # Calculate the hash of the file
            current_hash = hashlib.sha256()
            with open(file_path, "rb") as file:
                for chunk in iter(lambda: file.read(4096), b""):
                    current_hash.update(chunk)

            current_hash_hex = current_hash.hexdigest()

            file_hashes[file_path] = current_hash_hex

    # Write the hashes to the hash file
    with open(hash_file_path, "w") as hash_file:
        for file_path, file_hash in file_hashes.items():
            hash_file.write(f"{file_path}:{file_hash}\n")


def public_menu():
    options = ["Login", "Sign up", "Explore the blockchain","Explore the transactionpool", "Exit"]
    actions = [login, sign_up, explore_blockchain,check_pool, exit_program]  # Define your action functions here

    index = menuMaker.select_menu_option(None, options)
    if index < len(actions):
        actions[index]()

if __name__ == "__main__":
    # test_file.test_transaction_pool()
    check_file_integrity()
    create_hashes()
    public_menu()

