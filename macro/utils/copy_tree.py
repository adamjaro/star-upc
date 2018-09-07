#!/usr/bin/python

import ROOT as rt
from ROOT import TFile




#_____________________________________________________________________________
if __name__ == "__main__":

    #data
    basedir = "../../ana/muDst/muDst_run2a/gg0"
    infile = "ana_muDst_run2a_all_gg0.root"

    outfile = "out.root"
    #outfile = "gg_sel0_run10_11.root"

    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("jRecTree")

    tree.SetBranchStatus("*", 0)
    tree.SetBranchStatus("jRecPt", 1)
    tree.SetBranchStatus("jRecM", 1)

    out = TFile.Open(basedir+"/"+outfile, "recreate")

    #output tree with selection
    tout = tree.CopyTree("jRecPt<0.1")

    print "Output file:", outfile
    print "Selected output events:", tout.GetEntries()

    tout.Write()
    out.Close()

