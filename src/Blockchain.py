import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import block
import Transaction
from block import Block
import TransactionPool

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 0  # You can adjust this value
        self.load_from_file()

    def add_block(self, block):
        self.chain.append(block)
        self.save_to_file()

    def mine_block(self, transactions):
        block = Block(transactions, self.chain[-1].hash if self.chain else None)
        block.mine_block(self.difficulty)
        self.add_block(block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def start_up(self, user):
        newBlocks = 0
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

            if user not in current_block.validated_By:
                current_block.validated_By.append(user)
                newBlocks += 1
        return True, newBlocks
    def load_from_file(self):
        if os.path.exists('../data/block.dat'):
            with open('../data/block.dat', 'rb') as file:
                while True:
                    try:
                        block_data = file.read()
                        if not block_data:
                            break
                        block = Block.deserialize(block_data)
                        self.chain.append(block)
                    except EOFError:
                        break

    def save_to_file(self):
        with open('../data/block.dat', 'ab') as file:
            file.write(self.chain[-1].serialize())

    def validate_block(self, block):
        block_hash = block.calculate_hash()
        prefix = b'0' * self.difficulty

        return block_hash.startswith(prefix)

    def select_transactions(self):
        selected_txs = []

        # Get transactions from the TransactionPool
        tx_pool = TransactionPool.TransactionPool()
        transactions_from_pool = tx_pool.get_transactions()

        # Iterate over a copy of the transactions to avoid modifying the original list
        for tx in transactions_from_pool.copy():
            if tx.verify():
                selected_txs.append(tx)
                tx_pool.remove_transaction(tx)

        return selected_txs

    def print_blockchain(self):
        for i, block in enumerate(self.chain):
            print("-------------------------")
            print(f"Block {i + 1}:")
            print(f"Timestamp: {block.timestamp}")
            print(f"Transactions: {block.transactions}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Nonce: {block.nonce}")
            print(f"Hash: {block.hash.hex()}")
            print(f"Amount of people who validated: {len(block.validated_By)}")
