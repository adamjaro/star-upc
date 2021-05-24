#!/usr/bin/python

#cross section comparison

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append('../')
import plot_utils as ut

from models import *

#_____________________________________________________________________________
def main():

    #range for |t|
    tmin = 0.
    tmax = 0.11  #   0.109  0.01 for interference range
    #tmax = 0.015

    #dy = 2. # rapidity interval
    dy = 1.

    gSlight = load_starlight(dy)

    can = ut.box_canvas()
    #frame = gPad.DrawFrame(tmin, 1e-5, tmax, 11)
    frame = gPad.DrawFrame(0, -0.2, tmax, 0.3)

    ut.set_margin_lbtr(gPad, 0.1, 0.09, 0.055, 0.01)

    ytit = "d#it{#sigma}/d#it{t}d#it{y} (mb/(GeV/c)^{2})"
    xtit = "|#kern[0.3]{#it{t}}| ((GeV/c)^{2})"

    ut.put_yx_tit(frame, ytit, xtit, 1.4, 1.2)

    frame.Draw()

    #gPad.SetLogy()

    #run 14
    inp14 = TFile.Open("sigma.root", "read")
    gSig = inp14.Get("sigma")
    ut.set_H1D_col(gSig, rt.kBlack)
    inp14.Close()

    #run 16
    #inp16 = TFile.Open("/home/jaroslav/sim/data_run16/postlim_04.21/subt_corr/root/JPsiPt_corr_14nn.root", "read")
    inp16 = TFile.Open("/home/jaroslav/sim/data_run16/postlim_04.21/subt_corr/root/JPsiPt_corr_XnXn.root", "read")
    h16 = inp16.Get("hpt2corsub_JPsicoh")
    #inp16.ls()
    ut.set_H1D(h16)
    ut.set_H1D_col(h16, rt.kRed)


    #for i in range(h16.GetNbinsX()):
    #    print i, h16.GetBinContent(i), h16.GetBinError(i)

    #scale to mb
    h16.Sumw2()
    h16.Scale(1e-3)

    #Starlight
    gSlight.Draw("lsame")

    #data
    gSig.Draw("psame")
    h16.Draw("e1same")

    cleg = ut.prepare_leg(0.1, 0.96, 0.14, 0.01, 0.035)
    cleg.AddEntry(None, "Au+Au #rightarrow J/#psi + Au+Au + XnXn, #sqrt{#it{s}_{#it{NN}}} = 200 GeV", "")
    cleg.Draw("same")

    leg = ut.prepare_leg(0.68, 0.76, 0.3, 0.16, 0.035)
    leg.AddEntry(gSig, "Run 14", "lp")
    leg.AddEntry(h16, "Run 16", "lp")
    leg.AddEntry(gSlight, "STARLIGHT", "l")
    leg.Draw("same")

    #gPad.SetGrid()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#main

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    main()

