from dydx3 import Client
from dydx3 import constants
from sys import argv
import pprint
pp = pprint.PrettyPrinter(width = 41, compact = True)

my_api_network_id = str(constants.NETWORK_ID_MAINNET)
#my_api_network_id is set to either str(constants.NETWORK_ID_MAINNET) or str(constants.NETWORK_ID_GOERLI)
my_api_host = constants.API_HOST_MAINNET
#my_api_host is set to either constants.API_HOST_MAINNET or constants.API_HOST_GOERLI

client = Client(
        host = my_api_host,
        network_id = my_api_network_id
)

historical_funding = client.public.get_historical_funding(market = argv[1])
pp.pprint(historical_funding.data)
