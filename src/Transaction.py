from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from datetime import datetime

class Tx:
    def __init__(self, type='transaction'):
        self.inputs = []
        self.outputs = []
        self.type = type
        self.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_input(self, from_address, amount, fee=0):
        """
        Add an input to the transaction.

        Args:
        - from_address (str): Public key of the sender.
        - amount (float): Amount to be sent.
        - fee (float): Transaction fee to be deducted from the sender's balance.
        """
        self.inputs.append((from_address, amount + fee))

    def set_type(self, type):
        if type == 'reward' or type == 'minereward':
            self.type = type
            return True
        return False

    def add_output(self, to_address, amount):
        """
        Add an output to the transaction.

        Args:
        - to_address (str): Public key of the receiver.
        - amount (float): Amount to be received.
        """
        self.outputs.append((to_address, amount))

    def sign(self, private_key):
        """
        Sign the transaction with a private key.

        Args:
        - private_key (str): Private key used for signing.
        """
        message = self.__gather_message()
        signature = private_key.sign(
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        self.signature = signature

    def verify(self):
        """
        Verify the signature of the transaction.

        Returns:
        - bool: True if the signature is valid, False otherwise.
        """
        if self.type == 'reward' or self.type == 'minereward':
            return True
        message = self.__gather_message()
        public_key = serialization.load_pem_public_key(
            self.inputs[0][0].encode()
        )
        try:
            public_key.verify(
                self.signature,
                message.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except:
            return False

    def __gather_message(self):
        """
        Gather message to be signed or verified.

        Returns:
        - str: Concatenated string of inputs and outputs.
        """
        message = ""
        for address, amount in self.inputs:
            if isinstance(address, bytes):
                address_str = address.decode('utf-8')
            else:
                address_str = address
            message += address_str + str(amount)
        for address, amount in self.outputs:
            if isinstance(address, bytes):
                address_str = address.decode('utf-8')
            else:
                address_str = address
            message += address_str + str(amount)
        return message

    def __repr__(self):
        repr_str = f"Type: {self.type}, Time: {self.time}\n"

        repr_str += " INPUTS:\n"
        for addr, amount in self.inputs:
            fee = amount - sum(output_amount for _, output_amount in self.outputs)
            repr_str += f"  {amount} from {addr} (Fee: {fee})\n"

        repr_str += "OUTPUTS:\n"
        for addr, amount in self.outputs:
            repr_str += f"  {amount} to {addr}\n"

        return repr_str