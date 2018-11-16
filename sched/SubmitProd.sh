#!/usr/bin/bash

#top directory for all outputs
top="/gpfs01/star/pwg/jaroslav/star-upc/trees/muDst/muDst_VPDZDCmon1"

#production names for jobs outputs
#plist=("prod" "low" "mid" "high")
plist=("prod" "low" "mid")

#catalog query for each production
trgsetupname=(
  "AuAu_200_production_2014"
  "AuAu_200_production_low_2014"
  "AuAu_200_production_mid_2014"
  "AuAu_200_production_high_2014"
)

#submit xml
submit="SchedSubmit.xml"
#submit="SchedSubmitConv.xml"

#loop over productions
i=0
while [ $i -lt ${#plist[@]} ]
do
  echo $i

  #create jobs output folders
  basedir=$top"/"${plist[$i]}
  mkdir -p $basedir"/logs"
  mkdir -p $basedir"/sched"

  #create xml for each production
  xml="submit_"$i".xml"
  cat $submit | sed "s%__BASEDIR__%$basedir%g" | sed "s%__TRG__%${trgsetupname[$i]}%g" > $xml

  #submit for a given production
  star-submit $xml

  sleep 2
  (( i++ ))
done
#loop over productions




















