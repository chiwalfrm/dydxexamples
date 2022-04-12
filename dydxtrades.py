import datetime
import json
import logging
import os
import pprint
import sys
import time
from logging.handlers import RotatingFileHandler
from os.path import exists
from sys import platform
from websocket import create_connection

if platform == "linux" or platform == "linux2":
        # linux
        ramdiskpath = '/mnt/ramdisk'
elif platform == "darwin":
        # OS X
        ramdiskpath = '/Volumes/RAMDisk'
logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)

pp = pprint.PrettyPrinter(width = 41, compact = True)
if len(sys.argv) < 2:
        market = 'BTC-USD'
else:
        market = sys.argv[1]
handler = RotatingFileHandler(ramdiskpath+'/dydxtrades'+market+'.log', maxBytes=1048576,
                              backupCount = 4)
logger.addHandler(handler)
if exists(ramdiskpath) == False:
        print('Error: Ramdisk', ramdiskpath, 'not mounted')
        exit()
if os.path.ismount(ramdiskpath) == False:
        print('Warning:', ramdiskpath, 'is not a mount point')
ws = create_connection("wss://api.dydx.exchange/v3/ws")
api_data = {"type":"subscribe", "channel":"v3_trades", "id":market}
ws.send(json.dumps(api_data))
api_data = ws.recv()
api_data = json.loads(api_data)
pp.pprint(api_data)
api_data = ws.recv()
api_data = json.loads(api_data)
pp.pprint(api_data)
while True:
        try:
                trades = api_data['contents']['trades'][0]
                tradecreatedat = trades['createdAt']
                tradeprice = trades['price']
                tradeside = trades['side']
                tradesize = trades['size']
                with open(ramdiskpath+'/'+market+'/lasttrade', "w") as fp:
                        fp.write(tradecreatedat+' '+tradeprice+' '+tradeside+' ('+tradesize+')\n')
                fp.close()
                logger.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' '+tradecreatedat+' '+tradeprice+' '+tradeside.ljust(4)+' ('+tradesize+')')
                api_data = ws.recv()
                api_data = json.loads(api_data)
        except KeyboardInterrupt:
                ws.close()
                sys.exit(0)
        except Exception as error:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "WebSocket message failed (%s)" % error)
                ws.close()
                time.sleep(1)
