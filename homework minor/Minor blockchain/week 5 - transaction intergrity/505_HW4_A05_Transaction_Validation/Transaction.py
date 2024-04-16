from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from Signature import *

class Tx:
    inputs = None
    outputs = None
    sigs = None
    reqd = None

    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.reqd = []

    def add_input(self, from_addr, amount):
        self.inputs.append((from_addr, amount))

    def add_output(self, to_addr, amount):
        self.outputs.append((to_addr, amount))

    def add_reqd(self, addr):
        self.reqd.append(addr)

    def sign(self, private):
        tx_data = self._gather_tx_data()
        signature = sign(tx_data, private)
        self.sigs.append(signature)

    def _gather_tx_data(self):
        return [self.inputs, self.outputs, self.reqd]

    def is_valid(self):
        total_in = 0
        total_out = 0
        message = self._gather_tx_data()

        # Check each input
        for addr, amount in self.inputs:
            found = False
            # Verify each signature against the input address
            for s in self.sigs:
                if verify(message, s, addr):
                    found = True
                    break  # Break the loop once a valid signature is found for the current input
            if not found:
                return False
            if amount < 0:
                return False
            total_in += amount

        # Check each output
        for addr, amount in self.outputs:
            if amount < 0:
                return False
            total_out += amount

        # Ensure outputs do not exceed inputs
        if total_out > total_in:
            return False

        # Additional check for transactions requiring an arbiter signature
        for arbiter_addr in self.reqd:
            arbiter_signed = False
            for s in self.sigs:
                if verify(message, s, arbiter_addr):
                    arbiter_signed = True
                    break
            if not arbiter_signed:
                return False

        return True