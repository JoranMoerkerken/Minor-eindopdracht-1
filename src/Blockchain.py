import os
import pickle
import Block
import TransactionPool
import GoodChain
import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 110  # You can adjust this value
        self.leading_zeroes = 3
        self.load_from_file()

    def add_block(self, block):
        self.chain.append(block)
        self.save_to_file()

    def mine_block(self, transactions, user):
        block = Block.Block(transactions, self.chain[-1].hash if self.chain else None, self.chain[-1].id + 1 if self.chain else 0, user)
        correctTime = False
        mined_difficulties = []
        while not correctTime:
            startTime = time.time()
            if self.difficulty > 255:
                self.leading_zeroes += 1
                self.difficulty = 0
            elif self.difficulty < 0:
                self.difficulty = 255
                self.leading_zeroes -= 1

            block.mine_block(self.leading_zeroes, self.difficulty)
            elapsed_time = time.time() - startTime

            print(f"Elapsed time: {elapsed_time}")

            if elapsed_time >= 10 and elapsed_time <= 20:
                correctTime = True
                print("Block has been mined in: ", elapsed_time)
                input("Press enter to confirm and mine the block")
            elif elapsed_time < 10:
                time_difference = 10 - elapsed_time
                self.difficulty += int(time_difference + 2)
                print(f"Hash was found too fast, increasing difficulty",
                      elapsed_time)
            elif elapsed_time > 20:
                time_difference = elapsed_time - 20
                self.difficulty -= int(time_difference + 1)
                print(f"Hash was found too slow, decreasing difficulty",
                      elapsed_time)

            key = (self.leading_zeroes, self.difficulty)

            # Check if this combination has been used before
            while key in mined_difficulties:
                self.difficulty += 1  # Increase difficulty by one if combination was already used

            mined_difficulties.append(key)
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
        GoodChain.check_file_integrity()
        if os.path.exists('../data/block.dat'):
            with open('../data/block.dat', 'rb') as file:
                self.chain = pickle.load(file)

    def save_to_file(self):
        GoodChain.check_file_integrity()
        with open('../data/block.dat', 'wb') as file:
            pickle.dump(self.chain, file)
        GoodChain.create_hashes()

    def validate_block(self, block):
        block_hash = block.calculate_hash()
        prefix = b'0' * self.difficulty

        return block_hash.startswith(prefix)

    def select_transactions(self):
        selected_txs = []

        # Get transactions from the TransactionPool
        tx_pool = TransactionPool.TransactionPool()
        transactions_from_pool = tx_pool.get_transactions()

        # Separate transactions into 'reward' and 'transaction' lists
        reward_txs = [tx for tx in transactions_from_pool if tx.verify() and tx.type == 'reward']

        # Sort 'transaction' transactions by transaction fee in descending order
        regular_txs = sorted(
            [tx for tx in transactions_from_pool if tx.verify() and tx.type == 'transaction'],
            key=lambda tx: tx.inputs[0][1] - (tx.outputs[0][1] if tx.outputs else 50),
            reverse=True
        )

        # Select reward transactions first
        selected_txs.extend(reward_txs[:min(9, len(reward_txs))])

        # If we still need more transactions, select regular transactions
        if len(selected_txs) < 9:
            selected_txs.extend(regular_txs[:min(9 - len(selected_txs), len(regular_txs))])

        return selected_txs[:9]  # Return at most 9 transactions

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
                print(f"║ Block {block.id}:")
                print(f"║ Timestamp: {block.timestamp}")
                print(f"║ Previous Hash: {block.previous_hash}")
                print(f"║ Nonce: {block.nonce}")
                print(f"║ Hash: {block.hash}")
                print(f"║ Amount of transactions: {len(block.transactions)}")
                print(f"║ Amount of people who validated: {len(block.validated_By)}")
                print(f"║ Amount of people who marked this block invalid: {len(block.invalidated_by)}")
                print(f"║ Created By: {block.Creator}")
                print("╚═══════════════════════════════════════════╝")
                print("")
            input("Press Enter to continue...")
