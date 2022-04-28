#!/bin/sh
zerosumhistoryfile=$1
cut -d , -f 5 $zerosumhistoryfile | sort -u | while read l1
do
        f1sum=0
        grep ",$l1," $zerosumhistoryfile | grep ",BUY," | cut -d , -f 9 | while read f1
        do
                f1
                sum=`echo $f1sum + $f1 | bc -l`
                echo $f1sum > f1sum
        done
        f1sum=0
        grep ",$l1," $zerosumhistoryfile | grep ",SELL," | cut -d , -f 9 | while read f1
        do
                f1sum=`echo $f1sum +
                $f1 | bc -l`
                echo $f1sum > f1sum2
        done
        echo $l1 `echo \`cat f1sum\` - \`cat f1sum2\` | bc -l`
done | grep -v ' 0$'
rm f1sum f1sum2
