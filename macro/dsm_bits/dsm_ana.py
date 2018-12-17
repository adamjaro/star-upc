#!/usr/bin/python

import ROOT as rt
from ROOT import TFile, TTree

#_____________________________________________________________________________
if __name__ == "__main__":

    #data
    basedir = "../../../star-upc-data/ana/muDst/UPC_main_JpsiB_10_11_14/sel5"
    infile = "ana_main_r14_sel5z.root"

    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("jRecTree")

    #ptsel = "jRecPt<0.18"
    #vtxsel = "jVtxZ>-30 && jVtxZ<30"
    ptsel = "jRecPt<999"
    vtxsel = "jVtxZ>-100 && jVtxZ<100"
    runsel = "jRunNum>=15084051 && jRunNum<=15167007"

    nall = float( tree.Draw("", ptsel+" && "+vtxsel+" && "+runsel) )
    nsel = float( tree.Draw("", ptsel+" && "+vtxsel+" && "+runsel+" && "+"jInpBemcTopo == 1") )

    print nsel, nall, nsel/nall

