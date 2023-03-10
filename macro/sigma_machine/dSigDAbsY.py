#!/usr/bin/python3

# dSigma / dy as a function of y as shown in Eur. Phys. J. C (2013) 73:2617

import ROOT as rt
from ROOT import gStyle, TCanvas, gPad, gROOT, TFile, TH1D

import sys
sys.path.append("..")
import plot_utils as ut

#_____________________________________________________________________________
def main():

    inp = "/home/jaroslav/sim/starlight_tx/slight_AuAu_200GeV_Jpsi_coh_intmax0p34_6Mevt.root"

    infile = TFile.Open(inp)
    tree = infile.Get("slight_tree")

    hY = TH1D("hY", "", 70, -3, 3)

    tree.Draw("rapidity >> hY")

    #total cross section for AuAu at 200 GeV
    sigma_tot = 67.958 # micro barn

    hY.Scale(sigma_tot/hY.Integral("width"))

    can = TCanvas("can", "can", 768, 768)

    frame = gPad.DrawFrame(0, 0, 1.7, 40) # xmin, ymin, xmax, ymax
    frame.Draw()

    ut.put_yx_tit(frame, "d#it{#sigma}/d#it{y} (#mub)", "|#it{y}|", 1.4, 1.2)

    ut.set_margin_lbtr(gPad, 0.1, 0.09, 0.02, 0.01)

    gPad.SetGrid()

    gY = ut.h1_to_graph(hY)

    gY.SetLineColor(rt.kRed)
    gY.SetLineWidth(3)

    gY.Draw("same")

    # Integrated sigma from data (mb): 0.023004428341012642 +/- 0.0021194215697785544
    # Sigma (micro barn): 25.33529625253031 1.3670506187705376
    hDat = ut.prepare_TH1D_n("hDat", 1, 0, 1)
    #hDat.SetBinContent(1, 23.004) # micro barn
    #hDat.SetBinError(1, 2.119)
    hDat.SetBinContent(1, 22.84) # micro barn
    hDat.SetBinError(1, 1.31)

    ut.set_H1D_col(hDat, rt.kBlue)

    hDat.Draw("e1same")

    hDat1 = ut.prepare_TH1D_n("hDat1", 1, 0, 0.2)
    hDat1.SetBinContent(1, 32.25) # micro barn
    hDat1.SetBinError(1, 3.29)

    #hDat1.Draw("e1same")

    hDat2 = ut.prepare_TH1D_n("hDat2", 1, 0.2, 0.5)
    hDat2.SetBinContent(1, 33.62) # micro barn
    hDat2.SetBinError(1, 2.77)

    #hDat2.Draw("e1same")

    hDat3 = ut.prepare_TH1D_n("hDat3", 1, 0.5, 1)
    hDat3.SetBinContent(1, 13.65) # micro barn
    hDat3.SetBinError(1, 1.82)

    #hDat3.Draw("e1same")

    leg = ut.prepare_leg(0.5, 0.76, 0.2, 0.2, 0.035)
    leg.AddEntry("", "#it{J/}#it{#psi} + XnXn, 200 GeV, run 14", "")
    leg.AddEntry(hDat, "Full interval", "lp")
    leg.AddEntry(hDat1, "Bins", "lp")
    leg.AddEntry(gY, "Starlight", "l")
    leg.Draw("same")

    ut.invert_col(gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)
    gStyle.SetFrameLineWidth(2)
    gStyle.SetOptStat("")
    gStyle.SetPalette(1)

    main()










