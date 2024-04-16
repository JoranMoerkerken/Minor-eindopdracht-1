from BlockChain import CBlock
from Signature import generate_keys, sign, verify
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from Transaction import Tx

timing_variable = 20

class TxBlock (CBlock):
    
    # TODO 1: Initialize the block
    # Each block contains a list for the data and a hash value to previous block
    def __init__(self, previousBlock):
        super(TxBlock, self).__init__([], previousBlock)
    
    # TODO 2: Append the transaction to the data list
    def addTx(self, Tx_in):
        self.data.append(Tx_in)
    
    # TODO 3: Check the validity of each transaction in the data list 
    # and check the validity of other blocks in the chain to make the chain tamper-proof
    # Expected return value is true or false
    def is_valid(self):
        if not super(TxBlock, self).is_valid():
            return False
        for tx in self.data:
            if not tx.is_valid():
                return False
        return True
    
    def mine(self, leading_zero):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data), 'utf-8'))
        digest.update(bytes(str(self.previousHash), 'utf-8'))
        
        found = False
        nonce = 0
        while not found:
            h = digest.copy()
            h.update(bytes(str(nonce), 'utf-8'))
            hash = h.finalize()
            if hash[:leading_zero] == bytes('0'*leading_zero, 'utf-8'):
                if int(hash[leading_zero]) < timing_variable:
                    found = True
                    self.nonce = nonce
            nonce += 1
            del h
        self.blockHash = self.computeHash()
            