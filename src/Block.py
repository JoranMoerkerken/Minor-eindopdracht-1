from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import pickle
import datetime
import hashlib
import time

class Block:
    def __init__(self, transactions, previous_hash):
        self.timestamp = datetime.datetime.now()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
        self.validated_By = []
        self.invalidated_by = []

    def calculate_hash(self):
        block_string = f"{self.timestamp}{self.transactions}{self.previous_hash}{self.nonce}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, leading_zeroes, difficulty):
        self.nonce = 0
        self.hash = self.calculate_hash()
        startTime = time.time()
        elapsed_time= 0
        inRange = 10 - int(difficulty % 10)
        print(leading_zeroes, " and in range is ", inRange)
        if inRange == 10:
            while elapsed_time < 30 and not self.hash.startswith('0' * leading_zeroes):
                self.nonce += 1
                self.hash = self.calculate_hash()
                elapsed_time = time.time() - startTime
        else:
            while elapsed_time < 30 and not self.hash.startswith('0' * leading_zeroes) or not (self.hash[leading_zeroes].isdigit() and int(self.hash[leading_zeroes]) <= inRange):
                self.nonce += 1
                self.hash = self.calculate_hash()
                elapsed_time = time.time() - startTime
        print(f"Block mined: {self.hash}, with difficulty: {difficulty}")

    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(data):
        return pickle.loads(data)
