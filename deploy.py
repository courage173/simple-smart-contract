from solcx import compile_standard, get_installable_solc_versions, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

# install_solc('0.6.0')
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.12",
)

with open("compile_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get byte code
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/39ddd0af27c54b6bbcd77547f8f54b75"))
chain_id = 4
my_address = "0xB90e466B33b6476Db1b55A4749124e91736E002E"
private_key = os.getenv("PRIVATE_KEY")

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# build a transaction
# Sign a transaction
# Send a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"gasPrice": w3.eth.gas_price, "chainId": chain_id, "from": my_address, "nonce": nonce}
)

print("starting contract deploy")
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# send the signed transaction to the
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("finished deploying contract")
# working with a contract
# contract address
# contract abi
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

print("retrieving storage detail")
print(simple_storage.functions.retrieve().call())

# creating a transaction
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"gasPrice": w3.eth.gas_price, "chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)
print("updating deployment")
store_signed_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
store_tx_hash = w3.eth.send_raw_transaction(store_signed_txn.rawTransaction)
store_tx_hash_receipt = w3.eth.wait_for_transaction_receipt(store_tx_hash)
print("update done")

print(simple_storage.functions.retrieve().call())
# simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)












