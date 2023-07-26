from web3 import Web3

# Replace the following variables with your Besu node information
RPC_URL = "http://localhost:8545"  # Replace with the RPC URL of your Besu node
PRIVATE_KEY = "c87509a1c067bbde78beb793e6fa76530b6382a4c0241e5e4a9ec0a0f44dc0d3"   # Replace with the private key of the sender's account

# Function to send a transaction
def send_transaction(to_address, amount_wei):
    try:
        # Connect to the Besu node
        w3 = Web3(Web3.HTTPProvider(RPC_URL))

        # Validate the address
        if not w3.is_address(to_address):
            raise ValueError("Invalid recipient address")

        # Convert the private key to an Ethereum account
        account = w3.eth.account.from_key(PRIVATE_KEY)

        # Get the current nonce for the sender's account
        nonce = w3.eth.get_transaction_count(account.address)

        # Build the transaction
        transaction = {
            'to': to_address,
            'value': amount_wei,
            'gas': 2000000,  # Replace with an appropriate gas value
            'gasPrice': w3.to_wei('10', 'gwei'),  # Replace with an appropriate gas price
            'nonce': nonce,
            'chainId': 1337  # Replace with the chain ID of your Besu network
        }

        # Sign the transaction
        signed_transaction = account.sign_transaction(transaction)

        # Send the transaction
        tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        # Wait for the transaction to be mined
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        print("Transaction successful. Transaction hash:", tx_hash.hex())
        print("Receipt:", receipt)

    except Exception as e:
        print("Error:", e)

# Usage example
if __name__ == "__main__":
    recipient_address = "0xf17f52151EbEF6C7334FAD080c5704D77216b732"  # Replace with the recipient's address
    amount_wei = Web3.to_wei(1, 'ether')  # Replace 1 with the desired amount of Ether to send
    send_transaction(recipient_address, amount_wei)
