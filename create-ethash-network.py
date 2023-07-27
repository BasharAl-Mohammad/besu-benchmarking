import subprocess
import json
import os
import shutil

def create_network_structure():
    try:
        name = "Ethash"
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

    fixeddifficulty = int(input("Enter fixeddifficulty: "))

    genesis_data = {
        "config": {
        "berlinBlock": 0,
        "ethash": {
            "fixeddifficulty": fixeddifficulty
            },
        "chainID": 1337
        },
        "nonce": "0x00",
        "gasLimit": "0x1000000",
        "difficulty": "0x10000",
        "alloc": {
            "fe3b557e8fb62b89f4916b721be55ceb828dbd73": {
                "privateKey": "8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63",
                "comment": "private key and this comment are ignored.  In a real chain, the private key should NOT be stored",
                "balance": "0xad78ebc5ac6200000"
                },
            "f17f52151EbEF6C7334FAD080c5704D77216b732": {
                "privateKey": "ae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f",
                "comment": "private key and this comment are ignored.  In a real chain, the private key should NOT be stored",
                "balance": "90000000000000000000000"
                }
            }
        }

    if not os.path.exists("config"):
        os.makedirs("config")

    with open(f"{name}-Network/genesis.json", "w") as file:
        json.dump(genesis_data, file, indent=2)

    print(f"Genesis block data has been saved to '{name}-Network/genesis.json'")

if __name__ == "__main__":
    name, num_nodes = create_network_structure()
    generate_genesis_block(name, num_nodes)