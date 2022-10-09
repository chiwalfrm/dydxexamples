import datetime
import json
import logging
import os
import pprint
import random
import sys
import time
from logging.handlers import RotatingFileHandler
from os.path import exists
from sys import platform
from websocket import create_connection

def openconnection():
        global ws
#       ws = create_connection("wss://api.stage.dydx.exchange/v3/ws")
        ws = create_connection("wss://api.dydx.exchange/v3/ws")
        api_data = {"type":"subscribe", "channel":"v3_markets"}
        ws.send(json.dumps(api_data))
        api_data = ws.recv()
        api_data = json.loads(api_data)
        pp.pprint(api_data)
        api_data = ws.recv()
        api_data = json.loads(api_data)
        pp.pprint(api_data)

def checkwidth(elementname, elementsize):
        global maxwidthindexPrice
        global maxwidthnextFundingAt
        global maxwidthnextFundingRate
        global maxwidthopenInterest
        global maxwidthoraclePrice
        global maxwidthpriceChange24H
        global maxwidthtrades24H
        global maxwidthvolume24H
        if elementname == 'indexPrice' and elementsize > maxwidthindexPrice:
                fp = open(ramdiskpath+'/maxwidth'+elementname, "w")
                fp.write(str(elementsize)+'\n')
                fp.close()
                maxwidthindexPrice = elementsize
        elif elementname == 'nextFundingAt' and elementsize > maxwidthnextFundingAt:
                fp = open(ramdiskpath+'/maxwidth'+elementname, "w")
                fp.write(str(elementsize)+'\n')
                fp.close()
                maxwidthnextFundingAt = elementsize
        elif elementname == 'nextFundingRate' and elementsize > maxwidthnextFundingRate:
                fp = open(ramdiskpath+'/maxwidth'+elementname, "w")
                fp.write(str(elementsize)+'\n')
                fp.close()
                maxwidthnextFundingRate = elementsize
        elif elementname == 'openInterest' and elementsize > maxwidthopenInterest:
                fp = open(ramdiskpath+'/maxwidth'+elementname, "w")
                fp.write(str(elementsize)+'\n')
                fp.close()
                maxwidthopenInterest = elementsize
        elif elementname == 'oraclePrice' and elementsize > maxwidthoraclePrice:
                fp = open(ramdiskpath+'/maxwidth'+elementname, "w")
                fp.write(str(elementsize)+'\n')
                fp.close()
                maxwidthoraclePrice = elementsize
        elif elementname == 'priceChange24H' and elementsize > maxwidthpriceChange24H:
                fp = open(ramdiskpath+'/maxwidth'+elementname, "w")
                fp.write(str(elementsize)+'\n')
                fp.close()
                maxwidthpriceChange24H = elementsize
        elif elementname == 'trades24H' and elementsize > maxwidthtrades24H:
                fp = open(ramdiskpath+'/maxwidth'+elementname, "w")
                fp.write(str(elementsize)+'\n')
                fp.close()
                maxwidthtrades24H = elementsize
        elif elementname == 'volume24H' and elementsize > maxwidthvolume24H:
                fp = open(ramdiskpath+'/maxwidth'+elementname, "w")
                fp.write(str(elementsize)+'\n')
                fp.close()
                maxwidthvolume24H = elementsize

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' dydxv3markets.py')
logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
pp = pprint.PrettyPrinter(width = 41, compact = True)
if platform == "linux" or platform == "linux2":
        # linux
        ramdiskpath = '/mnt/ramdisk'
elif platform == "darwin":
        # OS X
        ramdiskpath = '/Volumes/RAMDisk'

handler = RotatingFileHandler(ramdiskpath+'/dydxv3markets.log', maxBytes=2097152,
                              backupCount = 4)
logger.addHandler(handler)

if exists(ramdiskpath) == False:
        print('Error: Ramdisk', ramdiskpath, 'not mounted')
        exit()
if os.path.ismount(ramdiskpath) == False:
        print('Warning:', ramdiskpath, 'is not a mount point')

maxwidthindexPrice = 0
maxwidthnextFundingAt = 0
maxwidthnextFundingRate = 0
maxwidthopenInterest = 0
maxwidthoraclePrice = 0
maxwidthpriceChange24H = 0
maxwidthtrades24H = 0
maxwidthvolume24H = 0
openconnection()
while True:
        try:
                api_data = ws.recv()
                api_data = json.loads(api_data)
                logger.info("{'timestamp': '"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"'}")
                logger.info(api_data)
                for item in api_data['contents'].items():
                        market = item[0]
                        marketdata = item[1]
                        if exists(ramdiskpath+'/'+market) == False:
                                os.system('mkdir -p '+ramdiskpath+'/'+market)
                        for marketdata in marketdata.items():
                                marketdataelement = marketdata[0]
                                marketdatavalue = marketdata[1]
                                fp = open(ramdiskpath+'/'+market+'/'+marketdataelement, "w")
                                fp.write(marketdatavalue+' '+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
                                fp.close()
                                checkwidth(marketdataelement, len(marketdatavalue))
        except KeyboardInterrupt:
                ws.close()
                sys.exit(0)
        except Exception as error:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "WebSocket message failed (%s)" % error)
                ws.close()
                time.sleep(1)
                try:
                        openconnection()
                except Exception as error:
                        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "WebSocket message failed (%s)" % error)
                        ws.close()
                        time.sleep(random.randint(1,10))
