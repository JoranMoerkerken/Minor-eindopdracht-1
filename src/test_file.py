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
        for _ in range(3):
            tx = Transaction.Tx()
            tx.add_input(user1['public_key'], 10)
            tx.add_output(user2['public_key'], 10)
            tx.sign(user1['private_key'])
            tx_pool.add_transaction(tx)

        # Mine a block
        tx_pool.print_transactions()
        transactions = blockchain.select_transactions()
        tx_pool.load_from_file()
        blockchain.mine_block(transactions)
        tx_pool.print_transactions()

        # Verify block validation
        if blockchain.is_valid():
            print("Blockchain is valid.")
        else:
            print("Blockchain is not valid.")

        # Create more transactions and mine another block
        for _ in range(3):
            tx = Transaction.Tx()
            tx.add_input(user2['public_key'], 5)
            tx.add_output(user1['public_key'], 5)
            tx.sign(user2['private_key'])
            tx_pool.add_transaction(tx)

        # Mine another block
        tx_pool.print_transactions()
        transactions = blockchain.select_transactions()
        tx_pool.load_from_file()
        blockchain.mine_block(transactions)
        tx_pool.print_transactions()

        # Verify block validation again
        if blockchain.is_valid():
            print("Blockchain is valid.")
        else:
            print("Blockchain is not valid.")


        blockchain.print_blockchain()

    else:
        print("Not enough users to create transactions.")

if __name__ == "__main__":
    test_blockchain()
