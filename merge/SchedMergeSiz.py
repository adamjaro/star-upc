#!/usr/bin/python

from glob import glob
from subprocess import Popen, PIPE

#_____________________________________________________________________________
if __name__ == "__main__":

    #merge output files by chunks of a given size

    top = "/gpfs01/star/pwg/jaroslav/star-upc/trees/muDst/muDst_VPDZDCmon1"
    pattern = "/*/*.root"
    outfile = "StUPC_muDst_VPDZDCmon1_mer0.root"

    chunksiz = int(2e6)  # approx kB


    #list done jobs
    totsiz = 0
    ichunk = 0
    nchunk = 0
    tmpnam = "files.tmp"
    tmp = open(tmpnam, "w")
    cmd = "ls -s " + top + pattern
    out = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()[0].split("\n")
    print "Number of all outputs:", len(out)
    for iline in xrange(len(out)):
        fline = out[iline]
        size = 0
        if len(fline) > 0:
            siznam = fline.lstrip().split(" ")
            size = int(siznam[0])
            name = siznam[1]
        if size > 0:
            totsiz += size
            tmp.write(name+"\n")
            nchunk += 1
        if totsiz >= chunksiz or iline == len(out)-1:
            tmp.close()
            print
            print "Chunk:", ichunk
            print "Num files:", nchunk
            print "Size:", totsiz
            merge_cmd = "root -l -b -q MergeFiles.C(\"" + tmpnam + "\",\"" + outfile + "\")"
            merg = Popen(merge_cmd.split(), stdout=PIPE, stderr=PIPE).communicate()
            print merg[0]
            print merg[1]
            break
            tmp = open(tmpnam, "w")
            totsiz = 0
            nchunk = 0
            ichunk += 1

    print "All done."
























