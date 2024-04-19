import menuMaker, GoodChain
import os
import sqlite3
import Transaction
import TransactionPool
import Blockchain
import database

def transfer_coin(user):
    # Fetch all users' usernames
    users = database.fetch_all_users()
    allUserNames = [names['username'] for names in users if names['username'] != user.username]

    if not allUserNames:
        print("No other users found.")
        UserMenu(user)
        return

    index = menuMaker.select_menu_option("Please choose the member you wish to transfer coin to", allUserNames)

    # Selected recipient
    selected_username = allUserNames[index]

    # Input the amount to transfer
    try:
        amount = float(input("Enter the amount to transfer. example inputs are 5 or 5.0:\n"))
    except ValueError:
        print("Invalid amount. Please enter a valid number.")
        input("Press Enter to try agian...")
        transfer_coin(user)
        return
    if amount < 0:
        print("Invalid amount. Please enter a valid number.")
        input("Press Enter to try agian...")
        transfer_coin(user)
        return

    #to lazy to match selected username to users
    receiver = database.fetch_user_data(selected_username)

    # Create a new transaction
    tx = Transaction.Tx()
    tx.add_input(user.publicKey, amount)
    tx.add_output(receiver[4], amount)
    tx.sign(user.privateKey)

    # Add transaction to the transaction pool
    transaction_pool = TransactionPool.TransactionPool()
    transaction_pool.add_transaction(tx)

    print(f"Ur transaction is now pending. {amount} coins to {selected_username}.")
    input("Press Enter to continue...")
    UserMenu(user)



def explore_blockchain(user):
    Blockchain.Blockchain().print_blockchain()
    UserMenu(user)

def explore_transactions(user):
    # Retrieve transactions related to the specified user from the transaction pool
    transaction_pool = TransactionPool.TransactionPool()
    user_transactions = [tx for tx in transaction_pool.get_transactions() if tx.inputs and tx.inputs[0][0] == user.publicKey]

    if not user_transactions:
        print("No transactions found.")
        UserMenu(user)
        return

    # Display user's active transactions
    transaction_list = []
    for i, tx in enumerate(user_transactions):
        sender = 'system' if not tx.inputs else database.get_username(tx.inputs[0][0])
        receiver = database.get_username(tx.outputs[0][0])
        amount = tx.outputs[0][1] if tx.outputs else 50
        transaction_str = f"{i + 1}. {amount} to {receiver}"
        transaction_list.append(transaction_str)

    # Join transaction strings into a single list
    transaction_output = "\n".join(transaction_list)
    print(transaction_output)
    input("Press Enter to continue...")
    UserMenu(user)


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
    input("Press Enter to continue...")
    UserMenu(user)

def check_pool(user):
    TransactionPool.TransactionPool().print_transactions()
    UserMenu(user)

def cancel_transaction(user):
    print(f"Greetings {user.username}. Inside this function, you can cancel your own transactions!")

    # Retrieve transactions related to the logged-in user from the transaction pool
    transaction_pool = TransactionPool.TransactionPool()
    user_transactions = [tx for tx in transaction_pool.get_transactions() if tx.inputs and tx.inputs[0][0] == user.publicKey]

    if not user_transactions:
        print("No transactions to cancel.")
        return

    transaction_list = []
    for i, tx in enumerate(user_transactions):
        sender = 'system' if not tx.inputs else database.get_username(tx.inputs[0][0])
        receiver = database.get_username(tx.outputs[0][0])
        amount = tx.outputs[0][1] if tx.outputs else 50
        transaction_str = f"{i + 1}. {amount} to {receiver}"
        transaction_list.append(transaction_str)

    header = (f"Greetings {user.username}. Inside this function, you can cancel your own transactions!"
              "Select a transaction to cancel:")
    # Select transaction to cancel
    index = menuMaker.select_menu_option("Select a transaction to cancel:", transaction_list)

    if index is None:
        print("Invalid selection.")
        return

    # Remove selected transaction from the transaction pool
    selected_tx = user_transactions[index]
    transaction_pool.remove_transaction(selected_tx)
    print("Transaction cancelled successfully!")
    UserMenu(user)

def mine_block(user):
    print("Mine")

def logout(user):
    print("Logout")

def newBlocks(user):
    blockchain = Blockchain.Blockchain()
    newBlocks = 0
    for i in range(1, len(blockchain.chain)):
        current_block = blockchain.chain[i]
        previous_block = blockchain.chain[i - 1]

        if current_block.hash != current_block.calculate_hash():
            return False, newBlocks

        if current_block.previous_hash != previous_block.hash:
            return False, newBlocks

        # Check if the user is already in the validated_By list
        if user not in current_block.validated_By:
            current_block.validated_By.append(user)
            newBlocks += 1

    return True, newBlocks


def UserMenu(user):

    options = ["Transfer coins", "Explore the blockchain","Explore your pending transactions", "Search users", "Explore the transactionpool", "Cancel a pending transaction", "Mine a block", "logout"]
    actions = [transfer_coin, explore_blockchain,explore_transactions, search_user, check_pool ,cancel_transaction, mine_block,logout ]

    is_valid, new_blocks_count = newBlocks(user)

    if not is_valid:
        print("Blockchain validation failed.")
        return False

    message = (
        f"Welcome to Goodchain {user.username}!\n\n"
        f"your confirmed balance =\n"
        f"your pending balance = \n"
        f"your actual balance = \n\n"
        f"Amount of new blocks since your last login! {new_blocks_count}\n\n"
        f"Current amount of transactions in pool is: {len(TransactionPool.TransactionPool().get_transactions())}\n"
        f"Current amount of blocks in the chain is: {len(Blockchain.Blockchain().chain)}\n"
    )

    index = menuMaker.select_menu_option(message, options)

    actions[index](user)

