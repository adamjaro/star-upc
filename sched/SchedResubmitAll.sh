#!/usr/bin/bash

#resubmit aborted jobs

#top directory for all outputs
basedir="/gpfs01/star/pwg/jaroslav/star-upc/trees/dev/muDst_dev1/out"

#path to log file
logpath="/logs/*.out"

#loop over log files
nabort=0
ilog=0
for logfile in `ls $basedir$logpath`
do
    if [ $ilog == 0 ]
    then
        session=$(echo $logfile | sed "s%$basedir/logs/%%g" | awk -F "_" 'NR==1 {print $1}')
        echo "  Session: "$session
    fi
    cat $logfile | grep "Running copy command:" > /dev/null 2>&1
    stat=$?
    if [ $stat != 0 ]
    then
        #'copy command for root file' was not found by grep
        jobnum=$(echo $logfile | sed "s%$basedir/logs/%%g" | awk -F "[_.]" 'NR==1 {print $2}')
        echo "  job: "$jobnum
        #resubmit the job
        star-submit -r $jobnum $session.session.xml
        (( nabort++ ))
    fi
    (( ilog++ ))
done
#loop over log files

echo "Aborted jobs: "$nabort



























