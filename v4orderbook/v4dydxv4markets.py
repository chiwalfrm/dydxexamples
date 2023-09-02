import json
import logging
import os
import sys
import time
from datetime import datetime
from logging import handlers
from random import randint
from websocket import create_connection
WSINDEXERURL = 'wss://indexer.v4testnet2.dydx.exchange/v4/ws'

def openconnection():
        global ws
        ws = create_connection(WSINDEXERURL)
        api_data = {
                "type": "subscribe",
                "channel": "v4_markets"
        }
        ws.send(json.dumps(api_data))
        api_data = ws.recv()
        api_data = json.loads(api_data)
        print(api_data)
        api_data = ws.recv()
        api_data = json.loads(api_data)
        print(api_data)

def checkwidth(elementname, elementsize):
#       global maxwidthindexPrice
#       global maxwidthnextFundingAt
        global maxwidthnextFundingRate
        global maxwidthopenInterest
#       global maxwidthoraclePrice
        global maxwidthpriceChange24H
        global maxwidthtrades24H
        global maxwidthvolume24H
        global maxwidtheffectiveAt
        global maxwidtheffectiveAtHeight
        global maxwidthmarketId
        global maxwidthprice
#       if elementname == 'indexPrice' and elementsize > maxwidthindexPrice:
#               fp = open(ramdiskpath+'/maxwidth'+elementname, "w")
#               fp.write(str(elementsize)+'\n')
#               fp.close()
#               maxwidthindexPrice = elementsize
#       elif elementname == 'nextFundingAt' and elementsize > maxwidthnextFundingAt:
#               fp = open(ramdiskpath+'/maxwidth'+elementname, "w")
#               fp.write(str(elementsize)+'\n')
#               fp.close()
#               maxwidthnextFundingAt = elementsize
        if elementname == 'nextFundingRate' and elementsize > maxwidthnextFundingRate:
                fp = open(ramdiskpath+'/maxwidth'+elementname, "w")
                fp.write(str(elementsize)+'\n')
                fp.close()
                maxwidthnextFundingRate = elementsize
        elif elementname == 'openInterest' and elementsize > maxwidthopenInterest:
                fp = open(ramdiskpath+'/maxwidth'+elementname, "w")
                fp.write(str(elementsize)+'\n')
                fp.close()
                maxwidthopenInterest = elementsize
#       elif elementname == 'oraclePrice' and elementsize > maxwidthoraclePrice:
#               fp = open(ramdiskpath+'/maxwidth'+elementname, "w")
#               fp.write(str(elementsize)+'\n')
#               fp.close()
#               maxwidthoraclePrice = elementsize
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
        elif elementname == 'effectiveAt' and elementsize > maxwidtheffectiveAt:
                fp = open(ramdiskpath+'/maxwidth'+elementname, "w")
                fp.write(str(elementsize)+'\n')
                fp.close()
                maxwidtheffectiveAt = elementsize
        elif elementname == 'effectiveAtHeight' and elementsize > maxwidtheffectiveAtHeight:
                fp = open(ramdiskpath+'/maxwidth'+elementname, "w")
                fp.write(str(elementsize)+'\n')
                fp.close()
                maxwidtheffectiveAtHeight = elementsize
        elif elementname == 'marketId' and elementsize > maxwidthmarketId:
                fp = open(ramdiskpath+'/maxwidth'+elementname, "w")
                fp.write(str(elementsize)+'\n')
                fp.close()
                maxwidthmarketId = elementsize
        elif elementname == 'price' and elementsize > maxwidthprice:
                fp = open(ramdiskpath+'/maxwidth'+elementname, "w")
                fp.write(str(elementsize)+'\n')
                fp.close()
                maxwidthprice = elementsize
        elif elementname not in [
                'nextFundingRate',
                'openInterest',
                'priceChange24H',
                'trades24H',
                'volume24H',
                'effectiveAt',
                'effectiveAtHeight',
                'marketId',
                'price'
        ]:
                fp = open(ramdiskpath+'/maxwidthgeneric', "a")
                fp.write(elementname+' '+str(elementsize)+'\n')
                fp.close()

def processcontentsdict():
        for market, marketdata in contentsdict.items():
                if os.path.isdir(ramdiskpath+'/'+market) == False:
                        os.system('mkdir -p '+ramdiskpath+'/'+market)
                for marketdataelement, marketdatavalue in marketdata.items():
                        fp = open(ramdiskpath+'/'+market+'/'+marketdataelement, "w")
                        fp.write(str(marketdatavalue)+' '+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
                        fp.close()
                        checkwidth(marketdataelement, len(str(marketdatavalue)))

print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' v4dydxv4markets.py')
logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
if sys.platform == "linux" or sys.platform == "linux2":
        # linux
        ramdiskpath = '/mnt/ramdisk5'
elif sys.platform == "darwin":
        # OS X
        ramdiskpath = '/Volumes/RAMDisk5'

handler = logging.handlers.RotatingFileHandler(ramdiskpath+'/v4dydxv4markets.log',
        maxBytes = 2097152,
        backupCount = 4
)
logger.addHandler(handler)

if os.path.isdir(ramdiskpath) == False:
        print('Error: Ramdisk', ramdiskpath, 'not mounted')
        sys.exit()
if os.path.ismount(ramdiskpath) == False:
        print('Warning:', ramdiskpath, 'is not a mount point')

#maxwidthindexPrice = 0
#maxwidthnextFundingAt = 0
maxwidthnextFundingRate = 0
maxwidthopenInterest = 0
#maxwidthoraclePrice = 0
maxwidthpriceChange24H = 0
maxwidthtrades24H = 0
maxwidthvolume24H = 0
maxwidtheffectiveAt = 0
maxwidtheffectiveAtHeight = 0
maxwidthmarketId = 0
maxwidthprice = 0
openconnection()
while True:
        try:
                global contentsdict
                api_data = ws.recv()
                api_data = json.loads(api_data)
                logger.info("{'timestamp': '"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"'}")
                logger.info(api_data)
                if 'trading' in api_data['contents'].keys():
                        contentsdict = api_data['contents']['trading']
                        processcontentsdict()
                elif 'oraclePrices' in api_data['contents'].keys():
                        contentsdict = api_data['contents']['oraclePrices']
                        processcontentsdict()
                else:
                        print(api_data['contents'])
        except KeyboardInterrupt:
                ws.close()
                sys.exit(0)
        except Exception as error:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "WebSocket message failed (%s)" % error)
                ws.close()
                time.sleep(1)
                try:
                        openconnection()
                except Exception as error:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "WebSocket message failed (%s)" % error)
                        ws.close()
                        time.sleep(randint(1,10))
