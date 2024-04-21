from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import pickle
import datetime
import hashlib
import time

class Block:
    def __init__(self, transactions, previous_hash, Id, user):
        self.id = Id
        self.timestamp = datetime.datetime.now()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
        self.validated_By = []
        self.invalidated_by = []
        self.Creator = []
        self.Creator.append(user.username)

    def calculate_hash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.timestamp), 'utf8'))
        digest.update(bytes(str(self.transactions), 'utf8'))
        digest.update(bytes(str(self.previous_hash), 'utf8'))
        digest.update(bytes(str(self.nonce), 'utf8'))
        return digest.finalize()

    def mine_block(self, leading_zeroes, difficulty):
        starttime = time.time()
        elapsedTime = 0
        elapsedNonse= 0
        while elapsedTime < 25:
            self.nonce += 1
            self.hash = self.calculate_hash()
            if elapsedTime > 10:
                elapsedNonse += 1
                if elapsedNonse % 4000 == 0:
                    elapsedNonse = 0
                    difficulty -= 10
                    if difficulty < 0:
                        difficulty = 255
                        leading_zeroes -= 1
            if difficulty == 0:
                if self.hash[:leading_zeroes] == bytes('0' * leading_zeroes, 'utf8'):
                    return
            else:
                if self.hash[:leading_zeroes] == bytes('0' * leading_zeroes, 'utf8') and int(self.hash[leading_zeroes]) > difficulty:
                    return
            elapsedTime = time.time() - starttime


    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(data):
        return pickle.loads(data)
