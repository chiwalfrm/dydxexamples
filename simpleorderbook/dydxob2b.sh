#!/bin/sh
if [ -t 1 ]
then
        RED='\033[0;31m'
        GREEN='\033[0;32m'
        YELLOW='\033[0;33m'
        CYAN='\033[0;36m'
        NC='\033[0m' # No Color
        REDWHITE='\033[0;31;47m'
        GREENWHITE='\033[0;32;47m'
else
        RED=''
        GREEN=''
        YELLOW=''
        CYAN=''
        NC=''
        REDWHITE=''
        GREENWHITE=''
fi
ppid=$1
marketusd=$2
depth=$3
counter=0
lasttrade=`head -1 /tmp/${marketusd}trades$ppid`
lasttradeprice=`echo $lasttrade | awk '{print $2}'`
echo "`date +"%Y-%m-%d %H:%M:%S"` Last trade: $lasttrade"
echo "Bid                   | Ask"
bidvolume=0
askvolume=0
paste -d ',' /tmp/${marketusd}bids$ppid /tmp/${marketusd}asks$ppid > /tmp/${marketusd}orderbook$ppid
cat /tmp/${marketusd}orderbook$ppid | while read l1
do
        bid=`echo $l1 | cut -d , -f 1`
        ask=`echo $l1 | cut -d , -f 2`
        if [ ! -z "$bid" ]
        then
                bidprice=`echo $bid | cut -d ' ' -f 2`
                bidsize=`echo $bid | cut -d ' ' -f 1`
        fi
        if [ ! -z "$ask" ]
        then
                askprice=`echo $ask | cut -d ' ' -f 2`
                asksize=`echo $ask | cut -d ' ' -f 1`
        fi
        if [ "$counter" -eq 0 ]
        then
                echo $bidprice > /tmp/${marketusd}maxbid$ppid
                echo $askprice > /tmp/${marketusd}minask$ppid
        fi
        bidvolume=`echo $bidvolume + $bidsize | bc -l`
        askvolume=`echo $askvolume + $asksize | bc -l`
        echo $bidvolume > /tmp/${marketusd}bidvolume$ppid
        echo $askvolume > /tmp/${marketusd}askvolume$ppid
        if [ "$counter" -eq 0 -a "$4" != "noansi" ]
        then
                if [ "$bidprice" = "$lasttradeprice" ]
                then
                        /usr/bin/printf "${REDWHITE}%-10s${NC} %-10s | %-10s %-10s\n" $bidprice "($bidsize)" $askprice "($asksize)"
                elif [ "$askprice" = "$lasttradeprice" ]
                then
                        /usr/bin/printf "%-10s %-10s | ${GREENWHITE}%-10s${NC} %-10s\n" $bidprice "($bidsize)" $askprice "($asksize)"
                else
                        /usr/bin/printf "%-10s %-10s | %-10s %-10s\n" $bidprice "($bidsize)" $askprice "($asksize)"
                fi
        else
                /usr/bin/printf "%-10s %-10s | %-10s %-10s\n" $bidprice "($bidsize)" $askprice "($asksize)"
        fi
        counter=$((counter+1))
        if [ "$counter" -gt "$depth" ]
        then
                exit
        fi
done
maxbid=`cat /tmp/${marketusd}maxbid$ppid`
minask=`cat /tmp/${marketusd}minask$ppid`
bidvolume=`cat /tmp/${marketusd}bidvolume$ppid`
askvolume=`cat /tmp/${marketusd}askvolume$ppid`
bidaskdifference=`echo $minask - $maxbid | bc -l`
bidaskdifferencepercentage=`echo $bidaskdifference / $maxbid "*" 100 | bc -l`
echo "maxbid   : $maxbid"
/usr/bin/printf "minask   : %s (+%.4f) %.4f%%\n" $minask $bidaskdifference $bidaskdifferencepercentage
echo "bidvolume: $bidvolume"
echo "askvolume: $askvolume"
cat /tmp/${marketusd}markets$ppid
rm -f /tmp/${marketusd}bids$ppid /tmp/${marketusd}asks$ppid /tmp/${marketusd}trades$ppid /tmp/${marketusd}markets$ppid /tmp/${marketusd}orderbook$ppid /tmp/${marketusd}maxbid$ppid /tmp/${marketusd}minask$ppid /tmp/${marketusd}bidvolume$ppid /tmp/${marketusd}askvolume$ppid
