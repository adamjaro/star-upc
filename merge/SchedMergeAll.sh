#!/bin/bash

top="/gpfs01/star/pwg/jaroslav/star-upc/trees/muDst/muDst_run4"
pattern="*/*.root"
#pattern="2010/*.root"
outfile="StUPC_muDst_run4_all.root"

root -l -b -q 'MergeFiles.C('\"$top'/'$pattern\"','\"$top'/'$outfile\"')'
stat=$?
echo "Merging exit status: "$stat
ls $top"/"$outfile -alh




