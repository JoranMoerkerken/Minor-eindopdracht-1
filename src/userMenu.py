import menuMaker, GoodChain
import sqlite3
import os
import hashlib

def transfer_coin():
    print("transfer coin has been selected")
def explore_blockchain():
    print("Explore the blockchain has been selected")


import os
import sqlite3
import hashlib
from cryptography.hazmat.primitives import serialization


import os
import sqlite3
import hashlib
from cryptography.hazmat.primitives import serialization

def search_user(logged_in_user):
    print(f"Greetings {logged_in_user.username}. Inside this function, you can search for other members' public keys!\n"
          f"You can also search your own name and look up your own public and private keys!")

    search_username = input("Enter the username to search for: ")

    db_path = "../data/user_database.db"
    if not os.path.exists("../data"):
        print("User database does not exist.")
        return

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Search for the user based on username
    c.execute("SELECT * FROM users WHERE username=?", (search_username,))
    user = c.fetchone()

    if not user:
        print("User not found.")
        conn.close()
        return

    user_id, found_username, password_hash, private_key_str, public_key_pem = user

    # Deserialize public key
    public_key = serialization.load_pem_public_key(public_key_pem.encode())

    # If the found user is the logged-in user
    if found_username == logged_in_user.username:
        password = input("Please enter your password to view your private key: ")

        # Verify password
        if not GoodChain.verify_password(logged_in_user.publicKey, password, password_hash):
            print("Incorrect password.")
            conn.close()
            return

        print(f"Username: {found_username}")
        print(f"Public Key:\n {public_key_pem}")
        print(f"Private Key:\n {private_key_str}")

    else:
        print(f"Username: {found_username}")
        print(f"Public Key: \n{public_key_pem}")

    conn.close()



def check_pool():
    print("Check the pool has been selected")

def cancel_transaction():
    print("Cancel a transaction has been selected")

def mine_block():
    print("Mine")

def logout():
    print("Logout")


def UserMenu(user):
    options = ["Transfer coins", "Explore the blockchain","Search users", "Check the pool", "Cancel a transaction", "Mine a block", "logout"]
    actions = [transfer_coin, explore_blockchain,search_user, check_pool ,cancel_transaction, mine_block,logout ]

    index = menuMaker.select_menu_option(f"welcome to Goodchain {user.username}!", options)
    if index < len(actions):
        if index == 2:
            actions[index](user)
        else:
            actions[index]()
