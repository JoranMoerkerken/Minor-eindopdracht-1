import os
import pickle


class TransactionPool:
    def __init__(self, filename='../data/TransactionPool.dat'):
        self.filename = filename
        self.transactions = []
        self.load_transactions()

    def load_transactions(self):
        try:
            with open(self.filename, 'rb') as file:
                self.transactions = pickle.load(file)
        except FileNotFoundError:
            pass

    def save_transactions(self):
        directory = os.path.dirname(self.filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(self.filename, 'wb') as file:
            pickle.dump(self.transactions, file)

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
                sender_data = fetch_user_by_public_key(sender_key.decode())
                sender_username = sender_data[1] if sender_data else sender_key.decode()

                for receiver_key, amount_out in tx.outputs:
                    receiver_data = fetch_user_by_public_key(receiver_key.decode())
                    receiver_username = receiver_data[1] if receiver_data else receiver_key.decode()

                    print(f"{sender_username}\t{receiver_username}\t{amount_out}")

