from dydx3 import Client
from dydx3 import constants
from dydx3 import private_key_to_public_key_pair_hex

########################## YOU FILL THIS OUT #################
_private_key = '<FILL_THIS_OUT>'
#_private_key is optional and may be set to '' (hardware wallets do not generally provide this information)
#If _private_key is set, you do not need to set _api_key/_api_secret/_api_passphrase/_stark_private_key
_api_key = '<FILL_THIS_OUT>'
_api_secret = '<FILL_THIS_OUT>'
_api_passphrase = '<FILL_THIS_OUT>'
_stark_private_key = '<FILL_THIS_OUT>'
_eth_address = '<FILL_THIS_OUT>'
_network_id = str(constants.NETWORK_ID_GOERLI)
#_network_id is set to either str(constants.NETWORK_ID_MAINNET) or str(constants.NETWORK_ID_GOERLI)
_api_host = constants.API_HOST_GOERLI
#_api_host is set to either constants.API_HOST_MAINNET or constants.API_HOST_GOERLI
##############################################################

if _private_key != '':
        client = Client(
                host = _api_host,
                default_ethereum_address = _eth_address,
                eth_private_key = _private_key,
                network_id = _network_id
        )
        derive_stark_key_result = client.onboarding.derive_stark_key()
        stark_private_key = derive_stark_key_result['private_key']
        client.stark_private_key = stark_private_key
else:
        client = Client(
                host = _api_host,
                network_id = _network_id,
                api_key_credentials = {
                        'key': _api_key,
                        'secret': _api_secret,
                        'passphrase': _api_passphrase
                }
        )
        client.stark_private_key = _stark_private_key

public_x, public_y = private_key_to_public_key_pair_hex(stark_private_key)
#Uncomment this block if you have never onboarded before
#create_user_result = client.onboarding.create_user(
#       stark_public_key = public_x,
#       stark_public_key_y_coordinate = public_y,
#)
recover_default_api_key_credentials_results = client.onboarding.recover_default_api_key_credentials()
print('_private_key=\'' + _private_key + '\'')
print('_api_key=\'' + recover_default_api_key_credentials_results['key'] + '\'')
print('_api_secret=\'' + recover_default_api_key_credentials_results['secret'] + '\'')
print('_api_passphrase=\'' + recover_default_api_key_credentials_results['passphrase'] + '\'')
print('_stark_private_key=\'' + stark_private_key + '\'')
print('_eth_address=\'' + _eth_address + '\'')
print('_stark_public_key=\'' + public_x + '\'')
print('_stark_public_key_y_coordinate=\'' + public_y + '\'')
#Uncomment this block to request free testnet tokens
#request_testnet_tokens_results = client.private.request_testnet_tokens()
#print(request_testnet_tokens_results.data)
#print(request_testnet_tokens_results.headers)
get_account_results = client.private.get_account()
print(get_account_results.data)
print(get_account_results.headers)
