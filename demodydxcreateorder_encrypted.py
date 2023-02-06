import time
from cryptography.fernet import Fernet
from datetime import datetime
from dydx3 import Client
from dydx3 import constants
from dydx3 import epoch_seconds_to_iso
from base64 import b64decode
from os import path
from random import randint
from requests import get
from sys import argv

########################## YOU FILL THIS OUT #################
my_eth_private_key_encrypted = '<FILL_THIS_OUT>'
#my_eth_private_key_encrypted is optional and may be set to '' (hardware wallets do not generally provide this information)
#If my_eth_private_key_encrypted is set, you do not need to set my_api_key_encrypted/my_api_secret_encrypted/my_api_passphrase_encrypted/my_stark_private_key_encrypted
my_api_key_encrypted = '<FILL_THIS_OUT>'
my_api_secret_encrypted = '<FILL_THIS_OUT>'
my_api_passphrase_encrypted = '<FILL_THIS_OUT>'
my_stark_private_key_encrypted = '<FILL_THIS_OUT>'
my_eth_address_encrypted = '<FILL_THIS_OUT>'
my_api_network_id = str(constants.NETWORK_ID_GOERLI)
#my_api_network_id is set to either str(constants.NETWORK_ID_MAINNET) or str(constants.NETWORK_ID_GOERLI)
##############################################################

def encrypt(message: bytes, key: bytes) -> bytes:
        return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes) -> bytes:
        return Fernet(key).decrypt(token)

if path.exists(argv[1]):
        exec(open(argv[1]).read())
if my_api_network_id == str(constants.NETWORK_ID_MAINNET):
        my_api_host = constants.API_HOST_MAINNET
        my_ws_host = constants.WS_HOST_MAINNET
elif my_api_network_id == str(constants.NETWORK_ID_GOERLI):
        my_api_host = constants.API_HOST_GOERLI
        my_ws_host = constants.WS_HOST_GOERLI
else:
        print(f"Error: my_api_network_id is not {constants.NETWORK_ID_MAINNET} or {constants.NETWORK_ID_GOERLI}.")
        exit()

print("Enter decryption key (type 'encrypt' to encrypt): ", end = '')
decryptionkey = input()
if decryptionkey == 'encrypt':
        print("Enter encryption key (type 'new' to generate one): ", end = '')
        encryptkey = input()
        if encryptkey == 'new':
                encryptkey = Fernet.generate_key()
                print('Key (SAVE THIS!):', encryptkey.decode())
        while True:
                print("Enter string to encrypt (press Ctrl-D to exit): ", end = '')
                try:
                        encryptstring = input()
                except EOFError:
                        print()
                        exit()
                encryptedmessage = encrypt(encryptstring.encode(), encryptkey)
                print(b64encode(encryptedmessage))
my_eth_address = decrypt(b64decode(my_eth_address_encrypted), decryptionkey).decode()

if my_eth_private_key_encrypted != '':
        my_eth_private_key = decrypt(b64decode(my_eth_private_key_encrypted), decryptionkey).decode()
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
        my_api_key = decrypt(b64decode(my_api_key_encrypted), decryptionkey).decode()
        my_api_secret = decrypt(b64decode(my_api_secret_encrypted), decryptionkey).decode()
        my_api_passphrase = decrypt(b64decode(my_api_passphrase_encrypted), decryptionkey).decode()
        my_stark_private_key = decrypt(b64decode(my_stark_private_key_encrypted), decryptionkey).decode()
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
create_order_result = client.private.create_order(
        position_id = account['positionId'],
        market = constants.MARKET_BTC_USD,
        side = constants.ORDER_SIDE_BUY,
        order_type = constants.ORDER_TYPE_LIMIT,
        post_only = False,
        size = '0.001',
        price = '1000',
        limit_fee = '0.1',
        expiration = one_minute_from_now_iso,
)
print(create_order_result.data)
print(create_order_result.headers)
