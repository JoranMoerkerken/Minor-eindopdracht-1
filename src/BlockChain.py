from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

class CBlock:

    data = None
    previousHash = None
    previousBlock = None
    def __init__(self, data, previousBlock):
        self.data = data
        self.blockHash = None
        self.previousBlock = previousBlock
        self.nonce = 0
        if previousBlock != None:
            self.previousHash = previousBlock.computeHash()
    
    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data),'utf8'))
        digest.update(bytes(str(self.previousHash),'utf8'))
        return digest.finalize()

    def is_valid(self):
        if self.previousBlock == None:
            if self.blockHash == self.computeHash():
                return True
            else:
                return False
        else:
            # return self.previousBlock.computeHash() == self.previousHash
            current_block_validity = self.blockHash == self.computeHash()
            previous_block_validity = self.previousBlock.is_valid()
            return current_block_validity and previous_block_validity