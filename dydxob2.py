import os
import signal
import sys
import time
from datetime import datetime
from pprint import PrettyPrinter

widthmarketstats = 24
widthprice = 10
widthsize = 10
widthoffset = 11

if sys.platform == "linux" or sys.platform == "linux2":
        # linux
        ramdiskpath = '/mnt/ramdisk'
elif sys.platform == "darwin":
        # OS X
        ramdiskpath = '/Volumes/RAMDisk'
#Note: regular output needs 103 columns, compact 67, ultracompact 39

RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
CYAN = '\033[0;36m'
NC = '\033[0m' # No Color
REDWHITE = '\033[0;31m\u001b[47m'
GREENWHITE = '\033[0;32m\u001b[47m'

def handler(signum, frame):
        sys.exit()

def checkmarketdata(file):
        if os.path.isfile(ramdiskpath+'/'+market+'/'+file) == True:
                fname = []
                while len(fname) != 3:
                        fp = open(ramdiskpath+'/'+market+'/'+file)
                        line = fp.readline()
                        fname = line.strip('\n\r').split(sep)
                        fp.close()
                element0 = fname[0]
                if len(sys.argv) > 3 and sys.argv[3] == 'ultracompact':
                        element1 = ''
                else:
                        element1 = ' '+fname[1]+' '+fname[2]
                print(file.ljust(15)+':', element0[:widthmarketstats].ljust(widthmarketstats)+element1)

pp = PrettyPrinter(width = 41, compact = True)
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' dydxob2.py')
pid = os.getpid()
sep = " "
signal.signal(signal.SIGINT, handler)
if len(sys.argv) < 2:
        market = 'BTC-USD'
else:
        market = sys.argv[1]
if len(sys.argv) < 3:
        depth = 10
else:
        depth = int(sys.argv[2])
if os.path.isdir(ramdiskpath+'/'+market+'/asks') == False:
        print('Error: Asks directory', ramdiskpath+'/'+market+'/asks', 'not found')
        sys.exit()
if os.path.isdir(ramdiskpath+'/'+market+'/bids') == False:
        print('Error: Bids directory', ramdiskpath+'/'+market+'/bids', 'not found')
        sys.exit()
if os.path.isfile(ramdiskpath+'/'+market+'/lasttrade') == False:
        print('Warning: lasttrade file', ramdiskpath+'/'+market+'/lasttrade', 'not found')
while True:
        starttime = datetime.now()
        if os.path.isfile(ramdiskpath+'/'+market+'/lasttrade') == True:
                fname = []
                while len(fname) != 4:
                        fp = open(ramdiskpath+'/'+market+'/lasttrade')
                        line = fp.readline()
                        fname = line.strip('\n\r').split(sep)
                        fp.close()
                fcreatedat = fname[0]
                fprice = fname[1]
                fside = fname[2]
                fsize = fname[3]
        else:
                fcreatedat = 0
        askarray = []
        bidarray = []
        count = 0
        while os.path.isdir(ramdiskpath+'/'+market+'/asks') == False:
                time.sleep(1)
                count += 1
                if count > 60:
                        print("Error: Timeout waiting for", ramdiskpath+'/'+market+'/asks')
                        sys.exit()
        askprices = os.popen('cd '+ramdiskpath+'/'+market+'/asks; grep "" /dev/null * 2>> /dev/null | sed \'s/:/ /\' | sort -n').read()
        askpriceslist = askprices.split("\n")
        for askprice in askpriceslist:
                if askprice != '':
                        fname = askprice.split(sep)
                        if len(fname) == 5:
                                line = fname[0]
                                faskoffset = fname[1]
                                fasksize = fname[2]
                                fdate = fname[3]
                                ftime = fname[4]
                                askarray.append([line, fasksize, faskoffset, fdate, ftime])
        count = 0
        while os.path.isdir(ramdiskpath+'/'+market+'/bids') == False:
                time.sleep(1)
                count += 1
                if count > 60:
                        print("Error: Timeout waiting for", ramdiskpath+'/'+market+'/bids')
                        sys.exit()
        bidprices = os.popen('cd '+ramdiskpath+'/'+market+'/bids; grep "" /dev/null * 2>> /dev/null | sed \'s/:/ /\' | sort -n -r').read()
        bidpriceslist = bidprices.split("\n")
        for bidprice in bidpriceslist:
                if bidprice != '':
                        fname = bidprice.split(sep)
                        if len(fname) == 5:
                                line = fname[0]
                                fbidoffset = fname[1]
                                fbidsize = fname[2]
                                fdate = fname[3]
                                ftime = fname[4]
                                bidarray.append([line, fbidsize, fbidoffset, fdate, ftime])
        if len(bidarray) == 0 or len(askarray) == 0:
                print('Warning: asks or bids empty', str(len(bidarray)), str(len(askarray)), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                fp = open(ramdiskpath+'/'+market+'/TRAPemptyarrays', "a")
                fp.write(str(len(bidarray))+','+str(len(askarray))+',0,'+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
                fp.close()
                if os.path.isfile(os.path.dirname(__file__)+'/'+market+'/EXITFLAG'):
                        sys.exit()
                elif os.path.isfile(ramdiskpath+'/'+market+'/EXITFLAG') == True:
                        os.system('rm '+ramdiskpath+'/'+market+'/EXITFLAG')
                        sys.exit()
                else:
                        time.sleep(1)
                        continue
        highestbidprice = 0
        lowestaskprice = 0
        while len(bidarray) > 0 and len(askarray) > 0 and ( highestbidprice == 0 or highestbidprice >= lowestaskprice ):
                highestbid = bidarray[0]
                lowestask = askarray[0]
                highestbidprice = float(highestbid[0])
                lowestaskprice = float(lowestask[0])
                highestbidsize = float(highestbid[1])
                lowestasksize = float(lowestask[1])
                highestbidoffset = int(highestbid[2])
                lowestaskoffset = int(lowestask[2])
                if highestbidprice >= lowestaskprice:
                        if highestbidoffset < lowestaskoffset:
                                bidarray.pop(0)
                        elif highestbidoffset > lowestaskoffset:
                                askarray.pop(0)
                        else:
                                fp = open(ramdiskpath+'/'+market+'/TRAPsameoffset', "a")
                                fp.write(str(highestbidprice)+','+str(lowestaskprice)+','+str(highestbidoffset)+','+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
                                fp.close()
                                if highestbidsize < lowestasksize:
                                        bidarray.pop(0)
                                else:
                                        askarray.pop(0)
        if len(bidarray) == 0 or len(askarray) == 0:
                print('Warning: asks or bids empty', str(len(bidarray)), str(len(askarray)), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                fp = open(ramdiskpath+'/'+market+'/TRAPemptyarrays', "a")
                fp.write(str(len(bidarray))+','+str(len(askarray))+',1,'+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
                fp.close()
                if os.path.isfile(os.path.dirname(__file__)+'/'+market+'/EXITFLAG'):
                        sys.exit()
                elif os.path.isfile(ramdiskpath+'/'+market+'/EXITFLAG') == True:
                        os.system('rm '+ramdiskpath+'/'+market+'/EXITFLAG')
                        sys.exit()
                else:
                        time.sleep(1)
                        continue
        count = 0
        highestoffset = 0
        lowestoffset = 0
        bidsizetotal = 0
        asksizetotal = 0
        if len(sys.argv) > 3 and ( sys.argv[3] == 'compact' or sys.argv[3] == 'ultracompact' ):
                if sys.argv[3] == 'compact':
                        if fcreatedat != 0:
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fcreatedat, fprice, fside, fsize)
                        print('Bid'+' '.ljust(widthprice+widthsize+26)+'| Ask')
                elif sys.argv[3] == 'ultracompact':
                        if fcreatedat != 0:
                                print(fcreatedat[5:], fprice, fside, fsize)
                        print('Bid'+' '.ljust(widthprice+widthsize+12)+'| Ask')
        else:
                if fcreatedat != 0:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Last trade:', fcreatedat, fprice, fside, fsize)
                print('Bid'+' '.ljust(widthprice+widthsize+widthoffset+21)+'| Ask')
        while count < min(depth, max(len(bidarray), len(askarray))):
                if count < len(bidarray):
                        biditem = bidarray[count]
                        biditemprice = float(biditem[0])
                        biditemsize = float(biditem[1])
                        biditemoffset = int(biditem[2])
                        biditemdate = ' '+biditem[3]
                        biditemtime = ' '+biditem[4]
                else:
                        biditemprice = ''
                        biditemsize = ''
                        biditemoffset = 0
                        biditemdate = ''
                        biditemtime = ''
                if count < len(askarray):
                        askitem = askarray[count]
                        askitemprice = float(askitem[0])
                        askitemsize = float(askitem[1])
                        askitemoffset = int(askitem[2])
                        askitemdate = ' '+askitem[3]
                        askitemtime = ' '+askitem[4]
                else:
                        askitemprice = ''
                        askitemsize = ''
                        askitemoffset = 0
                        askitemdate = ''
                        askitemtime = ''
                highestoffset = max(biditemoffset, askitemoffset, highestoffset)
                if biditemsize != '':
                        bidsizetotal += biditemsize
                        biditemsizet = '('+str(biditemsize)+')'
                        biditemoffsett = str(biditemoffset)
                else:
                        biditemsizet = ''
                        biditemoffsett = ''
                if askitemsize != '':
                        asksizetotal += askitemsize
                        askitemsizet = '('+str(askitemsize)+')'
                        askitemoffsett = str(askitemoffset)
                else:
                        askitemsizet = ''
                        askitemoffsett = ''
                if count == 0:
                        highestbidprice = biditemprice
                        lowestaskprice = askitemprice
                        lowestoffset = min(biditemoffset, askitemoffset)
                else:
                        lowestoffset = min(biditemoffset, askitemoffset, lowestoffset)
                if len(sys.argv) > 3 and ( sys.argv[3] == 'compact' or sys.argv[3] == 'ultracompact' ):
                        if sys.argv[3] == 'compact':
                                biditemoffset = ''
                                askitemoffset = ''
                                biditemdate = biditemdate[6:]
                                askitemdate = askitemdate[6:]
                        elif sys.argv[3] == 'ultracompact':
                                biditemoffset = ''
                                askitemoffset = ''
                                biditemdate = ''
                                askitemdate = ''
                                biditemtime = ''
                                askitemtime = ''
                else:
                        biditemoffset = ' '+str(biditemoffset).ljust(widthoffset)
                        askitemoffset = ' '+str(askitemoffset).ljust(widthoffset)
                print(str(biditemprice).ljust(widthprice), biditemsizet.ljust(widthsize+2)+biditemoffsett.rjust(widthoffset)+biditemdate+biditemtime+' | '+str(askitemprice).ljust(widthprice), askitemsizet.ljust(widthsize+2)+askitemoffsett.rjust(widthoffset)+askitemdate+askitemtime, end = '\r')
                if sys.argv[-1] != 'noansi' and fcreatedat != 0:
                        if biditemprice == float(fprice):
                                print(f"{REDWHITE}{biditemprice}{NC}", end = '\r')
                        elif askitemprice == float(fprice):
                                print(str(biditemprice).ljust(widthprice), biditemsizet.ljust(widthsize+2)+biditemoffsett.rjust(widthoffset)+biditemdate+biditemtime+' | '+GREENWHITE+str(askitemprice)+NC, end = '\r')
                print()
                count += 1
        print('maxbid   :', highestbidprice)
        print('minask   :', lowestaskprice, '(+'+'{0:.4f}'.format(lowestaskprice - highestbidprice)+')', '{0:.4f}'.format((lowestaskprice - highestbidprice) / highestbidprice * 100)+'%')
        print('bidvolume:', bidsizetotal)
        print('askvolume:', asksizetotal)
        print('minoffset:', lowestoffset)
        print(f"maxoffset: {highestoffset} (+{highestoffset - lowestoffset})")
        checkmarketdata('indexPrice')
        checkmarketdata('oraclePrice')
        checkmarketdata('priceChange24H')
        checkmarketdata('nextFundingRate')
        checkmarketdata('nextFundingAt')
        checkmarketdata('openInterest')
        checkmarketdata('trades24H')
        checkmarketdata('volume24H')
        endtime = datetime.now()
        print('Runtime        :' , endtime - starttime)
        if os.path.isfile(os.path.dirname(__file__)+'/'+market+'/EXITFLAG'):
                sys.exit()
        elif os.path.isfile(ramdiskpath+'/'+market+'/EXITFLAG') == True:
                os.system('rm '+ramdiskpath+'/'+market+'/EXITFLAG')
                sys.exit()
        else:
                time.sleep(1)
