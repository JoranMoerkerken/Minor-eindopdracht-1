from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import pickle
import datetime
import hashlib

class Block:
    def __init__(self, transactions, previous_hash=None):
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

    def mine_block(self, difficulty):
        while not self.hash.startswith('0' * difficulty):
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(data):
        return pickle.loads(data)
