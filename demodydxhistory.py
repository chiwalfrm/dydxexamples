from dydx3 import Client
from dydx3 import constants
from os import path
import ciso8601
import datetime
import sys

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

if len(sys.argv) > 3:
        if not path.exists(sys.argv[3]):
                print('ERROR: File', sys.argv[3], 'does not exist.')
                exit()
        else:
                exec(open(sys.argv[3]).read())
                _private_key = my_eth_private_key
                _api_key = my_api_key
                _api_secret = my_api_secret
                _api_passphrase = my_api_passphrase
                _stark_private_key = my_stark_private_key
                _eth_address = my_eth_address
                _network_id = my_api_network_id
else:
        my_api_network_id = _network_id
if my_api_network_id == str(constants.NETWORK_ID_MAINNET):
        my_api_host = constants.API_HOST_MAINNET
elif my_api_network_id == str(constants.NETWORK_ID_GOERLI):
        my_api_host = constants.API_HOST_GOERLI
else:
        print('Error: my_api_network_id is not '+str(constants.NETWORK_ID_MAINNET)+' or '+str(constants.NETWORK_ID_GOERLI)+'.')
        exit()
_api_host = my_api_host

if _private_key != '':
        client = Client(
                host = _api_host,
                default_ethereum_address = _eth_address,
                eth_private_key = _private_key,
                network_id = _network_id
        )
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

if len(sys.argv) > 1:
        start_timestamp = sys.argv[1]
else:
        start_timestamp = datetime.datetime.utcnow() + datetime.timedelta(days = -7)
        start_timestamp = start_timestamp.isoformat()[:-3] + 'Z'
if len(sys.argv) > 2:
        stop_timestamp = sys.argv[2]
else:
        stop_timestamp = datetime.datetime.utcnow()
        stop_timestamp = stop_timestamp.isoformat()[:-3] + 'Z'
list_of_fills = [ ]
while ciso8601.parse_datetime(stop_timestamp) > ciso8601.parse_datetime(start_timestamp):
        get_fills_results = client.private.get_fills(created_before_or_at = stop_timestamp)
        get_fills_results = get_fills_results.data
        firstrecorddate = get_fills_results['fills'][0]['createdAt']
        lastrecorddate  = get_fills_results['fills'][-1]['createdAt']
        if firstrecorddate == lastrecorddate:
                print('You have more than 100 trades in the same millisecond:', firstrecorddate)
                print('Please contact customer service for further assistance.')
                exit()
        for fill in get_fills_results['fills']:
                if ciso8601.parse_datetime(fill['createdAt']) > ciso8601.parse_datetime(start_timestamp):
                        list_of_fills.append(fill)
        if len(get_fills_results['fills']) < 100:
                break
        stop_timestamp = ciso8601.parse_datetime(get_fills_results['fills'][-1]['createdAt']) + datetime.timedelta(microseconds = 1000)
        stop_timestamp = stop_timestamp.isoformat()[:-9] + 'Z'
list_of_fills_unique = [ ]
for fill in list_of_fills:
        if fill not in list_of_fills_unique:
                list_of_fills_unique.append(fill)
                print(fill['createdAt']+','+
                      fill['fee']+','+
                      fill['id']+','+
                      fill['liquidity']+','+
                      fill['market']+','+
                      str(fill['orderId'])+','+
                      fill['price']+','+
                      fill['side']+','+
                      fill['size']+','+
                      fill['type'])
