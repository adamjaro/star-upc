#!/usr/bin/bash

#top directory for outputs
top="/gpfs01/star/pwg/jaroslav/star-upc/trees/muDst_run0"

#list of runs
runlist="../txt/runlist_UPC-jpsi-B.txt"

#macro to run the maker
macro="RunFilterMaker.C"
#macro="RunConvElMaker.C"

#submit xml
submit="SchedSubmitFilelist.xml"

#end of configuration


echo "Creating list of files"
#formulate catalog query for the runlist
runcond="\""
irun=0
for runnum in `cat $runlist`
do
    if [ $irun -eq 0 ]
    then
        runcond=$runcond$runnum
    else
        runcond=$runcond" || "$runnum
    fi
    (( irun++ ))
done
runcond=$runcond"\""

#catalog query for list of runs in run condition runcond
tmplist="filelist_tmp.list"
cat /dev/null > $tmplist
#get_file_list.pl -keys node,path,filename\
# -cond production=P16id,filetype=daq_reco_MuDst,filename~st_upc,storage=local,runnumber="$runcond"\
# -limit 0 >> $tmplist

get_file_list.pl -keys node,path,filename\
 -cond production=P16id,filetype=daq_reco_MuDst,filename~st_upc,storage=local -limit 0 >> $tmplist

exit

#convert to format for scheduler, section 3.6 The <input> element in submit script, full path ot filelist
filelist=`pwd`"/filelist.list"
cat /dev/null > $filelist
for line in `cat $tmplist`
do
  echo "file://"$line | sed "s%::/%/%g" | sed "s%::%/%g" >> $filelist
done
rm $tmplist

echo "Submitting the jobs"
#create jobs output folder
basedir=$top"/out"
mkdir -p $basedir"/logs"
mkdir -p $basedir"/sched"

#create xml for the filelist
xml="submit_filelist.xml"
cat $submit | sed "s%__BASEDIR__%$basedir%g" | sed "s%__FILELIST__%$filelist%g" | sed "s%__MACRO__%$macro%g" > $xml

#submit for the filelist
star-submit $xml
























