import os
import pickle
from cryptography.hazmat.primitives import serialization
import database
import base64
import Transaction



class TransactionPool:
    def __init__(self, filename='../data/TransactionPool.dat'):
        self.filename = filename
        self.transactions = []
        self.load_transactions()

    def load_transactions(self):
        try:
            with open(self.filename, 'rb') as file:
                transactions_data = pickle.load(file)
                self.transactions = self.deserialize_transactions(transactions_data)
        except FileNotFoundError:
            pass

    def save_transactions(self):
        directory = os.path.dirname(self.filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

        transactions_data = self.serialize_transactions(self.transactions)
        with open(self.filename, 'wb') as file:
            pickle.dump(transactions_data, file)

    from cryptography.hazmat.primitives.asymmetric import rsa, dsa, ec

    def serialize_transactions(self, transactions):
        serialized_transactions = []
        for tx in transactions:
            serialized_tx = {
                'inputs': [(base64.b64encode(addr.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )).decode(), amount) if isinstance(addr, (
                self.rsa.RSAPublicKey, self.dsa.DSAPublicKey, self.ec.EllipticCurvePublicKey)) else (
                base64.b64encode(addr).decode(), amount) for addr, amount in tx.inputs],
                'outputs': [(base64.b64encode(addr.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )).decode(), amount) if isinstance(addr, (
                self.rsa.RSAPublicKey, self.dsa.DSAPublicKey, self.ec.EllipticCurvePublicKey)) else (
                base64.b64encode(addr).decode(), amount) for addr, amount in tx.outputs],
                'sigs': [base64.b64encode(sig).decode() for sig in tx.sigs],
                'reqd': [base64.b64encode(addr.encode()).decode() for addr in tx.reqd],
                'type': tx.type
            }
            serialized_transactions.append(serialized_tx)
        return serialized_transactions

    def deserialize_transactions(self, serialized_transactions):
        deserialized_transactions = []
        for serialized_tx in serialized_transactions:
            tx = Transaction.Tx(serialized_tx['type'])
            tx.inputs = [(base64.b64decode(addr).decode(), amount) for addr, amount in serialized_tx['inputs']]
            tx.outputs = [(base64.b64decode(addr).decode(), amount) for addr, amount in serialized_tx['outputs']]
            tx.sigs = [base64.b64decode(sig.encode()) for sig in serialized_tx['sigs']]
            tx.reqd = [base64.b64decode(addr).decode() for addr in serialized_tx['reqd']]
            deserialized_transactions.append(tx)
        return deserialized_transactions

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.save_transactions()

    def remove_transaction(self, transaction):
        if transaction in self.transactions:
            self.transactions.remove(transaction)
            self.save_transactions()

    def get_transactions(self):
        return self.transactions

    def clear_transactions(self):
        self.transactions = []
        self.save_transactions()

    def get_balance(self, public_key):
        balance = 0
        for tx in self.transactions:
            for addr, amount in tx.inputs:
                if addr == public_key:
                    balance -= amount
            for addr, amount in tx.outputs:
                if addr == public_key:
                    balance += amount
        return balance

    def print_transactions(self):
        print("Transaction Pool:")
        print("Sender\t\tReceiver\tAmount")
        print("=" * 40)
        for tx in self.transactions:
            for sender_key, amount in tx.inputs:
                if isinstance(sender_key, (self.rsa.RSAPublicKey, self.dsa.DSAPublicKey, self.ec.EllipticCurvePublicKey)):
                    sender_key_str = sender_key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo
                    ).decode()
                else:
                    sender_key_str = sender_key.decode()

                sender_data = database.fetch_user_by_public_key(sender_key_str)
                print(sender_key_str)[1]
                sender_username = sender_data[1] if sender_data else sender_key_str

                for receiver_key, amount_out in tx.outputs:
                    if isinstance(receiver_key, (self.rsa.RSAPublicKey, self.dsa.DSAPublicKey, self.ec.EllipticCurvePublicKey)):
                        receiver_key_str = receiver_key.public_bytes(
                            encoding=serialization.Encoding.PEM,
                            format=serialization.PublicFormat.SubjectPublicKeyInfo
                        ).decode()
                    else:
                        receiver_key_str = receiver_key.decode()

                    receiver_data = database.fetch_user_by_public_key(receiver_key_str)
                    receiver_username = receiver_data[1] if receiver_data else receiver_key_str

                    print(f"{sender_username}\t{receiver_username}\t{amount_out}")


