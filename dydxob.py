import json
import logging
import os
import sys
import time
from datetime import datetime
from logging import handlers
from pprint import PrettyPrinter
from random import randint
from websocket import create_connection

def checkaskfiles():
        global zeroaskoffset
        if os.path.isfile(ramdiskpath+'/'+market+'/asks/'+askprice) == True:
                fp = open(ramdiskpath+'/'+market+'/asks/'+askprice)
                line = fp.readline()
                fname = line.strip('\n\r').split(sep)
                fp.close()
                faskoffset = fname[0]
                fasksize = fname[1]
        else:
                faskoffset = 0
        if ( os.path.isfile(ramdiskpath+'/'+market+'/asks/'+askprice) == False and int(askoffset) > zeroaskoffset ) or int(askoffset) > int(faskoffset):
                if asksize == '0':
                        if os.path.isfile(ramdiskpath+'/'+market+'/asks/'+askprice) == True:
                                os.remove(ramdiskpath+'/'+market+'/asks/'+askprice)
                                zeroaskoffset = int(askoffset)
                else:
                        fp = open(ramdiskpath+'/'+market+'/asks/'+askprice, "w")
                        fp.write(askoffset+' '+asksize+' '+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
                        fp.close()
                logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' Updated '+ramdiskpath+'/'+market+'/asks/'+askprice+': '+str('('+asksize+')').ljust(10)+' '+askoffset)

def checkbidfiles():
        global zerobidoffset
        if os.path.isfile(ramdiskpath+'/'+market+'/bids/'+bidprice) == True:
                fp = open(ramdiskpath+'/'+market+'/bids/'+bidprice)
                line = fp.readline()
                fname = line.strip('\n\r').split(sep)
                fp.close()
                fbidoffset = fname[0]
                fbidsize = fname[1]
        else:
                fbidoffset = 0
        if ( os.path.isfile(ramdiskpath+'/'+market+'/bids/'+bidprice) == False and int(bidoffset) > zerobidoffset ) or int(bidoffset) > int(fbidoffset):
                if bidsize == '0':
                        if os.path.isfile(ramdiskpath+'/'+market+'/bids/'+bidprice) == True:
                                os.remove(ramdiskpath+'/'+market+'/bids/'+bidprice)
                                zerobidoffset = int(bidoffset)
                else:
                        fp = open(ramdiskpath+'/'+market+'/bids/'+bidprice, "w")
                        fp.write(bidoffset+' '+bidsize+' '+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
                        fp.close()
                logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' Updated '+ramdiskpath+'/'+market+'/bids/'+bidprice+': '+str('('+bidsize+')').ljust(10)+' '+bidoffset)

def openconnection():
        global ws
        global askprice
        global askoffset
        global asksize
        global bidprice
        global bidoffset
        global bidsize
#       ws = create_connection("wss://api.stage.dydx.exchange/v3/ws")
        ws = create_connection("wss://api.dydx.exchange/v3/ws")
        api_data = {
                "type": "subscribe",
                "channel": "v3_orderbook",
                "id": market,
                "includeOffsets": True
        }
        ws.send(json.dumps(api_data))
        api_data = ws.recv()
        api_data = json.loads(api_data)
        pp.pprint(api_data)
        api_data = ws.recv()
        api_data = json.loads(api_data)
        asks = api_data['contents']['asks']
        bids = api_data['contents']['bids']
        for askitem in asks:
                askprice = askitem['price']
                askoffset = askitem['offset']
                asksize = askitem['size']
                checkaskfiles()
                checkwidth('price', len(askprice))
                checkwidth('size', len(asksize))
        for biditem in bids:
                bidprice = biditem['price']
                bidoffset = biditem['offset']
                bidsize = biditem['size']
                checkbidfiles()
                checkwidth('price', len(bidprice))
                checkwidth('size', len(bidsize))

def checkwidth(elementname, elementsize):
        global maxwidthprice
        global maxwidthsize
        if elementname == 'price' and elementsize > maxwidthprice:
                fp = open(ramdiskpath+'/'+market+'/maxwidth'+elementname, "w")
                fp.write(str(elementsize)+'\n')
                fp.close()
                maxwidthprice = elementsize
        elif elementname == 'size' and elementsize > maxwidthsize:
                fp = open(ramdiskpath+'/'+market+'/maxwidth'+elementname, "w")
                fp.write(str(elementsize)+'\n')
                fp.close()
                maxwidthsize = elementsize

print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' dydxob.py')
logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
pp = PrettyPrinter(width = 41, compact = True)
if sys.platform == "linux" or sys.platform == "linux2":
        # linux
        ramdiskpath = '/mnt/ramdisk'
elif sys.platform == "darwin":
        # OS X
        ramdiskpath = '/Volumes/RAMDisk'
sep = " "

if len(sys.argv) < 2:
        market = 'BTC-USD'
else:
        market = sys.argv[1]
handler = logging.handlers.RotatingFileHandler(ramdiskpath+'/dydxob'+market+'.log',
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
                asks = api_data['contents']['asks']
                bids = api_data['contents']['bids']
                offset = api_data['contents']['offset']
                if asks != []:
                        for askitem in asks:
                                askprice = askitem[0]
                                askoffset = offset
                                asksize = askitem[1]
                                checkaskfiles()
                                checkwidth('price', len(askprice))
                                checkwidth('size', len(asksize))
                if bids != []:
                        for biditem in bids:
                                bidprice = biditem[0]
                                bidoffset = offset
                                bidsize = biditem[1]
                                checkbidfiles()
                                checkwidth('price', len(bidprice))
                                checkwidth('size', len(bidsize))
        except KeyboardInterrupt:
                ws.close()
                sys.exit(0)
        except Exception as error:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "WebSocket message failed (%s)" % error)
                ws.close()
                time.sleep(1)
                try:
                        os.system('rm -rf '+ramdiskpath+'/'+market+'/asks')
                        os.system('rm -rf '+ramdiskpath+'/'+market+'/bids')
                        os.system('mkdir -p '+ramdiskpath+'/'+market+'/asks')
                        os.system('mkdir -p '+ramdiskpath+'/'+market+'/bids')
                        openconnection()
                except Exception as error:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "WebSocket message failed (%s)" % error)
                        ws.close()
                        time.sleep(randint(1,10))
