import menuMaker, GoodChain

def transfer_coin():
    print("transfer coin has been selected")
def explore_blockchain():
    print("Explore the blockchain has been selected")

def check_pool():
    print("Check the pool has been selected")

def cancel_transaction():
    print("Cancel a transaction has been selected")

def mine_block():
    print("Mine")

def logout():
    print("Logout")


def UserMenu(user):
    options = ["Transfer coins", "Explore the blockchain", "Check the pool", "Cancel a transaction", "Mine a block", "logout"]
    actions = [transfer_coin, explore_blockchain,check_pool ,cancel_transaction, mine_block,logout ]

    index = menuMaker.select_menu_option(f"welcome to Goodchain {user.username}!", options)
    if index < len(actions):
        actions[index]()
