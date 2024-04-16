from BlockChain import *
from Signature import *
from Transaction import *
from TxBlock import *
import pickle
import TransactionPool
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import database

def load_keys(private_key_str, public_key_str):
    backend = default_backend()

    # Load private key from string
    private_key = serialization.load_pem_private_key(
        private_key_str,
        password=None,
        backend=backend
    )

    # Load public key from string
    public_key = serialization.load_pem_public_key(
        public_key_str,
        backend=backend
    )

    return private_key, public_key

if __name__ == "__main__":
    user1 = database.fetch_user_data("test", "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08")
    user2 = database.fetch_user_data("bert", "32987c4b7a9fb90e729425fc63e7bb81ce2cb1f80140ddeddc968aa79a34e8f8")
    user3 = database.fetch_user_data("lol", "07123e1f482356c415f684407a3b8723e10b2cbbc0b8fcd6282c49d37c9c1abc")

    alex_prv, alex_pbc = load_keys(user1[3], user1[4])
    mike_prv, mike_pbc = load_keys(user2[3], user2[4])
    rose_prv, rose_pbc = load_keys(user3[3], user3[4])
    mara_prv, mara_pbc = generate_keys()

    Tx1 = Tx()
    Tx1.add_input(alex_pbc, 6)
    Tx1.add_output(mike_pbc, 4)
    Tx1.sign(alex_prv)

    Tx2 = Tx()
    Tx2.add_input(rose_pbc, 2.2)
    Tx2.add_output(mara_pbc, 2.1)
    Tx2.sign(rose_prv)

    Tx3 = Tx()
    Tx3.add_input(mara_pbc, 2.1)
    Tx3.add_input(rose_pbc, 1.4)
    Tx3.add_output(alex_pbc, 3.2)
    Tx3.sign(mara_prv)
    Tx3.sign(rose_prv)

    Tx4 = Tx()
    Tx4.add_input(rose_pbc, 1.3)
    Tx4.add_output(mara_pbc, 0.6)
    Tx4.add_output(mike_pbc, 0.7)
    Tx4.sign(rose_prv)

    Tx6 = Tx(type=REWARD)
    Tx6.add_output(mike_pbc, REWARD_VALUE)

    Tx5 = Tx()
    Tx5.add_input(rose_pbc, 3)
    Tx5.add_output(alex_pbc, 5)
    Tx5.sign(rose_prv)

    tx_pool = TransactionPool.TransactionPool()

    tx_pool.add_transaction(Tx1)
    tx_pool.add_transaction(Tx2)
    tx_pool.add_transaction(Tx3)
    tx_pool.add_transaction(Tx4)

    tx_pool.remove_transaction(Tx1)

    transactions = tx_pool.get_transactions()
    print("Transactions in the pool:")
    for tx in transactions:
        print(tx)

    tx_pool.clear_transactions()

    tx_pool.add_transaction(Tx1)
    tx_pool.add_transaction(Tx2)
    tx_pool.add_transaction(Tx3)
    tx_pool.add_transaction(Tx4)
    tx_pool.add_transaction(Tx6)

    alex_balance = tx_pool.get_balance(alex_pbc)
    print(f"Alex's balance: {alex_balance}")

    rose_balance = tx_pool.get_balance(rose_pbc)
    print(f"Rose's balance: {rose_balance}")

    mike_balance = tx_pool.get_balance(mike_pbc)
    print(f"Mike's balance: {mike_balance}")

    tx_pool.clear_transactions()

    tx_pool.add_transaction(Tx1)
    tx_pool.add_transaction(Tx2)
    tx_pool.add_transaction(Tx3)
    tx_pool.add_transaction(Tx4)
    tx_pool.add_transaction(Tx6)

    tx_pool.print_transactions()
