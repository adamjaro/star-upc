#!/usr/bin/bash

#submit for a given list of catalog queries

#top directory for all outputs
top="/gpfs01/star/pwg/jaroslav/star-upc/trees/muDst/muDst_run2a"

#names for individual query outputs
qnames=("2010" "2011")

#catalog queries
qlist=(
  "production=P10ik,trgsetupname=AuAu200_production,filetype=daq_reco_MuDst,filename~st_upc,storage=local"
  "production=P11id,trgsetupname=AuAu200_production_2011,filetype=daq_reco_MuDst,filename~st_upc,storage=local"
)

#submit xml
submit="SchedSubmitQuery.xml"

#loop over catalog queries
i=0
while [ $i -lt ${#qnames[@]} ]
do
  echo $i

  #create jobs output folders
  basedir=$top"/"${qnames[$i]}
  mkdir -p $basedir"/logs"
  mkdir -p $basedir"/sched"

  #create xml for each query in the list
  xml="submit_"$i".xml"
  cat $submit | sed "s%__BASEDIR__%$basedir%g" | sed "s%__QUERY__%${qlist[$i]}%g" > $xml

  #submit for a given catalog query
  star-submit $xml

  sleep 1
  (( i++ ))
done
#loop over productions













