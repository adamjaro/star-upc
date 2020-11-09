#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    infile = "FastZDC.root"

    iplot = 4
    funclist = []
    funclist.append( neut_en_pn ) # 0
    funclist.append( plot_zdc_2d ) # 1
    funclist.append( acc_XnXn ) # 2
    funclist.append( neut_en ) # 3
    funclist.append( neut_mult ) # 4

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
    nmax = 40

    can = ut.box_canvas()

    hN = ut.prepare_TH1I("hN", nbin, nmin, nmax)

    tree.Draw("npos >> hN")
    tree.Draw("nneg >>+ hN")

    gPad.SetGrid()
    gPad.SetLogy()

    hN.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#neut_mult

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()





















