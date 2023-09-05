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

def checkwidth(
        framdiskpath,
        fmarket,
        felementname,
        felementsize
):
#       global maxwidthindexPrice
#       global maxwidthnextFundingAt
        global maxwidthnextFundingRate
        global maxwidthopenInterest
        global maxwidthoraclePrice
        global maxwidthpriceChange24H
        global maxwidthtrades24H
        global maxwidthvolume24H
        global maxwidtheffectiveAt
        global maxwidtheffectiveAtHeight
        global maxwidthmarketId
        global maxwidthatomicResolution
        global maxwidthbaseAsset
        global maxwidthbasePositionNotional
        global maxwidthbasePositionSize
        global maxwidthclobPairId
        global maxwidthincrementalPositionSize
        global maxwidthinitialMarginFraction
        global maxwidthlastPrice
        global maxwidthmaintenanceMarginFraction
        global maxwidthmaxPositionSize
        global maxwidthminOrderBaseQuantums
        global maxwidthquantumConversionExponent
        global maxwidthquoteAsset
        global maxwidthstatus
        global maxwidthstepBaseQuantums
        global maxwidthstepSize
        global maxwidthsubticksPerTick
        global maxwidthticker
        global maxwidthtickSize
        if felementsize == 0:
                return None
#       elif felementname == 'indexPrice' and felementsize > maxwidthindexPrice:
#               fp = open(framdiskpath+'/maxwidth'+felementname, "w")
#               fp.write(str(felementsize)+'\n')
#               fp.close()
#               maxwidthindexPrice = felementsize
#       elif felementname == 'nextFundingAt' and felementsize > maxwidthnextFundingAt:
#               fp = open(framdiskpath+'/maxwidth'+felementname, "w")
#               fp.write(str(felementsize)+'\n')
#               fp.close()
#               maxwidthnextFundingAt = felementsize
        elif felementname == 'nextFundingRate' and felementsize > maxwidthnextFundingRate:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthnextFundingRate = felementsize
        elif felementname == 'openInterest' and felementsize > maxwidthopenInterest:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthopenInterest = felementsize
        elif felementname == 'oraclePrice' and felementsize > maxwidthoraclePrice:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthoraclePrice = felementsize
        elif felementname == 'priceChange24H' and felementsize > maxwidthpriceChange24H:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthpriceChange24H = felementsize
        elif felementname == 'trades24H' and felementsize > maxwidthtrades24H:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthtrades24H = felementsize
        elif felementname == 'volume24H' and felementsize > maxwidthvolume24H:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthvolume24H = felementsize
        elif felementname == 'effectiveAt' and felementsize > maxwidtheffectiveAt:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidtheffectiveAt = felementsize
        elif felementname == 'effectiveAtHeight' and felementsize > maxwidtheffectiveAtHeight:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidtheffectiveAtHeight = felementsize
        elif felementname == 'marketId' and felementsize > maxwidthmarketId:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthmarketId = felementsize
        elif felementname == 'atomicResolution' and felementsize > maxwidthatomicResolution:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthprice = felementsize
        elif felementname == 'baseAsset' and felementsize > maxwidthbaseAsset:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthprice = felementsize
        elif felementname == 'basePositionNotional' and felementsize > maxwidthbasePositionNotional:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthprice = felementsize
        elif felementname == 'basePositionSize' and felementsize > maxwidthbasePositionSize:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthprice = felementsize
        elif felementname == 'clobPairId' and felementsize > maxwidthclobPairId:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthprice = felementsize
        elif felementname == 'incrementalPositionSize' and felementsize > maxwidthincrementalPositionSize:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthprice = felementsize
        elif felementname == 'initialMarginFraction' and felementsize > maxwidthinitialMarginFraction:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthprice = felementsize
        elif felementname == 'lastPrice' and felementsize > maxwidthlastPrice:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthprice = felementsize
        elif felementname == 'maintenanceMarginFraction' and felementsize > maxwidthmaintenanceMarginFraction:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthprice = felementsize
        elif felementname == 'maxPositionSize' and felementsize > maxwidthmaxPositionSize:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthprice = felementsize
        elif felementname == 'minOrderBaseQuantums' and felementsize > maxwidthminOrderBaseQuantums:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthprice = felementsize
        elif felementname == 'quantumConversionExponent' and felementsize > maxwidthquantumConversionExponent:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthprice = felementsize
        elif felementname == 'quoteAsset' and felementsize > maxwidthquoteAsset:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthprice = felementsize
        elif felementname == 'status' and felementsize > maxwidthstatus:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthprice = felementsize
        elif felementname == 'stepBaseQuantums' and felementsize > maxwidthstepBaseQuantums:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthprice = felementsize
        elif felementname == 'stepSize' and felementsize > maxwidthstepSize:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthprice = felementsize
        elif felementname == 'subticksPerTick' and felementsize > maxwidthsubticksPerTick:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthprice = felementsize
        elif felementname == 'ticker' and felementsize > maxwidthticker:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthprice = felementsize
        elif felementname == 'tickSize' and felementsize > maxwidthtickSize:
                fp = open(framdiskpath+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthprice = felementsize
        elif felementname not in [
                'price',
                'size',
                'nextFundingRate',
                'openInterest',
                'priceChange24H',
                'trades24H',
                'volume24H',
                'effectiveAt',
                'effectiveAtHeight',
                'marketId',
                'oraclePrice',
                'atomicResolution',
                'baseAsset',
                'basePositionNotional',
                'basePositionSize',
                'clobPairId',
                'incrementalPositionSize',
                'initialMarginFraction',
                'lastPrice',
                'maintenanceMarginFraction',
                'maxPositionSize',
                'minOrderBaseQuantums',
                'quantumConversionExponent',
                'quoteAsset',
                'status',
                'stepBaseQuantums',
                'stepSize',
                'subticksPerTick',
                'ticker',
                'tickSize',
        ]:
                fp = open(framdiskpath+'/maxwidthgeneric', "a")
                fp.write(felementname+' '+str(felementsize)+'\n')
                fp.close()

def processcontentsdict(
        framdiskpath,
        fcontentsdict
):
        for market, marketdata in fcontentsdict.items():
                if os.path.isdir(framdiskpath+'/'+market) == False:
                        os.system('mkdir -p '+framdiskpath+'/'+market)
                for marketdataelement, marketdatavalue in marketdata.items():
                        if marketdataelement == 'price':
                                marketdataelement = 'oraclePrice'
                        fp = open(framdiskpath+'/'+market+'/'+marketdataelement, "w")
                        fp.write(str(marketdatavalue)+' '+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
                        fp.close()
                        checkwidth(
                                framdiskpath = framdiskpath,
                                fmarket = market,
                                felementname = marketdataelement,
                                felementsize = len(str(marketdatavalue))
                        )

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
maxwidthoraclePrice = 0
maxwidthpriceChange24H = 0
maxwidthtrades24H = 0
maxwidthvolume24H = 0
maxwidtheffectiveAt = 0
maxwidtheffectiveAtHeight = 0
maxwidthmarketId = 0
maxwidthatomicResolution = 0
maxwidthbaseAsset = 0
maxwidthbasePositionNotional = 0
maxwidthbasePositionSize = 0
maxwidthclobPairId = 0
maxwidthincrementalPositionSize = 0
maxwidthinitialMarginFraction = 0
maxwidthlastPrice = 0
maxwidthmaintenanceMarginFraction = 0
maxwidthmaxPositionSize = 0
maxwidthminOrderBaseQuantums = 0
maxwidthquantumConversionExponent = 0
maxwidthquoteAsset = 0
maxwidthstatus = 0
maxwidthstepBaseQuantums = 0
maxwidthstepSize = 0
maxwidthsubticksPerTick = 0
maxwidthticker = 0
maxwidthtickSize = 0
openconnection()
while True:
        try:
                api_data = ws.recv()
                api_data = json.loads(api_data)
                if isinstance(api_data['contents'], dict):
                        if 'markets' in api_data['contents'].keys():
                                processcontentsdict(
                                        framdiskpath = ramdiskpath,
                                        fcontentsdict = api_data['contents']['markets']
                                )
                                logger.info("{'timestamp': '"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"'} (markets)")
                                logger.info(api_data['contents']['markets'])
                        elif 'trading' in api_data['contents'].keys():
                                processcontentsdict(
                                        framdiskpath = ramdiskpath,
                                        fcontentsdict = api_data['contents']['trading']
                                )
                                logger.info("{'timestamp': '"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"'} (trading)")
                                logger.info(api_data['contents']['trading'])
                        elif 'oraclePrices' in api_data['contents'].keys():
                                processcontentsdict(
                                        framdiskpath = ramdiskpath,
                                        fcontentsdict = api_data['contents']['oraclePrices']
                                )
                                logger.info("{'timestamp': '"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"'} (oraclePrices)")
                                logger.info(api_data['contents']['oraclePrices'])
                        else:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" === v4_markets key not handled ===")
                                print(api_data['contents'].keys)
                                logger.info("{'timestamp': '"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"'} (OTHER)")
                                logger.info(api_data['contents'])
                        logger.info("{'timestamp': '"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"'} (DICT)")
                        logger.info(api_data)
                elif isinstance(api_data['contents'], list):
                        for item in api_data['contents']:
                                if 'markets' in item.keys():
                                        processcontentsdict(
                                                framdiskpath = ramdiskpath,
                                                fcontentsdict = item['markets']
                                        )
                                        logger.info("{'timestamp': '"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"'} (markets)")
                                        logger.info(item['markets'])
                                if 'trading' in item.keys():
                                        processcontentsdict(
                                                framdiskpath = ramdiskpath,
                                                fcontentsdict = item['trading']
                                        )
                                        logger.info("{'timestamp': '"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"'} (trading)")
                                        logger.info(item['trading'])
                                elif 'oraclePrices' in item.keys():
                                        processcontentsdict(
                                                framdiskpath = ramdiskpath,
                                                fcontentsdict = item['oraclePrices']
                                )
                                        logger.info("{'timestamp': '"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"'} (oraclePrices)")
                                        logger.info(item['oraclePrices'])
                                else:
                                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" === v4_markets key not handled ===")
                                        print(item.keys())
                                        logger.info("{'timestamp': '"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"'} (OTHER)")
                                        logger.info(item)
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
