#!/bin/bash

SRC="src"
INC="include"
DEST="StRoot/StUPCFilterMaker"

srclist=( StUPCBemcCluster StUPCEvent StUPCFilterMaker StUPCConvElMaker StUPCFilterBemcUtil StUPCFilterTrgUtil
StUPCTrack StUPCVertex )

mkdir -p $DEST

i=0
for file in ${srclist[@]}
do
  cp -f $SRC"/"${srclist[$i]}".cxx" $DEST/
  cp -f $INC"/"${srclist[$i]}".h" $DEST/
  ((i++))
done

cons




























