#!/usr/bin/env python3
""" 
The goal of this exercise is to complete the TXBlock class. We want be able to correctly store and 
load a block on disk. You have already completed every required modules seperately in the previous tutorials.
In this exercise, you have to integrate all the previously created modules, and ensure
all components are properly working together.

In addition, we would also like to see details of a transaction. For this part, check the assignment
for Transaction.py file

Your task is to:
    * locate the TODOs in this file
    * complete the missing part from the code 
    * run the test of this exercise located in same folder.

To test run 'TxBlock_t.py' in your command line

Notes:
    * do not change class structure or method signature to not break unit tests
    * Check previous tutorials for more information on this topic
"""

from BlockChain import CBlock
from Signature import generate_keys, sign, verify
import hashlib
from Transaction import Tx
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class TxBlock (CBlock):

    # TODO 1: Initialize the block
    # Each block contains a list for the data and a hash value to previous block
    def __init__(self, previousBlock):
        super(TxBlock, self).__init__([], previousBlock)

    # TODO 2: Append the transaction to the data list
    def addTx(self, Tx_in):
        self.data.append(Tx_in)

    # TODO 3: Check the validity of each transaction in the data list
    # and check the validity of other blocks in the chain to make the cchain tamper-proof
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
        digest.update(bytes(str(self.data), 'utf8'))
        digest.update(bytes(str(self.previousHash), 'utf8'))

        found = False
        nonce = 0
        while not found:
            digest_temp = digest.copy()
            digest_temp.update(bytes(str(nonce), 'utf8'))
            hash = digest_temp.finalize()
            if hash[:leading_zero] == bytes('0' * leading_zero, 'utf8'):
                if int(hash(leading_zero)) < 128: #128 == timing variable
                    found = True
                    self.nonce = nonce
            nonce += 1
            del digest_temp

        self.blockHash = self.computeHash()
        return
