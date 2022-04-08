import datetime
import os
import sys
import time

RED='\033[0;31m'
GREEN='\033[0;32m'
REDWHITE='\033[0;31mi\u001b[47m'
GREENWHITE='\033[0;32m\u001b[47m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

sep = " "
while True:
        with open('/mnt/ramdisk/lasttrade') as fp:
                for line in fp:
                        fname = line.strip('\n\r').split(sep)
                        fcreatedat = fname[0]
                        fprice = fname[1]
                        fside = fname[2]
                        fsize = fname[3]
        fp.close()
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Last trade: ', fcreatedat, fprice, fside, fsize)
        askarray = []
        bidarray = []
        if fside == 'BUY':
                os.system('ls /mnt/ramdisk/asks | sort -n > /mnt/ramdisk/list')
                count = 1
                with open('/mnt/ramdisk/list') as fp:
                        for line in fp:
                                line = line.strip('\n\r')
                                if count > 10:
                                        break
                                else:
                                        if float(line) >= float(fprice):
                                                with open('/mnt/ramdisk/asks/'+line) as fp2:
                                                        for line2 in fp2:
                                                                fname = line2.strip('\n\r').split(sep)
                                                                faskoffset = fname[0]
                                                                fasksize = fname[1]
                                                                fdate = fname[2]
                                                                ftime = fname[3]
                                                                if fasksize != '0':
                                                                        askarray.append([line, fasksize, faskoffset, fdate, ftime])
                                                                        count += 1
                                                fp2.close()
                fp.close()
                os.system('ls /mnt/ramdisk/bids | sort -n -r > /mnt/ramdisk/list')
                count = 1
                with open('/mnt/ramdisk/list') as fp:
                        for line in fp:
                                line = line.strip('\n\r')
                                if count > 10:
                                        break
                                else:
                                        if float(line) < float(fprice):
                                                with open('/mnt/ramdisk/bids/'+line) as fp2:
                                                        for line2 in fp2:
                                                                fname = line2.strip('\n\r').split(sep)
                                                                fbidoffset = fname[0]
                                                                fbidsize = fname[1]
                                                                fdate = fname[2]
                                                                ftime = fname[3]
                                                                if fbidsize != '0':
                                                                        bidarray.append([line, fbidsize, fbidoffset, fdate, ftime])
                                                                        count += 1
                                                fp2.close()
                fp.close()
        else:
                os.system('ls /mnt/ramdisk/asks | sort -n > /mnt/ramdisk/list')
                count = 1
                with open('/mnt/ramdisk/list') as fp:
                        for line in fp:
                                line = line.strip('\n\r')
                                if count > 10:
                                        break
                                else:
                                        if float(line) > float(fprice):
                                                with open('/mnt/ramdisk/asks/'+line) as fp2:
                                                        for line2 in fp2:
                                                                fname = line2.strip('\n\r').split(sep)
                                                                faskoffset = fname[0]
                                                                fasksize = fname[1]
                                                                fdate = fname[2]
                                                                ftime = fname[3]
                                                                if fasksize != '0':
                                                                        askarray.append([line, fasksize, faskoffset, fdate, ftime])
                                                                        count += 1
                                                fp2.close()
                fp.close()
                os.system('ls /mnt/ramdisk/bids | sort -n -r > /mnt/ramdisk/list')
                count = 1
                with open('/mnt/ramdisk/list') as fp:
                        for line in fp:
                                line = line.strip('\n\r')
                                if count > 10:
                                        break
                                else:
                                        if float(line) <= float(fprice):
                                                with open('/mnt/ramdisk/bids/'+line) as fp2:
                                                        for line2 in fp2:
                                                                fname = line2.strip('\n\r').split(sep)
                                                                fbidoffset = fname[0]
                                                                fbidsize = fname[1]
                                                                fdate = fname[2]
                                                                ftime = fname[3]
                                                                if fbidsize != '0':
                                                                        bidarray.append([line, fbidsize, fbidoffset, fdate, ftime])
                                                                        count += 1
                                                fp2.close()
                fp.close()
        count = 0
        if len(sys.argv) > 1 and sys.argv[1] == 'compact':
                print('Bid                                   | Ask')
        else:
                print('Bid                                              | Ask')
        while count < 10:
                biditem = bidarray[count]
                biditemprice = biditem[0]
                biditemsize = biditem[1]
                biditemoffset = biditem[2]
                biditemdate = biditem[3]
                biditemtime = biditem[4]
                askitem = askarray[count]
                askitemprice = askitem[0]
                askitemsize = askitem[1]
                askitemoffset = askitem[2]
                askitemdate = askitem[3]
                askitemtime = askitem[4]
                if len(sys.argv) > 1 and sys.argv[1] == 'compact':
                        biditemoffset=''
                        askitemoffset=''
                if biditemprice == fprice:
                        print(REDWHITE+biditemprice+NC, str('('+biditemsize+')').ljust(10), biditemoffset, biditemdate, biditemtime+' | '+askitemprice, str('('+askitemsize+')').ljust(10), askitemoffset, askitemdate, askitemtime)
                elif askitemprice == fprice:
                        print(biditemprice, str('('+biditemsize+')').ljust(10), biditemoffset, biditemdate, biditemtime+' | '+GREENWHITE+askitemprice+NC, str('('+askitemsize+')').ljust(10), askitemoffset, askitemdate, askitemtime)
                else:
                        print(biditemprice, str('('+biditemsize+')').ljust(10), biditemoffset, biditemdate, biditemtime+' | '+askitemprice, str('('+askitemsize+')').ljust(10), askitemoffset, askitemdate, askitemtime)
                count += 1
        time.sleep(1)
