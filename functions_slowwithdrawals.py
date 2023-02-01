#withdrawalamount/my_eth_address (SET THESE)
def createwithdrawal():
        create_withdrawal_result = client.private.create_withdrawal(
                position_id = account['positionId'],
                amount = withdrawalamount,
                asset = constants.ASSET_USDC,
                to_address = my_eth_address,
                expiration = epoch_seconds_to_iso(time() + 604801)
        )
        print(create_withdrawal_result.data)

#my_api_network_id/infurakey/my_eth_address/my_eth_private_key (SET THESE)
def createwithdrawalpart2():
        if my_api_network_id == str(constants.NETWORK_ID_MAINNET):
                w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/' + infurakey))
        else:
                w3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/' + infurakey))
        stark_public_key_2, stark_public_key_y_coordinate_2 = private_key_to_public_key_pair_hex(client.stark_private_key)
        assettype = constants.COLLATERAL_ASSET_ID_BY_NETWORK_ID.get(int(my_api_network_id))
        dydxabi = requests.get(url = 'https://raw.githubusercontent.com/dydxprotocol/dydx-v3-python/master/dydx3/abi/starkware-perpetuals.json').json()
        dydxcontract = constants.STARKWARE_PERPETUALS_CONTRACT.get(int(my_api_network_id))
        contract = w3.eth.contract(address = dydxcontract, abi = dydxabi)
        transaction = contract.functions.withdraw(
                starkKey = int(stark_public_key_2,16),
                assetType = assettype
                ).buildTransaction()
        transaction.update(
                { 'from' : my_eth_address,
                  'nonce' : w3.eth.get_transaction_count(my_eth_address) }
                )
        signed_tx = w3.eth.account.sign_transaction(transaction, my_eth_private_key)
        txn_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print("Waiting for transaction to be confirmed...")
        txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
        print(txn_receipt)

#limitx = set this to number of records to retrieve (SET THIS)
def checktransfers():
        get_transfers_result = client.private.get_transfers(limit = limitx)
        print(get_transfers_result.data)
