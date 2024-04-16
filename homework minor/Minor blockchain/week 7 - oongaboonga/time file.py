import time
import hashlib

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce)).encode('utf-8'))
        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # Adjust difficulty to target desired mining time
        self.block_time_target = 15  # Target time for mining a block in seconds

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_last_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def mine_block(self, new_block):
        start_time = time.time()
        end_time = start_time + 20  # Set the timeout to 20 seconds
        while time.time() < end_time:
            new_block.hash = new_block.calculate_hash()
            if new_block.hash.startswith('0' * self.difficulty):
                time_taken = time.time() - start_time
                if 10 <= time_taken <= 20:
                    print("Block mined successfully in", time_taken, "seconds")
                    return
                elif time_taken < 10:
                    self.difficulty += 1  # Increase difficulty
                else:
                    self.difficulty -= 1  # Decrease difficulty
                    if self.difficulty < 0:
                        self.difficulty = 0
            new_block.nonce += 1

        print("Failed to mine block within 20 seconds.")

# Usage
blockchain = Blockchain()
block_to_mine = Block(1, time.time(), "Transaction Data", "")
blockchain.mine_block(block_to_mine)
blockchain.add_block(block_to_mine)

