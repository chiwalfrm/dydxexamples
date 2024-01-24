#!/bin/sh
high=0
maxdelta=0
maxdeltapercentage=0
firstrun=1
if [ $# -ne 1 ]
then
        echo "Error: Must provide price file"
        exit
fi
file=$1
if [ `grep -c : $file` -eq 0 ]
then
        sep=,
else
        sep=:
fi
grep -v '^Date,Open,High,Low,Close,Adj Close,Volume$' $file | while read f1
do
        date=`echo $f1 | cut -d $sep -f 1`
        highprice=`echo $f1 | cut -d $sep -f 3`
        lowprice=`echo $f1 | cut -d $sep -f 4`
        if [ `echo "$highprice > $high" | bc -l` -eq 1 ]
        then
                high=$highprice
                maxdelta=0
                if [ ! -z "$msg" ]
                then
                        echo $msg | tee /tmp/analyzedrawdown1.log$$
                        msg=
                fi
        else
                delta=`echo "$high - $lowprice" | bc -l`
                if [ `echo "$delta > $maxdelta" | bc -l` -eq 1 ]
                then
                        maxdelta=$delta
                        maxdeltapercentage=`echo "$maxdelta / $high * 100" | bc -l`
                        if [ "$firstrun" -ne 1 ] && [ `echo "$maxdeltapercentage >= 20" | bc -l` -eq 1 ]
                        then
                                msg=`printf "date=$date high=$high lowprice=$lowprice delta=$delta %.2f%s\n" -$maxdeltapercentage '%'`
                        fi
                        printf "date=$date high=$high lowprice=$lowprice delta=$delta %.2f%s\n" -$maxdeltapercentage '%' > /tmp/analyzedrawdown2.log$$
                fi
        fi
        if [ "$firstrun" -eq 1 ]
        then
                firstrun=0
        fi
done
cmp /tmp/analyzedrawdown[12].log$$ >> /dev/null
if [ $? -ne 0 ]
then
        cat /tmp/analyzedrawdown2.log$$
fi
rm /tmp/analyzedrawdown[12].log$$
