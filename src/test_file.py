from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import sqlite3
import TransactionPool
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

        private_key_user1_data = user1[3].encode('utf-8')  # Encoding string to bytes
        private_key_user1 = serialization.load_pem_private_key(
            private_key_user1_data, password=None
        )

        public_key_user1_data = user1[4].encode('utf-8')  # Encoding string to bytes
        public_key_user1 = serialization.load_pem_public_key(
            public_key_user1_data
        )

        # Deserialize private and public keys for user2
        private_key_user2_data = user2[3].encode('utf-8')  # Encoding string to bytes
        private_key_user2 = serialization.load_pem_private_key(
            private_key_user2_data, password=None
        )

        public_key_user2_data = user2[4].encode('utf-8')  # Encoding string to bytes
        public_key_user2 = serialization.load_pem_public_key(
            public_key_user2_data
        )

        # Create a transaction from user1 to user2
        tx1 = Transaction.Tx()
        tx1.add_input(public_key_user1, 50)  # Using public_key_user1 as the address
        tx1.add_output(public_key_user2, 50)
        tx1.sign(private_key_user1)  # Using private_key_user1 to sign

        # Add the transaction to the transaction pool
        tx_pool.add_transaction(tx1)

        # Print transactions in the pool
        tx_pool.print_transactions()
