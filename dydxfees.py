from dydx3 import Client
from dydx3 import constants
from requests import get

client = Client(
        host = constants.API_HOST_MAINNET,
        network_id = constants.NETWORK_ID_MAINNET
)

#r = get(url = 'https://api.stage.dydx.exchange/v3/markets')
r = get(url = 'https://api.dydx.exchange/v3/markets')
r.raise_for_status()
if r.status_code == 200:
        totalfees = 0
        for key, value in r.json()['markets'].items():
                market_statistics1 = client.public.get_stats(
                        market=key,
                        days=constants.MARKET_STATISTIC_DAY_ONE,
                )
                fees=market_statistics1.data['markets'][key]['fees']
                totalfees = totalfees + float(fees)
                print(key, fees)
#               print(market_statistics.headers)
        print('TOTAL', totalfees)
else:
        print('Bad requests status code:', r.status_code)
