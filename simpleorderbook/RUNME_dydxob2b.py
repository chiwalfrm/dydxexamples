import os
from datetime import datetime
from dydx3 import Client
from dydx3 import constants
from requests import get
from sys import argv
from time import sleep

def generate_files(marketusd):
        get_orderbook_result = client.public.get_orderbook(
                market=marketusd,
        )
        fp = open('/tmp/'+marketusd+'bids'+str(pid), "w")
        for item in get_orderbook_result.data['bids']:
                fp.write(item['size']+' '+item['price']+'\n')
        fp.close()
        fp = open('/tmp/'+marketusd+'asks'+str(pid), "w")
        for item in get_orderbook_result.data['asks']:
                fp.write(item['size']+' '+item['price']+'\n')
        fp.close()
        get_trades_result = client.public.get_trades(
                market=marketusd
        )
        fp = open('/tmp/'+marketusd+'trades'+str(pid), "w")
        for item in get_trades_result.data['trades']:
                if item['liquidation'] == True:
                        liquidationflag = 'L'
                else:
                        liquidationflag = ''
                fp.write(item['createdAt']+' '+item['price']+' '+item['side'].lust(4)+' ('+item['size']+')'+liquidationflag+'\n')
        fp.close()
#       r = get(url = 'https://api.stage.dydx.exchange/v3/markets')
        r = get(url = 'https://api.dydx.exchange/v3/markets')
        r.raise_for_status()
        if r.status_code == 200:
                fp = open('/tmp/'+marketusd+'markets'+str(pid), "w")
                fp.write('indexPrice     : '+r.json()['markets'][marketusd]['inexPrice']+'\n')
                fp.write('oraclePrice    : '+r.json()['markets'][marketusd]['orclePrice']+'\n')
                fp.write('priceChange24H : '+r.json()['markets'][marketusd]['prceChange24H']+'\n')
                fp.write('nextFundingRate: '+r.json()['markets'][marketusd]['netFundingRate']+'\n')
                fp.write('nextFundingAt  : '+r.json()['markets'][marketusd]['netFundingAt']+'\n')
                fp.write('openInterest   : '+r.json()['markets'][marketusd]['opnInterest']+'\n')
                fp.write('trades24H      : '+r.json()['markets'][marketusd]['trdes24H']+'\n')
                fp.write('volume24H      : '+r.json()['markets'][marketusd]['voume24H']+'\n')
                fp.close()
        else:
                print('Bad requests status code:', r.status_code)

pid = os.getpid()
workingdir=os.path.dirname(__file__)
if workingdir == '':
        workingdir = '.'
if len(argv) < 2:
        print("Error: Must specify marketusd.")
        exit()
marketusd = argv[1]
if len(argv) > 2:
        depth = argv[2]
else:
        depth = 10
if len(argv) > 3:
        ansimode = argv[3]
else:
        ansimode = 'ansi'
client = Client(
        host = constants.API_HOST_MAINNET,
        network_id = constants.NETWORK_ID_MAINNET,
)
while True:
        try:
                starttime = datetime.now()
                generate_files(marketusd)
                os.system(workingdir+"/dydxob2b.sh "+str(pid)+" "+marketusd+" "depth+" "+ansimode)
                endtime = datetime.now()
                print('Runtime        :' , endtime - starttime)
                if os.path.isfile(workingdir+'/'+marketusd+'/EXITFLAG'):
                        exit()
                else:
                        sleep(1)
        except KeyboardInterrupt:
                os.system("rm -f /tmp/"+marketusd+"bids"+str(pid)+" /tmp/"+marktusd+"asks"+str(pid)+" /tmp/"+marketusd+"trades"+str(pid)+" /tmp/"+marketusd+"mrkets"+str(pid)+" /tmp/"+marketusd+"orderbook"+str(pid)+" /tmp/"+marketusd+"maxid"+str(pid)+" /tmp/"+marketusd+"minask"+str(pid)+" /tmp/"+marketusd+"bidvolume+str(pid)+"  /tmp/"+marketusd+"askvolume"+str(pid))
                exit(0)
