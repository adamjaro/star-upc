#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def plot_vtx_z():

    #primary vertex position along z from data and MC
    vbin = 4.
    vmax = 120.

    mmin = 1.5
    mmax = 5.

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    can = ut.box_canvas()

    hVtx = ut.prepare_TH1D("hVtx", vbin, -vmax, vmax)
    hVtxMC = ut.prepare_TH1D("hVtxMC", vbin, -vmax, vmax)

    tree.Draw("jVtxZ >> hVtx", strsel)

    hVtx.SetYTitle("Counts / {0:.0f} cm".format(vbin));
    hVtx.SetXTitle("#it{z} of primary vertex (cm)");

    hVtx.SetTitleOffset(1.5, "Y")
    hVtx.SetTitleOffset(1.3, "X")

    gPad.SetTopMargin(0.02)
    gPad.SetRightMargin(0.02)
    gPad.SetBottomMargin(0.1)
    gPad.SetLeftMargin(0.11)

    leg = ut.prepare_leg(0.16, 0.82, 0.23, 0.05, 0.025)
    leg.SetMargin(0.02)
    leg.SetBorderSize(1)
    ut.add_leg_mass(leg, mmin, mmax)

    cut_lo = ut.cut_line(-30, 0.8, hVtx)
    cut_hi = ut.cut_line(40, 0.8, hVtx)

    hVtx.Draw()
    leg.Draw("same")
    cut_lo.Draw("same")
    cut_hi.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_vtx_z

#_____________________________________________________________________________
if __name__ == "__main__":

    basedir = "../../ana/muDst/muDst_run1/sel3"

    infile = "ana_muDst_run1_all_sel3_nzvtx.root"

    interactive = False

    if interactive == False: gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    iplot = 0
    funclist = []
    funclist.append(plot_vtx_z) # 0

    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("jRecTree")

    #call the plot function
    funclist[iplot]()

    #to prevent 'pure virtual method called'
    gPad.Close()

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")



