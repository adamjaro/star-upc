#!/usr/bin/bash

#top directory for outputs
top="/gpfs01/star/pwg/jaroslav/star-upc/trees/muDst_run0"

#macro to run the maker
macro="RunFilterMaker.C"
#macro="RunConvElMaker.C"

#submit xml
submit="SchedSubmitFilelist.xml"

#end of configuration


echo "Creating the list of files"
#catalog query for all the productions
tmplist="filelist_tmp.list"
cat /dev/null > $tmplist
get_file_list.pl -keys node,path,filename\
 -cond production=P16id,filetype=daq_reco_MuDst,filename~st_upc,storage=local,runnumber[]15078073-15167014,\
trgsetupname="AuAu_200_production_2014 || AuAu_200_production_low_2014 || AuAu_200_production_mid_2014 || AuAu_200_production_high_2014"\
 -delim '/' -limit 0 >> $tmplist

#convert to format for scheduler, section 3.6 The <input> element in submit script, full path ot filelist
filelist=`pwd`"/filelist.list"
cat /dev/null > $filelist
for line in `cat $tmplist`
do
  echo "file://"$(echo $line | sed "s%//%/%g") >> $filelist
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
































