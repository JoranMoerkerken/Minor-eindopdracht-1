import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import block
import Transaction
from block import Block

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

    def calculate_balance(self, public_key):
        balance = 0

        for block in self.chain:
            if self.validate_block(block):
                for tx in block.transactions:
                    if tx.type == 'reward' and tx.outputs[0].recipient == public_key:
                        balance += tx.outputs[0].amount

        return balance

    def validate_block(self, block):
        block_hash = block.calculate_hash()
        prefix = b'0' * self.difficulty

        return block_hash.startswith(prefix)

    def select_transactions(self, user_public_key, num_transactions):
        selected_txs = []

        for block in self.chain:
            if self.validate_block(block):  # <-- Change here
                for tx in block.transactions:
                    if len(selected_txs) >= num_transactions:
                        break

                    if tx.is_valid() and not self.would_cause_negative_balance(tx, user_public_key):
                        selected_txs.append(tx)

        return selected_txs

    def would_cause_negative_balance(self, transaction, public_key):
        balance = self.calculate_balance(public_key)
        for input in transaction.inputs:
            if input.sender == public_key:
                balance -= input.amount

        return balance < 0
