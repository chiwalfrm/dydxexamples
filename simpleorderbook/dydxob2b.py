import os
from dydx3 import Client
from dydx3 import constants
from requests import get
from sys import argv

def generate_files(marketusd):
        get_orderbook_result = client.public.get_orderbook(
                market=marketusd,
        )
        fp = open(marketusd+"bids", "w")
        for item in get_orderbook_result.data['bids']:
                fp.write(item['size']+' '+item['price']+'\n')
        fp.close()
        fp = open(marketusd+"asks", "w")
        for item in get_orderbook_result.data['asks']:
                fp.write(item['size']+' '+item['price']+'\n')
        fp.close()
        get_trades_result = client.public.get_trades(
                market=marketusd
        )
        fp = open(marketusd+"trades", "w")
        for item in get_trades_result.data['trades']:
                if item['liquidation'] == True:
                        liquidationflag = 'L'
                else:
                        liquidationflag = ''
                fp.write(item['createdAt']+' '+item['price']+' '+item['side'].ljust(4)+' ('+item['size']+')'+liquidationflag+'\n')
        fp.close()
#       r = get(url = 'https://api.stage.dydx.exchange/v3/markets')
        r = get(url = 'https://api.dydx.exchange/v3/markets')
        r.raise_for_status()
        if r.status_code == 200:
                fp = open(marketusd+"markets", "w")
                fp.write('indexPrice     : '+r.json()['markets'][marketusd]['indexPrice']+'\n')
                fp.write('oraclePrice    : '+r.json()['markets'][marketusd]['oraclePrice']+'\n')
                fp.write('priceChange24H : '+r.json()['markets'][marketusd]['priceChange24H']+'\n')
                fp.write('nextFundingRate: '+r.json()['markets'][marketusd]['nextFundingRate']+'\n')
                fp.write('nextFundingAt  : '+r.json()['markets'][marketusd]['nextFundingAt']+'\n')
                fp.write('openInterest   : '+r.json()['markets'][marketusd]['openInterest']+'\n')
                fp.write('trades24H      : '+r.json()['markets'][marketusd]['trades24H']+'\n')
                fp.write('volume24H      : '+r.json()['markets'][marketusd]['volume24H']+'\n')
                fp.close()
        else:
                print('Bad requests status code:', r.status_code)

if len(argv) < 2:
        print("Error: Must specify market.")
        exit()
marketusd = argv[1]
client = Client(
        host = constants.API_HOST_MAINNET,
        network_id = constants.NETWORK_ID_MAINNET,
)
generate_files(marketusd)
os.system("paste -d ',' "+marketusd+"bids "+marketusd+"asks > "+marketusd+"orderbook")
