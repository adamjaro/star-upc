#!/usr/bin/bash

basedir="/gpfs01/star/pwg/jaroslav/star-upc/trees/muDst/muDst_run1/*"

nall=$(ls $basedir/sched/*_*.csh | wc -l)

nout=$(ls $basedir/*.root | wc -l)

echo $basedir
echo "-------------------------"
echo "Jobs:             "$nall
echo "Unfinished jobs:  "$(expr $nall - $nout)
echo "Done jobs:        "$nout
echo "Jobs completed:   "$(echo -e "if $nall > 0: print '%.1f' %(100.*$nout/$nall) \nelse: print 0" | python 2>/dev/null)" %"
echo "-------------------------"

