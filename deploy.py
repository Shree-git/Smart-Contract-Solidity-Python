from solcx import compile_standard, install_solc
import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

install_solc("0.6.0")

with open("./SimpleStorage.sol", "r") as file:
    simpleStorageFile = file.read()


# Compile Our Solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simpleStorageFile}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganashe
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x8B90F5128b3E0c4e060c57A018381b0443a41ab9"
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)


# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# build a transaction
# sign a transaction
# send a transaction

transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send the signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# Wait for blcok confirmation
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Working with the contract, you need
# Contract Address
# Contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> Simulate making the call and getting a return value
# Transat -> Actually make a state change

# Initial value of fav number
print(simple_storage.functions.retrieve().call())
