#!/usr/bin/python3

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    basedir = "../../../star-upc-data/ana/muDst/muDst_run1/sel5"
    infile = "ana_muDst_run1_all_sel5z.root"

    iplot = 1
    func = {}
    func[0] = plot_pt
    func[1] = plot_logPt2

    inp = TFile.Open(basedir+"/"+infile)
    global tree
    tree = inp.Get("jRecTree")

    func[iplot]()

#main

#_____________________________________________________________________________
def plot_pt():

    #ptbin = 0.03
    #ptmax = 1.1
    #ptbin = 1e-2
    ptbin = 0.5e-2
    ptmax = 0.11

    mmin = 2.8
    mmax = 3.2

    east_1n = 120.3335
    west_1n = 138.9685

    strsel = "(jRecM>{0:.3f} && jRecM<{1:.3f})".format(mmin, mmax)
    #strsel += " && (jZDCUnAttEast<{0:.3f} && jZDCUnAttWest<{1:.3f})".format(east_1n, west_1n)
    strsel += " && (jZDCUnAttEast>{0:.3f} && jZDCUnAttWest>{1:.3f})".format(east_1n, west_1n)

    can = ut.box_canvas()

    hPt = ut.prepare_TH1D("hPt", ptbin, 0, ptmax)

    #tree.Draw("jRecPt >> hPt", strsel)
    tree.Draw("jRecPt*jRecPt >> hPt", strsel)

    print("Entries: ", hPt.GetEntries())

    hPt.Draw()

    gPad.SetGrid()
    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#plot_pt

#_____________________________________________________________________________
def plot_logPt2():

    #ptbin = 0.12
    ptbin = 0.1
    ptmin = -5
    ptmax = 1

    mmin = 2.8
    mmax = 3.2

    east_1n = 120.3335
    west_1n = 138.9685

    strsel = "(jRecM>{0:.3f} && jRecM<{1:.3f})".format(mmin, mmax)
    #strsel += " && (jZDCUnAttEast<{0:.3f} && jZDCUnAttWest<{1:.3f})".format(east_1n, west_1n)
    strsel += " && (jZDCUnAttEast>{0:.3f} && jZDCUnAttWest>{1:.3f})".format(east_1n, west_1n)

    can = ut.box_canvas()

    hPt = ut.prepare_TH1D("hPt", ptbin, ptmin, ptmax)

    tree.Draw("TMath::Log10(jRecPt*jRecPt) >> hPt", strsel)

    print("Entries: ", hPt.GetEntries())

    hPt.Draw()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#plot_logPt2

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()


















