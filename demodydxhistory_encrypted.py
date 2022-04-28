from cryptography.fernet import Fernet
from dydx3 import Client
from dydx3 import constants
import base64
import ciso8601
import datetime
import sys

########################## YOU FILL THIS OUT #################
_private_key_encrypted = '<FILL_THIS_OUT>'
#_private_key_encrypted is optional and may be set to '' (hardware wallets do not generally provide this information)
#If _private_key_encrypted is set, you do not need to set _api_key_encrypted/_api_secret_encrypted/_api_passphrase_encrypted/_stark_private_key_encrypted
_api_key_encrypted = '<FILL_THIS_OUT>'
_api_secret_encrypted = '<FILL_THIS_OUT>'
_api_passphrase_encrypted = '<FILL_THIS_OUT>'
_stark_private_key_encrypted = '<FILL_THIS_OUT>'
_eth_address_encrypted = '<FILL_THIS_OUT>'
_network_id = str(constants.NETWORK_ID_ROPSTEN)
#_network_id is set to either str(constants.NETWORK_ID_MAINNET) or str(constants.NETWORK_ID_ROPSTEN)
_api_host = constants.API_HOST_ROPSTEN
#_api_host is set to either constants.API_HOST_MAINNET or constants.API_HOST_ROPSTEN
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

if len(sys.argv) > 1:
        start_timestamp = sys.argv[1]
else:
        start_timestamp = datetime.datetime.utcnow() + datetime.timedelta(days = -7)
        start_timestamp = start_timestamp.isoformat()[:-3] + 'Z'
if len(sys.argv) > 2:
        stop_timestamp = sys.argv[2]
else:
        stop_timestamp = datetime.datetime.utcnow()
        stop_timestamp = stop_timestamp.isoformat()[:-3] + 'Z'
list_of_fills = [ ]
while ciso8601.parse_datetime(stop_timestamp) > ciso8601.parse_datetime(start_timestamp):
        get_fills_results = client.private.get_fills(created_before_or_at = stop_timestamp)
        get_fills_results = get_fills_results.data
        for fill in get_fills_results['fills']:
                if ciso8601.parse_datetime(fill['createdAt']) > ciso8601.parse_datetime(start_timestamp):
                        list_of_fills.append(fill)
        if len(get_fills_results['fills']) < 100:
                break
        stop_timestamp = ciso8601.parse_datetime(get_fills_results['fills'][-1]['createdAt']) + datetime.timedelta(microseconds = 1000)
        stop_timestamp = stop_timestamp.isoformat()[:-9] + 'Z'
list_of_fills_unique = [ ]
for fill in list_of_fills:
        if fill not in list_of_fills_unique:
                list_of_fills_unique.append(fill)
                print(fill['createdAt']+','+
                      fill['fee']+','+
                      fill['id']+','+
                      fill['liquidity']+','+
                      fill['market']+','+
                      fill['orderId']+','+
                      fill['price']+','+
                      fill['side']+','+
                      fill['size']+','+
                      fill['type'])
