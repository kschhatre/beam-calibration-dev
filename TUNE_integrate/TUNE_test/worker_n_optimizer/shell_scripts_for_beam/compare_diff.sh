#!/bin/bash

THRES=50

runtime="30 seconds"
endtime=$(date -ud "$runtime" +%s)

while [[ $(date -u +%s) -le $endtime ]]
do 
    DIFF=$(python compute_diff.py 2>&1)
    echo "$DIFF"
    sleep 1s
done

INTDIFF=${DIFF%.*}

if [ "$INTDIFF" -gt "$THRES" ] ; then
    
    ./kill.sh & export BEAM_TEMP_PID=$!

fi



    

