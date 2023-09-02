from dydx4 import chain
from dydx4 import clients
from os import path
from random import randrange
from sys import argv
import requests

########################## YOU FILL THIS OUT #################
DYDX_TEST_MNEMONIC = '<FILL_THIS_OUT>'
##############################################################

if len(argv) > 1 and path.isfile(argv[1]):
        exec(open(argv[1]).read())

wallet = chain.aerial.wallet.LocalWallet.from_mnemonic(DYDX_TEST_MNEMONIC, clients.constants.BECH32_PREFIX)
network = clients.constants.Network.testnet()
client = clients.CompositeClient(
        network,
)
subaccount = clients.Subaccount(wallet, 0)

clientid = randrange(0, 2**31 - 1) #random number between 0 and max(int32) inclusive
place_order_result = client.place_order(
        subaccount,
        market = 'BTC-USD',
        type = clients.helpers.chain_helpers.OrderType.LIMIT,
        side = clients.helpers.chain_helpers.OrderSide.BUY,
        price = 1000,
        size = 0.001,
        client_id = clientid,
        time_in_force = clients.helpers.chain_helpers.OrderTimeInForce.GTT,
        good_til_time_in_seconds = 60,
        execution = clients.helpers.chain_helpers.OrderExecution.DEFAULT,
        post_only = False,
        reduce_only = False
)
print('client_id       :', clientid)
print('tx_hash         :', place_order_result.tx_hash)
print('response        :', place_order_result.response)
print('contract_code_id:', place_order_result.contract_code_id)
print('contract_address:', place_order_result.contract_address)
