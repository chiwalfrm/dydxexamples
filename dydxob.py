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

def openconnection():
        global ws
        global api_data
#       ws = create_connection("wss://api.stage.dydx.exchange/v3/ws")
        ws = create_connection("wss://api.dydx.exchange/v3/ws")
        api_data = {
                "type": "subscribe",
                "channel": "v3_trades",
                "id": market
        }
        ws.send(json.dumps(api_data))
        api_data = ws.recv()
        api_data = json.loads(api_data)
        pp.pprint(api_data)
        api_data = ws.recv()
        api_data = json.loads(api_data)
        pp.pprint(api_data)

def checkwidth(elementname, elementsize):
        global maxwidthtradeprice
        global maxwidthtradesize
        if elementname == 'tradeprice' and elementsize > maxwidthtradeprice:
                fp = open(ramdiskpath+'/'+market+'/maxwidth'+elementname, "w")
                fp.write(str(elementsize)+'\n')
                fp.close()
                maxwidthtradeprice = elementsize
        elif elementname == 'tradesize' and elementsize > maxwidthtradesize:
                fp = open(ramdiskpath+'/'+market+'/maxwidth'+elementname, "w")
                fp.write(str(elementsize)+'\n')
                fp.close()
                maxwidthtradesize = elementsize

print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' dydxtrades.py')
logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
pp = PrettyPrinter(width = 41, compact = True)
if sys.platform == "linux" or sys.platform == "linux2":
        # linux
        ramdiskpath = '/mnt/ramdisk'
elif sys.platform == "darwin":
        # OS X
        ramdiskpath = '/Volumes/RAMDisk'

if len(sys.argv) < 2:
        market = 'BTC-USD'
else:
        market = sys.argv[1]
handler = logging.handlers.RotatingFileHandler(ramdiskpath+'/dydxtrades'+market+'.log',
        maxBytes = 2097152,
        backupCount = 4
)
logger.addHandler(handler)

if os.path.isdir(ramdiskpath) == False:
        print('Error: Ramdisk', ramdiskpath, 'not mounted')
        sys.exit()
if os.path.ismount(ramdiskpath) == False:
        print('Warning:', ramdiskpath, 'is not a mount point')
if os.path.isdir(ramdiskpath+'/'+market) == False:
        os.system('mkdir -p '+ramdiskpath+'/'+market)

maxwidthtradeprice = 0
maxwidthtradesize = 0
openconnection()
while True:
        try:
                trades = api_data['contents']['trades'][0]
                tradecreatedat = trades['createdAt']
                tradeliquidation = trades['liquidation']
                tradeprice = trades['price']
                tradeside = trades['side']
                tradesize = trades['size']
                if tradeliquidation == True:
                        liquidationstring = 'L'
                        fp = open(ramdiskpath+'/'+market+'/liquidations', "a")
                        fp.write(tradecreatedat+' '+tradeprice+' '+tradeside+' ('+tradesize+')L\n')
                        fp.close()
                else:
                        liquidationstring = ''
                fp = open(ramdiskpath+'/'+market+'/lasttrade', "w")
                fp.write(tradecreatedat+' '+tradeprice+' '+tradeside+' ('+tradesize+')'+liquidationstring+'\n')
                fp.close()
                logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' '+tradecreatedat+' '+tradeprice+' '+tradeside.ljust(4)+' ('+tradesize+')'+liquidationstring)
                checkwidth('tradeprice', len(tradeprice))
                checkwidth('tradesize', len(tradesize))
                api_data = ws.recv()
                api_data = json.loads(api_data)
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
vmware@ubuntu20041a:/mnt/repository$ ls -altr `cat /tmp/boo`
-rwxr-xr-x 1 vmware vmware  928 Apr 29  2022 dydxcheckhistory.sh
-rwxr-xr-x 1 vmware vmware  510 Sep 30 09:47 monitorfilesystem.sh
-rwxr-xr-x 1 vmware vmware 7779 Jan 18 09:41 update_rewards.sh
-rw-rw-r-- 1 vmware vmware  225 Feb  1 10:14 gasnow.py
-rw-rw-r-- 1 vmware vmware  321 Feb  1 10:15 dydxmarkets.py
-rw-rw-r-- 1 vmware vmware  400 Feb  1 15:54 dydxl2funding.txt
-rw-rw-r-- 1 vmware vmware  751 Feb  3 15:50 dydxfees.py
-rwxr-xr-x 1 vmware vmware 2109 Feb  3 23:43 dydxl2funding.sh
-rw-rw-r-- 1 vmware vmware  628 Feb  6 01:46 dydxl2funding.py
-rw-rw-r-- 1 vmware vmware 4626 Feb  7 08:12 dydxv3markets.py
-rw-rw-r-- 1 vmware vmware 3473 Feb  7 08:22 dydxtrades.py
-rw-rw-r-- 1 vmware vmware 6022 Feb  7 08:22 dydxob.py
-rw-rw-r-- 1 vmware vmware 8232 Feb  7 11:34 dydxob2.py
vmware@ubuntu20041a:/mnt/repository$ claer; cat dydxob.py

Command 'claer' not found, did you mean:

  command 'clear' from deb ncurses-bin (6.2-0ubuntu2)

Try: sudo apt install <deb name>

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
                        os.system('rmdir -r '+ramdiskpath+'/'+market+'/asks')
                        os.system('rmdir -r '+ramdiskpath+'/'+market+'/bids')
                        os.system('mkdir -p '+ramdiskpath+'/'+market+'/asks')
                        os.system('mkdir -p '+ramdiskpath+'/'+market+'/bids')
                        openconnection()
                except Exception as error:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "WebSocket message failed (%s)" % error)
                        ws.close()
                        time.sleep(randint(1,10))
