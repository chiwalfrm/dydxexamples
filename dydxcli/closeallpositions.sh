#!/bin/sh
datestart=`date +%s`
WORKINGDIR=`dirname $0`
if [ $# -eq 0 ]
then
        echo "Error: Must specify apikeyfile"
        exit
fi
apikeyfile=$1
if [ ! -f "$apikeyfile" ]
then
        echo "Error: apikeyfile $apikeyfile not found"
        exit
fi
python3 $WORKINGDIR/dydxcli.py $apikeyfile positions > /tmp/closeallpositions.log$$
if [ ! -s /tmp/closeallpositions.log$$ ]
then
        echo "*** NO OPEN POSITIONS ***"
        exit
fi
cat /tmp/closeallpositions.log$$ | while read l1
do
        dydxmarket=`echo $l1 | awk '{print $1}'`
        quantity=`echo $l1 | awk '{print $2}'`
        echo "=== Closing $dydxmarket $quantity"
        if [ "`echo $quantity | cut -c 1`" = '-' ]
        then
                # close short position
                echo "python3 $WORKINGDIR/dydx.py $apikeyfile buyquantity $dydxmarket ${quantity#-}"
                python3 $WORKINGDIR/dydx.py $apikeyfile buyquantity $dydxmarket ${quantity#-} > /tmp/closeallpositions2.log$$
                if [ "`tail -1 /tmp/closeallpositions2.log$$`" != FILLED ]
                then
                        echo "Error: Problem with order"
                        cat /tmp/closeallpositions2.log$$
                        sendnotification "Error: Problem with order"
                fi
        else
                # close long position
                echo "python3 $WORKINGDIR/dydx.py $apikeyfile buyquantity $dydxmarket $quantity"
                python3 $WORKINGDIR/dydx.py $apikeyfile sellquantity $dydxmarket $quantity > /tmp/closeallpositions2.log$$
                if [ "`tail -1 /tmp/closeallpositions2.log$$`" != FILLED ]
                then
                        echo "Error: Problem with order"
                        cat /tmp/closeallpositions2.log$$
                        sendnotification "Error: Problem with order"
                fi
        fi
done
python3 $WORKINGDIR/dydx.py $apikeyfile positions > /tmp/closeallpositions.log$$
if [ ! -s /tmp/closeallpositions.log$$ ]
then
        echo "*** ALL POSITIONS CLOSED ***"
else
        echo "Error: Some positions still open"
        cat /tmp/closeallpositions.log$$
fi
dateend=`date +%s`
echo "===== `date` Runtime $((dateend-datestart)) seconds (closeallpositions.sh)"
rm -f /tmp/closeallpositions.log$$ /tmp/closeallpositions2.log$$
