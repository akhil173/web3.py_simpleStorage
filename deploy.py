from solcx import compile_standard
import json
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()  # Loads the environment variables from .env file

with open("./SimpleStorage.sol", "r") as file:
    simple_storage = file.read()
    # print(simple_storage)


# To Compile Solidity

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.10",
)

# with open("./compiled_code.json", "w") as file:
#    json.dump(compiled_sol, file)


# To get the bytecode from compiled_sol
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# To get the abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# To connect to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
# w3.isConnected()
# w3.eth.get_block#('latest')
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = os.getenv("PRIVATE_KEY")


# Create contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get nonce. Nonce = latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)

"""
To deploy contract:
1. Build a transaction
2. Sign the transaction
3. Send the transaction
"""

# 1. Building transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
# print(w3.eth.gas_price)

# print(transaction)

# 2. Signing the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key)


# 3. Send the signed transaction
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_reciept = w3.eth.wait_for_transaction_receipt(txn_hash)

contract_address = os.getenv("CONTRACT_ADDRESS")
# tx_reciept.contractAddress
simple_storage = w3.eth.contract(address=contract_address, abi=abi)

simple_storage.functions.retrieve().call()

nonce = w3.eth.getTransactionCount(my_address)

# building transaction
func_txn = simple_storage.functions.store(1034).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
# signing transaction
func_txn_sign = w3.eth.account.sign_transaction(func_txn, private_key)

# sending transaction
func_txn_send = w3.eth.send_raw_transaction(func_txn_sign.rawTransaction)
func_reciept = w3.eth.wait_for_transaction_receipt(func_txn_send)
