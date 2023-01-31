from dydx3 import Client
from dydx3 import constants
from dydx3 import private_key_to_public_key_pair_hex
from os import path
import datetime
import requests
import sys

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

if path.exists(sys.argv[1]):
        exec(open(sys.argv[1]).read())
if my_api_network_id == str(constants.NETWORK_ID_MAINNET):
        my_api_host = constants.API_HOST_MAINNET
        my_ws_host = constants.WS_HOST_MAINNET
elif my_api_network_id == str(constants.NETWORK_ID_GOERLI):
        my_api_host = constants.API_HOST_GOERLI
        my_ws_host = constants.WS_HOST_GOERLI
else:
        print('Error: my_api_network_id is not '+str(constants.NETWORK_ID_MAINNET)+' or '+str(constants.NETWORK_ID_GOERLI)+'.')
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

public_x, public_y = private_key_to_public_key_pair_hex(stark_private_key)
#Uncomment this block if you have never onboarded before
#create_user_result = client.onboarding.create_user(
#       stark_public_key = public_x,
#       stark_public_key_y_coordinate = public_y,
#)
recover_default_api_key_credentials_results = client.onboarding.recover_default_api_key_credentials()
print('my_eth_private_key=\'' + my_eth_private_key + '\'')
print('my_api_key=\'' + recover_default_api_key_credentials_results['key'] + '\'')
print('my_api_secret=\'' + recover_default_api_key_credentials_results['secret'] + '\'')
print('my_api_passphrase=\'' + recover_default_api_key_credentials_results['passphrase'] + '\'')
print('my_stark_private_key=\'' + stark_private_key + '\'')
print('my_eth_address=\'' + my_eth_address + '\'')
print('_stark_public_key=\'' + public_x + '\'')
print('_stark_public_key_y_coordinate=\'' + public_y + '\'')
#Uncomment this block to request free testnet tokens
#request_testnet_tokens_results = client.private.request_testnet_tokens()
#print(request_testnet_tokens_results.data)
#print(request_testnet_tokens_results.headers)
get_account_results = client.private.get_account()
print(get_account_results.data)
print(get_account_results.headers)
