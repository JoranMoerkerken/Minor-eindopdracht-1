from BlockChain import *
from Signature import *
from Transaction import *
from TxBlock import *
import pickle
import TransactionPool
from cryptography.hazmat.primitives import serialization

Leading_Zero = 2

if __name__ == "__main__":
    alex_prv, alex_pbc = generate_keys()
    mike_prv, mike_pbc = generate_keys()
    rose_prv, rose_pbc = generate_keys()
    mara_prv, mara_pbc = generate_keys()

    print(alex_prv)
    # create few valid transactions and valid blocks
    Tx1 = Tx()
    Tx1.add_input(alex_pbc, 6)
    Tx1.add_output(mike_pbc, 4)
    Tx1.sign(alex_prv)

    Tx2 = Tx()
    Tx2.add_input(rose_pbc, 2.2)
    Tx2.add_output(mara_pbc, 2.1)
    Tx2.sign(rose_prv)

    genesis_block = TxBlock(None)
    genesis_block.addTx(Tx1)
    genesis_block.addTx(Tx2)
    genesis_block.mine(Leading_Zero)

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
    
    Tx6 = Tx(type = REWARD)
    Tx6.add_output(mike_pbc, REWARD_VALUE)
    
    B1 = TxBlock(genesis_block)
    B1.addTx(Tx3)
    B1.addTx(Tx4)
    B1.addTx(Tx6)
    B1.mine(Leading_Zero)

    fh = open('blockchain.dat', 'wb')
    pickle.dump(B1, fh)
    fh.close()

    fh = open('blockchain.dat', 'rb')
    B1_prime = pickle.load(fh)
    fh.close()

    for b in [genesis_block, B1, B1_prime]:
        if b.is_valid():
            print("Success! Block is valid")
        else:
            print("Error! Block is invalid")
            
    Tx5 = Tx()
    Tx5.add_input(rose_pbc, 3)
    Tx5.add_output(alex_pbc, 5)
    Tx5.sign(rose_prv)

    B2 = TxBlock(B1)
    B2.addTx(Tx5)
    
    B1.addTx(Tx1)
    
    for b in [B2, B1]:
        if b.is_valid():
            print("Error! Block is valid")
        else:
            print("Success! Block is invalid")

    if __name__ == "__main__":
        # ... (your existing code)

        # Create a TransactionPool instance
        tx_pool = TransactionPool.TransactionPool()

        # Add transactions to the pool
        tx_pool.add_transaction(Tx1)
        tx_pool.add_transaction(Tx2)
        tx_pool.add_transaction(Tx3)
        tx_pool.add_transaction(Tx4)

        # Remove a transaction from the pool
        tx_pool.remove_transaction(Tx1)

        # Get the transactions from the pool
        transactions = tx_pool.get_transactions()
        print("Transactions in the pool:")
        for tx in transactions:
            print(tx)

        # Clear the transaction pool
        tx_pool.clear_transactions()

        tx_pool.add_transaction(Tx1)
        tx_pool.add_transaction(Tx2)
        tx_pool.add_transaction(Tx3)
        tx_pool.add_transaction(Tx4)
        tx_pool.add_transaction(Tx6)

        # Get the balance of a person using their public key
        alex_balance = tx_pool.get_balance(alex_pbc)
        print(f"Alex's balance: {alex_balance}")

        rose_balance = tx_pool.get_balance(rose_pbc)
        print(f"Rose's balance: {rose_balance}")

        mike_balance = tx_pool.get_balance(mike_pbc)
        print(f"Mike's balance: {mike_balance}")

        # Clear the transaction pool
        tx_pool.clear_transactions()

        # Add transactions to the pool
        tx_pool.add_transaction(Tx1)
        tx_pool.add_transaction(Tx2)
        tx_pool.add_transaction(Tx3)
        tx_pool.add_transaction(Tx4)
        tx_pool.add_transaction(Tx6)

        # Print the transactions in the pool
        tx_pool.print_transactions()

    