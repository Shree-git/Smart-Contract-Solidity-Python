from solcx import compile_standard, install_solc
import os
import json
from web3 import Web3

install_solc("0.8.0")

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
    solc_version="0.8.0",
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
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 5777
my_address = "0xCF415fe60fdE8c8F0f7fFA0fd7Db710140Cb0A16"
private_key = "0x451cf0f2a2f97f1f72f1081a546b7225515f6034164c26b3c4b08724be23c5cb"

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)


# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)
# build a transaction
# sign a transaction
# send a transaction

transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)

print(transaction)
