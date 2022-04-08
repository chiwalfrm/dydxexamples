import datetime
import json
import pprint
import sys
from websocket import create_connection

pp = pprint.PrettyPrinter(width = 41, compact = True)
ws = create_connection("wss://api.dydx.exchange/v3/ws")
api_data = {"type":"subscribe", "channel":"v3_trades", "id":"BTC-USD"}
ws.send(json.dumps(api_data))
api_data = ws.recv()
api_data = json.loads(api_data)
pp.pprint(api_data)
api_data = ws.recv()
api_data = json.loads(api_data)
pp.pprint(api_data)
while True:
        try:
                api_data = ws.recv()
                api_data = json.loads(api_data)
                trades = api_data['contents']['trades'][0]
                tradecreatedat = trades['createdAt']
                tradeprice = trades['price']
                tradeside = trades['side']
                tradesize = trades['size']
                with open('/mnt/ramdisk/lasttrade', "w") as fp:
                        fp.write(tradecreatedat+' '+tradeprice+' '+tradeside+' ('+tradesize+')\n')
                fp.close()
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tradecreatedat, tradeprice, tradeside.ljust(4), '('+tradesize+')')
        except KeyboardInterrupt:
                ws.close()
                sys.exit(0)
        except Exception as error:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" WebSocket message failed (%s)" % error)
                ws.close()
                time.sleep(1)
