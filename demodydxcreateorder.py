import time
from datetime import datetime
from dydx3 import Client
from dydx3 import constants
from dydx3 import epoch_seconds_to_iso
from os import path
from random import randint
from requests import get
from sys import argv

########################## YOU FILL THIS OUT #################
my_eth_private_key = '<FILL_THIS_OUT>'
#my_eth_private_key is optional and may be set to '' (hardware wallets do not generally provide this information)
#If my_eth_private_key is set, you do not need to set my_api_key/my_api_secret/my_api_passphrase/my_stark_private_key
my_api_key = '<FILL_THIS_OUT>'
my_api_secret = '<FILL_THIS_OUT>'
my_api_passphrase = '<FILL_THIS_OUT>'
my_stark_private_key = '<FILL_THIS_OUT>'
my_eth_address = '<FILL_THIS_OUT>'
my_api_network_id = str(constants.NETWORK_ID_GOERLI)
#my_api_network_id is set to either str(constants.NETWORK_ID_MAINNET) or str(constants.NETWORK_ID_GOERLI)
##############################################################

if len(argv) > 1 and path.exists(argv[1]):
        exec(open(argv[1]).read())
if my_api_network_id == str(constants.NETWORK_ID_MAINNET):
        my_api_host = constants.API_HOST_MAINNET
        my_ws_host = constants.WS_HOST_MAINNET
elif my_api_network_id == str(constants.NETWORK_ID_GOERLI):
        my_api_host = constants.API_HOST_GOERLI
        my_ws_host = constants.WS_HOST_GOERLI
else:
        print(f"Error: my_api_network_id is not {constants.NETWORK_ID_MAINNET} or {constants.NETWORK_ID_GOERLI}.")
        exit()

if my_eth_private_key != '':
        client = Client(
                host = my_api_host,
                default_ethereum_address = my_eth_address,
                eth_private_key = my_eth_private_key,
                network_id = my_api_network_id
        )
        derive_stark_key_result = client.onboarding.derive_stark_key()
        stark_private_key = derive_stark_key_result['private_key']
        client.stark_private_key = stark_private_key
else:
        client = Client(
                host = my_api_host,
                network_id = my_api_network_id,
                api_key_credentials = {
                        'key': my_api_key,
                        'secret': my_api_secret,
                        'passphrase': my_api_passphrase
                }
        )
        client.stark_private_key = my_stark_private_key

get_account_result = client.private.get_account(
        ethereum_address = my_eth_address
)
account = get_account_result.data['account']
one_minute_from_now_iso = epoch_seconds_to_iso(time.time() + 70)
create_order_result = client.private.create_order(
        position_id = account['positionId'],
        market = constants.MARKET_BTC_USD,
        side = constants.ORDER_SIDE_BUY,
        order_type = constants.ORDER_TYPE_LIMIT,
        post_only = False,
        size = '0.001',
        price = '1000',
        limit_fee = '0.1',
        expiration = one_minute_from_now_iso,
)
print(create_order_result.data)
print(create_order_result.headers)
