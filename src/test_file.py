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

        # Create transactions from user1 to user2
        for _ in range(5):
            tx = Transaction.Tx()
            tx.add_input(user1['public_key'], 10)
            tx.add_output(user2['public_key'], 10)
            tx.sign(user1['private_key'])
            tx_pool.add_transaction(tx)

        # Mine a block
        transactions = blockchain.select_transactions(user1['public_key'], 4)
        blockchain.mine_block(transactions)

        # Check user balances
        balance_user1 = blockchain.calculate_balance(user1['public_key'])
        balance_user2 = blockchain.calculate_balance(user2['public_key'])

        print(f"Balance of {user1['username']}: {balance_user1}")
        print(f"Balance of {user2['username']}: {balance_user2}")

        # Verify block validation
        if blockchain.is_valid():
            print("Blockchain is valid.")
        else:
            print("Blockchain is not valid.")

        # Create more transactions and mine another block
        for _ in range(5):
            tx = Transaction.Tx()
            tx.add_input(user2['public_key'], 5)
            tx.add_output(user1['public_key'], 5)
            tx.sign(user2['private_key'])
            tx_pool.add_transaction(tx)

        # Mine another block
        transactions = blockchain.select_transactions(user2['public_key'], 4)
        blockchain.mine_block(transactions)

        # Check user balances again
        balance_user1 = blockchain.calculate_balance(user1['public_key'])
        balance_user2 = blockchain.calculate_balance(user2['public_key'])

        print(f"Updated balance of {user1['username']}: {balance_user1}")
        print(f"Updated balance of {user2['username']}: {balance_user2}")

        # Verify block validation again
        if blockchain.is_valid():
            print("Blockchain is valid.")
        else:
            print("Blockchain is not valid.")

    else:
        print("Not enough users to create transactions.")

if __name__ == "__main__":
    test_blockchain()
