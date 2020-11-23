#!/usr/bin/python

import ROOT as rt
from ROOT import TF1, gPad, gROOT, gStyle, TFile

import sys
sys.path.append('../')
import plot_utils as ut
from parameter_descriptor import parameter_descriptor as pdesc

#_____________________________________________________________________________
def main():

    #data
    basedir = "../../../star-upc-data/ana/muDst/muDst_run1/sel5"
    infile = "ana_muDst_run1_all_sel5z.root"

    #MC
    #basedir_coh = "../../../star-upc-data/ana/starsim/slight14e/sel5"
    #infile_coh = "ana_slight14e1x3_s6_sel5z.root"
    basedir_coh = "../FastZDC"
    infile_coh = "FastZDC.root"

    ymin = -1
    ymax = 1

    #mmin = 1.5
    #mmax = 5
    mmin = 2.8
    mmax = 3.2

    ptmax = 0.18

    iplot = 3
    funclist = []
    funclist.append( tracks_eta ) # 0
    funclist.append( zdc_east ) # 1
    funclist.append( zdc_west ) # 2
    funclist.append( pT ) # 3

    inp = TFile.Open(basedir+"/"+infile)
    global tree
    tree = inp.Get("jRecTree")

    inp_coh = TFile.Open(basedir_coh+"/"+infile_coh)
    global tree_coh
    tree_coh = inp_coh.Get("jRecTree")

    global gsel
    gsel = "jRecM>"+str(mmin)+" && jRecM<"+str(mmax)+" && jRecY>"+str(ymin)+" && jRecY<"+str(ymax)+" && jRecPt<"+str(ptmax)

    global gsel_ym
    gsel_ym = "jRecM>"+str(mmin)+" && jRecM<"+str(mmax)+" && jRecY>"+str(ymin)+" && jRecY<"+str(ymax)

    funclist[iplot]()

#main

#_____________________________________________________________________________
def tracks_eta():

    #bins in eta
    ebin = 0.2
    emin = -1.2
    emax = 1.2

    hEta = ut.prepare_TH1D("hEta", ebin, emin, emax)
    hEtaMC = ut.prepare_TH1D("hEtaMC", ebin, emin, emax)

    can = ut.box_canvas()

    tree.Draw("jT0eta >> hEta", gsel)
    tree.Draw("jT1eta >>+ hEta", gsel)

    tree_coh.Draw("jT0eta >> hEtaMC", gsel)
    tree_coh.Draw("jT1eta >>+ hEtaMC", gsel)

    ut.norm_to_data(hEtaMC, hEta)

    #gPad.SetLogy()

    hEta.Draw()
    hEtaMC.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#tracks_eta

#_____________________________________________________________________________
def zdc_east():

    #bins in eta
    xbin = 18
    xmin = 0
    xmax = 1300

    plot = "jZDCUnAttEast"

    hDat = ut.prepare_TH1D("hDat", xbin, xmin, xmax)
    hMC = ut.prepare_TH1D("hMC", xbin, xmin, xmax)

    can = ut.box_canvas()

    tree.Draw(plot+" >> hDat", gsel)
    tree_coh.Draw(plot+" >> hMC", gsel)

    ut.norm_to_data(hMC, hDat)

    #gPad.SetLogy()

    hMC.Draw()
    hDat.Draw("e1same")
    hMC.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#zdc_east

#_____________________________________________________________________________
def zdc_west():

    #bins in eta
    xbin = 18
    xmin = 0
    xmax = 1300

    plot = "jZDCUnAttWest"

    hDat = ut.prepare_TH1D("hDat", xbin, xmin, xmax)
    hMC = ut.prepare_TH1D("hMC", xbin, xmin, xmax)

    can = ut.box_canvas()

    tree.Draw(plot+" >> hDat", gsel)
    tree_coh.Draw(plot+" >> hMC", gsel)

    ut.norm_to_data(hMC, hDat)

    #gPad.SetLogy()

    hMC.Draw()
    hDat.Draw("e1same")
    hMC.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#zdc_west

#_____________________________________________________________________________
def pT():

    #pT in data and MC

    pbin = 0.015
    pmin = 0.
    pmax = 1.

    hPt = ut.prepare_TH1D("hPt", pbin, pmin, pmax)
    hPtMC = ut.prepare_TH1D("hPtMC", pbin, pmin, pmax)

    can = ut.box_canvas()

    tree.Draw("jRecPt >> hPt", gsel_ym)

    tree_coh.Draw("jRecPt >> hPtMC", gsel_ym)
    #tree_coh.Draw("jGenPt >> hPtMC", gsel_ym)

    ut.norm_to_data(hPtMC, hPt)

    #gPad.SetLogy()

    hPtMC.Draw()
    hPt.Draw("e1same")
    hPtMC.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#pT

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()























