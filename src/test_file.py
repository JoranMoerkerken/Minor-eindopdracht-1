import Transaction
import TransactionPool
import database

def test_transaction_pool():
    # Create a TransactionPool object
    tx_pool = TransactionPool.TransactionPool()

    users = database.fetch_all_users()

    # Create transactions using the first two users
    if len(users) >= 2:
        user1 = users[0]
        user2 = users[1]

        # Create a transaction from user1 to user2
        tx1 = Transaction.Tx()
        tx1.add_input(user1['public_key'], 50)  # Using public_key_user1 as the address
        tx1.add_output(user2['public_key'], 50)
        tx1.sign(user1['private_key'])  # Using private_key_user1 to sign

        # Add the transaction to the transaction pool
        tx_pool.add_transaction(tx1)

        # Print transactions in the pool
        tx_pool.print_transactions()

        # Print balance of users
        print(f"Balance of {user1['username']}: {tx_pool.get_balance(user1['public_key'])}")
        print(f"Balance of {user2['username']}: {tx_pool.get_balance(user2['public_key'])}")

    # Verify the transaction
    if tx1.verify():
        print("Transaction is valid.")
    else:
        print("Transaction is not valid.")
