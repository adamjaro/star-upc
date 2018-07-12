#!/usr/bin/bash

#top directory for outputs
top="/gpfs01/star/pwg/jaroslav/StUPCLib/ver2/trees/test/muDst_test1"

runlist=(15129018 15098003 15094069 15140030)

#full path to filelist
filelist="/star/u/jaroslav/StUPCLib/ver2/sched/filelist.list"

#macro to run the maker
#macro="RunFilterMaker.C"
macro="RunConvElMaker.C"

#submit xml
submit="SchedSubmitFilelist.xml"


#get files for runlist from catalog
runcond="\"${runlist[0]}"
irun=1
while [ $irun -lt ${#runlist[@]} ]
do
  runcond=$runcond" || ${runlist[$irun]}"
  (( irun++ ))
done
runcond=$runcond"\""

#catalog query for list of runs in run condition runcond
tmplist="filelist_tmp.list"
cat /dev/null > $tmplist
get_file_list.pl -keys node,path,filename\
 -cond production=P16id,filetype=daq_reco_MuDst,filename~st_upc,storage=local,runnumber="$runcond" >> $tmplist

#convert to format for scheduler, section 3.6 The <input> element in submit script
cat /dev/null > $filelist
for line in `cat $tmplist`
do
  echo "file://"$line | sed "s%::/%/%g" | sed "s%::%/%g" >> $filelist
done
rm $tmplist

#create jobs output folder
basedir=$top"/out"
mkdir -p $basedir"/logs"
mkdir -p $basedir"/sched"

#create xml for the filelist
xml="submit_filelist.xml"
cat $submit | sed "s%__BASEDIR__%$basedir%g" | sed "s%__FILELIST__%$filelist%g" | sed "s%__MACRO__%$macro%g" > $xml

#submit for the filelist
star-submit $xml




















