#!/bin/bash

trees="/gpfs01/star/pwg/jaroslav/star-upc/trees/test/muDst_test0"
pattern="*/*.root"
outfile="StUPC_muDst_test0_all.root"

root -l -b -q 'MergeFiles.C('\"$trees'/'$pattern\"','\"$trees'/'$outfile\"')'
stat=$?
echo "Merging exit status: "$stat
ls $trees"/"$outfile -alh

