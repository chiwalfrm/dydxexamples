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

def checkaskfiles():
        if exists(ramdiskpath+'/'+market+'/asks/'+askprice) == True:
                with open(ramdiskpath+'/'+market+'/asks/'+askprice) as fp:
                        for line in fp:
                                fname = line.strip('\n\r').split(sep)
                                faskoffset = fname[0]
                                fasksize = fname[1]
                fp.close()
        if exists(ramdiskpath+'/'+market+'/asks/'+askprice) == False or askoffset > faskoffset:
                with open(ramdiskpath+'/'+market+'/asks/'+askprice, "w") as fp:
                        fp.write(askoffset+' '+asksize+' '+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
                logger.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' Updated '+ramdiskpath+'/'+market+'/asks/'+askprice+': '+str('('+asksize+')').ljust(10)+' '+askoffset)
                fp.close()

def checkbidfiles():
        if exists(ramdiskpath+'/'+market+'/bids/'+bidprice) == True:
                with open(ramdiskpath+'/'+market+'/bids/'+bidprice) as fp:
                        for line in fp:
                                fname = line.strip('\n\r').split(sep)
                                fbidoffset = fname[0]
                                fbidsize = fname[1]
                fp.close()
        if exists(ramdiskpath+'/'+market+'/bids/'+bidprice) == False or bidoffset > fbidoffset:
                with open(ramdiskpath+'/'+market+'/bids/'+bidprice, "w") as fp:
                        fp.write(bidoffset+' '+bidsize+' '+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
                logger.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' Updated '+ramdiskpath+'/'+market+'/bids/'+bidprice+': '+str('('+bidsize+')').ljust(10)+' '+bidoffset)
                fp.close()

def openconnection():
        global ws
        global askprice
        global askoffset
        global asksize
        global bidprice
        global bidoffset
        global bidsize
        ws = create_connection("wss://api.dydx.exchange/v3/ws")
        api_data = {"type":"subscribe", "channel":"v3_orderbook", "id":market, "includeOffsets":True}
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
        for biditem in bids:
                bidprice = biditem['price']
                bidoffset = biditem['offset']
                bidsize = biditem['size']
                checkbidfiles()

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
pp = pprint.PrettyPrinter(width = 41, compact = True)
if platform == "linux" or platform == "linux2":
        # linux
        ramdiskpath = '/mnt/ramdisk'
elif platform == "darwin":
        # OS X
        ramdiskpath = '/Volumes/RAMDisk'
sep = " "

if len(sys.argv) < 2:
        market = 'BTC-USD'
else:
        market = sys.argv[1]
handler = RotatingFileHandler(ramdiskpath+'/dydxob'+market+'.log', maxBytes=1048576,
                              backupCount = 4)
logger.addHandler(handler)

if exists(ramdiskpath) == False:
        print('Error: Ramdisk', ramdiskpath, 'not mounted')
        exit()
if os.path.ismount(ramdiskpath) == False:
        print('Warning:', ramdiskpath, 'is not a mount point')
if exists(ramdiskpath+'/'+market+'/asks') == False:
        os.system('mkdir -p '+ramdiskpath+'/'+market+'/asks')
if exists(ramdiskpath+'/'+market+'/bids') == False:
        os.system('mkdir -p '+ramdiskpath+'/'+market+'/bids')

openconnection()
while True:
        try:
                api_data = ws.recv()
                api_data = json.loads(api_data)
                asks = api_data['contents']['asks']
                bids = api_data['contents']['bids']
                offset = api_data['contents']['offset']
                if asks != []:
                        askprice = asks[0][0]
                        asksize = asks[0][1]
                        askoffset = offset
                        checkaskfiles()
                if bids != []:
                        bidprice = bids[0][0]
                        bidsize = bids[0][1]
                        bidoffset = offset
                        checkbidfiles()
        except KeyboardInterrupt:
                ws.close()
                sys.exit(0)
        except Exception as error:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "WebSocket message failed (%s)" % error)
                ws.close()
                time.sleep(1)
                openconnection()
