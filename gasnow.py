from requests import get
r = get(url = 'https://etherchain.org/api/gasnow')
for key, value in r.json()['data'].items():
        if key != 'timestamp' and key != 'priceUSD':
                print(key.ljust(8), str(int(value/1000000000)).rjust(3))
