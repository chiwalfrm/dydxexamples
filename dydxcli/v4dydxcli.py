import os
import sys
import time
from datetime import datetime
from dateutil.parser import isoparse
from os import path
from random import randrange
from requests import get
from sys import argv, maxsize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/v4-clients/v4-client-py')
from v4_client_py import chain
from v4_client_py import clients
from v4_client_py.clients.constants import Network
MAX_CLIENT_ID = 2 ** 32 - 1

import pprint
pp = pprint.PrettyPrinter(width = 41, compact = True)

counterlimit = 10

########################## YOU FILL THIS OUT #################
DYDX_TEST_MNEMONIC = '<FILL_THIS_OUT>'
#INDEXERURL = 'https://indexer.dydx.trade/v4'
INDEXERURL = 'https://indexer.v4testnet.dydx.exchange/v4'
##############################################################

#ordermarket/orderside/ordertype/ordersize/orderprice/orderexpiration/ordertif/clientid/good_til_block_value
def sendorder():
        global place_order_result
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' sendorder()')
        try:
                place_order_result = client.place_order(
                        wallet,
                        market = ordermarket,
                        type = ordertype,
                        side = orderside,
                        price = orderprice,
                        size = ordersize,
                        client_id = clientid,
                        time_in_force = ordertif,
                        good_til_block = good_til_block_value,
                        good_til_time_in_seconds = orderexpiration,
                        execution = clients.helpers.chain_helpers.OrderExecution.DEFAULT,
                        post_only = False,
                        reduce_only = False
                )
        except Exception as error:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "api query failed (%s)" % error)

#dydxmarket
def getprices():
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
        except Exception as error:
                print('Market not found', dydxmarket)
                return None

#dydxmarket
def getticksize():
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
                print('Market not found', dydxmarket)
                return None

#dydxmarket
def getstepsize():
        global dydxstepsize
        r = get(url = INDEXERURL+'/perpetualMarkets', params = {
                'ticker': dydxmarket
        })
        try:
                r.raise_for_status()
                if r.status_code == 200:
                        dydxstepsize = r.json()['markets'][dydxmarket]['stepSize']
                else:
                        print('Bad requests status code:', r.status_code)
        except Exception as error:
                print('Market not found', dydxmarket)
                return None

#clientid
#walletaddress
def findorder():
        order = findordera()
        if order == None:
                order = findorderb()
        return order

def findordera():
        counter = 0
        print('Searching short-term orders...')
        subaccountlist = getsubaccounts()
        for subaccountnumber in subaccountlist:
                if len(subaccountlist) > 1:
                        print('Searching subaccount', str(subaccountnumber)+'...')
                height = maxsize
                newheight = 0
                while newheight < height:
                        if counter > counterlimit:
                                #reached counterlimit, move to next subaccount
                                break
                        try:
                                get_subaccount_orders_result = client.indexer_client.account.get_subaccount_orders(
                                        address = walletaddress,
                                        subaccount_number = subaccountnumber,
                                        good_til_block_before_or_at = height,
                                        return_latest_orders = True
                                )
                                if len(get_subaccount_orders_result.data) > 0:
                                        if len(get_subaccount_orders_result.data) > 1:
                                                topheight = get_subaccount_orders_result.data[0]['createdAtHeight']
                                                newheight = get_subaccount_orders_result.data[-1]['createdAtHeight']
                                                if topheight == newheight:
                                                        print('Error: more than 100 records with the same createdAtHeight', topheight)
                                                        #move to next subaccount
                                                        break
                                        for item in get_subaccount_orders_result.data:
                                                if item['clientId'] == str(clientid):
                                                        return item
                                        if int(newheight) < height:
                                                height = int(newheight) - 1
                                                newheight = 0
                                                counter += 1
                                        else:
                                                #end of results, move to next subaccount
                                                break
                                else:
                                        #no results, move to next subaccount
                                        break
                        except Exception as error:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "api query failed (%s)" % error)
                                return None

#clientid
#walletaddress
def findorderb():
        counter = 0
        print('Searching long-term orders...')
        subaccountlist = getsubaccounts()
        for subaccountnumber in subaccountlist:
                if len(subaccountlist) > 1:
                        print('Searching subaccount', str(subaccountnumber)+'...')
                height = isoparse('9999-12-31T23:59:59.999Z').timestamp()
                newheight = 0
                while newheight < height:
                        if counter > counterlimit:
                                #reached counterlimit, move to next subaccount
                                break
                        try:
                                get_subaccount_orders_result = client.indexer_client.account.get_subaccount_orders(
                                        address = walletaddress,
                                        subaccount_number = subaccountnumber,
                                        good_til_block_time_before_or_at = datetime.utcfromtimestamp(height).isoformat()[:-3]+'Z',
                                        return_latest_orders = True
                                )
                                if len(get_subaccount_orders_result.data) > 0:
                                        if len(get_subaccount_orders_result.data) > 1:
                                                topheight = isoparse(get_subaccount_orders_result.data[0]['goodTilBlockTime']).timestamp()
                                                newheight = isoparse(get_subaccount_orders_result.data[-1]['goodTilBlockTime']).timestamp()
                                                if topheight == newheight:
                                                        print('Error: more than 100 records with the same goodTilBlockTime', topheight)
                                                        #move to next subaccount
                                                        break
                                        for item in get_subaccount_orders_result.data:
                                                if item['clientId'] == str(clientid):
                                                        return item
                                        if newheight < height:
                                                height = newheight - 0.001
                                                newheight = 0
                                                counter += 1
                                        else:
                                                #end of results, move to next subaccount
                                                break
                                else:
                                        #no results, move to next subaccount
                                        break
                        except Exception as error:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "api query failed (%s)" % error)
                                return None

#clientid
#walletaddress
def findorder2():
        order = findorder2a()
        if order == None:
                order = findorder2b()
        return order

#clientid
#walletaddress
def findorder2a():
        counter = 0
        print('Searching short-term orders...')
        subaccountlist = getsubaccounts()
        for subaccountnumber in subaccountlist:
                if len(subaccountlist) > 1:
                        print('Searching subaccount', str(subaccountnumber)+'...')
                height = maxsize
                newheight = 0
                while newheight < height:
                        if counter > counterlimit:
                                #reached counterlimit, move to next subaccount
                                break
                        r = get(INDEXERURL+'/orders', params = {
                                'address': walletaddress,
                                'subaccountNumber': subaccountnumber,
                                'return_latest_orders': True,
                                'goodTilBlockBeforeOrAt': height,
                        })
                        try:
                                r.raise_for_status()
                                if r.status_code == 200:
                                        if len(r.json()) > 0:
                                                if len(r.json()) > 1:
                                                        topheight = r.json()[0]['createdAtHeight']
                                                        newheight = r.json()[-1]['createdAtHeight']
                                                        if topheight == newheight:
                                                                print('Error: more than 100 records with the same createdAtHeight', topheight)
                                                                #move to next subaccount
                                                                break
                                                for item in r.json():
                                                        if item['clientId'] == str(clientid):
                                                                return item
                                                if int(newheight) < height:
                                                        height = int(newheight) - 1
                                                        newheight = 0
                                                        counter += 1
                                                else:
                                                        #end of results, move to next subaccount
                                                        break
                                        else:
                                                #no results, move to next subaccount
                                                break
                                else:
                                        print('Bad requests status code:', r.status_code)
                                        return None
                        except Exception as error:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "api query failed (%s)" % error)
                                return None

#clientid
#walletaddress
def findorder2b():
        counter = 0
        print('Searching long-term orders...')
        subaccountlist = getsubaccounts()
        for subaccountnumber in subaccountlist:
                if len(subaccountlist) > 1:
                        print('Searching subaccount', str(subaccountnumber)+'...')
                height = isoparse('9999-12-31T23:59:59.999Z').timestamp()
                newheight = 0
                while newheight < height:
                        if counter > counterlimit:
                                #reached counterlimit, move to next subaccount
                                break
                        r = get(INDEXERURL+'/orders', params = {
                                'address': walletaddress,
                                'subaccountNumber': subaccountnumber,
                                'return_latest_orders': True,
                                'goodTilBlockTimeBeforeOrAt': datetime.utcfromtimestamp(height).isoformat()[:-3]+'Z',
                        })
                        try:
                                r.raise_for_status()
                                if r.status_code == 200:
                                        if len(r.json()) > 0:
                                                if len(r.json()) > 1:
                                                        topheight = isoparse(r.json()[0]['goodTilBlockTime']).timestamp()
                                                        newheight = isoparse(r.json()[-1]['goodTilBlockTime']).timestamp()
                                                        if topheight == newheight:
                                                                print('Error: more than 100 records with the same goodTilBlockTime', topheight)
                                                                #move to next subaccount
                                                                break
                                                for item in r.json():
                                                        if item['clientId'] == str(clientid):
                                                                return item
                                                if newheight < height:
                                                        height = newheight - 0.001
                                                        newheight = 0
                                                        counter += 1
                                                else:
                                                        #end of results, move to next subaccount
                                                        break
                                        else:
                                                #no results, move to next subaccount
                                                break
                                else:
                                        print('Bad requests status code:', r.status_code)
                                        return None
                        except Exception as error:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "api query failed (%s)" % error)
                                return None

#orderid
def findorderid():
        try:
                get_order_result = client.indexer_client.account.get_order(orderid)
                return get_order_result.data
        except Exception as error:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "api query failed (%s)" % error)

#orderid
def findorderid2():
        r = get(INDEXERURL+'/orders/'+orderid)
        try:
                r.raise_for_status()
                if r.status_code == 200:
                        return r.json()
                else:
                        print('Bad requests status code:', r.status_code)
        except Exception as error:
                print('Order not found', orderid)
                return None

#walletaddress
def getsubaccounts():
        subaccountslist = []
        r = get(INDEXERURL+'/addresses/'+walletaddress)
        try:
                r.raise_for_status()
                if r.status_code == 200:
                        for item in r.json()['subaccounts']:
                                subaccountslist.append(item['subaccountNumber'])
                        return subaccountslist
                else:
                        print('Bad requests status code:', r.status_code)
        except Exception as error:
                print('Address not found', walletaddress)
                return None

#walletaddress
def getbalance():
        try:
                subaccounts_response = client.indexer_client.account.get_subaccounts(walletaddress)
                for item in subaccounts_response.data['subaccounts']:
                        print(item['address']+':'+str(item['subaccountNumber']), item['equity'])
        except Exception as error:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "api query failed (%s)" % error)

#walletaddress
def getbalance2():
        r = get(INDEXERURL+'/addresses/'+walletaddress)
        try:
                if r.status_code == 200:
                        for item in r.json()['subaccounts']:
                                print(item['address']+':'+str(item['subaccountNumber']), item['equity'])
                else:
                        print('Bad requests status code:', r.status_code)
        except Exception as error:
                print('Address not found', walletaddress)

#walletaddress
def getpositions():
        try:
                subaccounts_response = client.indexer_client.account.get_subaccounts(walletaddress)
                for item in subaccounts_response.data['subaccounts']:
                        for key, value in item['openPerpetualPositions'].items():
                                print(item['address']+':'+str(item['subaccountNumber']), key.ljust(9), value['size'])
        except Exception as error:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "api query failed (%s)" % error)

#walletaddress
def getpositions2():
        r = get(INDEXERURL+'/addresses/'+walletaddress)
        try:
                if r.status_code == 200:
                        for item in r.json()['subaccounts']:
                                for key, value in item['openPerpetualPositions'].items():
                                        print(item['address']+':'+str(item['subaccountNumber']), key.ljust(9), value['size'])
                else:
                        print('Bad requests status code:', r.status_code)
        except Exception as error:
                print('Address not found', walletaddress)

#walletaddress
def getpositions3():
        counter = 0
        subaccountlist = getsubaccounts()
        for subaccountnumber in subaccountlist:
                if len(subaccountlist) > 1:
                        print('Searching subaccount', str(subaccountnumber)+'...')
                r = get(INDEXERURL+'/height')
                try:
                        if r.status_code == 200:
                                height = r.json()['height']
                                newheight = 0
                                while int(newheight) < int(height):
                                        if counter > counterlimit:
                                                #reached counterlimit, move to next subaccount
                                                break
                                        r = get(INDEXERURL+'/perpetualPositions', params = {
                                                'address': walletaddress,
                                                'subaccountNumber': subaccountnumber,
                                                'status': 'OPEN',
                                                'createdBeforeOrAtHeight': height
                                        })
                                        try:
                                                r.raise_for_status()
                                                if r.status_code == 200:
                                                        if len(r.json()['positions']) > 0:
                                                                if len(r.json()['positions']) == 100:
                                                                        topheight = r.json()['positions'][0]['createdAtHeight']
                                                                        newheight = r.json()['positions'][-1]['createdAtHeight']
                                                                        if topheight == newheight:
                                                                               print('Error: more than 100 records with the same createdAtHeight', topheight)
                                                                               #move to next subaccount
                                                                               break
                                                                for item in r.json()['positions']:
                                                                        print(walletaddress+':'+str(subaccountnumber), item['market'].ljust(9), item['size'])
                                                                if int(newheight) < int(height):
                                                                        height = int(newheight) - 1
                                                                        newheight = 0
                                                                        counter += 1
                                                                else:
                                                                        #end of results, move to next subaccount
                                                                        break
                                                        else:
                                                                #no results, move to next subaccount
                                                                break
                                                else:
                                                        print('Bad requests status code:', r.status_code)
                                        except Exception as error:
                                                print('Address not found', walletaddress)
                        else:
                                print('Bad requests status code:', r.status_code)
                except Exception as error:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "api query failed (%s)" % error)

def getpositions4():
        counter = 0
        subaccountlist = getsubaccounts()
        for subaccountnumber in subaccountlist:
                if len(subaccountlist) > 1:
                        print('Searching subaccount', str(subaccountnumber)+'...')
                r = get(INDEXERURL+'/height')
                try:
                        if r.status_code == 200:
                                height = r.json()['height']
                                newheight = 0
                                while int(newheight) < int(height):
                                        if counter > counterlimit:
                                                #reached counterlimit, move to next subaccount
                                                break
                                        try:
                                                get_subaccount_perpetual_positions_result = client.indexer_client.account.get_subaccount_perpetual_positions(
                                                        address = walletaddress,
                                                        subaccount_number = subaccountnumber,
                                                        status = 'OPEN',
                                                        created_before_or_at_height = height
                                                )
                                                if len(get_subaccount_perpetual_positions_result.data['positions']) > 0:
                                                        if len(get_subaccount_perpetual_positions_result.data['positions']) == 100:
                                                                topheight = get_subaccount_perpetual_positions_result.data['positions'][0]['createdAtHeight']
                                                                newheight = get_subaccount_perpetual_positions_result.data['positions'][-1]['createdAtHeight']
                                                                if topheight == newheight:
                                                                        print('Error: more than 100 records with the same createdAtHeight', topheight)
                                                                        #move to next subaccount
                                                                        break
                                                        for item in get_subaccount_perpetual_positions_result.data['positions']:
                                                                print(walletaddress+':'+str(subaccountnumber), item['market'].ljust(9), item['size'])
                                                        if int(newheight) < int(height):
                                                                height = int(newheight) - 1
                                                                newheight = 0
                                                                counter += 1
                                                        else:
                                                                #end of results, move to next subaccount
                                                                break
                                                else:
                                                        #no results, move to next subaccount
                                                        break
                                        except Exception as error:
                                                print('Address not found', walletaddress)
                        else:
                                print('Bad requests status code:', r.status_code)
                except Exception as error:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "api query failed (%s)" % error)

if len(argv) > 1 and path.isfile(argv[1]):
        exec(open(argv[1]).read())

wallet = clients.Subaccount.from_mnemonic(DYDX_TEST_MNEMONIC)
network = Network.config_network()
client = clients.CompositeClient(
        network,
)
if len(argv) > 2:
        command = argv[2]
else:
        command = 'balance'

if command == 'balance':
#note: two ways to get balance getbalance() and getbalance2()
        if len(argv) > 3:
                for walletaddress in argv[3:]:
#                       getbalance()
                        getbalance2()
        else:
                walletaddress = wallet.address
#               getbalance()
                getbalance2()
elif command == 'positions':
#note: four ways to get positions getposition(), getposition2(), getposition3(), and getposition4()
        if len(argv) > 3:
                for walletaddress in argv[3:]:
#                       getpositions()
#                       getpositions2()
#                       getpositions3()
                        getpositions4()
        else:
                walletaddress = wallet.address
#               getpositions()
#               getpositions2()
#               getpositions3()
                getpositions4()
elif command == 'buyquantity':
        if len(argv) < 4:
                print('Error: Must specify market, quantity')
                exit()
        ordermarket = argv[3]
        ordersize = float(argv[4])
        orderside = clients.helpers.chain_helpers.OrderSide.BUY
        ordertype = clients.helpers.chain_helpers.OrderType.MARKET
        dydxmarket = ordermarket
        getprices()
        orderprice = float(bestask) * 2
        orderexpiration = 0
        ordertif = clients.helpers.chain_helpers.OrderTimeInForce.GTT
        clientid = randrange(0, 2**31 - 1) #random number between 0 and max(int32) inclusive
        latest_block = client.validator_client.get.latest_block()
        good_til_block_value = latest_block.block.header.height + 1 + 10
        print(ordermarket, orderside, ordertype, ordersize, orderprice, orderexpiration, ordertif, clientid, good_til_block_value)
        sendorder()
        print('client_id       :', clientid)
        print('tx_hash         :', place_order_result.tx_hash)
        print('response        :', place_order_result.response)
        print('contract_code_id:', place_order_result.contract_code_id)
        print('contract_address:', place_order_result.contract_address)
        walletaddress = wallet.address
        counter2=0
        while counter2 < 10:
                try:
#                       order = findordera()
                        order = findorder2a()
                        print(order['status'])
                        break
                except Exception as error:
                        print('Waiting 1 second for order to be visible.')
                        time.sleep(1)
                counter2 += 1
elif command == 'sellquantity':
        if len(argv) < 4:
                print('Error: Must specify market, quantity')
                exit()
        ordermarket = argv[3]
        ordersize = float(argv[4])
        orderside = clients.helpers.chain_helpers.OrderSide.SELL
        ordertype = clients.helpers.chain_helpers.OrderType.MARKET
        dydxmarket = ordermarket
        getticksize()
        getprices()
        orderprice = float(bestbid) / 2
        orderprice = float('%g'%(orderprice - (orderprice % float(dydxticksize))))
        orderexpiration = 0
        ordertif = clients.helpers.chain_helpers.OrderTimeInForce.IOC
        clientid = randrange(0, 999999999) #random number between 0 and 999,999,999 inclusive
        latest_block = client.validator_client.get.latest_block()
        good_til_block_value = latest_block.block.header.height + 1 + 10
        print(ordermarket, orderside, ordertype, ordersize, orderprice, orderexpiration, ordertif, clientid, good_til_block_value)
        sendorder()
        print('client_id       :', clientid)
        print('tx_hash         :', place_order_result.tx_hash)
        print('response        :', place_order_result.response)
        print('contract_code_id:', place_order_result.contract_code_id)
        print('contract_address:', place_order_result.contract_address)
        walletaddress = wallet.address
        counter2=0
        while counter2 < 10:
                try:
#                       order = findordera()
                        order = findorder2a()
                        print(order['status'])
                        break
                except Exception as error:
                        print('Waiting 1 second for order to be visible.')
                        time.sleep(1)
                counter2 += 1
elif command == 'buyusdc':
        if len(argv) < 4:
                print('Error: Must specify market, USDCquantity')
                exit()
        dydxmarket = argv[3]
        getprices()
        ordermarket = argv[3]
        orderside = clients.helpers.chain_helpers.OrderSide.BUY
        ordertype = clients.helpers.chain_helpers.OrderType.MARKET
        getstepsize()
        dydxquantity = float(argv[4]) / float(bestbid)
        dydxquantity = float('%g'%(dydxquantity - (dydxquantity % float(dydxstepsize))))
        ordersize = dydxquantity
        orderprice = float(bestask) * 2
        orderexpiration = 0
        ordertif = clients.helpers.chain_helpers.OrderTimeInForce.IOC
        clientid = randrange(0, 999999999) #random number between 0 and 999,999,999 inclusive
        latest_block = client.validator_client.get.latest_block()
        good_til_block_value = latest_block.block.header.height + 1 + 10
        print(ordermarket, orderside, ordertype, ordersize, orderprice, orderexpiration, ordertif, clientid, good_til_block_value)
        sendorder()
        print('client_id       :', clientid)
        print('tx_hash         :', place_order_result.tx_hash)
        print('response        :', place_order_result.response)
        print('contract_code_id:', place_order_result.contract_code_id)
        print('contract_address:', place_order_result.contract_address)
        walletaddress = wallet.address
        counter2=0
        while counter2 < 10:
                try:
#                       order = findordera()
                        order = findorder2a()
                        print(order['status'])
                        break
                except Exception as error:
                        print('Waiting 1 second for order to be visible.')
                        time.sleep(1)
                counter2 += 1
elif command == 'sellusdc':
        if len(argv) < 4:
                print('Error: Must specify market, USDCquantity')
                exit()
        dydxmarket = argv[3]
        getprices()
        ordermarket = argv[3]
        orderside = clients.helpers.chain_helpers.OrderSide.SELL
        ordertype = clients.helpers.chain_helpers.OrderType.MARKET
        getticksize()
        getstepsize()
        dydxquantity = float(argv[4]) / float(bestbid)
        dydxquantity = float('%g'%(dydxquantity - (dydxquantity % float(dydxstepsize))))
        ordersize = dydxquantity
        orderprice = float(bestbid) / 2
        orderprice = float('%g'%(orderprice - (orderprice % float(dydxticksize))))
        orderexpiration = 0
        ordertif = clients.helpers.chain_helpers.OrderTimeInForce.IOC
        clientid = randrange(0, 999999999) #random number between 0 and 999,999,999 inclusive
        latest_block = client.validator_client.get.latest_block()
        good_til_block_value = latest_block.block.header.height + 1 + 10
        print(ordermarket, orderside, ordertype, ordersize, orderprice, orderexpiration, ordertif, clientid, good_til_block_value)
        sendorder()
        print('client_id       :', clientid)
        print('tx_hash         :', place_order_result.tx_hash)
        print('response        :', place_order_result.response)
        print('contract_code_id:', place_order_result.contract_code_id)
        print('contract_address:', place_order_result.contract_address)
        walletaddress = wallet.address
        counter2=0
        while counter2 < 10:
                try:
#                       order = findordera()
                        order = findorder2a()
                        print(order['status'])
                        break
                except Exception as error:
                        print('Waiting 1 second for order to be visible.')
                        time.sleep(1)
                counter2 += 1
elif command == 'getorder':
        if len(argv) < 4:
                print('Error: Must specify [short-term|long-term|both] clientid')
                exit()
        elif len(argv) > 4:
                searchtype = argv[3]
                clientid = argv[4]
        else:
                searchtype = 'both'
                clientid = argv[3]
        walletaddress = wallet.address
        if searchtype == 'short-term':
#               order = findordera()
                order = findorder2a()
        elif searchtype == 'long-term':
#               order = findorderb()
                order = findorder2b()
        else:
#               order = findorder()
                order = findorder2()
        print(order)
elif command == 'getorderid':
        if len(argv) < 3:
                print('Error: Must specify orderid')
                exit()
        orderid = argv[3]
#       order = findorderid()
        order = findorderid2()
        print(order)
elif command == 'buyquantitylimit':
        if len(argv) < 6:
                print('Error: Must specify market, quantity, limit, seconds')
                exit()
        ordermarket = argv[3]
        ordersize = float(argv[4])
        orderprice = float(argv[5])
        orderseconds = int(argv[6])
        orderside = clients.helpers.chain_helpers.OrderSide.BUY
        ordertype = clients.helpers.chain_helpers.OrderType.LIMIT
        orderexpiration = orderseconds
        ordertif = clients.helpers.chain_helpers.OrderTimeInForce.GTT
        clientid = randrange(0, 2**31 - 1) #random number between 0 and max(int32) inclusive
        good_til_block_value = 0
        print(ordermarket, orderside, ordertype, ordersize, orderprice, orderexpiration, ordertif, clientid, good_til_block_value)
        sendorder()
        print('client_id       :', clientid)
        print('tx_hash         :', place_order_result.tx_hash)
        print('response        :', place_order_result.response)
        print('contract_code_id:', place_order_result.contract_code_id)
        print('contract_address:', place_order_result.contract_address)
        walletaddress = wallet.address
        counter2=0
        while counter2 < 10:
                try:
#                       order = findorderb()
                        order = findorder2b()
                        print(order['status'])
                        break
                except Exception as error:
                        print('Waiting 1 second for order to be visible.')
                        time.sleep(1)
                counter2 += 1
elif command == 'sellquantitylimit':
        if len(argv) < 6:
                print('Error: Must specify market, quantity, limit, seconds')
                exit()
        ordermarket = argv[3]
        ordersize = float(argv[4])
        orderprice = float(argv[5])
        orderseconds = int(argv[6])
        orderside = clients.helpers.chain_helpers.OrderSide.SELL
        ordertype = clients.helpers.chain_helpers.OrderType.LIMIT
        orderexpiration = orderseconds
        ordertif = clients.helpers.chain_helpers.OrderTimeInForce.GTT
        clientid = randrange(0, 999999999) #random number between 0 and 999,999,999 inclusive
        good_til_block_value = 0
        print(ordermarket, orderside, ordertype, ordersize, orderprice, orderexpiration, ordertif, clientid, good_til_block_value)
        sendorder()
        print('client_id       :', clientid)
        print('tx_hash         :', place_order_result.tx_hash)
        print('response        :', place_order_result.response)
        print('contract_code_id:', place_order_result.contract_code_id)
        print('contract_address:', place_order_result.contract_address)
        walletaddress = wallet.address
        counter2=0
        while counter2 < 10:
                try:
#                       order = findorderb()
                        order = findorder2b()
                        print(order['status'])
                        break
                except Exception as error:
                        print('Waiting 1 second for order to be visible.')
                        time.sleep(1)
                counter2 += 1
