#!/bin/sh

sendnotification()
{
# this section is to send notification on trades and errors
# put your own code here
        echo
}

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
if [ ! -z "$2" ]
then
        # close a specific market
        python3 $WORKINGDIR/v4dydxcli.py $apikeyfile positions | awk '{print $2" "$3}' | grep "^$2 " > /tmp/closeallpositions.log$$
else
        # close all markets
        python3 $WORKINGDIR/v4dydxcli.py $apikeyfile positions | awk '{print $2" "$3}' > /tmp/closeallpositions.log$$
fi
if [ ! -s /tmp/closeallpositions.log$$ ]
then
        echo "*** NO OPEN POSITION(S) ***"
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
                echo "python3 $WORKINGDIR/v4dydxcli.py $apikeyfile buyquantity $dydxmarket ${quantity#-}"
                cd $WORKINGDIR
                python3 $WORKINGDIR/v4dydxcli.py $apikeyfile buyquantity $dydxmarket ${quantity#-} > /tmp/closeallpositions2.log$$
                cd -
                if [ "`tail -1 /tmp/closeallpositions2.log$$`" != FILLED ]
                then
                        echo "Error: Problem with order"
                        cat /tmp/closeallpositions2.log$$
                        sendnotification "Error: Problem with order"
                fi
        else
                # close long position
                echo "python3 $WORKINGDIR/v4dydxcli.py $apikeyfile sellquantity $dydxmarket $quantity"
                cd $WORKINGDIR
                python3 $WORKINGDIR/v4dydxcli.py $apikeyfile sellquantity $dydxmarket $quantity > /tmp/closeallpositions2.log$$
                cd -
                if [ "`tail -1 /tmp/closeallpositions2.log$$`" != FILLED ]
                then
                        echo "Error: Problem with order"
                        cat /tmp/closeallpositions2.log$$
                        sendnotification "Error: Problem with order"
                fi
        fi
done
python3 $WORKINGDIR/v4dydxcli.py $apikeyfile positions > /tmp/closeallpositions.log$$
if [ ! -s /tmp/closeallpositions.log$$ ]
then
        echo "*** ALL POSITION(S) CLOSED ***"
else
        echo "Error: Some position(s) still open"
        cat /tmp/closeallpositions.log$$
fi
dateend=`date +%s`
echo "===== `date` Runtime $((dateend-datestart)) seconds (closeallpositions.sh)"
rm -f /tmp/closeallpositions.log$$ /tmp/closeallpositions2.log$$
