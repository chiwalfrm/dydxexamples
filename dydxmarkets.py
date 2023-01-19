import requests
#r = requests.get(url = 'https://api.stage.dydx.exchange/v3/markets')
r = requests.get(url = 'https://api.dydx.exchange/v3/markets')
for key, value in r.json()['markets'].items():
        print(key, value['status'])
