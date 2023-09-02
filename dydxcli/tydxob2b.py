import os
from datetime import datetime
from dydx3 import Client
from dydx3 import constants
from requests import get
from sys import argv
from time import sleep

widthprice = 10
widthsize = 10

RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
CYAN = '\033[0;36m'
NC = '\033[0m' # No Color
REDWHITE = '\033[0;31m\u001b[47m'
GREENWHITE = '\033[0;32m\u001b[47m'

workingdir=os.path.dirname(os.path.abspath(__file__))
if len(argv) < 2:
        marketusd = 'BTC-USD'
else:
        marketusd = argv[1]
if len(argv) < 3:
        depth = 10
else:
        depth = int(argv[2])
if len(argv) > 3:
        ansimode = argv[3]
else:
        ansimode = 'ansi'
client = Client(
        host = constants.API_HOST_GOERLI,
        network_id = constants.NETWORK_ID_GOERLI,
)
while True:
        try:
                starttime = datetime.now()
                get_trades_result = client.public.get_trades(
                        market=marketusd
                )
                lasttradeprice = get_trades_result.data['trades'][0]['price']
                get_orderbook_result = client.public.get_orderbook(
                        market=marketusd,
                )
                askarray = get_orderbook_result.data['asks']
                bidarray = get_orderbook_result.data['bids']
                count = 0
                bidsizetotal = 0
                asksizetotal = 0
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Last trade:', get_trades_result.data['trades'][0]['createdAt'], get_trades_result.data['trades'][0]['price'], get_trades_result.data['trades'][0]['side'], get_trades_result.data['trades'][0]['size'])
                print('Bid'+' '.ljust(widthprice+widthsize+1)+'| Ask')
                while count < min(depth, max(len(bidarray), len(askarray))):
                        if count < len(bidarray):
                                biditemprice = float(bidarray[count]['price'])
                                biditemsize = float(bidarray[count]['size'])
                        else:
                                biditemprice = ''
                                biditemsize = ''
                        if count < len(askarray):
                                askitemprice = float(askarray[count]['price'])
                                askitemsize = float(askarray[count]['size'])
                        else:
                                askitemprice = ''
                                askitemsize = ''
                        if biditemsize != '':
                                bidsizetotal += biditemsize
                                biditemsizet = '('+str(biditemsize)+')'
                        else:
                                biditemsizet = ''
                        if askitemsize != '':
                                asksizetotal += askitemsize
                                askitemsizet = '('+str(askitemsize)+')'
                        else:
                                askitemsizet = ''
                        if count == 0:
                                highestbidprice = biditemprice
                                lowestaskprice = askitemprice
                        print(str(biditemprice).ljust(widthprice), biditemsizet.ljust(widthsize+2)+' | '+str(askitemprice).ljust(widthprice), askitemsizet.ljust(widthsize+2), end = '\r')
                        if ansimode != 'noansi':
                                if biditemprice == float(lasttradeprice):
                                        print(f"{REDWHITE}{biditemprice}{NC}", end = '\r')
                                elif askitemprice == float(lasttradeprice):
                                        print(str(biditemprice).ljust(widthprice), biditemsizet.ljust(widthsize+2)+' | '+GREENWHITE+str(askitemprice)+NC, end = '\r')
                        print()
                        count += 1
                print('maxbid   :', highestbidprice)
                print('minask   :', lowestaskprice, '(+'+'{0:.4f}'.format(lowestaskprice - highestbidprice)+')', '{0:.4f}'.format((lowestaskprice - highestbidprice) / highestbidprice * 100)+'%')
                print('bidvolume:', bidsizetotal)
                print('askvolume:', asksizetotal)
                r = get(url = 'https://api.stage.dydx.exchange/v3/markets')
#               r = get(url = 'https://api.dydx.exchange/v3/markets')
                r.raise_for_status()
                if r.status_code == 200:
                        print('indexPrice     :', r.json()['markets'][marketusd]['indexPrice'])
                        print('oraclePrice    :', r.json()['markets'][marketusd]['oraclePrice'])
                        print('priceChange24H :', r.json()['markets'][marketusd]['priceChange24H'])
                        print('nextFundingRate:', r.json()['markets'][marketusd]['nextFundingRate'])
                        print('nextFundingAt  :', r.json()['markets'][marketusd]['nextFundingAt'])
                        print('openInterest   :', r.json()['markets'][marketusd]['openInterest'])
                        print('trades24H      :', r.json()['markets'][marketusd]['trades24H'])
                        print('volume24H      :', r.json()['markets'][marketusd]['volume24H'])
                else:
                        print('Bad requests status code:', r.status_code)
                endtime = datetime.now()
                print('Runtime        :' , endtime - starttime)
                if os.path.isfile(workingdir+'/'+marketusd+'/EXITFLAG'):
                        exit()
                else:
                        sleep(1)
        except KeyboardInterrupt:
                exit(0)
