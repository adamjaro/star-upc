#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TF1

import sys
sys.path.append('../')
import plot_utils as ut
from parameter_descriptor import parameter_descriptor as pdesc

#_____________________________________________________________________________
def fit_vtx_z():

    #gaussian fit to vertex z-position
    datamc = False  #true - data, false - mc

    if datamc:
        vbin = 4.
    else:
        vbin = 1.
    vmax = 120.

    mmin = 1.5
    mmax = 5.

    if datamc:
        fit_lo = -30.
        fit_hi = 35.
    else:
        fit_lo = -40.
        fit_hi = 45.
    fitcol = rt.kBlue

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    out = open("out.txt", "w")

    can = ut.box_canvas()

    hVtx = ut.prepare_TH1D("hVtx", vbin, -vmax, vmax)
    if datamc:
        tree.Draw("jVtxZ >> hVtx", strsel)
    else:
        mctree.Draw("jVtxZ >> hVtx", strsel)

    f1 = TF1("f1", "gaus", fit_lo, fit_hi)
    f1.SetNpx(1000)
    f1.SetLineColor(fitcol)

    r1 = (hVtx.Fit(f1, "RS")).Get()
    #print r1
    out.write(ut.log_tfit_result(r1))

    hVtx.SetYTitle("Counts / {0:.0f} cm".format(vbin));
    hVtx.SetXTitle("#it{z} of primary vertex (cm)");

    hVtx.SetTitleOffset(1.5, "Y")
    hVtx.SetTitleOffset(1.3, "X")

    gPad.SetTopMargin(0.02)
    gPad.SetRightMargin(0.02)
    gPad.SetBottomMargin(0.1)
    gPad.SetLeftMargin(0.11)

    leg = ut.prepare_leg(0.15, 0.82, 0.28, 0.12, 0.025)
    leg.SetMargin(0.17)
    ut.add_leg_mass(leg, mmin, mmax)
    if datamc:
        leg.AddEntry(hVtx, "Data")
    else:
        leg.AddEntry(hVtx, "MC")
    leg.AddEntry(f1, "Gaussian fit", "l")

    #fit parameters on the plot
    desc = pdesc(hVtx, 0.14, 0.82, 0.057)
    desc.set_text_size(0.03)
    desc.itemD("#chi^{2}/ndf", r1.Chi2()/r1.Ndf(), -1, fitcol)
    desc.prec = 2
    desc.itemRes("mean", r1, 1, fitcol)
    desc.itemRes("#it{#sigma}", r1, 2, fitcol)
    desc.itemRes("norm", r1, 0, fitcol)

    hVtx.Draw()
    leg.Draw("same")
    desc.draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of fit_vtx_z

#_____________________________________________________________________________
def plot_vtx_z():

    #primary vertex position along z from data and MC
    vbin = 4.
    vmax = 120.

    mmin = 1.5
    mmax = 5

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    can = ut.box_canvas()

    hVtx = ut.prepare_TH1D("hVtx", vbin, -vmax, vmax)
    hVtxMC = ut.prepare_TH1D("hVtxMC", vbin/2., -vmax, vmax)

    tree.Draw("jVtxZ >> hVtx", strsel)
    mctree.Draw("jVtxZ >> hVtxMC", strsel)
    ut.norm_to_data(hVtxMC, hVtx, rt.kBlue, -40, 40)

    hVtx.SetYTitle("Counts / {0:.0f} cm".format(vbin));
    hVtx.SetXTitle("#it{z} of primary vertex (cm)");

    hVtx.SetTitleOffset(1.5, "Y")
    hVtx.SetTitleOffset(1.3, "X")

    gPad.SetTopMargin(0.02)
    gPad.SetRightMargin(0.02)
    gPad.SetBottomMargin(0.1)
    gPad.SetLeftMargin(0.11)

    cut_lo = ut.cut_line(-35, 0.8, hVtx)
    cut_hi = ut.cut_line(35, 0.8, hVtx)

    leg = ut.prepare_leg(0.16, 0.82, 0.26, 0.12, 0.025)
    leg.SetMargin(0.15)
    leg.SetBorderSize(1)
    ut.add_leg_mass(leg, mmin, mmax)
    leg.AddEntry(hVtx, "Data")
    #leg.AddEntry(hVtxMC, "MC, coherent J/#it{#psi}", "l")
    leg.AddEntry(hVtxMC, "MC, #it{#gamma}#it{#gamma} #rightarrow e^{+}e^{-}", "l")
    leg.AddEntry(cut_lo, "Cut at #pm35 cm", "l")

    hVtx.Draw()
    hVtxMC.Draw("same")
    leg.Draw("same")
    cut_lo.Draw("same")
    cut_hi.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_vtx_z

#_____________________________________________________________________________
if __name__ == "__main__":

    #data
    basedir = "../../ana/muDst/muDst_run1/sel3"
    #infile = "ana_muDst_run1_all_sel3.root"
    infile = "ana_muDst_run1_all_sel3_nzvtx.root"

    #MC
    #basedir_mc = "../../ana/starsim/slight14b2/sel3"
    basedir_mc = "../../ana/starsim/slight14b1/sel3"
    #infile_mc = "ana_slight14b2x2_sel3_nzvtx.root"
    infile_mc = "ana_slight14b1x2_sel3_nzvtx.root"

    interactive = False

    if interactive == False: gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    iplot = 0
    funclist = []
    funclist.append(plot_vtx_z) # 0
    funclist.append(fit_vtx_z) # 1

    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("jRecTree")

    inp_mc = TFile.Open(basedir_mc+"/"+infile_mc)
    mctree = inp_mc.Get("jRecTree")

    #call the plot function
    funclist[iplot]()

    #to prevent 'pure virtual method called'
    gPad.Close()

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")



