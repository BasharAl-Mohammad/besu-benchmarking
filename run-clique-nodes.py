import os
import subprocess
from multiprocessing import Process

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for line in process.stdout:
        print(line.strip())
    process.wait()
    return process.returncode

def find_enode_url(base_data_path, genesis_file):
    node_1_data_path = os.path.join(base_data_path, "Node-1", "data")
    besu_command = f"besu/bin/besu --data-path={node_1_data_path} --genesis-file={genesis_file} --config-file=config/config.toml"

    process_node_1 = subprocess.Popen(besu_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    node_1_enode_url = None
    for line in process_node_1.stdout:
        print(line.strip())
        if "Enode URL" in line:
            node_1_enode_url = line.split()[-1]
            print("Found Enode URL:", node_1_enode_url)
            break

    return node_1_enode_url

if __name__ == "__main__":
    p2p_port=0  
    base_data_path = "Clique-Network"
    genesis_file = os.path.join(base_data_path, "genesis.json")

    node_1_enode_url = find_enode_url(base_data_path, genesis_file)

    if node_1_enode_url:
        command_template = (
            "besu/bin/besu --data-path={data_path} --genesis-file={genesis_file} "
            f"--bootnodes={node_1_enode_url} --p2p-port={p2p_port} --rpc-http-enabled "
            "--rpc-http-api=ETH,NET,QBFT --host-allowlist='*' --rpc-http-cors-origins='all' "
            "--rpc-http-port={rpc_port}"
        )

        num_nodes = len([name for name in os.listdir(base_data_path) if os.path.isdir(os.path.join(base_data_path, name))]) - 1

        # Start processes for Node-2 and subsequent nodes
        for i in range(2, num_nodes + 2):
            data_path = os.path.join(base_data_path, f"Node-{i}", "data")
            p2p_port = 30303 + i
            rpc_port = 8546 + i
            command = command_template.format(
                data_path=data_path, genesis_file=genesis_file, p2p_port=p2p_port, rpc_port=rpc_port
            )
            process_node = Process(target=run_command, args=(command,))
            process_node.start()
