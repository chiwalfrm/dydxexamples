#!/bin/sh
if [ $# -eq 0 ]
then
        echo "Error: Must specify filesystem to monitor"
fi
filesystem=$1
while true
do
        if [ "`df $1 | tail -1 | awk '{print $5}' | tr -d '%'`" -gt 90 ]
        then
##### THIS CODE BLOCKS RUNS WHEN FILESYSTEM IS >90% FULL
                ls -d $filesystem/list* | cut -d / -f 4 | sort -u | while read l1
                do
                        touch $filesystem/$l1/EXITFLAG
                done
##### END OF CODE BLOCK
                break
        fi
        sleep 60
done
