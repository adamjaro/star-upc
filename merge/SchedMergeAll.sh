#!/bin/bash

top="/gpfs01/star/pwg/jaroslav/star-upc/trees/muDst_run0"
pattern="out/*.root"
outfile="StUPC_muDst_test0_all.root"

root -l -b -q 'MergeFiles.C('\"$top'/'$pattern\"','\"$top'/'$outfile\"')'
stat=$?
echo "Merging exit status: "$stat
ls $top"/"$outfile -alh




