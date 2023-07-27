import subprocess
import json
import os
import shutil

def create_network_structure():
    try:
        name = "IBFT"
        num_nodes = int(input("Enter the number of nodes: "))

        base_dir = f"{name}-Network"
        os.makedirs(base_dir, exist_ok=True)

        for node_num in range(1, num_nodes + 1):
            node_dir = os.path.join(base_dir, f"Node-{node_num}")
            data_dir = os.path.join(node_dir, "data")
            os.makedirs(data_dir, exist_ok=True)

        print("Directory structure created successfully.")
        return name, num_nodes
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return None, None

def generate_genesis_block(name, num_nodes):
    if num_nodes is None:
        return

    blockperiodseconds = int(input("Enter blockperiodseconds: "))
    epochlength = int(input("Enter epochlength: "))
    requesttimeoutseconds = int(input("Enter requesttimeoutseconds: "))

    genesis_data = {
        "genesis": {
            "config": {
                "chainId": 1337,
                "berlinBlock": 0,
                "ibft2": {
                    "blockperiodseconds": blockperiodseconds,
                    "epochlength": epochlength,
                    "requesttimeoutseconds": requesttimeoutseconds
                }
            },
            "nonce": "0x0",
            "timestamp": "0x0",
            "gasLimit": "0x1fffffffffffff",
            "difficulty": "0x1",
            "mixHash": "0x63746963616c2062797a616e74696e65206661756c7420746f6c6572616e6365",
            "coinbase": "0x0000000000000000000000000000000000000000",
            "alloc": {
                "fe3b557e8fb62b89f4916b721be55ceb828dbd73": {
                    "privateKey": "8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63",
                    "comment": "private key and this comment are ignored.  In a real chain, the private key should NOT be stored",
                    "balance": "0xad78ebc5ac6200000"
                },
                "627306090abaB3A6e1400e9345bC60c78a8BEf57": {
                    "privateKey": "c87509a1c067bbde78beb793e6fa76530b6382a4c0241e5e4a9ec0a0f44dc0d3",
                    "comment": "private key and this comment are ignored.  In a real chain, the private key should NOT be stored",
                    "balance": "90000000000000000000000"
                },
                "f17f52151EbEF6C7334FAD080c5704D77216b732": {
                    "privateKey": "ae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f",
                    "comment": "private key and this comment are ignored.  In a real chain, the private key should NOT be stored",
                    "balance": "90000000000000000000000"
                }
            }
        },
        "blockchain": {
            "nodes": {
                "generate": True,
                "count": num_nodes
            }
        }
    }

    # Create the 'config' directory if it doesn't exist
    if not os.path.exists("config"):
        os.makedirs("config")

    with open(f"config/{name}genesis.json", "w") as file:
        json.dump(genesis_data, file, indent=2)

    print(f"Genesis block data has been saved to 'config/{name}genesis.json'")

def run_besu_operator(name):
    config_file = f"config/{name}genesis.json"
    # Define the command to run
    command = f"besu/bin/besu operator generate-blockchain-config --config-file={config_file} --to=networkFiles --private-key-file-name=key"

    try:
        # Run the command
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)

        # Print the output
        print("Command executed successfully:")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("Command failed with error:")
        print(e.stderr)

def copy_keys(name):
    source_dir = "networkFiles"
    destination_dir = f"{name}-Network"
    # Get a list of subdirectories in the source directory's 'keys' folder
    keys_dir = os.path.join(source_dir, 'keys')
    subdirectories = [name for name in os.listdir(keys_dir) if os.path.isdir(os.path.join(keys_dir, name))]
    
    # Copy genesis.json to the QBFT-Network folder
    shutil.copy(os.path.join(source_dir, 'genesis.json'), destination_dir)
    
    # Iterate through each subdirectory (address) in the 'keys' folder
    for i, address in enumerate(subdirectories, start=1):
        source_address_dir = os.path.join(keys_dir, address)
        destination_subdir = os.path.join(destination_dir, f'Node-{i}', 'data')
        
        # Create the data folder in QBFT-Network/Node-X if it doesn't exist
        os.makedirs(destination_subdir, exist_ok=True)
        
        # Copy the key and key.pub files to the corresponding Node-X/data folder
        shutil.copy(os.path.join(source_address_dir, 'key'), destination_subdir)
        shutil.copy(os.path.join(source_address_dir, 'key.pub'), destination_subdir)

if __name__ == "__main__":
    name, num_nodes = create_network_structure()
    generate_genesis_block(name, num_nodes)
    run_besu_operator(name)
    copy_keys(name)