import os
import time
from datetime import datetime
from dydx4 import chain
from dydx4 import clients
from os import path
from random import randrange
from requests import get
from sys import argv

########################## YOU FILL THIS OUT #################
DYDX_TEST_MNEMONIC = '<FILL_THIS_OUT>'
##############################################################

#ordermarket/orderside/ordertype/ordersize/orderprice/orderexpiration/ordertif/clientid
def sendorder():
        global place_order_result
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' sendorder()')
        place_order_result = client.place_order(
                subaccount,
                market = ordermarket,
                type = ordertype,
                side = orderside,
                price = orderprice,
                size = ordersize,
                client_id = clientid,
                time_in_force = ordertif,
                good_til_time_in_seconds = orderexpiration,
                execution = clients.helpers.chain_helpers.OrderExecution.DEFAULT,
                post_only = False,
                reduce_only = False
        )

#dydxmarket
def getprices():
        global bestbid
        global bestask
        r = get(url = 'https://indexer.v4testnet2.dydx.exchange/v4/orderbooks/perpetualMarket/'+dydxmarket)
        r.raise_for_status()
        if r.status_code == 200:
                bestbid = r.json()['bids'][0]['price']
                bestask = r.json()['asks'][0]['price']
        else:
                print('Bad requests status code:', r.status_code)

#dydxmarket
def getticksize():
        global dydxticksize
        r = get(url = 'https://indexer.v4testnet2.dydx.exchange/v4/perpetualMarkets', params={
                'ticker': dydxmarket
                }
        )
        r.raise_for_status()
        if r.status_code == 200:
                dydxticksize = r.json()['markets'][dydxmarket]['tickSize']
        else:
                print('Bad requests status code:', r.status_code)

#dydxmarket
def getstepsize():
        global dydxstepsize
        r = get(url = 'https://indexer.v4testnet2.dydx.exchange/v4/perpetualMarkets', params={
                'ticker': dydxmarket
                }
        )
        r.raise_for_status()
        if r.status_code == 200:
                dydxstepsize = r.json()['markets'][dydxmarket]['stepSize']
        else:
                print('Bad requests status code:', r.status_code)

#clientid
def findorder():
        get_subaccount_orders_result = client.indexer_client.account.get_subaccount_orders(subaccount.address, 0)
        for item in get_subaccount_orders_result.data:
                if item['clientId'] == clientid:
                        return item
        print('Order not found', clientid)
        return None

if len(argv) > 1 and path.isfile(argv[1]):
        exec(open(argv[1]).read())

wallet = chain.aerial.wallet.LocalWallet.from_mnemonic(DYDX_TEST_MNEMONIC, clients.constants.BECH32_PREFIX)
network = clients.constants.Network.testnet()
client = clients.CompositeClient(
        network,
)
subaccount = clients.Subaccount(wallet, 0)

if len(argv) > 2:
        command = argv[2]
else:
        command = 'balance'

if command == 'balance':
        subaccounts_response = client.indexer_client.account.get_subaccounts(subaccount.address)
        print(float(subaccounts_response.data['subaccounts'][0]['equity']))
elif command == 'positions':
        subaccounts_response = client.indexer_client.account.get_subaccounts(subaccount.address)
        for key, value in subaccounts_response.data['subaccounts'][0]['openPerpetualPositions'].items():
                print(key.ljust(9), value['size'])
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
        orderexpiration = 60
        ordertif = clients.helpers.chain_helpers.OrderTimeInForce.IOC
        clientid = randrange(0, 999999999) #random number between 0 and 999,999,999 inclusive
        print(ordermarket, orderside, ordertype, ordersize, orderprice, orderexpiration, ordertif, clientid)
        sendorder()
        print('client_id       :', clientid)
        print('tx_hash         :', place_order_result.tx_hash)
        print('response        :', place_order_result.response)
        print('contract_code_id:', place_order_result.contract_code_id)
        print('contract_address:', place_order_result.contract_address)
        print(clientid)
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
        orderexpiration = 60
        ordertif = clients.helpers.chain_helpers.OrderTimeInForce.IOC
        clientid = randrange(0, 999999999) #random number between 0 and 999,999,999 inclusive
        print(ordermarket, orderside, ordertype, ordersize, orderprice, orderexpiration, ordertif, clientid)
        sendorder()
        print('client_id       :', clientid)
        print('tx_hash         :', place_order_result.tx_hash)
        print('response        :', place_order_result.response)
        print('contract_code_id:', place_order_result.contract_code_id)
        print('contract_address:', place_order_result.contract_address)
        print(clientid)
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
        orderexpiration = 60
        ordertif = clients.helpers.chain_helpers.OrderTimeInForce.IOC
        clientid = randrange(0, 999999999) #random number between 0 and 999,999,999 inclusive
        print(ordermarket, orderside, ordertype, ordersize, orderprice, orderexpiration, ordertif, clientid)
        sendorder()
        print('client_id       :', clientid)
        print('tx_hash         :', place_order_result.tx_hash)
        print('response        :', place_order_result.response)
        print('contract_code_id:', place_order_result.contract_code_id)
        print('contract_address:', place_order_result.contract_address)
        print(clientid)
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
        orderexpiration = 60
        ordertif = clients.helpers.chain_helpers.OrderTimeInForce.IOC
        clientid = randrange(0, 999999999) #random number between 0 and 999,999,999 inclusive
        print(ordermarket, orderside, ordertype, ordersize, orderprice, orderexpiration, ordertif, clientid)
        sendorder()
        print('client_id       :', clientid)
        print('tx_hash         :', place_order_result.tx_hash)
        print('response        :', place_order_result.response)
        print('contract_code_id:', place_order_result.contract_code_id)
        print('contract_address:', place_order_result.contract_address)
        print(clientid)
elif command == 'getorder':
        if len(argv) < 3:
                print('Error: Must specify clientid')
                exit()
        clientid = argv[3]
        order = findorder()
        print(order)
