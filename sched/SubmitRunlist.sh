#!/usr/bin/bash

#top directory for outputs
top="/gpfs01/star/pwg/jaroslav/star-upc/trees/test/muDst_test1"

#list of runs
runlist="../txt/runlist_UPC-jpsi-B.txt"

#full path to filelist
#filelist="/star/u/jaroslav/star-upc/sched/filelist.list"

#macro to run the maker
macro="RunFilterMaker.C"
#macro="RunConvElMaker.C"

#submit xml
submit="SchedSubmitFilelist.xml"

#end of configuration


#formulate catalog query for the runlist
for runnum in `cat $runlist`
do
    echo $runnum
done













