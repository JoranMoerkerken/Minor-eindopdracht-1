from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

import Blockchain
import Transaction
import TransactionPool
import GoodChain
import database
import datetime
import menuMaker
import os
import sqlite3


def transfer_coin(balance, user):
    # Fetch all users' usernames
    users = database.fetch_all_users()
    allUserNames = [names['username'] for names in users if names['username'] != user.username]

    if not allUserNames:
        print("No other users found.")
        input("Press Enter to try agian...")
        UserMenu(user)
        return

    index = menuMaker.select_menu_option("Please choose the member you wish to transfer coin to", allUserNames)

    # Selected recipient
    selected_username = allUserNames[index]

    # Input the amount to transfer
    try:
        print(f"your current balance is: ", balance)
        amount = float(input("Enter the amount to transfer. example inputs are 5 or 5.2:\n"))
        fee = float(input("Enter the mining fee, the higher it is the more likely it is a miner will pick it up. example inputs are 5 or 5.2:\n"))
    except ValueError:
        print("Invalid input, your input must be a number. Please enter a valid number.")
        input("Press Enter to continue...")
        UserMenu(user)
        return
    if amount < 0 or fee < 0:
        print("Your input must be higher then zero. Please enter a valid number.")
        input("Press Enter to continue...")
        UserMenu(user)
        return
    elif amount + fee > balance:
        print("You are trying to send more then you currently have. Please enter a valid number.")
        input("Press Enter to continue...")
        UserMenu(user)
        return

    receiver = database.fetch_user_data(selected_username)

    # Create a new transaction
    tx = Transaction.Tx()
    tx.add_input(user.publicKey, amount, fee)
    tx.add_output(receiver[4], amount)
    tx.sign(user.privateKey)
    if not tx.verify():
        print("the transaction was invalid, please try again.")
        input("Press Enter to continue...")
        UserMenu(user)
        return


    # Add transaction to the transaction pool
    transaction_pool = TransactionPool.TransactionPool()
    # here i check if the transactions of the user are valid with the balance the user has and i check if all transactions are valid
    if transaction_pool.verify_pool_user(balance, user.publicKey) and transaction_pool.verify_pool():
        pass
    else:
        print(transaction_pool.verify_pool_user(balance, user.publicKey))
        print(transaction_pool.verify_pool())
        print("an invalid transaction was found in the transactionpool, please try again.")
        input("Press Enter to continue...")
        UserMenu(user)
        return

    transaction_pool.add_transaction(tx)
    print(f"Ur transaction is now pending. {amount} coins to {selected_username}.")
    input("Press Enter to continue...")
    UserMenu(user)

def change_password(user):
    print(f"Greetings {user.username}. Inside this function, you can change your password!")

    current_password = input("Enter your current password: ")
    os.system('cls' if os.name == 'nt' else 'clear')

    if not GoodChain.verify_password(user.publicKey, current_password, user.password):
        print("Incorrect password. Please try again.")
        input("Press Enter to continue...")
        UserMenu(user)
        return

    new_password = input("Enter your new password: ")
    confirm_new_password = input("Confirm your new password: ")

    # Check if the new passwords match
    if new_password != confirm_new_password:
        print("Passwords do not match.")
        input("Press Enter to continue...")
        UserMenu(user)
        return

    # Hash and save the new password
    new_password_hash = user.privateKey.sign(
        new_password.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    database.update_user_password(user.username, new_password_hash)
    print("Password changed successfully!")
    GoodChain.create_hashes()
    input("Press Enter to continue...")
    UserMenu(user)

def explore_blockchain(user):
    Blockchain.Blockchain().print_blockchain()
    UserMenu(user)

def explore_transactions(user):
    blockchain = Blockchain.Blockchain()
    transaction_pool = TransactionPool.TransactionPool()

    # Retrieve transactions related to the specified user from the blockchain
    user_transactions_blockchain = [tx for block in blockchain.chain for tx in block.transactions if tx.inputs and tx.inputs[0][0] == user.publicKey]

    # Retrieve transactions related to the specified user from the transaction pool
    user_transactions_pool = [tx for tx in transaction_pool.get_transactions() if tx.inputs and tx.inputs[0][0] == user.publicKey]

    # Display user's active transactions from blockchain
    transaction_list_blockchain = []
    for i, tx in enumerate(user_transactions_blockchain):
        sender = 'system' if not tx.inputs else database.get_username(tx.inputs[0][0])
        receiver = database.get_username(tx.outputs[0][0])
        amount = tx.outputs[0][1] if tx.outputs else 50
        transaction_str = f"{i + 1}. {amount} to {receiver} at {tx.time}"
        transaction_list_blockchain.append(transaction_str)

    # Display user's active transactions from transaction pool
    transaction_list_pool = []
    for i, tx in enumerate(user_transactions_pool):
        sender = 'system' if not tx.inputs else database.get_username(tx.inputs[0][0])
        receiver = database.get_username(tx.outputs[0][0])
        amount = tx.outputs[0][1] if tx.outputs else 50
        transaction_str = f"{i + 1}. {amount} to {receiver} at {tx.time}"
        transaction_list_pool.append(transaction_str)

    # Join transaction strings into separate lists
    transaction_output_blockchain = "\n".join(transaction_list_blockchain)
    transaction_output_pool = "\n".join(transaction_list_pool)

    print("Transactions in blockchain:")
    print(transaction_output_blockchain)

    print("\nTransactions still in pool:")
    print(transaction_output_pool)

    input("Press Enter to continue...")
    UserMenu(user)



def search_user(logged_in_user):
    print(f"Greetings {logged_in_user.username}. Inside this function, you can search for other members' public keys!\n"
          f"You can also search your own name and look up your own public and private keys after using your password!")

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

def mine_block(balance, user):
    blockchain = Blockchain.Blockchain()

    # Check if the blockchain has at least one block
    if blockchain.chain:
        last_block = blockchain.chain[-1]
        time_difference = (datetime.datetime.now() - last_block.timestamp).total_seconds()
        validatedAmount = len(last_block.validated_By)
    else:
        time_difference = 181
        validatedAmount = 3

    # Check the timestamp difference

    remaining_time = 180 - time_difference

    # Check if there are at least 5 verified transactions in the pool
    tx_pool = TransactionPool.TransactionPool()
    #here i check if the transactions of the user are valid with the balance the user has and i check if all transactions are valid
    tx_pool.verify_pool_user(balance, user.publicKey)
    tx_pool.verify_pool()
    transactions_count = len(tx_pool.get_transactions())

    if time_difference > 180:
        if transactions_count >= 5:
            if validatedAmount >= 3:
                transactions = blockchain.select_transactions()
                blockchain.mine_block(transactions, user)
            else:
                print(f"The last block should at least be validated three times. current count: {validatedAmount}")
                input("Press Enter to continue...")
                UserMenu(user)
        else:
            print(f"There should be at least 5 verified transactions in the pool. Current count: {transactions_count}.")
            input("Press Enter to continue...")
            UserMenu(user)
    else:
        print(f"There need to be three minutes before a new block can be added. Please try again in {int(remaining_time)} seconds.")
        input("Press Enter to continue...")
        UserMenu(user)


def logout(user):
    GoodChain.public_menu()

def newBlocks(user):
    blockchain = Blockchain.Blockchain()

    newBlocks = 0
    for i in range(len(blockchain.chain)):
        current_block = blockchain.chain[i]

        if i == 0:
            if current_block.hash != current_block.calculate_hash():
                if user.username not in current_block.invalidated_by:
                    current_block.invalidated_by.append(user.username)
                    if len(current_block.invalidated_by) >= 3 and len(current_block.validated_By) < 3:
                        # Remove the invalid block from the blockchain
                        blockchain.chain.pop(i)
                        # Add transactions from the invalid block back to the transaction pool
                        tx_pool = TransactionPool.TransactionPool()
                        for tx in current_block.transactions:
                            tx_pool.add_transaction(tx)
                return False, newBlocks
            elif user.username not in current_block.validated_By and user.username not in current_block.Creator:
                    current_block.validated_By.append(user.username)
                    newBlocks += 1
                    # Check if the block has been validated three times
                    if len(current_block.validated_By) == 3:
                        # Add minereward to the mining pool
                        tx_pool = TransactionPool.TransactionPool()
                        minereward_tx = Transaction.Tx()
                        creator = database.fetch_user_data(current_block.Creator[0])

                        minereward_tx.add_output(creator[4], 50)
                        minereward_tx.set_type('minereward')
                        minereward_tx.verify()
                        tx_pool.add_transaction(minereward_tx)
        else:
            previous_block = blockchain.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                if user.username not in current_block.invalidated_by:
                    current_block.invalidated_by.append(user.username)
                    if len(current_block.invalidated_by) >= 3 and len(current_block.validated_By) < 3:
                        # Remove the invalid block from the blockchain
                        blockchain.chain.pop(i)
                        # Add transactions from the invalid block back to the transaction pool
                        tx_pool = TransactionPool.TransactionPool()
                        for tx in current_block.transactions:
                            tx_pool.add_transaction(tx)

                return False, newBlocks

            if current_block.previous_hash != previous_block.hash:
                if user.username not in current_block.invalidated_by and user.username not in current_block.Creator:
                    current_block.invalidated_by.append(user.username)
                    if len(current_block.invalidated_by) >= 3 and len(current_block.validated_By) < 3:
                        blockchain.chain.pop(i)
                return False, newBlocks
            # Check if the user is already in the validated_By list
            if user.username not in current_block.validated_By and user.username not in current_block.Creator:
                current_block.validated_By.append(user.username)
                newBlocks += 1

                # Check if the block has been validated three times
                if len(current_block.validated_By) == 3:
                    # Add minereward to the mining pool
                    tx_pool = TransactionPool.TransactionPool()
                    minereward_tx = Transaction.Tx()
                    creator = database.fetch_user_data(current_block.Creator[0])

                    minereward_tx.add_output(creator[4], 50)
                    minereward_tx.set_type('minereward')
                    minereward_tx.verify()
                    tx_pool.add_transaction(minereward_tx)

    blockchain.save_to_file()
    return True, newBlocks


def UserMenu(user):

    options = ["Transfer coins", "Mine a block", "Explore the blockchain", "Explore your transaction history",
               "Explore the transactionpool", "Search users", "Cancel a pending transaction", "Change password",
               "Logout"]
    actions = [transfer_coin, mine_block, explore_blockchain, explore_transactions, check_pool, search_user,
               cancel_transaction, change_password, logout]

    is_valid, new_blocks_count = newBlocks(user)

    if not is_valid:
        print("Blockchain validation failed. A block has been removed")
        return False

    blockchain = Blockchain.Blockchain()
    confirmed_balance, pending_incoming_chain, pending_outgoing_chain = blockchain.get_balance(user.publicKey)

    pool = TransactionPool.TransactionPool()
    pending_incoming, pending_outgoing = pool.get_balance(user.publicKey)

    pending_balance_outgoing = pending_outgoing + pending_outgoing_chain
    pending_balance_incoming = pending_incoming_chain + pending_incoming
    actual_balance = confirmed_balance - pending_balance_outgoing

    pool = TransactionPool.TransactionPool()

    pool.verify_pool_user(actual_balance, user.publicKey)
    pool.verify_pool()

    # Get the current number of transactions in the blockchain chain
    current_transactions_count = sum(len(block.transactions) for block in blockchain.chain)

    #next assignment i need to make a notification class. this is awfull
    message = (
        f"Welcome to Goodchain {user.username}!\n"
        f"===============================================================================\n"
        f"Your confirmed balance = {confirmed_balance}\n"
        f"Your pending incoming balance = {pending_balance_incoming}\n"
        f"Your pending outgoing balance = {0 - pending_balance_outgoing}\n"
        f"Your spendable balance = {actual_balance}\n"
        f"===============================================================================\n"
        f"Amount of new blocks since your last login: {new_blocks_count}\n"
        f"Current amount of valid transactions in pool: {len(TransactionPool.TransactionPool().get_transactions())}\n"
        f"{'this means you are allowed to mine!\n' if len(TransactionPool.TransactionPool().get_transactions()) > 5 else ''}"
        f"===============================================================================\n"
        f"Current amount of blocks in the chain: {len(blockchain.chain)}\n"
        f"Current amount of transactions in the chain: {current_transactions_count}\n"
        f"===============================================================================\n"
    )

    index = menuMaker.select_menu_option(message, options)
    if index == 1 or index == 0:
        actions[index](actual_balance, user)
        return
    actions[index](user)

