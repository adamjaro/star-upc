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
    funclist = []
    funclist.append( plot_2d ) # 0
    funclist.append( plot_east ) # 1
    funclist.append( plot_west ) # 2

    inp = TFile.Open(basedir+"/"+infile)
    global tree
    tree = inp.Get("jRecTree")

    funclist[iplot]()

#main

#_____________________________________________________________________________
def plot_2d():

    zmin = 0
    zbin = 10
    zmax = 400

    ptmax = 0.18
    #mmin = 1.5
    #mmax = 5.
    mmin = 2.8
    mmax = 3.2

    znam = ["jZDCUnAttEast", "jZDCUnAttWest"]
    xtit = ["ZDC East ADC", "ZDC West ADC"]

    can = ut.box_canvas()

    strsel = ""
    #strsel += "jRecPt<{0:.3f}".format(ptmax)
    #strsel += " && jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    hZdc = ut.prepare_TH2D("hZdc", zbin, zmin, zmax, zbin, zmin, zmax)

    tree.Draw(znam[1]+":"+znam[0]+" >> hZdc", strsel) # y:x

    ut.put_yx_tit(hZdc, xtit[1], xtit[0], 1.7, 1.2)
    ut.set_margin_lbtr(gPad, 0.12, 0.09, 0.02, 0.11)

    hZdc.SetMinimum(0.98)
    hZdc.SetContour(300)

    hZdc.Draw()

    gPad.SetGrid()
    gPad.SetLogz()

    ut.invert_col(gPad)
    can.SaveAs("01fig.pdf")

#plot_2d

#_____________________________________________________________________________
def plot_east():

    zmin = 0
    zbin = 10
    zmax = 400

    can = ut.box_canvas()

    hZdc = ut.prepare_TH1D("hZdc", zbin, zmin, zmax)

    tree.Draw("jZDCUnAttEast >> hZdc")

    ut.set_margin_lbtr(gPad, 0.1, 0.08, 0.01, 0.04)
    ut.put_yx_tit(hZdc, "ZDC East", "ADC")

    #middle point from 1n and 2n positions, dl-202011.03
    mid_1n2n = (164.996+75.671)/2
    print("mid_1n2n:", mid_1n2n)

    lin = ut.cut_line(mid_1n2n, 0.7, hZdc)

    gF = make_FastZDC("jZDCUnAttEast", hZdc)

    hZdc.Draw()
    gF.Draw("same")
    hZdc.Draw("e1same")
    lin.Draw("same")

    gPad.SetGrid()
    #gPad.SetLogy()

    #ut.invert_col(gPad)
    can.SaveAs("01fig.pdf")

#plot_east

#_____________________________________________________________________________
def plot_west():

    zmin = 0
    zbin = 10
    zmax = 400

    can = ut.box_canvas()

    hZdc = ut.prepare_TH1D("hZdc", zbin, zmin, zmax)

    tree.Draw("jZDCUnAttWest >> hZdc")

    ut.set_margin_lbtr(gPad, 0.1, 0.08, 0.01, 0.04)
    ut.put_yx_tit(hZdc, "ZDC West", "ADC")

    #middle point from 1n and 2n positions, dl-202011.03
    mid_1n2n = (187.879+90.058)/2
    print("mid_1n2n:", mid_1n2n)

    lin = ut.cut_line(mid_1n2n, 0.7, hZdc)

    gF = make_FastZDC("jZDCUnAttWest", hZdc)

    hZdc.Draw()
    gF.Draw("lsame")
    hZdc.Draw("e1same")
    lin.Draw("same")

    gPad.SetGrid()
    #gPad.SetLogy()

    ut.invert_col(gPad)
    can.SaveAs("01fig.pdf")

#plot_west

#_____________________________________________________________________________
def make_FastZDC(nam, hZ):

    #infile = "/home/jaroslav/analyza/star-upc-data/ana/FastZDC/STnOOn_eta1p2_1Mevt/FastZDC_HCal_allADC.root"
    infile = "/home/jaroslav/analyza/star-upc-data/ana/FastZDC/STnOOn_eta1p2_1Mevt/FastZDC_Grupen_allADC.root"

    inp = TFile.Open(infile)
    tree = inp.Get("jRecTree")

    hF = ut.prepare_TH1D("hF", 5, 0, 400)
    tree.Draw(nam+" >> hF")

    ut.norm_to_data(hF, hZ)

    gF = ut.h1_to_graph(hF)
    gF.SetLineColor(rt.kBlue)
    gF.SetLineWidth(3)

    return gF

#make_FastZDC

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()





























