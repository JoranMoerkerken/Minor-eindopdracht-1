import os

import Transaction
import TransactionPool
import database
import Blockchain


def test_blockchain():
    # Create a Blockchain object
    blockchain = Blockchain.Blockchain()

    # Fetch all users
    users = database.fetch_all_users()

    if len(users) >= 2:
        user1 = users[0]
        user2 = users[1]

        # Create a TransactionPool object
        tx_pool = TransactionPool.TransactionPool()

        # Create transactions from user1 to user2 with a transaction fee
        for _ in range(3):
            tx = Transaction.Tx()
            tx.add_input(user1['public_key'], 10, 1)  # Adding a transaction fee of 1 unit
            tx.add_output(user2['public_key'], 10)
            tx.sign(user1['private_key'])
            tx_pool.add_transaction(tx)

        for _ in range(10):
            tx = Transaction.Tx()
            tx.add_input(user1['public_key'], 10, 10)  # Adding a transaction fee of 1 unit
            tx.add_output(user2['public_key'], 10)
            tx.sign(user1['private_key'])
            tx_pool.add_transaction(tx)

        test = blockchain.select_transactions()
        for tssx in test:
            print(tssx)
        tx_pool.print_transactions()
        return
        # Mine a block
        transactions = blockchain.select_transactions()
        tx_pool.load_from_file()
        blockchain.mine_block(transactions)

        # Check balances after mining
        confirmed_balance_user1, pending_positive_user1, pending_negative_user1 = blockchain.get_balance(
            user1['public_key'])
        confirmed_balance_user2, pending_positive_user2, pending_negative_user2 = blockchain.get_balance(
            user2['public_key'])

        print(f"Confirmed Balance for User1: {confirmed_balance_user1}")  # Expected output: Confirmed Balance for User1: 0.0
        print(f"Pending Positive Balance for User1: {pending_positive_user1}")  # Expected output: Pending Positive Balance for User1: 0.0
        print(f"Pending Negative Balance for User1: {pending_negative_user1}")  # Expected output: Pending Negative Balance for User1: -30.0

        print(f"Confirmed Balance for User2: {confirmed_balance_user2}")  # Expected output: Confirmed Balance for User2: 30.0
        print(f"Pending Positive Balance for User2: {pending_positive_user2}")  # Expected output: Pending Positive Balance for User2: 0.0
        print(f"Pending Negative Balance for User2: {pending_negative_user2}")  # Expected output: Pending Negative Balance for User2: 0.0

        # Create more transactions and mine another block
        for _ in range(3):
            tx = Transaction.Tx()
            tx.add_input(user2['public_key'], 5)
            tx.add_output(user1['public_key'], 5)
            tx.sign(user2['private_key'])
            tx_pool.add_transaction(tx)

        # Mine another block
        transactions = blockchain.select_transactions()
        tx_pool.load_from_file()
        blockchain.mine_block(transactions)

        # Check balances after mining again
        confirmed_balance_user1, pending_positive_user1, pending_negative_user1 = blockchain.get_balance(
            user1['public_key'])
        confirmed_balance_user2, pending_positive_user2, pending_negative_user2 = blockchain.get_balance(
            user2['public_key'])

        print(f"Confirmed Balance for User1: {confirmed_balance_user1}")  # Expected output: Confirmed Balance for User1: 15.0
        print(f"Pending Positive Balance for User1: {pending_positive_user1}")  # Expected output: Pending Positive Balance for User1: 0.0
        print(f"Pending Negative Balance for User1: {pending_negative_user1}")  # Expected output: Pending Negative Balance for User1: -20.0

        print(f"Confirmed Balance for User2: {confirmed_balance_user2}")  # Expected output: Confirmed Balance for User2: 25.0
        print(f"Pending Positive Balance for User2: {pending_positive_user2}")  # Expected output: Pending Positive Balance for User2: 0.0
        print(f"Pending Negative Balance for User2: {pending_negative_user2}")  # Expected output: Pending Negative Balance for User2: 0.0

        # Verify block validation
        if blockchain.is_valid():
            print("Blockchain is valid.")  # Expected output: Blockchain is valid.
        else:
            print("Blockchain is not valid.")  # Expected output: Blockchain is not valid.
    else:
        print("Not enough users to create transactions.")  # Expected output: Not enough users to create transactions.



if __name__ == "__main__":
    test_blockchain()

