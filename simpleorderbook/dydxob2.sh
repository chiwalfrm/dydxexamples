#!/bin/sh
if [ $# -eq 0 ]
then
        echo "Error: Must specify marketusd."
        exit
fi
marketusd=$1
if [ -z "$2" ]
then
        depth=10
else
        depth=$2
fi
python3 dydxob2b.py $marketusd
counter=0
echo "`date +"%Y-%m-%d %H:%M:%S"` Last trade: `head -1 ${marketusd}trades`"
echo "Bid                   | Ask"
bidvolume=0
askvolume=0
cat ${marketusd}orderbook | while read l1
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
                echo $bidprice > ${marketusd}maxbid
                echo $askprice > ${marketusd}minask
        fi
        bidvolume=`echo $bidvolume + $bidsize | bc -l`
        askvolume=`echo $askvolume + $asksize | bc -l`
        echo $bidvolume > ${marketusd}bidvolume
        echo $askvolume > ${marketusd}askvolume
        /usr/bin/printf "%-10s %-10s | %-10s %-10s\n" $bidprice "($bidsize)" $askprice "($asksize)"
        counter=$((counter+1))
        if [ "$counter" -gt "$depth" ]
        then
                exit
        fi
done
maxbid=`cat ${marketusd}maxbid`
minask=`cat ${marketusd}minask`
bidvolume=`cat ${marketusd}bidvolume`
askvolume=`cat ${marketusd}askvolume`
bidaskdifference=`echo $minask - $maxbid | bc -l`
bidaskdifferencepercentage=`echo $bidaskdifference / $maxbid "*" 100 | bc -l`
echo "maxbid   : $maxbid"
/usr/bin/printf "minask   : %s (+%.4f) %.4f%%\n" $minask $bidaskdifference $bidaskdifferencepercentage
echo "bidvolume: $bidvolume"
echo "askvolume: $askvolume"
cat ${marketusd}markets
rm ${marketusd}bids ${marketusd}asks ${marketusd}orderbook ${marketusd}trades ${marketusd}maxbid ${marketusd}minask ${marketusd}markets ${marketusd}bidvolume ${marketusd}askvolume
