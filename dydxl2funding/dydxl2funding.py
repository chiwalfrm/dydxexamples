import pprint
import sys
from dydx3 import Client
from dydx3 import constants

pp = pprint.PrettyPrinter(width = 41, compact = True)

_network_id = str(constants.NETWORK_ID_MAINNET)
#_network_id is set to either str(constants.NETWORK_ID_MAINNET) or str(constants.NETWORK_ID_GOERLI)
_api_host = constants.API_HOST_MAINNET
#_api_host is set to either constants.API_HOST_MAINNET or constants.API_HOST_GOERLI

client = Client(
        host = _api_host,
        network_id = _network_id
)

historical_funding = client.public.get_historical_funding(market = sys.argv[1])
pp.pprint(historical_funding.data)
