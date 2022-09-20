from cryptography.fernet import Fernet
from dydx3 import Client
from dydx3 import constants
from dydx3 import epoch_seconds_to_iso
import base64
import time

########################## YOU FILL THIS OUT #################
_private_key_encrypted = '<FILL_THIS_OUT>'
#_private_key_encrypted is optional and may be set to '' (hardware wallets do not generally provide this information)
#If _private_key_encrypted is set, you do not need to set _api_key_encrypted/_api_secret_encrypted/_api_passphrase_encrypted/_stark_private_key_encrypted
_api_key_encrypted = '<FILL_THIS_OUT>'
_api_secret_encrypted = '<FILL_THIS_OUT>'
_api_passphrase_encrypted = '<FILL_THIS_OUT>'
_stark_private_key_encrypted = '<FILL_THIS_OUT>'
_eth_address_encrypted = '<FILL_THIS_OUT>'
_network_id = str(constants.NETWORK_ID_GOERLI)
#_network_id is set to either str(constants.NETWORK_ID_MAINNET) or str(constants.NETWORK_ID_GOERLI)
_api_host = constants.API_HOST_GOERLI
#_api_host is set to either constants.API_HOST_MAINNET or constants.API_HOST_GOERLI
##############################################################

def encrypt(message: bytes, key: bytes) -> bytes:
        return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes) -> bytes:
        return Fernet(key).decrypt(token)

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
                print(base64.b64encode(encryptedmessage))
_eth_address = decrypt(base64.b64decode(_eth_address_encrypted), decryptionkey).decode()

if _private_key != '':
        _private_key = decrypt(base64.b64decode(_private_key_encrypted), decryptionkey).decode()
        client = Client(
                host = _api_host,
                default_ethereum_address = _eth_address,
                eth_private_key = _private_key,
                network_id = _network_id
        )
        derive_stark_key_result = client.onboarding.derive_stark_key()
        stark_private_key = derive_stark_key_result['private_key']
        client.stark_private_key = stark_private_key
else:
        _api_key = decrypt(base64.b64decode(_api_key_encrypted), decryptionkey).decode()
        _api_secret = decrypt(base64.b64decode(_api_secret_encrypted), decryptionkey).decode()
        _api_passphrase = decrypt(base64.b64decode(_api_passphrase_encrypted), decryptionkey).decode()
        _stark_private_key = decrypt(base64.b64decode(_stark_private_key_encrypted), decryptionkey).decode()
        client = Client(
                host = _api_host,
                network_id = _network_id,
                api_key_credentials = {
                        'key': _api_key,
                        'secret': _api_secret,
                        'passphrase': _api_passphrase
                }
        )
        client.stark_private_key = _stark_private_key

get_account_result = client.private.get_account(
        ethereum_address = _eth_address
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
