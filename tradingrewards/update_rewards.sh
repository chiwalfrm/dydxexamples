#!/bin/sh

baseurl=https://chiwalfrm.github.io

cleanup ()
{
        if [ "$1" = "trap" ]
        then
                trap - EXIT INT HUP
                echo
                echo "Ctrl-C detected. Cleaning up. Please wait 60 seconds..."
                if [ "`uname`" = "Darwin" ]
                then
                        killpids="`ps -ef | awk '{print $2" "$3}' | grep " $pid$" | awk '{print $1}'`"
                else
                        killpids="`ps h --ppid $pid -o pid`"
                fi
                if [ "$killpids" != "" ]
                then
                        kill -TERM $killpids 2>> /dev/null
                fi
                sleep 60
        fi
        if [ "`uname`" = "Darwin" ]
        then
                hdiutil detach $TMPFOLDER
        else
                sudo umount $TMPFOLDER
        fi
        exit
}

pid=$$
trap 'cleanup trap' INT HUP

prepare_epoch_file ()
{
        epoch=$1
        cat epoch$epoch.json | python3 -m json.tool | grep -i 0x | cut -d \" -f 2 > $TMPFOLDER/update_rewards$$/epoch$epoch.col1
        cat epoch$epoch.json | python3 -m json.tool | grep -v -i 0x | grep "[0-9]" | cut -d \" -f 2 > $TMPFOLDER/update_rewards$$/epoch$epoch.col2
        paste $TMPFOLDER/update_rewards$$/epoch$epoch.col1 $TMPFOLDER/update_rewards$$/epoch$epoch.col2 > epoch$epoch.txt
}

update_rewards_for_account ()
{
        address=$1
        if [ "$startingepoch" -ne 0 ]
        then
                if [ "`uname`" = "Darwin" ]
                then
                        lastrewards=`grep -i "^$address"$"\t" epoch$startingepoch.txt | awk '{print $2}'`
                else
                        lastrewards=`grep -i -P "^$address\t" epoch$startingepoch.txt | awk '{print $2}'`
                fi
        else
                lastrewards=""
        fi
        if [ "$lastrewards" = "" ]
        then
                fstartingepoch=0
                lastrewards=0
                echo "Epoch#                               Rewards                   Total(Cumulative)"
        else
                fstartingepoch=$((startingepoch+1))
                lastrewards=`echo "$lastrewards / 10^18" | bc -l`
        fi
        while [ $fstartingepoch -le $lastepoch ]
        do
                if [ "`uname`" = "Darwin" ]
                then
                        rewards=`grep -i "^$address"$"\t" epoch$fstartingepoch.txt | awk '{print $2}'`
                else
                        rewards=`grep -i -P "^$address\t" epoch$fstartingepoch.txt | awk '{print $2}'`
                fi
                if [ "$rewards" = "" ]
                then
                        rewards=0
                else
                        rewards=`echo "$rewards / 10^18" | bc -l`
                fi
                f1=`/usr/bin/printf "%'f" \`echo "$rewards - $lastrewards" | bc -l\``
                f2=`/usr/bin/printf "%'f" $rewards`
                if [ $fstartingepoch -lt 10 ]
                then
                        /usr/bin/printf "Epoch%s %37s %35s\n" $fstartingepoch $f1 $f2
                elif [ $fstartingepoch -lt 100 ]
                then
                        /usr/bin/printf "Epoch%s %36s %35s\n" $fstartingepoch $f1 $f2
                fi
                lastrewards=$rewards
                fstartingepoch=$((fstartingepoch+1))
        done
}

create_epoch_html ()
{
        cd output
        count=0
        while [ "$count" -le "$lastepoch" ]
        do
                if [ -f epoch$count.html ]
                then
                        echo "Epoch$count already done (skipped)"
                else
                        for s1 in `ls | grep ^0x`
                        do
                                echo $s1 `grep "^Epoch$count " $s1`
                        done | grep " Epoch[0-9]" | awk '{print $1" "$3}' | grep -v ' 0.000000$' | tr -d , | sort -k 2 -n -r > epoch$count.txt
                        cat << EOF > epoch$count.html
<!DOCTYPE html PUBLIC"ISO/IEC 15445:2000//DTD HTML//EN"><html><head><title>title</title></head><body>
<p style="font-family:'Courier New'">
`wc -l epoch$count.txt | awk '{print $1}'` addresses loaded<br>
Updated at `date`<br>
EOF
                        count2=1
                        awk '{print $1}' epoch$count.txt | while read l1
                        do
                                echo "`grep $l1 whalelist.html | sed 's|<br>$||'` (#$count2)<br>" >> epoch$count.html
                                count2=$((count2+1))
                        done
                        echo '</body></html>' >> epoch$count.html
                        echo "Epoch$count done"
                        rm epoch$count.txt
                fi
                count=$((count+1))
        done
}

intensity=${1:-medium}
if [ "`uname`" = "Darwin" ]
then
        parallel=`sysctl -a | grep machdep.cpu.core_count | awk '{print $2}'`
else
        parallel=`nproc`
fi
case $intensity in
        low)
                parallel=$((parallel/2))
                ;;
        high)
                parallel=$((parallel*2))
                ;;
esac
echo "STAGE  1 Setting up ramdisk..."
if [ "`uname`" = "Darwin" ]
then
        diskutil erasevolume HFS+ "epochdisk" `hdiutil attach -nomount ram://1048576`
        TMPFOLDER=/Volumes/epochdisk
else
        sudo mkdir -p /mnt/epochdisk
        sudo mount -t tmpfs -o rw,size=1024M tmpfs /mnt/epochdisk
        sudo chmod 777 /mnt/epochdisk
        TMPFOLDER=/mnt/epochdisk
fi
mkdir -p $TMPFOLDER/update_rewards$$/output
echo "STAGE  2 Determining starting and last epoch..."
startingepoch=`ls epoch*.txt 2>> /dev/null | cut -c 6- | cut -d '.' -f 1 | sort -n | tail -1`
if [ "$startingepoch" = "" ]
then
        startingepoch=0
        prepare_epoch_file 0
fi
lastepoch=`ls epoch*.json | cut -c 6- | cut -d '.' -f 1 | sort -n | tail -1`
if [ "$lastepoch" = "" ]
then
        echo "Error: No epoch json files"
        exit
fi
echo "STAGE  3 Copying existing output/ directory data (if any)..."
if [ -d output ]
then
        cd output && tar cf - . | ( cd $TMPFOLDER/update_rewards$$/output && tar xf - )
        cd ..
else
        mkdir output
fi
echo "STAGE  4 Preparing epoch files..."
count=$((startingepoch+1))
while [ "$count" -le "$lastepoch" ]
do
        prepare_epoch_file $count
        count=$((count+1))
done
echo "STAGE  5 Generating address lists..."
sort -n -r +1 epoch$lastepoch.txt | awk '{print $1}' | tr "[A-Z]" "[a-z]" > epochaccounts_sorted_rewards.txt
echo "STAGE  6 Generating/updating trading reports..."
totaladdresses=`wc -l epochaccounts_sorted_rewards.txt | awk '{print $1}'`
cat <<EOF > $TMPFOLDER/update_rewards$$/output/whalelist.html
<!DOCTYPE html PUBLIC"ISO/IEC 15445:2000//DTD HTML//EN"><html><head><title>title</title></head><body>
<p style="font-family:'Courier New'">
$totaladdresses addresses loaded<br>
Updated at `date` (Epoch $lastepoch)<br>
See Leaderboard for:<br>
EOF
count=0
while [ "$count" -le "$lastepoch" ]
do
        echo "<a href=\"$baseurl/epoch$count.html\">Epoch$count</a><br>"
        count=$((count+1))
done >> $TMPFOLDER/update_rewards$$/output/whalelist.html
echo "STAGE  7 Generating parallel workloads..."
if [ "`uname`" = "Darwin" ]
then
        split -l $((totaladdresses/parallel)) epochaccounts_sorted_rewards.txt $TMPFOLDER/update_rewards$$/x
else
        split -n l/$parallel epochaccounts_sorted_rewards.txt $TMPFOLDER/update_rewards$$/x
fi
echo "STAGE  8 Executing parallel jobs..."
for xfile in `cd $TMPFOLDER/update_rewards$$; ls x??`
do
        count=1
        totalsubaddresses=`wc -l $TMPFOLDER/update_rewards$$/$xfile | awk '{print $1}'`
        for account in `cat $TMPFOLDER/update_rewards$$/$xfile`
        do
                update_rewards_for_account $account >> $TMPFOLDER/update_rewards$$/output/$account.txt
                echo "FILEUPDATE $account $count / $totalsubaddresses"
                count=$((count+1))
        done > $TMPFOLDER/update_rewards$$/$xfile.stdout 2> $TMPFOLDER/update_rewards$$/$xfile.stderr &
done
count=1
for account in `cat epochaccounts_sorted_rewards.txt`
do
        echo "<a href=\"$baseurl/$account.txt\">$account</a> #$count<br>" >> $TMPFOLDER/update_rewards$$/output/whalelist.html
        echo "WHALELIST $account $count / $totaladdresses"
        count=$((count+1))
done > $TMPFOLDER/update_rewards$$/whalelist.stdout 2> $TMPFOLDER/update_rewards$$/whalelist.stderr &
echo "STAGE  9 Waiting for completion of jobs..."
wait
cat $TMPFOLDER/update_rewards$$/*.stderr
echo "STAGE 10 Finalizing..."
echo "</body></html>" >> $TMPFOLDER/update_rewards$$/output/whalelist.html
WORKINGDIR=`pwd`
cd $TMPFOLDER/update_rewards$$/output && find . -newer $TMPFOLDER/update_rewards$$/xaa -type f -print0 | tar --null -T - -c | ( cd "$WORKINGDIR"/output && tar xf - )
cd "$WORKINGDIR"
echo "STAGE 11 Creating Epoch Leaderboards..."
create_epoch_html
echo "STAGE 12 Cleaning up..."
cleanup
echo "STAGE 13 Complete"
