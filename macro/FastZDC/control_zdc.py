#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    #infile = "FastZDC.root"
    infile = "/home/jaroslav/analyza/star-upc-data/ana/FastZDC/STnOOn_eta1p2_1Mevt/FastZDC_HCal_allADC.root"
    #infile = "/home/jaroslav/analyza/star-upc-data/ana/FastZDC/STnOOn_eta1p2_1Mevt/FastZDC_Grupen_allADC.root"

    iplot = 4
    funclist = []
    funclist.append( neut_en_pn ) # 0
    funclist.append( plot_zdc_2d ) # 1
    funclist.append( acc_XnXn ) # 2
    funclist.append( neut_en ) # 3
    funclist.append( neut_mult ) # 4
    funclist.append( en_1n ) # 5
    funclist.append( en_2n ) # 6

    inp = TFile.Open(infile)
    global tree
    tree = inp.Get("jRecTree")

    funclist[iplot]()

#main

#_____________________________________________________________________________
def neut_en_pn():

    #neutron energy and positive and negative rapidity

    #plot range
    ebin = 18
    emin = 10
    emax = 700

    sel = ""
    #sel = "npos==1 && nneg == 1"
    #sel = "npos==2 && nneg == 2"
    #sel = "npos>1 || nneg>1"

    hE = ut.prepare_TH2D("hE", ebin, emin, emax, ebin, emin, emax)

    can = ut.box_canvas()

    tree.Draw("epos:eneg >> hE", sel) #y:x

    ut.put_yx_tit(hE, "#it{E}_{#it{n}} (GeV),  #it{#eta} > 0", "#it{E}_{#it{n}} (GeV), #it{#eta} < 0", 1.7, 1.2)
    ut.set_margin_lbtr(gPad, 0.12, 0.09, 0.02, 0.11)

    hE.SetMinimum(0.98)
    hE.SetContour(300)

    hE.Draw()

    gPad.SetGrid()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#neut_en_pn

#_____________________________________________________________________________
def plot_zdc_2d():

    #ZDC ADC counts east vs. west 2D

    zbin = 18
    zmin = 10
    zmax = 700

    znam = ["jZDCUnAttEast", "jZDCUnAttWest"]
    xtit = ["FastZDC East ADC", "FastZDC West ADC"]

    can = ut.box_canvas()

    hZdc = ut.prepare_TH2D("hZdc", zbin, zmin, zmax, zbin, zmin, zmax)

    tree.Draw(znam[1]+":"+znam[0]+" >> hZdc")

    ut.put_yx_tit(hZdc, xtit[1], xtit[0], 1.7, 1.2)
    ut.set_margin_lbtr(gPad, 0.12, 0.09, 0.02, 0.11)

    hZdc.SetMinimum(0.98)
    hZdc.SetContour(300)

    hZdc.Draw()

    gPad.SetGrid()
    gPad.SetLogz()

    ut.invert_col(gPad)
    can.SaveAs("01fig.pdf")

#plot_zdc_2d

#_____________________________________________________________________________
def acc_XnXn():

    #accceptance to XnXn

    #amax = 1250
    amax = 1200

    znam = ["jZDCUnAttEast", "jZDCUnAttWest"]
    #znam = ["epos", "eneg"]

    sel = znam[0]+"<"+str(amax) +" && "+znam[1]+"<"+str(amax)

    print sel

    nall = float(tree.GetEntries())
    nsel = tree.Draw("", sel)

    print nall, nsel, nsel/nall

#acc_XnXn

#_____________________________________________________________________________
def neut_en():

    #neutron generated energy, both positive and negative rapidity

    ebin = 5
    emin = 0
    emax = 2500

    can = ut.box_canvas()

    hE = ut.prepare_TH1D("hE", ebin, emin, emax)

    tree.Draw("epos >> hE")
    tree.Draw("eneg >>+ hE")

    gPad.SetGrid()
    gPad.SetLogy()

    hE.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#neut_en

#_____________________________________________________________________________
def neut_mult():

    #neutron multiplicity, both positive and negative rapidity

    nbin = 1
    nmin = 0
    nmax = 55

    can = ut.box_canvas()

    hN = ut.prepare_TH1I("hN", nbin, nmin, nmax)
    hS = ut.prepare_TH1I("hS", nbin, nmin, nmax)

    hN.SetLineWidth(3)
    hS.SetLineWidth(3)
    hS.SetLineColor(rt.kRed)

    tree.Draw("npos >> hN")
    tree.Draw("nneg >>+ hN")

    tree.Draw("npos >> hS", "jZDCUnAttEast<1200 && jZDCUnAttWest<1200")
    tree.Draw("nneg >>+ hS", "jZDCUnAttEast<1200 && jZDCUnAttWest<1200")

    gPad.SetGrid()
    gPad.SetLogy()

    hN.SetTitle("")

    ut.put_yx_tit(hN, "Counts", "Neutrons in event", 1.4, 1.2)

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.03, 0.02)

    hN.Draw()
    hS.Draw("same")

    leg = ut.prepare_leg(0.5, 0.78, 0.2, 0.1, 0.035)
    leg.AddEntry(hN, "All central XnXn events", "l")
    leg.AddEntry(hS, "ADC < 1200", "l")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#neut_mult

#_____________________________________________________________________________
def en_1n():

    #energy for one neutron in both + and - eta for mean of 1n energy

    ebin = 2
    emin = 0
    emax = 200

    can = ut.box_canvas()

    hE = ut.prepare_TH1D("hE", ebin, emin, emax)

    tree.Draw("epos >> hE", "npos == 1")
    tree.Draw("eneg >>+ hE", "nneg == 1")

    print "UO:", hE.GetBinContent(0), hE.GetBinContent(hE.GetNbinsX()+1)
    print "Mean:", hE.GetMean(), "+/-", hE.GetMeanError()

    gPad.SetGrid()
    gPad.SetLogy()

    hE.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#en_1n

#_____________________________________________________________________________
def en_2n():

    #energy for two neutrons in both + and - eta for mean of 2n energy

    ebin = 2
    emin = 0
    emax = 500

    can = ut.box_canvas()

    hE = ut.prepare_TH1D("hE", ebin, emin, emax)

    tree.Draw("epos >> hE", "npos == 2")
    tree.Draw("eneg >>+ hE", "nneg == 2")

    print "UO:", hE.GetBinContent(0), hE.GetBinContent(hE.GetNbinsX()+1)
    print "Mean:", hE.GetMean(), "+/-", hE.GetMeanError()

    gPad.SetGrid()
    gPad.SetLogy()

    hE.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#en_2n

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()





















