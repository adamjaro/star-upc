#!/usr/bin/python

import ROOT as rt
from ROOT import TFile




#_____________________________________________________________________________
if __name__ == "__main__":

    #data
    #basedir = "../../ana/muDst/muDst_run2a/gg0"
    #infile = "ana_muDst_run2a_all_gg0.root"
    basedir = "../../../star-upc-data/ana/uTrees"
    infile = "xuTp_run16.root"

    #outfile = "out.root"
    #outfile = "gg_sel0_run10_11.root"
    outfile = "xuTp_run16_zdc_us.root"

    inp = TFile.Open(basedir+"/"+infile)
    #tree = inp.Get("jRecTree")
    tree = inp.Get("Tp")

    #tree.SetBranchStatus("*", 0)
    #tree.SetBranchStatus("jRecPt", 1)
    #tree.SetBranchStatus("jRecM", 1)

    out = TFile.Open(basedir+"/"+outfile, "recreate")

    #output tree with selection
    #tout = tree.CopyTree("jRecPt<0.1")
    tout = tree.CopyTree("trgUPCJPsizdc==1 && qpair==0")

    print "Output file:", outfile
    print "Selected output events:", tout.GetEntries()

    tout.Write()
    out.Close()













