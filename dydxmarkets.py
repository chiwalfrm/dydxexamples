import requests
#r = requests.get(url = 'https://www.gasnow.org/api/v3/gas/price?utm_source=:YourAPPName')
r = requests.get(url = 'https://api.dydx.exchange/v3/markets')
for key, value in r.json()['markets'].items():
        print(key, value['status'])
