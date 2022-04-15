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

def checkaskfiles():
        if exists(ramdiskpath+'/'+market+'/asks/'+askprice) == True:
                fp = open(ramdiskpath+'/'+market+'/asks/'+askprice)
                line = fp.readline()
                fname = line.strip('\n\r').split(sep)
                fp.close()
                faskoffset = fname[0]
                fasksize = fname[1]
        if exists(ramdiskpath+'/'+market+'/asks/'+askprice) == False or askoffset > faskoffset:
                fp = open(ramdiskpath+'/'+market+'/asks/'+askprice, "w")
                fp.write(askoffset+' '+asksize+' '+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
                fp.close()
                logger.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' Updated '+ramdiskpath+'/'+market+'/asks/'+askprice+': '+str('('+asksize+')').ljust(10)+' '+askoffset)

def checkbidfiles():
        if exists(ramdiskpath+'/'+market+'/bids/'+bidprice) == True:
                fp = open(ramdiskpath+'/'+market+'/bids/'+bidprice)
                line = fp.readline()
                fname = line.strip('\n\r').split(sep)
                fp.close()
                fbidoffset = fname[0]
                fbidsize = fname[1]
        if exists(ramdiskpath+'/'+market+'/bids/'+bidprice) == False or bidoffset > fbidoffset:
                fp = open(ramdiskpath+'/'+market+'/bids/'+bidprice, "w")
                fp.write(bidoffset+' '+bidsize+' '+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
                fp.close()
                logger.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' Updated '+ramdiskpath+'/'+market+'/bids/'+bidprice+': '+str('('+bidsize+')').ljust(10)+' '+bidoffset)

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

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' dydxob.py')
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
                try:
                        openconnection()
                except Exception as error:
                        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "WebSocket message failed (%s)" % error)
                        ws.close()
                        time.sleep(random.randint(1,10))
