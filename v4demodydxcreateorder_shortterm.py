from v4_client_py import chain
from v4_client_py import clients
from os import path
from random import randrange
from sys import argv
import time

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
height = client.get_current_block()
good_til_block = height + 4
print('height          :', height)
print('good_til_block  :', good_til_block)
place_short_term_order_result = client.place_short_term_order(
        subaccount,
        market = 'BTC-USD',
        side = clients.helpers.chain_helpers.OrderSide.BUY,
        price = 1000,
        size = 0.001,
        client_id = clientid,
        good_til_block=good_til_block,
        time_in_force = clients.helpers.chain_helpers.OrderExecution.DEFAULT,
        reduce_only = False,
)
print('tx_hash         :', place_short_term_order_result.tx_hash)
print('response        :', place_short_term_order_result.response)
print('contract_code_id:', place_short_term_order_result.contract_code_id)
print('contract_address:', place_short_term_order_result.contract_address)
print('good_til_block  :', good_til_block)
time.sleep(1)
cancel_order_result = client.validator_client.post.cancel_order(
        subaccount,
        client_id = clientid,
        clob_pair_id = 0,
        order_flags = 0,
        good_til_block = good_til_block,
        good_til_block_time = 0,
)
print('tx_hash         :', cancel_order_result.tx_hash)
print('response        :', cancel_order_result.response)
print('contract_code_id:', cancel_order_result.contract_code_id)
print('contract_address:', cancel_order_result.contract_address)
