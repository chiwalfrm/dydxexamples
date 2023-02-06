import datetime
from ciso8601 import parse_datetime
from dydx3 import Client
from dydx3 import constants
from os import path
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

if len(argv) > 3:
        if not path.exists(argv[3]):
                print('ERROR: File', argv[3], 'does not exist.')
                exit()
        exec(open(argv[3]).read())
if my_api_network_id == str(constants.NETWORK_ID_MAINNET):
        my_api_host = constants.API_HOST_MAINNET
elif my_api_network_id == str(constants.NETWORK_ID_GOERLI):
        my_api_host = constants.API_HOST_GOERLI
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

if len(argv) > 1:
        start_timestamp = argv[1]
else:
        start_timestamp = datetime.datetime.utcnow() + datetime.timedelta(days = -7)
        start_timestamp = start_timestamp.isoformat()[:-3] + 'Z'
if len(argv) > 2:
        stop_timestamp = argv[2]
else:
        stop_timestamp = datetime.datetime.utcnow()
        stop_timestamp = stop_timestamp.isoformat()[:-3] + 'Z'
list_of_fills = [ ]
while parse_datetime(stop_timestamp) > parse_datetime(start_timestamp):
        get_fills_results = client.private.get_fills(created_before_or_at = stop_timestamp)
        get_fills_results = get_fills_results.data
        firstrecorddate = get_fills_results['fills'][0]['createdAt']
        lastrecorddate = get_fills_results['fills'][-1]['createdAt']
        if firstrecorddate == lastrecorddate:
                print('You have more than 100 trades in the same millisecond:', firstrecorddate)
                print('Please contact customer service for further assistance.')
                exit()
        for fill in get_fills_results['fills']:
                if parse_datetime(fill['createdAt']) > parse_datetime(start_timestamp):
                        list_of_fills.append(fill)
        if len(get_fills_results['fills']) < 100:
                break
        stop_timestamp = parse_datetime(get_fills_results['fills'][-1]['createdAt']) + datetime.timedelta(microseconds = 1000)
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
