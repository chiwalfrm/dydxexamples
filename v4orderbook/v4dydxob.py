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

def checkaskfiles(
        framdiskpath,
        fmarket,
        faskprice,
        fasksize,
        faskoffset,
):
        global zeroaskoffset
        if os.path.isfile(framdiskpath+'/'+fmarket+'/asks/'+faskprice) == True:
                fp = open(framdiskpath+'/'+fmarket+'/asks/'+faskprice)
                line = fp.readline()
                fname = line.strip('\n\r').split(sep)
                fp.close()
                ffaskoffset = fname[0]
                ffasksize = fname[1]
        else:
                ffaskoffset = 0
        if ( os.path.isfile(framdiskpath+'/'+fmarket+'/asks/'+faskprice) == False and int(faskoffset) > zeroaskoffset ) or int(faskoffset) > int(ffaskoffset):
                if fasksize == '0':
                        if os.path.isfile(framdiskpath+'/'+fmarket+'/asks/'+faskprice) == True:
                                os.remove(framdiskpath+'/'+fmarket+'/asks/'+faskprice)
                                zeroaskoffset = int(faskoffset)
                else:
                        fp = open(framdiskpath+'/'+fmarket+'/asks/'+faskprice, "w")
                        fp.write(str(faskoffset)+' '+fasksize+' '+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
                        fp.close()
                logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' Updated '+framdiskpath+'/'+fmarket+'/asks/'+faskprice+': '+str('('+fasksize+')').ljust(10)+' '+str(faskoffset))

def checkbidfiles(
        framdiskpath,
        fmarket,
        fbidprice,
        fbidsize,
        fbidoffset,
):
        global zerobidoffset
        if os.path.isfile(framdiskpath+'/'+fmarket+'/bids/'+fbidprice) == True:
                fp = open(framdiskpath+'/'+fmarket+'/bids/'+fbidprice)
                line = fp.readline()
                fname = line.strip('\n\r').split(sep)
                fp.close()
                ffbidoffset = fname[0]
                ffbidsize = fname[1]
        else:
                ffbidoffset = 0
        if ( os.path.isfile(framdiskpath+'/'+fmarket+'/bids/'+fbidprice) == False and int(fbidoffset) > zerobidoffset ) or int(fbidoffset) > int(ffbidoffset):
                if fbidsize == '0':
                        if os.path.isfile(framdiskpath+'/'+fmarket+'/bids/'+fbidprice) == True:
                                os.remove(framdiskpath+'/'+fmarket+'/bids/'+fbidprice)
                                zerobidoffset = int(fbidoffset)
                else:
                        fp = open(framdiskpath+'/'+fmarket+'/bids/'+fbidprice, "w")
                        fp.write(str(fbidoffset)+' '+fbidsize+' '+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
                        fp.close()
                logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' Updated '+framdiskpath+'/'+fmarket+'/bids/'+fbidprice+': '+str('('+fbidsize+')').ljust(10)+' '+str(fbidoffset))

def openconnection():
        global ws
        ws = create_connection(WSINDEXERURL)
        api_data = {
                "type": "subscribe",
                "channel": "v4_orderbook",
                "id": market,
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
        global maxwidthprice
        global maxwidthsize
        if felementname == 'price' and felementsize > maxwidthprice:
                fp = open(framdiskpath+'/'+fmarket+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthprice = felementsize
        elif felementname == 'size' and felementsize > maxwidthsize:
                fp = open(framdiskpath+'/'+fmarket+'/maxwidth'+felementname, "w")
                fp.write(str(felementsize)+'\n')
                fp.close()
                maxwidthsize = felementsize

print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' v4dydxob.py')
logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
if sys.platform == "linux" or sys.platform == "linux2":
        # linux
        ramdiskpath = '/mnt/ramdisk5'
elif sys.platform == "darwin":
        # OS X
        ramdiskpath = '/Volumes/RAMDisk5'
sep = " "

if len(sys.argv) < 2:
        market = 'BTC-USD'
else:
        market = sys.argv[1]
handler = logging.handlers.RotatingFileHandler(ramdiskpath+'/v4dydxob'+market+'.log',
        maxBytes = 2097152,
        backupCount = 4
)
logger.addHandler(handler)

if os.path.isdir(ramdiskpath) == False:
        print('Error: Ramdisk', ramdiskpath, 'not mounted')
        sys.exit()
if os.path.ismount(ramdiskpath) == False:
        print('Warning:', ramdiskpath, 'is not a mount point')
if os.path.isdir(ramdiskpath+'/'+market+'/asks') == False:
        os.system('mkdir -p '+ramdiskpath+'/'+market+'/asks')
if os.path.isdir(ramdiskpath+'/'+market+'/bids') == False:
        os.system('mkdir -p '+ramdiskpath+'/'+market+'/bids')

maxwidthprice = 0
maxwidthsize = 0
zeroaskoffset = 0
zerobidoffset = 0
openconnection()
while True:
        try:
                api_data = ws.recv()
                api_data = json.loads(api_data)
                askoffset = api_data['message_id']
                bidoffset = api_data['message_id']
                if isinstance(api_data['contents'], dict):
                        if 'asks' in api_data['contents'].keys():
                                asks = api_data['contents']['asks']
                        else:
                                asks = []
                        if 'bids' in api_data['contents'].keys():
                                bids = api_data['contents']['bids']
                        else:
                                bids = []
                elif isinstance(api_data['contents'], list):
                        asks = []
                        bids = []
                        for item in api_data['contents']:
                                if 'asks' in item.keys():
                                        for bitem in item['asks']:
                                                if isinstance(bitem, dict):
                                                        askprice = bitem['price']
                                                        asksize = bitem['size']
                                                elif isinstance(bitem, list):
                                                        askprice = bitem[0]
                                                        asksize = bitem[1]
                                                askitem = {
                                                        "price": askprice,
                                                        "size": asksize
                                                }
                                                asks.append(askitem)
                                if 'bids' in item.keys():
                                        for bitem in item['bids']:
                                                if isinstance(bitem, dict):
                                                        bidprice = bitem['price']
                                                        bidsize = bitem['size']
                                                elif isinstance(bitem, list):
                                                        bidprice = bitem[0]
                                                        bidsize = bitem[1]
                                                biditem = {
                                                        "price": bidprice,
                                                        "size": bidsize
                                                }
                                                bids.append(biditem)


                if asks != []:
                        for askitem in asks:
                                if isinstance(askitem, dict):
                                        askprice = askitem['price']
                                        asksize = askitem['size']
                                elif isinstance(askitem, list):
                                        askprice = askitem[0]
                                        asksize = askitem[1]
                                checkaskfiles(
                                        framdiskpath = ramdiskpath,
                                        fmarket = market,
                                        faskprice = askprice,
                                        fasksize = asksize,
                                        faskoffset = askoffset,
                                )
                        checkwidth(
                                framdiskpath = ramdiskpath,
                                fmarket = market,
                                felementname = 'price',
                                felementsize = len(askprice)
                        )
                        checkwidth(
                                framdiskpath = ramdiskpath,
                                fmarket = market,
                                felementname = 'size',
                                felementsize = len(asksize)
                        )
                if bids != []:
                        for biditem in bids:
                                if isinstance(biditem, dict):
                                        bidprice = biditem['price']
                                        bidsize = biditem['size']
                                elif isinstance(biditem, list):
                                        bidprice = biditem[0]
                                        bidsize = biditem[1]
                                checkbidfiles(
                                        framdiskpath = ramdiskpath,
                                        fmarket = market,
                                        fbidprice = bidprice,
                                        fbidsize = bidsize,
                                        fbidoffset = bidoffset,
                                )
                        checkwidth(
                                framdiskpath = ramdiskpath,
                                fmarket = market,
                                felementname = 'price',
                                felementsize = len(bidprice)
                        )
                        checkwidth(
                                framdiskpath = ramdiskpath,
                                fmarket = market,
                                felementname = 'size',
                                felementsize = len(bidsize)
                        )
        except KeyboardInterrupt:
                ws.close()
                sys.exit(0)
        except Exception as error:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "WebSocket message failed (%s)" % error)
                ws.close()
                time.sleep(1)
                try:
                        os.system('rm -rf '+ramdiskpath+'/'+market+'/asks/*')
                        os.system('rm -rf '+ramdiskpath+'/'+market+'/bids/*')
                        openconnection()
                except Exception as error:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "WebSocket message failed (%s)" % error)
                        ws.close()
                        time.sleep(randint(1,10))
