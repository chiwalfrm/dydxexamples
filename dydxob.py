import sys
import json
from websocket import create_connection
from os.path import exists

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
                        fp.write(askoffset+' '+asksize+'\n')
                print('Updated /mnt/ramdisk/asks/'+askprice+': ', askoffset, asksize)
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
                        fp.write(bidoffset+' '+bidsize+'\n')
                print('Updated /mnt/ramdisk/bids/'+bidprice+': ', bidoffset, bidsize)
                fp.close()


sep = " "
ws = create_connection("wss://api.dydx.exchange/v3/ws")
api_data = {"type":"subscribe", "channel":"v3_orderbook", "id":"BTC-USD", "includeOffsets":True}
ws.send(json.dumps(api_data))
api_data = ws.recv()
api_data = json.loads(api_data)
print(api_data)
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
