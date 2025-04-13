#!/bin/sh
#11/21/2022 was the low
#get the csv file from https://www.investing.com/crypto/bitcoin/historical-data

printmsg()
{
        fmsg=$1
        fhighdate=`echo $msg | awk '{print $1}'`
        fhigh=`echo $msg | awk '{print $2}'`
        fhigh=`/usr/bin/printf "%'.2f\n" $fhigh`
        fdate=`echo $msg | awk '{print $3}'`
        flowprice=`echo $msg | awk '{print $4}'`
        flowprice=`/usr/bin/printf "%'.2f\n" $flowprice`
        fdelta=`echo $msg | awk '{print $5}'`
        fdelta=`/usr/bin/printf "%'.2f\n" $fdelta`
        fmaxdeltapercentage=`echo $msg | awk '{print $6}'`
        fnumdays=`echo $msg | awk '{print $7}'`
        printf "%10s:%11s:%10s:%11s:%11s:%7s:%4s\n" $fhighdate $fhigh $fdate $flowprice "-$fdelta" "-$fmaxdeltapercentage" "$fnumdays"
}
high=0
maxdelta=0
maxdeltapercentage=0
firstrun=1
if [ $# -lt 2 ]
then
        echo "Error: Must provide price file and percentage-drawdown"
        exit
fi
file=$1
drawdown=$2
sep='"'
echo "  HighDate:       High:   LowDate:        Low:      Delta: %Delta:Days"
grep -v '^"Date","Price","Open","High","Low","Vol.","Change %"$' $file | tac | while read f1
do
        date=`echo $f1 | cut -d "$sep" -f 2`
        highprice=`echo $f1 | cut -d "$sep" -f 8 | tr -d ,`
        lowprice=`echo $f1 | cut -d "$sep" -f 10 | tr -d ,`
        if [ `echo "$highprice > $high" | bc -l` -eq 1 ]
        then
                high=$highprice
                highdate=$date
                maxdelta=0
                if [ ! -z "$msg" ]
                then
                        printmsg $msg | tee /tmp/analyzedrawdown1.log$$
                        msg=
                fi
        else
                delta=`echo "$high - $lowprice" | bc -l`
                if [ `echo "$delta > $maxdelta" | bc -l` -eq 1 ]
                then
                        maxdelta=$delta
                        maxdeltapercentage=`echo "$maxdelta / $high * 100" | bc -l`
                        maxdeltapercentage=`printf "%.2f" $maxdeltapercentage`
                        if [ "$firstrun" -ne 1 ] && [ `echo "$maxdeltapercentage >= $drawdown" | bc -l` -eq 1 ]
                        then
#                               msg=`printf "%10s:%11s:%10s:%11s:%13s:%7s:%4s\n" $date $high $highdate $lowprice "-$delta" "-maxdeltapercentage" "$(( ($(date --date=$date +%s) - $(date --date=$highdate +%s) )/(60*60*24) ))"`
                                msg=`printf "$highdate $high $date $lowprice $delta $maxdeltapercentage $(( ($(date --date=$date +%s) - $(date --date=$highdate +%s) )/(60*60*24) ))\n"`
#                               msg=`printf "highdate=$highdate lowdate=$date high=$high low=$lowprice delta=-$delta days=$(( ($(date --date=$date +%s) - $(date --date=$highdate +%s) )/(60*60*24) )) %.2f%s\n" -$maxdeltapercentage '%'`
                        fi
#                       printf "%10s:%11s:%10s:%11s:%13s:%7s:%3s\n" $date $high $highdate $lowprice "-$delta" "-"-maxdeltapercentage" "$(( ($(date --date=$date +%s) - $(date --date=$highdate +%s) )/(60*60*24) ))"
                        printmsg "$highdate $high $date $lowprice $delta $maxdeltapercentage $(( ($(date --date=$date +%s) - $(date --date=$highdate +%s) )/(60*60*24) ))" > /tmp/analyzedrawdown2.log$$
#                       printf "highdate=$highdate lowdate=$date high=$high low=$lowprice delta=-$delta days=$(( ($(date --date=$date +%s) - $(date --date=$highdate +%s) )/(60*60*24) )) %.2f%s\n" -$maxdeltapercentage '%' > /tmp/analyzedrawdown2.log$$
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
