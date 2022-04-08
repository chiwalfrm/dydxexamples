import sys
import json
from websocket import create_connection

ws = create_connection("wss://api.dydx.exchange/v3/ws")
api_data = {"type":"subscribe", "channel":"v3_trades", "id":"BTC-USD"}
ws.send(json.dumps(api_data))
api_data = ws.recv()
api_data = json.loads(api_data)
print(api_data)
api_data = ws.recv()
api_data = json.loads(api_data)
print(api_data)
while True:
        try:
                api_data = ws.recv()
                api_data = json.loads(api_data)
                trades = api_data['contents']['trades'][0]
                tradeprice = trades['price']
                tradeside = trades['side']
                with open('/mnt/ramdisk/lasttrade', "w") as fp:
                        fp.write(tradeprice+' '+tradeside+'\n')
                fp.close()
                print(tradeprice, tradeside)
        except KeyboardInterrupt:
                ws.close()
                sys.exit(0)
