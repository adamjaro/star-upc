#!/usr/bin/python

import math
from time import time

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TH1D
from ROOT import vector, double

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def get_bins(tree, bnam, bmatch, prec, delt):

    #load tracks momenta to lists for all and matched tracks

    tree.SetBranchStatus("*", 0)
    tree.SetBranchStatus(bnam[0], 1)
    tree.SetBranchStatus(bnam[1], 1)
    tree.SetBranchStatus(bmatch[0], 1)
    tree.SetBranchStatus(bmatch[1], 1)

    #momenta values for all and matched tracks
    valAll = rt.list(double)()
    valSel = rt.list(double)()

    for i in range(tree.GetEntriesFast()):
        tree.GetEntry(i)
        exec("p0 = tree."+bnam[0])
        exec("p1 = tree."+bnam[1])
        exec("match0 = tree."+bmatch[0])
        exec("match1 = tree."+bmatch[1])
        valAll.push_back(p0)
        valAll.push_back(p1)
        if match0 == True: valSel.push_back(p0)
        if match1 == True: valSel.push_back(p1)

    #bin edges
    bins = vector(rt.double)()

    t0 = time()

    gROOT.LoadMacro("get_bins.C")
    rt.get_bins(bins, valAll, valSel, prec, delt)

    t1 = time()
    print "Time to calculate the bins (sec):", t1-t0

    return bins

#_____________________________________________________________________________
if __name__ == "__main__":

    basedir = "../../../star-upc-data/ana/muDst"

    infile = "muDst_run1a/conv0/ana_muDst_run1a_all_conv0.root"

    precision = 0.06   # 0.06
    delta = 1.e-7

    logx = True

    #branches with momentum at BEMC and matching information
    bnam = ["jT0bemcP", "jT1bemcP"]
    bmatch = ["jT0matchBemc", "jT1matchBemc"]

    #selection for basic input range
    strsel = bnam[0]+"<5 && "+bnam[1]+"<5"

    #line color for fit
    #clin = rt.kMagenta
    clin = rt.kBlue

    #-- end of config --


    gROOT.SetBatch()

    #output temporary file
    outnam = "tmp.root"
    #input and output
    inp = TFile.Open(basedir+"/"+infile)
    out = TFile.Open(outnam, "recreate")

    #get input tree, apply the selection
    tree = inp.Get("jRecTree").CopyTree(strsel)

    # bin edges
    bins = get_bins(tree, bnam, bmatch, precision, delta)

    #momenta and efficiency histograms
    nbins = len(bins)-1
    hAll = TH1D("hAll", "hAll", nbins, bins.data())
    hSel = TH1D("hSel", "hSel", nbins, bins.data())
    hAll.Sumw2()
    hSel.Sumw2()
    tree.Draw(bnam[0]+" >>  hAll")
    tree.Draw(bnam[1]+" >>+ hAll")
    tree.Draw(bnam[0]+" >>  hSel", bmatch[0]+"==1")
    tree.Draw(bnam[1]+" >>+ hSel", bmatch[1]+"==1")

    #calculate the efficiency
    hEff = TH1D("hEff", "hEff", nbins, bins.data())
    hEff.Divide(hSel, hAll, 1, 1, "B")

    #plot the efficiency
    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)

    can = ut.box_canvas()

    gPad.SetTopMargin(0.01)
    gPad.SetRightMargin(0.01)
    gPad.SetBottomMargin(0.12)
    gPad.SetLeftMargin(0.1)

    ut.set_H1D(hEff)

    hEff.SetTitleOffset(1.4, "Y")
    hEff.SetTitleOffset(1.5, "X")

    hEff.SetXTitle("Track momentum #it{p}_{tot} at BEMC (GeV)")
    hEff.SetYTitle("BEMC efficiency")
    hEff.SetTitle("")

    hEff.GetXaxis().SetMoreLogLabels()

    if logx == True: gPad.SetLogx()

    hEff.Draw()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

    #to prevent 'pure virtual method called'
    gPad.Close()

    #remove the temporary
    out.Close()
    gSystem.Exec("rm -f "+outnam)

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")























