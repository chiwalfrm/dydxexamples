import datetime
import os
import pprint
import signal
import sys
import time
from os.path import exists
from sys import platform

widthmarketstats = 24
widthprice = 10
widthsize = 10
widthoffset = 11

if platform == "linux" or platform == "linux2":
        # linux
        ramdiskpath = '/mnt/ramdisk'
elif platform == "darwin":
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
        cleanup()
        exit()

def checkmarketdata(file):
        if exists(ramdiskpath+'/'+market+'/'+file) == True:
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

def cleanup():
        os.system('rm '+ramdiskpath+'/'+market+'/lista'+str(pid))
        os.system('rm '+ramdiskpath+'/'+market+'/listb'+str(pid))

pp = pprint.PrettyPrinter(width = 41, compact = True)
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' dydxob2.py')
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
if exists(ramdiskpath+'/'+market+'/asks') == False:
        print('Error: Asks directory', ramdiskpath+'/'+market+'/asks', 'not found')
        exit()
if exists(ramdiskpath+'/'+market+'/bids') == False:
        print('Error: Bids directory', ramdiskpath+'/'+market+'/bids', 'not found')
        exit()
if exists(ramdiskpath+'/'+market+'/lasttrade') == False:
        print('Warning: lasttrade file', ramdiskpath+'/'+market+'/lasttrade', 'not found')
while True:
        if exists(ramdiskpath+'/'+market+'/lasttrade') == True:
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
        os.system('ls '+ramdiskpath+'/'+market+'/asks | sort -n > '+ramdiskpath+'/'+market+'/lista'+str(pid))
        os.system('ls '+ramdiskpath+'/'+market+'/bids | sort -n -r > '+ramdiskpath+'/'+market+'/listb'+str(pid))
        with open(ramdiskpath+'/'+market+'/lista'+str(pid)) as fp:
                for line in fp:
                        line = line.strip('\n\r')
                        fname = []
                        while len(fname) != 4:
                                fp2 = open(ramdiskpath+'/'+market+'/asks/'+line)
                                line2 = fp2.readline()
                                fname = line2.strip('\n\r').split(sep)
                                fp2.close()
                        faskoffset = fname[0]
                        fasksize = fname[1]
                        fdate = fname[2]
                        ftime = fname[3]
                        if fasksize != '0':
                                askarray.append([line, fasksize, faskoffset, fdate, ftime])
        with open(ramdiskpath+'/'+market+'/listb'+str(pid)) as fp:
                for line in fp:
                        line = line.strip('\n\r')
                        fname = []
                        while len(fname) != 4:
                                fp2 = open(ramdiskpath+'/'+market+'/bids/'+line)
                                line2 = fp2.readline()
                                fname = line2.strip('\n\r').split(sep)
                                fp2.close()
                        fbidoffset = fname[0]
                        fbidsize = fname[1]
                        fdate = fname[2]
                        ftime = fname[3]
                        if fbidsize != '0':
                                bidarray.append([line, fbidsize, fbidoffset, fdate, ftime])
        highestbidprice = 0
        while highestbidprice == 0 or highestbidprice > lowestaskprice:
                highestbid = bidarray[0]
                lowestask = askarray[0]
                highestbidprice = float(highestbid[0])
                lowestaskprice = float(lowestask[0])
                highestbidoffset = int(highestbid[2])
                lowestaskoffset = int(lowestask[2])
                if highestbidoffset < lowestaskoffset:
                        bidarray.pop(0)
                else:
                        askarray.pop(0)
        count = 0
        highestoffset = 0
        bidsizetotal = 0
        asksizetotal = 0
        if len(sys.argv) > 3 and ( sys.argv[3] == 'compact' or sys.argv[3] == 'ultracompact' ):
                if sys.argv[3] == 'compact':
                        if fcreatedat != 0:
                                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fcreatedat, fprice, fside, fsize)
                        print('Bid'+' '.ljust(widthprice+widthsize+15)+'| Ask')
                elif sys.argv[3] == 'ultracompact':
                        if fcreatedat != 0:
                                print(fcreatedat[5:], fprice, fside, fsize)
                        print('Bid'+' '.ljust(widthprice+widthsize+1)+'| Ask')
        else:
                if fcreatedat != 0:
                        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Last trade:', fcreatedat, fprice, fside, fsize)
                print('Bid'+' '.ljust(widthprice+widthsize+widthoffset+22)+'| Ask')
        while count < min(depth, len(bidarray), len(askarray)):
                biditem = bidarray[count]
                biditemprice = float(biditem[0])
                biditemsize = float(biditem[1])
                biditemoffset = int(biditem[2])
                biditemdate = ' '+biditem[3]
                biditemtime = ' '+biditem[4]
                askitem = askarray[count]
                askitemprice = float(askitem[0])
                askitemsize = float(askitem[1])
                askitemoffset = int(askitem[2])
                askitemdate = ' '+askitem[3]
                askitemtime = ' '+askitem[4]
                highestoffset = max(biditemoffset, askitemoffset, highestoffset)
                bidsizetotal += biditemsize
                asksizetotal += askitemsize
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
                print(str(biditemprice).ljust(widthprice), str('('+str(biditemsize)+')').ljust(widthsize+2)+biditemoffset+biditemdate+biditemtime+' | '+str(askitemprice).ljust(widthprice), str('('+str(askitemsize)+')').ljust(widthsize+2)+askitemoffset+askitemdate+askitemtime, end = '\r')
                if sys.argv[-1] != 'noansi' and fcreatedat != 0:
                        if biditemprice == float(fprice):
                                print(REDWHITE+str(biditemprice)+NC, end = '\r')
                        elif askitemprice == float(fprice):
                                print(str(biditemprice).ljust(widthprice), str('('+str(biditemsize)+')').ljust(widthsize+2)+biditemoffset+biditemdate+biditemtime+' | '+GREENWHITE+str(askitemprice)+NC, end = '\r')
                print()
                count += 1
        print('maxbid   :', highestbidprice)
        print('minask   :', lowestaskprice, '(+'+'{0:.4f}'.format(lowestaskprice - highestbidprice)+')', '{0:.4f}'.format((lowestaskprice - highestbidprice) / highestbidprice * 100)+'%')
        print('bidvolume:', bidsizetotal)
        print('askvolume:', asksizetotal)
        print('minoffset:', lowestoffset)
        print('maxoffset:', highestoffset, '(+'+str(highestoffset - lowestoffset)+')')
        checkmarketdata('indexPrice')
        checkmarketdata('oraclePrice')
        checkmarketdata('priceChange24H')
        checkmarketdata('nextFundingRate')
        checkmarketdata('nextFundingAt')
        checkmarketdata('openInterest')
        checkmarketdata('trades24H')
        checkmarketdata('volume24H')
        if exists(ramdiskpath+'/'+market+'/EXITFLAG') == True:
                os.system('rm '+ramdiskpath+'/'+market+'/EXITFLAG')
                cleanup()
                exit()
        else:
                time.sleep(1)
