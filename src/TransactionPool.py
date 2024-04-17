import pickle
import os
import sqlite3
import database


class TransactionPool:
    def __init__(self):
        self.transactions = []
        self.load_from_file()

    def add_transaction(self, tx):
        """
        Add a transaction to the transaction pool and save it to a .dat file.

        Args:
        - tx (Tx): Transaction object to be added.
        """
        self.transactions.append(tx)
        self.save_to_file()

    def remove_transaction(self, tx):
        """
        Remove a transaction from the transaction pool and save the updated pool to a .dat file.

        Args:
        - tx (Tx): Transaction object to be removed.
        """
        self.transactions.remove(tx)
        self.save_to_file()

    def get_transactions(self):
        """
        Get all transactions in the transaction pool.

        Returns:
        - list: List of transactions.
        """
        return self.transactions

    def clear_pool(self):
        """
        Clear all transactions from the transaction pool and remove the .dat file.
        """
        self.transactions = []
        self.remove_file()

    def save_to_file(self):
        """
        Save the current transaction pool to a .dat file.
        """
        # with open("../data/TransactionPool.dat", "wb") as file:
        #     pickle.dump(self.transactions, file)

    def load_from_file(self):
        """
        Load transactions from a .dat file into the transaction pool.
        If the file does not exist, it initializes an empty pool.
        """
        if os.path.exists("../data/TransactionPool.dat"):
            with open("../data/TransactionPool.dat", "rb") as file:
                self.transactions = pickle.load(file)

    def remove_file(self):
        """
        Remove the .dat file.
        """
        if os.path.exists("../data/TransactionPool.dat"):
            os.remove("../data/TransactionPool.dat")

    def print_transactions(self):
        if not self.transactions:
            print("No transactions in the pool.")
            return

        print("Transaction Pool:")
        print("----------------")
        for tx in self.transactions:
            sender = database.get_username(tx.inputs[0][0])
            receiver = database.get_username(tx.outputs[0][0])
            amount = tx.outputs[0][1] if tx.outputs else 50
            print(f"Type: {tx.type}, Sender: {sender}, Receiver: {receiver}, Amount: {amount}")


