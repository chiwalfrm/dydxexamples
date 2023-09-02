from requests import get
INDEXERURL = 'https://indexer.v4testnet2.dydx.exchange/v4'
r = get(url = INDEXERURL+'/perpetualMarkets')
r.raise_for_status()
if r.status_code == 200:
        for key, value in r.json()['markets'].items():
                print(key, value['status'])
else:
        print('Bad requests status code:', r.status_code)
