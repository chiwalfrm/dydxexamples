import os
import time
from datetime import datetime
from dydx3 import Client
from dydx3 import constants
from dydx3 import epoch_seconds_to_iso
from os import path
from random import randint
from requests import get
from sys import argv

########################## YOU FILL THIS OUT #################
my_eth_private_key = '<FILL_THIS_OUT>'
#my_eth_private_key is optional and may be set to '' (hardware wallets do not generally provide this information)
#If my_eth_private_key is set, you do not need to set my_api_key/my_api_secret/my_api_passphrase/my_stark_private_key
my_api_key = '<FILL_THIS_OUT>'
my_api_secret = '<FILL_THIS_OUT>'
my_api_passphrase = '<FILL_THIS_OUT>'
my_stark_private_key = '<FILL_THIS_OUT>'
my_eth_address = '<FILL_THIS_OUT>'
my_api_network_id = str(constants.NETWORK_ID_GOERLI)
#my_api_network_id is set to either str(constants.NETWORK_ID_MAINNET) or str(constants.NETWORK_ID_GOERLI)
whitelisted = False
simpleorderbook = 'n'
##############################################################

#ordermarket/orderside/ordertype/ordersize/orderprice/orderexpiration/ordertif
def sendorder():
        global create_order_result
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' sendorder()')
        create_order_result = client.private.create_order(
                position_id = account['positionId'],
                market = ordermarket,
                side = orderside,
                order_type = ordertype,
                post_only = False,
                size = ordersize,
                price = orderprice,
                limit_fee = '0.1',
                expiration = orderexpiration,
                time_in_force = ordertif
        )

#dydxmarket
def getprices():
        global bestbid
        global bestask
        bestbid = os.popen("python3 -u "+orderbookprogram+" "+dydxmarket+" 1 noansi | sed -n '"+str(orderbookline)+","+str(orderbookline)+"p' | awk '{print $1}'").read()[:-1]
        bestask = os.popen("python3 -u "+orderbookprogram+" "+dydxmarket+" 1 noansi | sed -n '"+str(orderbookline)+","+str(orderbookline)+"p' | cut -d \| -f 2 | awk '{print $1}'").read()[:-1]

#dydxmarket
def getticksize():
        global dydxticksize
        r = get(url = my_api_host+'/v3/markets')
        r.raise_for_status()
        if r.status_code == 200:
                for key, value in r.json()['markets'].items():
                        if key == dydxmarket:
                                dydxticksize = value['tickSize']
        else:
                print('Bad requests status code:', r.status_code)

#dydxmarket
def getstepsize():
        global dydxstepsize
        r = get(url = my_api_host+'/v3/markets')
        r.raise_for_status()
        if r.status_code == 200:
                for key, value in r.json()['markets'].items():
                        if key == dydxmarket:
                                dydxstepsize = value['stepSize']
        else:
                print('Bad requests status code:', r.status_code)

#orderid
def findorder():
        try:
                get_order_by_id_result = client.private.get_order_by_id(orderid)
                return get_order_by_id_result.data
        except Exception as error:
                print(error)
                return None

if len(argv) > 1 and path.isfile(argv[1]):
        exec(open(argv[1]).read())
if my_api_network_id == str(constants.NETWORK_ID_MAINNET):
        my_api_host = constants.API_HOST_MAINNET
        ramdiskpath = 'ramdisk'
        if simpleorderbook == 'y':
                orderbookprogram = 'dydxob2b.py'
                orderbookline = 3
        else:
                orderbookprogram = 'dydxob2.py'
                orderbookline = 4
elif my_api_network_id == str(constants.NETWORK_ID_GOERLI):
        my_api_host = constants.API_HOST_GOERLI
        ramdiskpath = 'ramdisk3'
        if simpleorderbook == 'y':
                orderbookprogram = 'tydxob2b.py'
                orderbookline = 3
        else:
                orderbookprogram = 'tydxob2.py'
                orderbookline = 4
else:
        print(f"Error: my_api_network_id is not {constants.NETWORK_ID_MAINNET} or {constants.NETWORK_ID_GOERLI}.")
        exit()

if my_eth_private_key != '':
        client = Client(
                host = my_api_host,
                default_ethereum_address = my_eth_address,
                eth_private_key = my_eth_private_key,
                network_id = my_api_network_id
        )
        derive_stark_key_result = client.onboarding.derive_stark_key()
        stark_private_key = derive_stark_key_result['private_key']
        client.stark_private_key = stark_private_key
else:
        client = Client(
                host = my_api_host,
                network_id = my_api_network_id,
                api_key_credentials = {
                        'key': my_api_key,
                        'secret': my_api_secret,
                        'passphrase': my_api_passphrase
                }
        )
        client.stark_private_key = my_stark_private_key

get_account_result = client.private.get_account(
        ethereum_address = my_eth_address
)
account = get_account_result.data['account']
one_minute_from_now_iso = epoch_seconds_to_iso(time.time() + 70)

if len(argv) > 2:
        command = argv[2]
else:
        command = 'balance'

if command == 'balance':
        get_accounts_result = client.private.get_accounts()
        print(get_accounts_result.data['accounts'][0]['equity'])
elif command == 'positions':
        get_positions_result = client.private.get_positions(
                status = constants.POSITION_STATUS_OPEN
        )
        for key in get_positions_result.data['positions']:
                print(key['market'].ljust(9), key['size'])
elif command == 'buyquantity':
        if len(argv) < 4:
                print('Error: Must specify market, quantity')
                exit()
        ordermarket = argv[3]
        ordersize = argv[4]
        orderside = 'BUY'
        ordertype = constants.ORDER_TYPE_MARKET
        dydxmarket = ordermarket
        getprices()
        orderprice = str(float(bestask) * 2)
        orderexpiration = epoch_seconds_to_iso(time.time() + 70)
        ordertif = 'FOK'
        print(ordermarket, orderside, ordertype, ordersize, orderprice, orderexpiration, ordertif)
        sendorder()
        print(create_order_result.data)
        print(create_order_result.headers)
        orderid = create_order_result.data['order']['id']
        time.sleep(1)
        get_order_by_id_result = client.private.get_order_by_id(orderid)
        print(get_order_by_id_result.data)
        print(get_order_by_id_result.headers)
        orderstatus = get_order_by_id_result.data['order']['status']
        print(orderstatus)
elif command == 'sellquantity':
        if len(argv) < 4:
                print('Error: Must specify market, quantity')
                exit()
        ordermarket = argv[3]
        ordersize = argv[4]
        orderside = 'SELL'
        ordertype = constants.ORDER_TYPE_MARKET
        dydxmarket = ordermarket
        if simpleorderbook == 'y':
                getticksize()
        else:
                dydxticksize = os.popen("tail -1 /mnt/"+ramdiskpath+"/dydxmarketdata/"+dydxmarket+"/tickSize").read()[:-1]
        getprices()
        orderprice = float(bestbid) / 2
        orderprice = '%g'%(orderprice - (orderprice % float(dydxticksize)))
        orderexpiration = epoch_seconds_to_iso(time.time() + 70)
        ordertif = 'FOK'
        print(ordermarket, orderside, ordertype, ordersize, orderprice, orderexpiration, ordertif)
        sendorder()
        print(create_order_result.data)
        print(create_order_result.headers)
        orderid = create_order_result.data['order']['id']
        time.sleep(1)
        get_order_by_id_result = client.private.get_order_by_id(orderid)
        print(get_order_by_id_result.data)
        print(get_order_by_id_result.headers)
        orderstatus = get_order_by_id_result.data['order']['status']
        print(orderstatus)
elif command == 'buyusdc':
        if len(argv) < 4:
                print('Error: Must specify market, USDCquantity')
                exit()
        dydxmarket = argv[3]
        getprices()
        ordermarket = argv[3]
        orderside = 'BUY'
        ordertype = constants.ORDER_TYPE_MARKET
        if simpleorderbook == 'y':
                getstepsize()
        else:
                dydxstepsize = os.popen("tail -1 /mnt/"+ramdiskpath+"/dydxmarketdata/"+dydxmarket+"/stepSize").read()[:-1]
        dydxquantity = float(argv[4]) / float(bestbid)
        dydxquantity = '%g'%(dydxquantity - (dydxquantity % float(dydxstepsize)))
        ordersize = str(dydxquantity)
        orderprice = str(float(bestask) * 2)
        orderexpiration = epoch_seconds_to_iso(time.time() + 70)
        ordertif = 'FOK'
        print(ordermarket, orderside, ordertype, ordersize, orderprice, orderexpiration, ordertif)
        sendorder()
        print(create_order_result.data)
        print(create_order_result.headers)
        orderid = create_order_result.data['order']['id']
        time.sleep(1)
        get_order_by_id_result = client.private.get_order_by_id(orderid)
        print(get_order_by_id_result.data)
        print(get_order_by_id_result.headers)
        orderstatus = get_order_by_id_result.data['order']['status']
        print(orderstatus)
elif command == 'sellusdc':
        if len(argv) < 4:
                print('Error: Must specify market, USDCquantity')
                exit()
        dydxmarket = argv[3]
        getprices()
        ordermarket = argv[3]
        orderside = 'SELL'
        ordertype = constants.ORDER_TYPE_MARKET
        if simpleorderbook == 'y':
                getticksize()
                getstepsize()
        else:
                dydxstepsize = os.popen("tail -1 /mnt/"+ramdiskpath+"/dydxmarketdata/"+dydxmarket+"/stepSize").read()[:-1]
                dydxticksize = os.popen("tail -1 /mnt/"+ramdiskpath+"/dydxmarketdata/"+dydxmarket+"/tickSize").read()[:-1]
        dydxquantity = float(argv[4]) / float(bestbid)
        dydxquantity = '%g'%(dydxquantity - (dydxquantity % float(dydxstepsize)))
        ordersize = str(dydxquantity)
        orderprice = float(bestbid) / 2
        orderprice = '%g'%(orderprice - (orderprice % float(dydxticksize)))
        orderexpiration = epoch_seconds_to_iso(time.time() + 70)
        ordertif = 'FOK'
        print(ordermarket, orderside, ordertype, ordersize, orderprice, orderexpiration, ordertif)
        sendorder()
        print(create_order_result.data)
        print(create_order_result.headers)
        orderid = create_order_result.data['order']['id']
        time.sleep(1)
        get_order_by_id_result = client.private.get_order_by_id(orderid)
        print(get_order_by_id_result.data)
        print(get_order_by_id_result.headers)
        orderstatus = get_order_by_id_result.data['order']['status']
        print(orderstatus)
elif command == 'getorder':
        if len(argv) < 3:
                print('Error: Must specify orderid')
                exit()
        orderid = argv[3]
        order = findorder()
        print(order)
