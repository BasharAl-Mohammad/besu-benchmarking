from web3 import Web3, HTTPProvider
import os

# Replace the following variables with your Besu network configuration
BESU_NODE_URL = "http://localhost:8545"
PASSWORD_FILE_PATH = "password.txt"  # Replace with the path to your password file

def create_account():
    # Connect to the Besu node
    w3 = Web3(HTTPProvider(BESU_NODE_URL))

    # Check if the node is accessible
    if not w3.is_connected():
        print("Error: Unable to connect to the Besu node.")
        return

    # Check if the password file exists
    if not os.path.exists(PASSWORD_FILE_PATH):
        print("Error: Password file not found.")
        return

    # Load the password from the file
    with open(PASSWORD_FILE_PATH, "r") as password_file:
        password = password_file.read().strip()

    # Create a new Ethereum account
    account = w3.eth.account.create(password)

    # Output the account details
    print("Account created successfully!")
    print("Address:", account.address)
    print("Private Key:", account._private_key.hex())

if __name__ == "__main__":
    create_account()
