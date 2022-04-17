#!/bin/sh

baseurl=http://lawrencedydx.freeddns.org:8080

cleanup ()
{
        if [ "`uname`" = "Darwin" ]
        then
                hdiutil detach $TMPFOLDER
        else
                sudo umount $TMPFOLDER
        fi
}

pid=$$
trap 'echo; echo "Ctrl-C detected. Cleaning up..."; kill -TERM `ps h --ppid $pid -o pid`; cleanup; exit' INT HUP

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
                lastrewards=`grep -i "^$address " epoch$startingepoch.txt | awk '{print $2}'`
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
                rewards=`grep -i "^$address     " epoch$fstartingepoch.txt | awk '{print $2}'`
                if [ "$rewards" = "" ]
                then
                        rewards=0
                else
                        rewards=`echo "$rewards / 10^18" | bc -l`
                fi
                f1=`/usr/bin/printf "%'f" \`echo "$rewards - $lastrewards" | bc -l\``
                f2=`/usr/bin/printf "%'f" $rewards`
                /usr/bin/printf "Epoch%s   %35s %35s\n" $fstartingepoch $f1 $f2
                lastrewards=$rewards
                fstartingepoch=$((fstartingepoch+1))
        done
}

echo "STAGE  1 Setting up ramdisk..."
if [ "`uname`" = "Darwin" ]
then
        diskutil erasevolume HFS+ "epochdisk" `hdiutil attach -nomount ram://1048576`
        TMPFOLDER=/Volumes/epochdisk
else
        sudo mkdir -p /mnt/epochdisk
        sudo mount -t tmpfs -o rw,size=512M tmpfs /mnt/epochdisk
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
cat $TMPFOLDER/update_rewards$$/epoch$lastepoch.col1 | tr "[A-Z]" "[a-z]" > epochaccounts_sorted_alpha.txt
sort -n -r +1 epoch$lastepoch.txt | awk '{print $1}' | tr "[A-Z]" "[a-z]" > epochaccounts_sorted_rewards.txt
echo "STAGE  6 Generating/updating trading reports..."
totaladdresses=`wc -l epochaccounts_sorted_alpha.txt | awk '{print $1}'`
cat <<EOF > $TMPFOLDER/update_rewards$$/output/fulllist.html
<!DOCTYPE html PUBLIC"ISO/IEC 15445:2000//DTD HTML//EN"><html><head><title>title</title></head><body>
<p style="font-family:'Courier New'">
$totaladdresses addresses loaded<br>
Updated at `date` (Epoch $lastepoch)<br>
EOF
cp $TMPFOLDER/update_rewards$$/output/fulllist.html $TMPFOLDER/update_rewards$$/output/whalelist.html
echo "STAGE  7 Generating parallel workloads..."
if [ "`uname`" = "Darwin" ]
then
        split -l $((totaladdresses / `sysctl -a | grep machdep.cpu.thread_count | awk '{print $2}'`)) epochaccounts_sorted_alpha.txt $TMPFOLDER/update_rewards$$/x
else
        split -n l/$((`nproc`*2)) epochaccounts_sorted_alpha.txt $TMPFOLDER/update_rewards$$/x
fi
echo "STAGE  8 Executing parallel jobs..."
for xfile in `cd $TMPFOLDER/update_rewards$$; ls x??`
do
        count=1
        totalsubaddresses=`wc -l $TMPFOLDER/update_rewards$$/$xfile | awk '{print $1}'`
        for account in `cat $TMPFOLDER/update_rewards$$/$xfile`
        do
                update_rewards_for_account $account >> $TMPFOLDER/update_rewards$$/output/$account
                echo "FILEUPDATE $account $count / $totalsubaddresses"
                count=$((count+1))
        done > $TMPFOLDER/update_rewards$$/$xfile.stdout 2> $TMPFOLDER/update_rewards$$/$xfile.stderr &
done
count=1
for account in `cat epochaccounts_sorted_rewards.txt`
do
        echo "<a href=\"$baseurl/$account\">$account</a> #$count<br>" >> $TMPFOLDER/update_rewards$$/output/fulllist.html
        echo "FULLLIST $account $count / $totaladdresses"
        count=$((count+1))
done > $TMPFOLDER/update_rewards$$/fulllist.stdout 2> $TMPFOLDER/update_rewards$$/fulllist.stderr &
count=1
for account in `cat epochaccounts_sorted_rewards.txt`
do
        echo "<a href=\"$baseurl/$account\">$account</a> #$count<br>" >> $TMPFOLDER/update_rewards$$/output/whalelist.html
        echo "WHALELIST $account $count / $totaladdresses"
        count=$((count+1))
done > $TMPFOLDER/update_rewards$$/whalelist.stdout 2> $TMPFOLDER/update_rewards$$/whalelist.stderr &
echo "STAGE  9 Waiting for completion of jobs..."
wait
cat $TMPFOLDER/update_rewards$$/*.stderr
echo "STAGE 10 Finalizing..."
echo "</body></html>" >> $TMPFOLDER/update_rewards$$/output/fulllist.html
echo "</body></html>" >> $TMPFOLDER/update_rewards$$/output/whalelist.html
WORKINGDIR=`pwd`
cd $TMPFOLDER/update_rewards$$/output && tar cf - . | ( cd "$WORKINGDIR"/output && tar xf - )
#cd $TMPFOLDER/update_rewards$$ && tar cf - . | gzip -c > /tmp/update_rewards$$.tar.gz
#cleanup
echo "STAGE 11 Complete"
