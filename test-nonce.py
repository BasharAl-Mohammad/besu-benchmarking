from web3 import Web3

RPC_URL = "http://localhost:8545"
PRIVATE_KEY = "7a98908635356bd15cdaf5f5224860315c8e3ed89268d3197896b513f51414d7"

def send_transaction(to_address, amount_wei):
    try:
        w3 = Web3(Web3.HTTPProvider(RPC_URL))

        if not w3.is_address(to_address):
            raise ValueError("Invalid recipient address")

        account = w3.eth.account.from_key(PRIVATE_KEY)

        nonce = w3.eth.get_transaction_count(account.address)

        print("Receipt:", nonce)


        # transaction = {
        #     'to': to_address,
        #     'value': amount_wei,
        #     'gas': 2000000,
        #     'gasPrice': w3.to_wei('10', 'gwei'),
        #     'nonce': nonce,
        #     'chainId': 1337
        # }

        # signed_transaction = account.sign_transaction(transaction)

        # tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        # receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        # print("Transaction successful. Transaction hash:", tx_hash.hex())
        # print("Receipt:", receipt)

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    recipient_address = "0xf17f52151EbEF6C7334FAD080c5704D77216b732"
    amount_wei = Web3.to_wei(1, 'ether')
    send_transaction(recipient_address, amount_wei)
