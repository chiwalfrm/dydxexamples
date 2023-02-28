#!/bin/sh
#per 1hr: 0.5 / 24 = 0.0208333333333333 --> 208
#per 1hr: 1.0 / 24 = 0.0416666666666667 --> 416
starttimestamp=`date +%s`
i1=416
if [ -t 1 ]
then
        RED='\033[0;31m'
        GREEN='\033[0;32m'
        YELLOW='\033[0;33m'
        CYAN='\033[0;36m'
        NC='\033[0m' # No Color
else
        RED=''
        GREEN=''
        YELLOW=''
        CYAN=''
        NC=''
fi
XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:-/tmp}
s8=0
s9=0
for s1 in $*
do
        market=`echo $s1 | cut -d : -f 1`
        python3 dydxl2funding.py $market | grep "'rate': " | cut -d \' -f 4 > $XDG_RUNTIME_DIR/dydxl2funding$market.out 2>&1 &
done
wait
for s1 in $*
do
        market=`echo $s1 | cut -d : -f 1`
        highlight=`echo $s1 | cut -d : -f 2`
        if [ "$highlight" = 1 ]
        then
                backgroundcolor='\e[1;46m'
        else
                backgroundcolor=
        fi
        s4=`head -1 $XDG_RUNTIME_DIR/dydxl2funding$market.out`
        for s5 in `head -8 $XDG_RUNTIME_DIR/dydxl2funding$market.out`
        do
                s9=`LC_NUMERIC=en_US.utf8 /usr/bin/printf "$s9 + %f\n" $s5 | bc`
        done
        for s2 in `head -24 $XDG_RUNTIME_DIR/dydxl2funding$market.out`
        do
                s8=`LC_NUMERIC=en_US.utf8 /usr/bin/printf "$s8 + %f\n" $s2 | bc`
        done
        /usr/bin/printf "${backgroundcolor}%-12s \e[0m" $market
        s10=`printf "%.0f\n" "\`LC_NUMERIC=en_US.utf8 /usr/bin/printf \"%f * 1000000\n\" $s4 | bc | sed 's/^-//'\`"`
        if [ "$s10" -gt "$i1" ]
        then
                LC_NUMERIC=en_US.utf8 /usr/bin/printf "${RED}%'9.6f (1hr)${NC} " $s4
        else
                LC_NUMERIC=en_US.utf8 /usr/bin/printf "${GREEN}%'9.6f (1hr)${NC} " $s4
        fi
        s10=`printf "%.0f\n" "\`LC_NUMERIC=en_US.utf8 /usr/bin/printf \"%f * 1000000\n\" $s9 | bc | sed 's/^-//'\`"`
        if [ "$s10" -gt "`echo \"$i1 * 8\" | bc`" ]
        then
                LC_NUMERIC=en_US.utf8 /usr/bin/printf "${RED}%'9.6f (8hr)${NC} " $s9
        else
                LC_NUMERIC=en_US.utf8 /usr/bin/printf "${GREEN}%'9.6f (8hr)${NC} " $s9
        fi
        s10=`printf "%.0f\n" "\`LC_NUMERIC=en_US.utf8 /usr/bin/printf \"%f * 1000000\n\" $s8 | bc | sed 's/^-//'\`"`
        if [ "$s10" -gt "`echo \"$i1 * 24\" | bc`" ]
        then
                LC_NUMERIC=en_US.utf8 /usr/bin/printf "${RED}%'9.6f (24hr)${NC} dydxl2\n" $s8
        else
                LC_NUMERIC=en_US.utf8 /usr/bin/printf "${GREEN}%'9.6f (24hr)${NC} dydxl2\n" $s8
        fi
done
endtimestamp=`date +%s`
echo "Generated: `date` / Runtime $((endtimestamp - starttimestamp)) seconds"
