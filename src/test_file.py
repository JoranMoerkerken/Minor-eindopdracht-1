from cryptography.hazmat.primitives import serialization

import TransactionPool
import sqlite3
import Transaction

def test_transaction_pool():
    # Create a TransactionPool object
    tx_pool = TransactionPool.TransactionPool()

    # Retrieve user data from the database
    db_path = "../data/user_database.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()

    # Create transactions using the first two users
    if len(users) >= 2:
        user1 = users[0]
        user2 = users[1]

        # Deserialize private and public keys
        private_key = serialization.load_pem_private_key(
            user1[3], password=None
        )
        public_key = serialization.load_pem_public_key(
            user2[4]
        )

        # Create a transaction from user1 to user2
        tx1 = Transaction.Tx()
        tx1.add_input(user1[4], 50)  # Using public_key as the address
        tx1.add_output(user2[4], 50)
        tx1.sign(private_key)  # Using private_key to sign

        # Add the transaction to the transaction pool
        tx_pool.add_transaction(tx1)

        # Print transactions in the pool
        tx_pool.print_transactions()
