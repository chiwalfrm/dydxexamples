#!/bin/sh
if [ ! -t 0 ]
then
        while read -r line
        do
                echo $line
        done > /tmp/dydxcheckhistoryzerosum.stdout$$
        zerosumhistoryfile=/tmp/dydxcheckhistoryzerosum.stdout$$
else
        zerosumhistoryfile=$1
fi
cut -d , -f 5 $zerosumhistoryfile | sort -u | while read l1
do
        f1sum=0
        if [ `grep ",$l1," $zerosumhistoryfile | grep -c ",BUY,"` -eq 0 ]
        then
                echo 0 > f1sum
        else
                grep ",$l1," $zerosumhistoryfile | grep ",BUY," | cut -d , -f 9 | while read f1
                do
                        f1sum=`echo $f1sum + $f1 | bc -l`
                        echo $f1sum > f1sum
                done
        fi
        f1sum=0
        if [ `grep ",$l1," $zerosumhistoryfile | grep -c ",SELL,"` -eq 0 ]
        then
                echo 0 > f1sum2
        else
                grep ",$l1," $zerosumhistoryfile | grep ",SELL," | cut -d , -f 9 | while read f1
                do
                        f1sum=`echo $f1sum + $f1 | bc -l`
                        echo $f1sum > f1sum2
                done
        fi
        echo $l1 `echo \`cat f1sum\` - \`cat f1sum2\` | bc -l`
done | grep -v ' 0$'
rm -f f1sum f1sum2 /tmp/dydxcheckhistoryzerosum.stdout$$
