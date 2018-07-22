#!/usr/bin/bash

#resubmit aborted jobs

#top directory for all outputs
top="/gpfs01/star/pwg/jaroslav/StUPCLib/ver2/trees/muDst_run3"

#production names for jobs outputs
plist=("prod" "low" "mid" "high")

#path to log file in each production
#logpath="/sched/*.condor.log"
logpath="/logs/*.out"

#loop over productions
i=0
nabort=0
while [ $i -lt ${#plist[@]} ]
#while [ $i -lt 1 ]
do
  basedir=$top"/"${plist[$i]}
  echo ${plist[$i]}":"
  #log file loop
  ilog=0
  for logfile in `ls $basedir$logpath`
  do
    if [ $ilog == 0 ]
    then
      #session=$(echo $logfile | sed "s%$basedir/sched/sched%%g" | awk -F "_" 'NR==1 {print $1}')
      session=$(echo $logfile | sed "s%$basedir/logs/%%g" | awk -F "_" 'NR==1 {print $1}')
      echo "  Session: "$session
    fi
    #echo $logfile
    #cat $logfile | grep "Normal termination" > /dev/null 2>&1
    cat $logfile | grep "Running copy command:" > /dev/null 2>&1
    stat=$?
    if [ $stat != 0 ]
    then
      #'copy command for root file' was found by grep
      #jobnum=$(echo $logfile | sed "s%$basedir/sched/sched%%g" | awk -F "[_.]" 'NR==1 {print $2}')
      jobnum=$(echo $logfile | sed "s%$basedir/logs/%%g" | awk -F "[_.]" 'NR==1 {print $2}')
      echo "  job: "$jobnum
      #resubmit the job
      star-submit -r $jobnum $session.session.xml
      (( nabort++ ))
    fi
    (( ilog++ ))
  done
  #log file loop

  (( i++ ))
done
#loop over productions

echo "Aborted jobs: "$nabort



























