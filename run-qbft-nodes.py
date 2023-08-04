import multiprocessing
import subprocess
import os

def run_command(command):
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    # Find the number of nodes based on the available folders in QBFT-Network directory
    qbft_network_path = "QBFT-Network"
    node_folders = [folder for folder in os.listdir(qbft_network_path) if folder.startswith("Node-")]
    num_nodes = len(node_folders) - 1
    processes = []


    # Step 1: Run the first command to capture the enode URL
    enode_output = []
    first_command = f"besu/bin/besu --data-path={os.path.join(qbft_network_path, 'Node-1', 'data')} --genesis-file={os.path.join(qbft_network_path, 'genesis.json')} --config-file=config/config.toml"
    process = multiprocessing.Process(target=run_command, args=(first_command,))
    processes.append(process)
    process.start()


    # List of commands to run in parallel
    commands = []
    for i in range(2, num_nodes + 2):  # Assuming node IDs start from 2
        command = f"besu/bin/besu --data-path={os.path.join(qbft_network_path, f'Node-{i}', 'data')} --genesis-file={os.path.join(qbft_network_path, 'genesis.json')} --bootnodes=enode://751fef3bff526efb44f076ce6c8f4c9e37691c75cc27a8a328a8310979aa4ce89d1e8d698aeb3612d55093640dc427fc99e7c65c1cc0a7dd2d0c98c951586ec2@127.0.0.1:30303 --p2p-port={30303+i} --rpc-http-enabled --rpc-http-api=ETH,NET,QBFT --host-allowlist=\"*\" --rpc-http-cors-origins=\"all\" --rpc-http-port={8547+i}"
        commands.append(command)

    # Create a process for each command and start them
    for command in commands:
        process = multiprocessing.Process(target=run_command, args=(command,))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    print("All commands have been executed.")
