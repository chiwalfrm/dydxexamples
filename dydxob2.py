import os
import time

sep = " "
while True:
        with open('/mnt/ramdisk/lasttrade') as fp:
                for line in fp:
                        fname = line.strip('\n\r').split(sep)
                        fprice = fname[0]
                        fside = fname[1]
        fp.close()
        print('Last trade: ', fprice, fside)
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
                                                                if fasksize != '0':
                                                                        askarray.append([line, fasksize, faskoffset])
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
                                                                if fbidsize != '0':
                                                                        bidarray.append([line, fbidsize, fbidoffset])
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
                                                                if fasksize != '0':
                                                                        askarray.append([line, fasksize, faskoffset])
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
                                                                if fbidsize != '0':
                                                                        bidarray.append([line, fbidsize, fbidoffset])
                                                                        count += 1
                                                fp2.close()
                fp.close()
        count = 0
        print('Bid                                        Ask')
        while count < 10:
                biditem = bidarray[count]
                biditemprice = biditem[0]
                biditemsize = biditem[1]
                biditemoffset = biditem[2]
                askitem = askarray[count]
                askitemprice = askitem[0]
                askitemsize = askitem[1]
                askitemoffset = askitem[2]
                print(biditemprice.ljust(10), str('('+biditemsize+')').ljust(10), biditemoffset.ljust(20), askitemprice.ljust(10), str('('+askitemsize+')').ljust(10), askitemoffset.ljust(20))
                count += 1
        time.sleep(1)
vmware@ubuntu20041a:~/extra/github$ vi dydxob2.py
vmware@ubuntu20041a:~/extra/github$ cat dydxob2.py
import os
import time

sep = " "
while True:
        with open('/mnt/ramdisk/lasttrade') as fp:
                for line in fp:
                        fname = line.strip('\n\r').split(sep)
                        fprice = fname[0]
                        fside = fname[1]
        fp.close()
        print('Last trade: ', fprice, fside)
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
                                                                if fasksize != '0':
                                                                        askarray.append([line, fasksize, faskoffset])
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
                                                                if fbidsize != '0':
                                                                        bidarray.append([line, fbidsize, fbidoffset])
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
                                                                if fasksize != '0':
                                                                        askarray.append([line, fasksize, faskoffset])
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
                                                                if fbidsize != '0':
                                                                        bidarray.append([line, fbidsize, fbidoffset])
                                                                        count += 1
                                                fp2.close()
                fp.close()
        count = 0
        print('Bid                                        Ask')
        while count < 10:
                biditem = bidarray[count]
                biditemprice = biditem[0]
                biditemsize = biditem[1]
                biditemoffset = biditem[2]
                askitem = askarray[count]
                askitemprice = askitem[0]
                askitemsize = askitem[1]
                askitemoffset = askitem[2]
                print(biditemprice.ljust(10), str('('+biditemsize+')').ljust(10), biditemoffset.ljust(20), askitemprice.ljust(10), str('('+askitemsize+')').ljust(10), askitemoffset.ljust(20))
                count += 1
        time.sleep(1)
