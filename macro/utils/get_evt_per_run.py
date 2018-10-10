#!/usr/bin/python

import ROOT as rt
from ROOT import gROOT, TFile, TTree, TH1I

#_____________________________________________________________________________
if __name__ == "__main__":

    #get number of selected events per run number

    basedir = "../../../star-upc-data/ana/muDst"

    infile = "muDst_run1/sel5/ana_muDst_run1_all_sel5_v2.root"

    mmin = 1.5
    mmax = 5.

    ptmax = 0.17

    outnam = "evt_per_run_muDst_run1_sel5.txt"

    rmin = 15084000
    rmax = 15167100

    #get the input
    gROOT.SetBatch()
    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("jRecTree")

    hrun = TH1I("hrun", "hrun", rmax-rmin, rmin, rmax)
    tree.Draw("jRunNum >> hrun", "jRecM>{0:.3f} && jRecM<{1:.3f} && jRecPt<{2:.3f}".format(mmin, mmax, ptmax))

    print hrun.IsBinUnderflow(0)
    print hrun.IsBinOverflow(hrun.GetNbinsX()+1)
    print hrun.GetEntries(), hrun.GetBinContent(0), hrun.GetBinContent(hrun.GetNbinsX()+1)

    #content list
    rlist = []
    for i in xrange(hrun.GetNbinsX()):
        if hrun.GetBinContent(i) < 0.1: continue
        rlist.append( (int(hrun.GetBinLowEdge(i)), int(hrun.GetBinContent(i))) )

    #sort the list according to number of events per run
    slist = sorted(rlist, key=lambda kv: -kv[1])

    #output file
    out = open(outnam, "w")
    for i in xrange(len(slist)):
        out.write(str(slist[i][0])+" "+str(slist[i][1])+"\n")























