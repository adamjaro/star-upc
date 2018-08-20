#!/bin/bash

top="/gpfs01/star/pwg/jaroslav/star-upc/trees/muDst/muDst_run1a"
pattern="*/*.root"
outfile="StUPC_muDst_run1a_all.root"

root -l -b -q 'MergeFiles.C('\"$top'/'$pattern\"','\"$top'/'$outfile\"')'
stat=$?
echo "Merging exit status: "$stat
ls $top"/"$outfile -alh




