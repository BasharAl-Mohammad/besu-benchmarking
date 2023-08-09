import subprocess
import json
import os
import shutil

def create_network_structure():
    try:
        name = "Clique"
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

def run_besu_command():
    command = "besu/bin/besu --data-path=Clique-Network/Node-1/data public-key export-address --to=Clique-Network/Node-1/data/node1Address"
    try:
        subprocess.run(command, shell=True, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing the command. Return code: {e.returncode}")
        print(f"Error message: {e.stderr}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def read_address_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            address = file.read().strip()

            if address.startswith('0x'):
                address = address[2:]

            return address
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return None

def create_genesis_file(file_path, node1_address, blockperiodseconds, epochlength):
    genesis_data = {
        "config": {
            "chainId": 1337,
            "berlinBlock": 0,
            "clique": {
                "blockperiodseconds": blockperiodseconds,
                "epochlength": epochlength
            }
        },
        "coinbase": "0x0000000000000000000000000000000000000000",
        "difficulty": "0x1",
        "extraData": f"0x0000000000000000000000000000000000000000000000000000000000000000{node1_address}0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        "gasLimit": "0xa00000",
        "mixHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "nonce": "0x0",
        "timestamp": "0x5c51a607",
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
    }

    try:
        with open(file_path, 'w') as file:
            json.dump(genesis_data, file, indent=2)
        print(f"Genesis file '{file_path}' created successfully.")
    except Exception as e:
        print(f"An error occurred while creating the genesis file: {str(e)}")

if __name__ == "__main__":
    name, num_nodes = create_network_structure()
    run_besu_command()

    file_path = "Clique-Network/Node-1/data/node1Address"
    node1_address = read_address_from_file(file_path)

    if node1_address:
        print("Extracted Address:", node1_address)

        blockperiodseconds = int(input("Enter blockperiodseconds: "))
        epochlength = int(input("Enter epochlength: "))

        genesis_file_path = "Clique-Network/genesis.json"
        create_genesis_file(genesis_file_path, node1_address, blockperiodseconds, epochlength)