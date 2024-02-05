#Example shell command: while true; do clear; python3 ./v4checkmarkets.py BTC-USD ETH-USD LINK-USD MATIC-USD; sleep 15; done
from requests import get
from sys import argv
#INDEXERURL = 'https://indexer.v4testnet.dydx.exchange/v4'
INDEXERURL = 'https://indexer.dydx.trade/v4'

#dydxmarket
def getprices():
        count = 0
        global bestbid
        global bestask
        r = get(url = INDEXERURL+'/orderbooks/perpetualMarket/'+dydxmarket)
        try:
                r.raise_for_status()
                if r.status_code == 200:
                        bestbid = r.json()['bids'][0]['price']
                        bestask = r.json()['asks'][0]['price']
                else:
                        print('Bad requests status code:', r.status_code)
                return 0
        except Exception as error:
                count += 1
                print('getprices() exception, will retry... count='+count)
                if count > 9:
                        print('getprices() Market not found', dydxmarket)
                        return None

#dydxmarket
def getticksize():
        count = 0
        global dydxticksize
        r = get(url = INDEXERURL+'/perpetualMarkets', params = {
                'ticker': dydxmarket
        })
        try:
                r.raise_for_status()
                if r.status_code == 200:
                        dydxticksize = r.json()['markets'][dydxmarket]['tickSize']
                else:
                        print('Bad requests status code:', r.status_code)
        except Exception as error:
                count += 1
                print('getticksize() exception, will retry... count='+count)
                if count > 9:
                        print('getticksize() Market not found', dydxmarket)
                        return None

print('Market           Price')
print('======================')
for dydxmarket in argv[1:]:
        getprices()
        getticksize()
#       decimals = max(bestbid[::-1].find('.'), bestask[::-1].find('.'))
#       if decimals < 0:
#               decimals = -decimals
#               dydxticksize = float("10e-"+str(decimals))
#       else:
#               dydxticksize = float("10e-"+str(decimals+1))
        midprice = ( float(bestbid) + float(bestask) ) / 2
        midprice = float('%g'%(midprice - (midprice % float(dydxticksize))))
        if str(midprice)[-2:] == '.0':
                midprice = int(midprice)
        print(dydxmarket.ljust(9), str(midprice).rjust(12))
