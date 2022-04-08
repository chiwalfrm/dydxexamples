import datetime
import json
import pprint
import sys
import time
from os.path import exists
from websocket import create_connection

def checkaskfiles():
        if exists('/mnt/ramdisk/asks/'+askprice) == True:
                with open('/mnt/ramdisk/asks/'+askprice) as fp:
                        for line in fp:
                                fname = line.strip('\n\r').split(sep)
                                faskoffset = fname[0]
                                fasksize = fname[1]
                fp.close()
        if exists('/mnt/ramdisk/asks/'+askprice) == False or askoffset > faskoffset:
                with open('/mnt/ramdisk/asks/'+askprice, "w") as fp:
                        fp.write(askoffset+' '+asksize+' '+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' Updated /mnt/ramdisk/asks/'+askprice+':', str('('+asksize+')').ljust(10), askoffset)
                fp.close()

def checkbidfiles():
        if exists('/mnt/ramdisk/bids/'+bidprice) == True:
                with open('/mnt/ramdisk/bids/'+bidprice) as fp:
                        for line in fp:
                                fname = line.strip('\n\r').split(sep)
                                fbidoffset = fname[0]
                                fbidsize = fname[1]
                fp.close()
        if exists('/mnt/ramdisk/bids/'+bidprice) == False or bidoffset > fbidoffset:
                with open('/mnt/ramdisk/bids/'+bidprice, "w") as fp:
                        fp.write(bidoffset+' '+bidsize+' '+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' Updated /mnt/ramdisk/bids/'+bidprice+':', str('('+bidsize+')').ljust(10), bidoffset)
                fp.close()


pp = pprint.PrettyPrinter(width = 41, compact = True)
sep = " "
ws = create_connection("wss://api.dydx.exchange/v3/ws")
api_data = {"type":"subscribe", "channel":"v3_orderbook", "id":"BTC-USD", "includeOffsets":True}
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
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" WebSocket message failed (%s)" % error)
                ws.close()
                time.sleep(1)
