import os
import pickle
import Block
import TransactionPool

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 2  # You can adjust this value
        self.load_from_file()

    def add_block(self, block):
        self.chain.append(block)
        self.save_to_file()

    def mine_block(self, transactions):
        block = Block.Block(transactions, self.chain[-1].hash if self.chain else None)
        block.mine_block(self.difficulty)
        self.add_block(block)

    def is_valid(self):
        for i in range(len(self.chain)):
            current_block = self.chain[i]

            # Check if it's the genesis block
            if i == 0:
                if current_block.hash != current_block.calculate_hash():
                    return False
            else:
                previous_block = self.chain[i - 1]

                # Check hash
                if current_block.hash != current_block.calculate_hash():
                    return False

                # Check previous_hash
                if current_block.previous_hash != previous_block.hash:
                    return False

        return True

    def load_from_file(self):
        if os.path.exists('../data/block.dat'):
            with open('../data/block.dat', 'rb') as file:
                self.chain = pickle.load(file)

    def save_to_file(self):
        with open('../data/block.dat', 'wb') as file:
            pickle.dump(self.chain, file)

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


    def get_balance(self, public_key):
        """
        Get the balance of a user based on the transactions in the chain.

        Args:
        - public_key (str): Public key of the user.

        Returns:
        - float: Confirmed positive balance (received amount).
        - float: Pending positive balance (received but not verified amount).
        - float: Pending negative balance (sent but not verified amount).
        """
        confirmed_positive_balance = 0.0
        pending_positive_balance = 0.0
        pending_negative_balance = 0.0

        for block in self.chain:
            for tx in block.transactions:
                for address, amount in tx.inputs:
                    if address == public_key:
                        if len(block.validated_By) >= 3:
                            confirmed_positive_balance -= amount
                        else:
                            pending_negative_balance += amount
                for address, amount in tx.outputs:
                    if address == public_key:
                        if len(block.validated_By) >= 3:
                            confirmed_positive_balance += amount
                        else:
                            pending_positive_balance += amount

        return confirmed_positive_balance, pending_positive_balance, pending_negative_balance

    def print_blockchain(self):
        if len(self.chain) == 0:
            print("The Chain is empty")
            input("Press Enter to continue...")
        else:
            for i, block in enumerate(self.chain):
                print("╔═══════════════════════════════════════════╗")
                print(f"║ Block {i + 1}:")
                print(f"║ Timestamp: {block.timestamp}")
                print(f"║ Previous Hash: {block.previous_hash}")
                print(f"║ Nonce: {block.nonce}")
                print(f"║ Hash: {block.hash}")
                print(f"║ Amount of people who validated: {len(block.validated_By)}")
                print(f"║ Amount of people who marked this block invalid: {len(block.invalidated_by)}")
                print("╚═══════════════════════════════════════════╝")
                print("")
            input("Press Enter to continue...")
