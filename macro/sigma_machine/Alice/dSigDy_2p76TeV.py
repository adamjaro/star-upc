#!/usr/bin/python3

# dSigma / dy as a function of y as shown in Eur. Phys. J. C (2013) 73:2617

import ROOT as rt
from ROOT import gStyle, TCanvas, gPad, gROOT, TFile, TH1D

import sys
sys.path.append("../../")
import plot_utils as ut

#_____________________________________________________________________________
def main():

    gROOT.SetBatch()

    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)
    gStyle.SetFrameLineWidth(2)
    gStyle.SetOptStat("")
    gStyle.SetPalette(1)

    inp = "/home/jaroslav/sim/starlight_tx/slight_Jpsi_PbPb_coh.root"

    infile = TFile.Open(inp)
    tree = infile.Get("slight_tree")

    hY = TH1D("hY", "", 50, -5, 5)

    tree.Draw("rapidity >> hY")

    #total cross section for PbPb at 2.76 GeV
    sigma_tot = 23.162 # mb

    hY.Scale(sigma_tot/hY.Integral("width"))

    can = TCanvas("can", "can", 768, 768)

    frame = gPad.DrawFrame(-5.1, 0, 5.1, 5) # xmin, ymin, xmax, ymax
    frame.Draw()

    ut.put_yx_tit(frame, "d#it{#sigma}/d#it{y} (mb)", "#it{y}", 1.6, 1.3)

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.02, 0.01)

    gPad.SetGrid()

    #convert to graph
    gY = ut.h1_to_graph(hY)

    gY.SetLineColor(rt.kRed)
    gY.SetLineWidth(3)

    gY.Draw("same")

    ut.invert_col(gPad)

    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
if __name__ == "__main__":

    main()










