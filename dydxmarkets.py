from requests import get
#r = get(url = 'https://api.stage.dydx.exchange/v3/markets')
r = get(url = 'https://api.dydx.exchange/v3/markets')
r.raise_for_status()
if r.status_code == 200:
        for key, value in r.json()['markets'].items():
                print(key, value['status'])
else:
        print('Bad requests status code:', r.status_code)
