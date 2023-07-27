import subprocess
import re
import time
import threading

# Shared variable to control the termination of the initial thread
terminate_initial_thread = False

# Function to run the initial command and extract the enode URL
def run_initial_command():
    command = "besu/bin/besu --data-path=Clique-Network/Node-1/data --genesis-file=Clique-Network/genesis.json --network-id 123 --rpc-http-enabled --rpc-http-api=ETH,NET,CLIQUE --host-allowlist=\"*\" --rpc-http-cors-origins=\"all\""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, universal_newlines=True)

    # Regular expression pattern to find the enode URL
    enode_pattern = r"enode:\/\/[^\s]+"

    enode_url = None

    while not terminate_initial_thread:
        output_line = process.stdout.readline()
        if not output_line:
            break

        print(output_line, end='')

        # Search for the enode URL in the output
        enode_match = re.search(enode_pattern, output_line)
        if enode_match:
            enode_url = enode_match.group()
            print(f"Enode URL: {enode_url}")
            break

    process.terminate()

    return enode_url

# Function to run a single additional command with a specific port and data path
def run_additional_command(enode_url, port, data_path):
    command = f"besu/bin/besu --data-path={data_path} --genesis-file=Clique-Network/genesis.json --bootnodes={enode_url} --network-id 123 --p2p-port={port} --rpc-http-enabled --rpc-http-api=ETH,NET,CLIQUE --host-allowlist=\"*\" --rpc-http-cors-origins=\"all\" --rpc-http-port={port + 8000}"
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    # Start the initial command in a separate thread
    initial_thread = threading.Thread(target=run_initial_command)
    initial_thread.start()

    # Let the initial command run for some time (adjust the duration as needed)
    time.sleep(10)

    # Signal the initial thread to terminate
    terminate_initial_thread = True
    initial_thread.join()

    # Retrieve the enode URL from the initial command
    enode_url = run_initial_command()

    # Number of additional nodes to run
    num_nodes = 5

    # Start threads for running additional commands in parallel
    if enode_url:
        threads = []
        for index in range(2, num_nodes + 2):  # Start from index 2 as Node-1 is reserved for the bootnode
            port = 30300 + index
            data_path = f"Clique-Network/Node-{index}/data"
            print(data_path)
            thread = threading.Thread(target=run_additional_command, args=(enode_url, port, data_path))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

    print("All commands completed.")
