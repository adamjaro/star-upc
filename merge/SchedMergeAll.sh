#!/bin/bash

trees="/gpfs01/star/pwg/jaroslav/StUPCLib/ver2/trees/test/muDst_test1"
pattern="*/*.root"
outfile="StUPC_muDst_test1_all.root"

root -l -b -q 'MergeFiles.C('\"$trees'/'$pattern\"','\"$trees'/'$outfile\"')'
stat=$?
echo "Merging exit status: "$stat
ls $trees"/"$outfile -alh

