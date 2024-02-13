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
from v4_client_py import clients
from v4_client_py.clients import constants
from v4_client_py.clients.constants import Network, CHAIN_ID

counterlimit = 10

########################## YOU FILL THIS OUT #################
DYDX_TEST_MNEMONIC = '<FILL_THIS_OUT>'
simpleorderbook = 'y'
#simpleorderbook should be set to 'y' unless you are running my orderbook software and the data is available in /mnt/<ramdisk>
#https://github.com/chiwalfrm/dydxexamples/tree/main/v4orderbook
##############################################################

#dydxmarket/orderside/ordertype/ordersize/orderprice/orderexpiration/ordertif/clientid/good_til_block_value
def sendorder():
        global place_order_result
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' sendorder()')
        try:
                place_order_result = client.place_order(
                        wallet,
                        market = dydxmarket,
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
        count = 0
        global bestbid
        global bestask
        try:
                r = get(url = INDEXERURL+'/orderbooks/perpetualMarket/'+dydxmarket)
                r.raise_for_status()
                if r.status_code == 200:
                        bestbid = r.json()['bids'][0]['price']
                        bestask = r.json()['asks'][0]['price']
                        return 0
                else:
                        print('Bad requests status code:', r.status_code)
                        count += 1
                        if count > 9:
                                print('getprices() Market not found', dydxmarket)
                                return None
        except Exception as error:
                count += 1
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "api query failed (%s)" % error)
                print('getprices() exception, will retry... count='+str(count))
                if count > 9:
                        print('getprices() Market not found', dydxmarket)
                        return None

#dydxmarket
def getticksize():
        count = 0
        try:
                r = get(url = INDEXERURL+'/perpetualMarkets', params = {
                        'ticker': dydxmarket
                })
                r.raise_for_status()
                if r.status_code == 200:
                        return r.json()['markets'][dydxmarket]['tickSize']
                else:
                        print('Bad requests status code:', r.status_code)
                        count += 1
                        if count > 9:
                                print('getticksize() Market not found', dydxmarket)
                                return None
        except Exception as error:
                count += 1
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "api query failed (%s)" % error)
                print('getticksize() exception, will retry... count='+str(count))
                if count > 9:
                        print('getticksize() Market not found', dydxmarket)
                        return None

#dydxmarket
def getstepsize():
        count = 0
        try:
                r = get(url = INDEXERURL+'/perpetualMarkets', params = {
                        'ticker': dydxmarket
                })
                r.raise_for_status()
                if r.status_code == 200:
                        return r.json()['markets'][dydxmarket]['stepSize']
                else:
                        print('Bad requests status code:', r.status_code)
                        count += 1
                        if count > 9:
                                print('getstepsize() Market not found', dydxmarket)
                                return None
        except Exception as error:
                count += 1
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "api query failed (%s)" % error)
                print('getstepsize() exception, will retry... count='+str(count))
                if count > 9:
                        print('getstepsize() Market not found', dydxmarket)
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
        print('findordera() Searching short-term orders...')
        subaccountlist = getsubaccounts()
        for subaccountnumber in subaccountlist:
                if len(subaccountlist) > 1:
                        print('Searching subaccount', str(subaccountnumber)+'...')
#               height = maxsize
#               height limited to 2147483647 for 32-bit OS, equivalent to 2038-01-19T03:14Z
                height = 2147483647
                newheight = 0
                while newheight < height:
                        if counter > counterlimit:
                                #reached counterlimit, move to next subaccount
                                break
                        try:
                                if clientid == constants.ORDER_STATUS_OPEN or clientid == constants.ORDER_STATUS_FILLED or clientid == constants.ORDER_STATUS_CANCELED or clientid == constants.ORDER_STATUS_UNTRIGGERED:
                                        get_subaccount_orders_result = client.indexer_client.account.get_subaccount_orders(
                                                address = walletaddress,
                                                subaccount_number = subaccountnumber,
                                                good_til_block_before_or_at = height,
                                                return_latest_orders = True,
                                                status = clientid
                                        )
                                else:
                                        get_subaccount_orders_result = client.indexer_client.account.get_subaccount_orders(
                                                address = walletaddress,
                                                subaccount_number = subaccountnumber,
                                                good_til_block_before_or_at = height,
                                                return_latest_orders = True,
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
                                                if clientid == constants.ORDER_STATUS_OPEN or clientid == constants.ORDER_STATUS_FILLED or clientid == constants.ORDER_STATUS_CANCELED or clientid == constants.ORDER_STATUS_UNTRIGGERED:
                                                        print(item)
                                                else:
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
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "findordera() api query failed (%s)" % error)
                                return None

#clientid
#walletaddress
def findorderb():
        counter = 0
        print('findorderb() Searching long-term orders...')
        subaccountlist = getsubaccounts()
        for subaccountnumber in subaccountlist:
                if len(subaccountlist) > 1:
                        print('Searching subaccount', str(subaccountnumber)+'...')
#               height = isoparse('9999-12-31T23:59:59.999Z').timestamp()
#               height limited to 2147483647 for 32-bit OS, equivalent to 2038-01-19T03:14Z
                height = isoparse('2038-01-19T03:14Z').timestamp()
                newheight = 0
                while newheight < height:
                        if counter > counterlimit:
                                #reached counterlimit, move to next subaccount
                                break
                        try:
                                if clientid == constants.ORDER_STATUS_OPEN or clientid == constants.ORDER_STATUS_FILLED or clientid == constants.ORDER_STATUS_CANCELED or clientid == constants.ORDER_STATUS_UNTRIGGERED:
                                        get_subaccount_orders_result = client.indexer_client.account.get_subaccount_orders(
                                                address = walletaddress,
                                                subaccount_number = subaccountnumber,
                                                good_til_block_time_before_or_at = datetime.utcfromtimestamp(height).isoformat()[:-3]+'Z',
                                                return_latest_orders = True,
                                                status = clientid
                                        )
                                else:
                                        get_subaccount_orders_result = client.indexer_client.account.get_subaccount_orders(
                                                address = walletaddress,
                                                subaccount_number = subaccountnumber,
                                                good_til_block_time_before_or_at = datetime.utcfromtimestamp(height).isoformat()[:-3]+'Z',
                                                return_latest_orders = True,
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
                                                if clientid == constants.ORDER_STATUS_OPEN or clientid == constants.ORDER_STATUS_FILLED or clientid == constants.ORDER_STATUS_CANCELED or clientid == constants.ORDER_STATUS_UNTRIGGERED:
                                                        print(item)
                                                else:
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
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "findorderb() api query failed (%s)" % error)
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
        print('findorder2a() Searching short-term orders...')
        subaccountlist = getsubaccounts()
        for subaccountnumber in subaccountlist:
                if len(subaccountlist) > 1:
                        print('Searching subaccount', str(subaccountnumber)+'...')
#               height = maxsize
#               height limited to 2147483647 for 32-bit OS, equivalent to 2038-01-19T03:14Z
                height = 2147483647
                newheight = 0
                while newheight < height:
                        if counter > counterlimit:
                                #reached counterlimit, move to next subaccount
                                break
                        if clientid == constants.ORDER_STATUS_OPEN or clientid == constants.ORDER_STATUS_FILLED or clientid == constants.ORDER_STATUS_CANCELED or clientid == constants.ORDER_STATUS_UNTRIGGERED:
                                r = get(INDEXERURL+'/orders', params = {
                                        'address': walletaddress,
                                        'subaccountNumber': subaccountnumber,
                                        'return_latest_orders': True,
                                        'goodTilBlockBeforeOrAt': height,
                                        'status': clientid
                                })
                        else:
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
                                                        if clientid == constants.ORDER_STATUS_OPEN or clientid == constants.ORDER_STATUS_FILLED or clientid == constants.ORDER_STATUS_CANCELED or clientid == constants.ORDER_STATUS_UNTRIGGERED:
                                                                print(item)
                                                        else:
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
                                        print('findorder2a() Bad requests status code:', r.status_code)
                                        return None
                        except Exception as error:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "findorder2a() api query failed (%s)" % error)
                                return None

#clientid
#walletaddress
def findorder2b():
        if command == 'cancelorder':
                global itemlist
                itemlist = []
        counter = 0
        print('findorder2b() Searching long-term orders...')
        subaccountlist = getsubaccounts()
        for subaccountnumber in subaccountlist:
                if len(subaccountlist) > 1:
                        print('Searching subaccount', str(subaccountnumber)+'...')
#               height = isoparse('9999-12-31T23:59:59.999Z').timestamp()
#               height limited to 2147483647 for 32-bit OS, equivalent to 2038-01-19T03:14Z
                height = isoparse('2038-01-19T03:14Z').timestamp()
                newheight = 0
                while newheight < height:
                        if counter > counterlimit:
                                #reached counterlimit, move to next subaccount
                                break
                        if clientid == constants.ORDER_STATUS_OPEN or clientid == constants.ORDER_STATUS_FILLED or clientid == constants.ORDER_STATUS_CANCELED or clientid == constants.ORDER_STATUS_UNTRIGGERED:
                                r = get(INDEXERURL+'/orders', params = {
                                        'address': walletaddress,
                                        'subaccountNumber': subaccountnumber,
                                        'return_latest_orders': True,
                                        'goodTilBlockTimeBeforeOrAt': datetime.utcfromtimestamp(height).isoformat()[:-3]+'Z',
                                        'status': clientid
                                })
                        else:
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
                                                        if clientid == constants.ORDER_STATUS_OPEN or clientid == constants.ORDER_STATUS_FILLED or clientid == constants.ORDER_STATUS_CANCELED or clientid == constants.ORDER_STATUS_UNTRIGGERED:
                                                                print(item)
                                                                if command == 'cancelorder':
                                                                        itemlist.append(item)
                                                        else:
                                                                if item['clientId'] == str(clientid):
                                                                        return item
                                                if command == 'cancelorder':
                                                        return itemlist
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
                                        print('findorder2b() Bad requests status code:', r.status_code)
                                        return None
                        except Exception as error:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "findorder2b() api query failed (%s)" % error)
                                return None

#orderid
def findorderid():
        try:
                get_order_result = client.indexer_client.account.get_order(orderid)
                return get_order_result.data
        except Exception as error:
                print('findorderid() Order not found', orderid)
                return None

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
                print('findorderid2() Order not found', orderid)
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
                print('getsubaccounts() Address not found', walletaddress)
                return None

#walletaddress
def getbalance():
        try:
                subaccounts_response = client.indexer_client.account.get_subaccounts(walletaddress)
                for item in subaccounts_response.data['subaccounts']:
                        if subaccount == 'all':
                                print(item['address']+':'+str(item['subaccountNumber']), item['equity'])
                        elif int(subaccount) == item['subaccountNumber']:
                                print(item['address']+':'+str(item['subaccountNumber']), item['equity'])
                                return item['equity']
        except Exception as error:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "api query failed (%s)" % error)

#walletaddress
def getbalance2():
        r = get(INDEXERURL+'/addresses/'+walletaddress)
        try:
                if r.status_code == 200:
                        for item in r.json()['subaccounts']:
                                if subaccount == 'all':
                                        print(item['address']+':'+str(item['subaccountNumber']), item['equity'])
                                elif int(subaccount) == item['subaccountNumber']:
                                        print(item['address']+':'+str(item['subaccountNumber']), item['equity'])
                                        return item['equity']
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
                                                'status': constants.ORDER_STATUS_OPEN,
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
                                                        status = constants.ORDER_STATUS_OPEN,
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

def checkorder():
        print('client_id       :', clientid)
        print('tx_hash         :', place_order_result.tx_hash)
        print('response        :', place_order_result.response)
        print('contract_code_id:', place_order_result.contract_code_id)
        print('contract_address:', place_order_result.contract_address)
        counter2 = 0
        while counter2 < 10:
                try:
                        if command == 'buyquantity' or command == 'sellquantity' or command == 'buyusdc' or command == 'sellusdc':
#                               order = findordera()
                                order = findorder2a()
                        elif command == 'buyquantitylimit' or command == 'sellquantitylimit':
#                               order = findorderb()
                                order = findorder2b()
                        else:
                                exit()
                        print(order)
                        orderstatus = order['status']
#                       temporary statuses are ignored: BEST_EFFORT_OPENED, BEST_EFFORT_CANCELED
                        if orderstatus == constants.ORDER_STATUS_OPEN or orderstatus == constants.ORDER_STATUS_FILLED or orderstatus == constants.ORDER_STATUS_CANCELED or orderstatus == constants.ORDER_STATUS_UNTRIGGERED:
                                print(orderstatus)
                                break
                        print('Waiting 1 second for order to be OPEN, FILLED, CANCELED, or UNTRIGGERED.')
                        time.sleep(1)
                except Exception as error:
                        print('Waiting 1 second for order to be visible.')
                        time.sleep(1)
                counter2 += 1

#clientid/dydxmarket/orderexpiration
def cancelorder():
        global cancel_order_result
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' cancelorder()')
        try:
                cancel_order_result = client.cancel_order(
                        wallet,
                        client_id = int(clientid),
                        market = dydxmarket,
                        order_flags = clients.helpers.chain_helpers.ORDER_FLAGS_LONG_TERM,
                        good_til_time_in_seconds = orderexpiration,
                        good_til_block = 0,
                )
        except Exception as error:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "api query failed (%s)" % error)

def checkcancel():
        print('client_id       :', clientid)
        print('tx_hash         :', cancel_order_result.tx_hash)
        print('response        :', cancel_order_result.response)
        print('contract_code_id:', cancel_order_result.contract_code_id)
        print('contract_address:', cancel_order_result.contract_address)
        counter2 = 0
        while counter2 < 10:
                try:
                        order = findorder2b()
                        print(order)
                        orderstatus = order['status']
#                       temporary statuses are ignored: BEST_EFFORT_OPENED, BEST_EFFORT_CANCELED
#                       permanent status is also ignored: OPEN, UNTRIGGERED
                        if orderstatus == constants.ORDER_STATUS_FILLED or orderstatus == constants.ORDER_STATUS_CANCELED:
                                print(orderstatus)
                                break
                        print('Waiting 1 second for order to be FILLED, or CANCELED.')
                        time.sleep(1)
                except Exception as error:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "api query failed (%s)" % error)
                        break
                counter2 += 1

global clientid
global walletaddress
if len(argv) < 2:
        print('Error: Must specify <apikeyfile>')
        exit()
if path.isfile(argv[1]):
        exec(open(argv[1]).read())
else:
        print('Error:', argv[1], 'is not found, or not a file')
        exit()
if CHAIN_ID == "dydx-testnet-4":
        INDEXERURL = 'https://indexer.v4testnet.dydx.exchange/v4'
        if sys.platform == "linux" or sys.platform == "linux2":
                # linux
                ramdiskpath = '/mnt/ramdisk7'
        elif sys.platform == "darwin":
                # OS X
                ramdiskpath = '/Volumes/RAMDisk7'
elif CHAIN_ID == "dydx-mainnet-1":
        INDEXERURL = 'https://indexer.dydx.trade/v4'
        if sys.platform == "linux" or sys.platform == "linux2":
                # linux
                ramdiskpath = '/mnt/ramdisk5'
        elif sys.platform == "darwin":
                # OS X
                ramdiskpath = '/Volumes/RAMDisk5'
else:
        print(f"Error: CHAIN_ID is not dydx-testnet-4 or dydx-mainnet-1.")
        exit()

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
#subaccount specified
                walletaddress = wallet.address
                subaccount = argv[3]
#               getbalance()
                getbalance2()
        else:
#no subaccount specified
                walletaddress = wallet.address
                subaccount = 'all'
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
        if len(argv) < 5:
                print('Error: Must specify market, quantity')
                print('Example: python3', argv[0], argv[1], argv[2], 'BTC-USD 0.1')
                exit()
        dydxmarket = argv[3]
        ordersize = float(argv[4])
        orderside = clients.helpers.chain_helpers.OrderSide.BUY
        ordertype = clients.helpers.chain_helpers.OrderType.MARKET
        if simpleorderbook == 'y':
                if getprices() == None:
                        print('Error: No such market', dydxmarket)
                        exit()
        else:
                bestbid = os.popen('cd '+ramdiskpath+'/'+dydxmarket+'/bids; grep "" /dev/null * 2>> /dev/null | sed \'s/:/ /\' | sort -n | tail -1 | awk \'{print $1}\'').read()[:-1]
                bestask = os.popen('cd '+ramdiskpath+'/'+dydxmarket+'/asks; grep "" /dev/null * 2>> /dev/null | sed \'s/:/ /\' | sort -n | head -1 | awk \'{print $1}\'').read()[:-1]
        orderprice = float(bestask) * 2
        orderexpiration = 0
        #should this be GTT or FOK
        ordertif = clients.helpers.chain_helpers.OrderTimeInForce.FOK
        clientid = randrange(0, 2**31 - 1) #random number between 0 and max(int32) inclusive
        latest_block_result = client.validator_client.get.latest_block()
        good_til_block_value = latest_block_result.block.header.height + 1 + 10
        print(dydxmarket, orderside, ordertype, ordersize, orderprice, orderexpiration, ordertif, clientid, good_til_block_value)
        sendorder()
        walletaddress = wallet.address
        checkorder()
elif command == 'sellquantity':
        if len(argv) < 5:
                print('Error: Must specify market, quantity')
                print('Example: python3', argv[0], argv[1], argv[2], 'BTC-USD 0.1')
                exit()
        dydxmarket = argv[3]
        ordersize = float(argv[4])
        orderside = clients.helpers.chain_helpers.OrderSide.SELL
        ordertype = clients.helpers.chain_helpers.OrderType.MARKET
        if simpleorderbook == 'y':
                if getprices() == None:
                        print('Error: No such market', dydxmarket)
                        exit()
                dydxticksize = getticksize()
                if dydxticksize == None:
                        print('Error: No such market', dydxmarket)
                        exit()
        else:
                bestbid = os.popen('cd '+ramdiskpath+'/'+dydxmarket+'/bids; grep "" /dev/null * 2>> /dev/null | sed \'s/:/ /\' | sort -n | tail -1 | awk \'{print $1}\'').read()[:-1]
                bestask = os.popen('cd '+ramdiskpath+'/'+dydxmarket+'/asks; grep "" /dev/null * 2>> /dev/null | sed \'s/:/ /\' | sort -n | head -1 | awk \'{print $1}\'').read()[:-1]
                dydxticksize = os.popen("tail -1 "+ramdiskpath+"/v4dydxmarketdata/"+dydxmarket+"/tickSize").read()[:-1]
        orderprice = float(bestbid) / 2
        orderprice = float('%g'%(orderprice - (orderprice % float(dydxticksize))))
        orderexpiration = 0
        #should be IOC or FOK
        ordertif = clients.helpers.chain_helpers.OrderTimeInForce.FOK
        clientid = randrange(0, 999999999) #random number between 0 and 999,999,999 inclusive
        latest_block_result = client.validator_client.get.latest_block()
        good_til_block_value = latest_block_result.block.header.height + 1 + 10
        print(dydxmarket, orderside, ordertype, ordersize, orderprice, orderexpiration, ordertif, clientid, good_til_block_value)
        sendorder()
        walletaddress = wallet.address
        checkorder()
elif command == 'buyusdc':
        if len(argv) < 5:
                print('Error: Must specify market, USDCquantity')
                print('Example: python3', argv[0], argv[1], argv[2], 'BTC-USD 1000')
                exit()
        dydxmarket = argv[3]
        usdcsize = argv[4]
        orderside = clients.helpers.chain_helpers.OrderSide.BUY
        ordertype = clients.helpers.chain_helpers.OrderType.MARKET
        if simpleorderbook == 'y':
                if getprices() == None:
                        print('Error: No such market', dydxmarket)
                        exit()
                dydxstepsize = getstepsize()
                if dydxstepsize == None:
                        print('Error: No such market', dydxmarket)
                        exit()
        else:
                bestbid = os.popen('cd '+ramdiskpath+'/'+dydxmarket+'/bids; grep "" /dev/null * 2>> /dev/null | sed \'s/:/ /\' | sort -n | tail -1 | awk \'{print $1}\'').read()[:-1]
                bestask = os.popen('cd '+ramdiskpath+'/'+dydxmarket+'/asks; grep "" /dev/null * 2>> /dev/null | sed \'s/:/ /\' | sort -n | head -1 | awk \'{print $1}\'').read()[:-1]
                dydxstepsize = os.popen("tail -1 "+ramdiskpath+"/v4dydxmarketdata/"+dydxmarket+"/stepSize").read()[:-1]
        dydxquantity = float(usdcsize) / float(bestbid)
        dydxquantity = float('%g'%(dydxquantity - (dydxquantity % float(dydxstepsize))))
        ordersize = dydxquantity
        orderprice = float(bestask) * 2
        orderexpiration = 0
        #should be IOC or FOK
        ordertif = clients.helpers.chain_helpers.OrderTimeInForce.FOK
        clientid = randrange(0, 999999999) #random number between 0 and 999,999,999 inclusive
        latest_block_result = client.validator_client.get.latest_block()
        good_til_block_value = latest_block_result.block.header.height + 1 + 10
        print(dydxmarket, orderside, ordertype, ordersize, orderprice, orderexpiration, ordertif, clientid, good_til_block_value)
        sendorder()
        walletaddress = wallet.address
        checkorder()
elif command == 'sellusdc':
        if len(argv) < 5:
                print('Error: Must specify market, USDCquantity')
                print('Example: python3', argv[0], argv[1], argv[2], 'BTC-USD 1000')
                exit()
        dydxmarket = argv[3]
        usdcsize = argv[4]
        orderside = clients.helpers.chain_helpers.OrderSide.SELL
        ordertype = clients.helpers.chain_helpers.OrderType.MARKET
        if simpleorderbook == 'y':
                if getprices() == None:
                        print('Error: No such market', dydxmarket)
                        exit()
                dydxticksize = getticksize()
                if dydxticksize == None:
                        print('Error: No such market', dydxmarket)
                        exit()
                dydxstepsize = getstepsize()
                if dydxstepsize == None:
                        print('Error: No such market', dydxmarket)
                        exit()
        else:
                bestbid = os.popen('cd '+ramdiskpath+'/'+dydxmarket+'/bids; grep "" /dev/null * 2>> /dev/null | sed \'s/:/ /\' | sort -n | tail -1 | awk \'{print $1}\'').read()[:-1]
                bestask = os.popen('cd '+ramdiskpath+'/'+dydxmarket+'/asks; grep "" /dev/null * 2>> /dev/null | sed \'s/:/ /\' | sort -n | head -1 | awk \'{print $1}\'').read()[:-1]
                dydxticksize = os.popen("tail -1 "+ramdiskpath+"/v4dydxmarketdata/"+dydxmarket+"/tickSize").read()[:-1]
                dydxstepsize = os.popen("tail -1 "+ramdiskpath+"/v4dydxmarketdata/"+dydxmarket+"/stepSize").read()[:-1]
        dydxquantity = float(usdcsize) / float(bestbid)
        dydxquantity = float('%g'%(dydxquantity - (dydxquantity % float(dydxstepsize))))
        ordersize = dydxquantity
        orderprice = float(bestbid) / 2
        orderprice = float('%g'%(orderprice - (orderprice % float(dydxticksize))))
        orderexpiration = 0
        #should be IOC or FOK
        ordertif = clients.helpers.chain_helpers.OrderTimeInForce.FOK
        clientid = randrange(0, 999999999) #random number between 0 and 999,999,999 inclusive
        latest_block_result = client.validator_client.get.latest_block()
        good_til_block_value = latest_block_result.block.header.height + 1 + 10
        print(dydxmarket, orderside, ordertype, ordersize, orderprice, orderexpiration, ordertif, clientid, good_til_block_value)
        sendorder()
        walletaddress = wallet.address
        checkorder()
elif command == 'getorder':
        if len(argv) < 4:
                print('Error: Must specify [short-term|long-term|both] clientid')
                print('clientid can also be a status such as OPEN, FILLED, CANCELED, or UNTRIGGERED')
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
        if len(argv) < 4:
                print('Error: Must specify orderid')
                exit()
        orderid = argv[3]
#       order = findorderid()
        order = findorderid2()
        print(order)
elif command == 'buyquantitylimit':
        if len(argv) < 7:
                print('Error: Must specify market, quantity, limit, seconds')
                print('Example: python3', argv[0], argv[1], argv[2], 'BTC-USD 0.1 4000 6000')
                exit()
        dydxmarket = argv[3]
        ordersize = float(argv[4])
        orderprice = float(argv[5])
        orderexpiration = int(argv[6])
        orderside = clients.helpers.chain_helpers.OrderSide.BUY
        ordertype = clients.helpers.chain_helpers.OrderType.LIMIT
        ordertif = clients.helpers.chain_helpers.OrderTimeInForce.GTT
        clientid = randrange(0, 2**31 - 1) #random number between 0 and max(int32) inclusive
        good_til_block_value = 0
        print(dydxmarket, orderside, ordertype, ordersize, orderprice, orderexpiration, ordertif, clientid, good_til_block_value)
        sendorder()
        walletaddress = wallet.address
        checkorder()
elif command == 'sellquantitylimit':
        if len(argv) < 7:
                print('Error: Must specify market, quantity, limit, seconds')
                print('Example: python3', argv[0], argv[1], argv[2], 'BTC-USD 0.1 400000 6000')
                exit()
        dydxmarket = argv[3]
        ordersize = float(argv[4])
        orderprice = float(argv[5])
        orderexpiration = int(argv[6])
        orderside = clients.helpers.chain_helpers.OrderSide.SELL
        ordertype = clients.helpers.chain_helpers.OrderType.LIMIT
        ordertif = clients.helpers.chain_helpers.OrderTimeInForce.GTT
        clientid = randrange(0, 999999999) #random number between 0 and 999,999,999 inclusive
        good_til_block_value = 0
        print(dydxmarket, orderside, ordertype, ordersize, orderprice, orderexpiration, ordertif, clientid, good_til_block_value)
        sendorder()
        walletaddress = wallet.address
        checkorder()
elif command == 'cancelorder':
        if len(argv) < 4:
                print('Error: Must specify clientid')
                print('clientid can also be the status OPEN to cancel all OPEN orders')
                exit()
        clientid = argv[3]
        walletaddress = wallet.address
        order = findorder2b()
        orderlist = []
        if clientid == constants.ORDER_STATUS_OPEN:
                orderlist = order
        else:
                orderlist.append(order)
        counter = 1
        for order in orderlist:
                if len(orderlist) > 1:
                        print('======================================== [ CANCELING ORDER', counter, 'OUT OF', len(orderlist), ']')
                        counter += 1
                clientid = order['clientId']
                orderstatus = order['status']
                if orderstatus != 'OPEN':
                        print('Error: order with clientid', clientid, 'is not OPEN')
                        break
                dydxmarket = order['ticker']
                orderexpiration = int(isoparse(order['goodTilBlockTime']).timestamp() - time.time() + 60)
                cancelorder()
                checkcancel()
else:
        print('Available commands: balance, positions, buyquantity, sellquantity, buyusdc, sellusdc, getorder, getorderid, buyquantitylimit, sellquantitylimit, cancelorder')
