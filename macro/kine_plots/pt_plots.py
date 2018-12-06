#!/usr/bin/python

import math

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TF1

import sys
sys.path.append('../')
import plot_utils as ut
from parameter_descriptor import parameter_descriptor as pdesc

#_____________________________________________________________________________
def fit_logPt2_incoh():

    #fit to incoherent log_10(pT^2)

    ptbin = 0.12
    ptmin = -5.
    ptmax = 1.

    mmin = 2.8
    mmax = 3.2

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    can = ut.box_canvas()

    hPtIncoh = ut.prepare_TH1D("hPtIncoh", ptbin/3., ptmin, ptmax)

    ut.put_yx_tit(hPtIncoh, "Events / ({0:.3f}".format(ptbin)+" GeV^{2})", "log_{10}( #it{p}_{T}^{2} ) (GeV^{2})")

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.01, 0.01)

    draw = "TMath::Log10(jRecPt*jRecPt)"
    tree_incoh.Draw(draw + " >> hPtIncoh", strsel)

    #hPtIncoh.Sumw2()
    #hPtIncoh.Scale(1./hPtIncoh.Integral("width"))

    func_incoh_logPt2 = TF1("func_incoh_logPt2", "[0]*log(10.)*pow(10.,x)*exp(-[1]*pow(10.,x))", -10., 10.)
    func_incoh_logPt2.SetParName(0, "A")
    func_incoh_logPt2.SetParName(1, "b")
    func_incoh_logPt2.SetNpx(1000)
    func_incoh_logPt2.SetLineColor(rt.kRed)

    func_incoh_logPt2.SetParameters(3000., 5.)

    r1 = (hPtIncoh.Fit(func_incoh_logPt2, "RS")).Get()

    hPtIncoh.Draw()
    func_incoh_logPt2.Draw("same")

    leg = ut.prepare_leg(0.18, 0.82, 0.14, 0.15, 0.03)
    ut.add_leg_mass(leg, mmin, mmax)
    leg.AddEntry(hPtIncoh, "Incoherent MC")
    leg.AddEntry(func_incoh_logPt2, "ln(10)*#it{A}*10^{log_{10}#it{p}_{T}^{2}}exp(-#it{b}10^{log_{10}#it{p}_{T}^{2}})", "l")
    leg.Draw("same")

    desc = pdesc(hPtIncoh, 0.18, 0.82, 0.057)
    desc.set_text_size(0.03)
    desc.itemD("#chi^{2}/ndf", r1.Chi2()/r1.Ndf(), -1, rt.kRed)
    desc.itemRes("#it{A}", r1, 0, rt.kRed)
    desc.itemRes("#it{b}", r1, 1, rt.kRed)
    desc.draw()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of fit_logPt2_incoh

#_____________________________________________________________________________
def fit_pt2_incoh():

    #fit to incoherent MC pT^2

    ptbin = 0.008
    ptmin = 0.
    ptmax = 1.

    mmin = 2.8
    mmax = 3.2

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    can = ut.box_canvas()

    hPtIncoh = ut.prepare_TH1D("hPtIncoh", ptbin, ptmin, ptmax)

    ut.put_yx_tit(hPtIncoh, "Events / ({0:.3f}".format(ptbin)+" GeV^{2})", "#it{p}_{T}^{2} (GeV^{2})")

    tree_incoh.Draw("jRecPt*jRecPt >> hPtIncoh", strsel)

    #hPtIncoh.Sumw2()
    #hPtIncoh.Scale(1./hPtIncoh.Integral("width"))

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.01, 0.01)

    func_incoh_pt2 = TF1("func_incoh", "[0]*exp(-[1]*x)", 0., 10.)
    func_incoh_pt2.SetParName(0, "A")
    func_incoh_pt2.SetParName(1, "b")
    func_incoh_pt2.SetNpx(1000)
    func_incoh_pt2.SetLineColor(rt.kRed)

    func_incoh_pt2.SetParameters(3000., 5.)

    r1 = (hPtIncoh.Fit(func_incoh_pt2, "RS")).Get()

    hPtIncoh.Draw()
    func_incoh_pt2.Draw("same")

    leg = ut.prepare_leg(0.67, 0.84, 0.14, 0.12, 0.03)
    ut.add_leg_mass(leg, mmin, mmax)
    leg.AddEntry(hPtIncoh, "Incoherent MC")
    leg.AddEntry(func_incoh_pt2, "#it{A}*exp(-#it{b}*#it{p}_{T}^{2})", "l")
    leg.Draw("same")

    desc = pdesc(hPtIncoh, 0.72, 0.84, 0.057)
    desc.set_text_size(0.03)
    desc.itemD("#chi^{2}/ndf", r1.Chi2()/r1.Ndf(), -1, rt.kRed)
    desc.itemRes("#it{A}", r1, 0, rt.kRed)
    desc.itemRes("#it{b}", r1, 1, rt.kRed)
    desc.draw()

    #gPad.SetLogy()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of fit_pt2_incoh

#_____________________________________________________________________________
def fit_pt_incoh():

    #fit to incoherent MC pT

    ptbin = 0.015
    #ptbin = math.sqrt(0.005)
    ptmin = 0.
    ptmax = 1.

    mmin = 2.8
    mmax = 3.2

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    can = ut.box_canvas()

    hPtIncoh = ut.prepare_TH1D("hPtIncoh", ptbin, ptmin, ptmax)
    ut.put_yx_tit(hPtIncoh, "Events / ({0:.3f}".format(ptbin)+" GeV)", "#it{p}_{T} (GeV)")

    tree_incoh.Draw("jRecPt >> hPtIncoh", strsel)

    #hPtIncoh.Sumw2()
    #hPtIncoh.Scale(1./hPtIncoh.Integral("width"))

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.01, 0.02)

    func_incoh = TF1("func_incoh", "2*[0]*x*exp(-[1]*x*x)", 0., 10.)
    func_incoh.SetParName(0, "A")
    func_incoh.SetParName(1, "b")
    func_incoh.SetNpx(1000)
    func_incoh.SetLineColor(rt.kRed)

    func_incoh.SetParameters(3000., 5.)

    r1 = (hPtIncoh.Fit(func_incoh, "RS")).Get()

    hPtIncoh.Draw()
    func_incoh.Draw("same")

    leg = ut.prepare_leg(0.67, 0.84, 0.14, 0.12, 0.03)
    ut.add_leg_mass(leg, mmin, mmax)
    leg.AddEntry(hPtIncoh, "Incoherent MC")
    leg.AddEntry(func_incoh, "2#it{A}*#it{p}_{T}exp(-#it{b}*#it{p}_{T}^{2})", "l")
    leg.Draw("same")

    desc = pdesc(hPtIncoh, 0.72, 0.84, 0.057)
    desc.set_text_size(0.03)
    desc.itemD("#chi^{2}/ndf", r1.Chi2()/r1.Ndf(), -1, rt.kRed)
    desc.prec = 2
    desc.itemRes("#it{A}", r1, 0, rt.kRed)
    desc.prec = 3
    desc.itemRes("#it{b}", r1, 1, rt.kRed)
    desc.draw()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of fit_pt_incoh

#_____________________________________________________________________________
def plot_pt():

    #pT with coherent incoherent and gamma-gamma components

    ptbin = 0.015
    ptmin = 0.
    ptmax = 1.1

    mmin = 2.8
    mmax = 3.2

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    can = ut.box_canvas()

    hPt = ut.prepare_TH1D("hPt", ptbin, ptmin, ptmax)
    hPtCoh = ut.prepare_TH1D("hPtCoh", ptbin/3., ptmin, ptmax)
    hPtIncoh = ut.prepare_TH1D("hPtIncoh", ptbin, ptmin, ptmax)
    hPtGG = ut.prepare_TH1D("hPtGG", ptbin, ptmin, ptmax)

    ut.put_yx_tit(hPt, "Events / ({0:.3f}".format(ptbin)+" GeV)", "#it{p}_{T} (GeV})")

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.01, 0.02)

    draw = "jRecPt"

    tree.Draw(draw + " >> hPt", strsel)
    tree_coh.Draw(draw + " >> hPtCoh", strsel)
    tree_incoh.Draw(draw + " >> hPtIncoh", strsel)
    tree_gg.Draw(draw + " >> hPtGG", strsel)

    ut.norm_to_data(hPtCoh, hPt, rt.kBlue, 0., 0.11)
    ut.norm_to_data(hPtIncoh, hPt, rt.kRed, 0.28, 1.)
    ut.norm_to_data(hPtGG, hPt, rt.kGreen, 0., 0.03)

    hPt.Draw()
    hPtCoh.Draw("same")
    hPtIncoh.Draw("same")
    hPtGG.Draw("same")

    leg = ut.prepare_leg(0.67, 0.78, 0.14, 0.18, 0.03)
    ut.add_leg_mass(leg, mmin, mmax)
    leg.AddEntry(hPt, "Data")
    leg.AddEntry(hPtCoh, "Coherent MC", "l")
    leg.AddEntry(hPtIncoh, "Incoherent MC", "l")
    leg.AddEntry(hPtGG, "#gamma#gamma#rightarrow e^{+}e^{-} MC", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hPt, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_pt

#_____________________________________________________________________________
def plot_pt2():

    #pT^2 with coherent incoherent and gamma-gamma components

    ptbin = 0.002
    ptmin = 0.
    ptmax = 0.2   # 0.3

    mmin = 2.8
    mmax = 3.2

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    can = ut.box_canvas()

    hPt = ut.prepare_TH1D("hPt", ptbin, ptmin, ptmax)
    hPtCoh = ut.prepare_TH1D("hPtCoh", ptbin/3., ptmin, ptmax)
    hPtIncoh = ut.prepare_TH1D("hPtIncoh", ptbin, ptmin, ptmax)
    hPtGG = ut.prepare_TH1D("hPtGG", ptbin, ptmin, ptmax)

    ut.put_yx_tit(hPt, "Events / ({0:.3f}".format(ptbin)+" GeV^{2})", "#it{p}_{T}^{2} (GeV^{2})")

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.01, 0.02)

    draw = "jRecPt*jRecPt"

    tree.Draw(draw + " >> hPt", strsel)
    tree_coh.Draw(draw + " >> hPtCoh", strsel)
    tree_incoh.Draw(draw + " >> hPtIncoh", strsel)
    tree_gg.Draw(draw + " >> hPtGG", strsel)

    ut.norm_to_data(hPtCoh, hPt, rt.kBlue, 0., 0.015)
    ut.norm_to_data(hPtIncoh, hPt, rt.kRed, 0.05, 0.16) # 0.3
    ut.norm_to_data(hPtGG, hPt, rt.kGreen, 0., 0.001)

    hPt.Draw()
    hPtCoh.Draw("same")
    hPtIncoh.Draw("same")
    hPtGG.Draw("same")

    leg = ut.prepare_leg(0.67, 0.78, 0.14, 0.18, 0.03)
    ut.add_leg_mass(leg, mmin, mmax)
    leg.AddEntry(hPt, "Data")
    leg.AddEntry(hPtCoh, "Coherent MC", "l")
    leg.AddEntry(hPtIncoh, "Incoherent MC", "l")
    leg.AddEntry(hPtGG, "#gamma#gamma#rightarrow e^{+}e^{-} MC", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hPt, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    gPad.SetLogy()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_pt2

#_____________________________________________________________________________
def plot_jpsi_logPt2():

    # log_10(pT^2)

    ptbin = 0.12
    ptmin = -5.
    ptmax = 1.

    mmin = 2.8
    mmax = 3.2

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    can = ut.box_canvas()

    hPt = ut.prepare_TH1D("hPt", ptbin, ptmin, ptmax)
    hPtCoh = ut.prepare_TH1D("hPtCoh", ptbin/3., ptmin, ptmax)
    hPtIncoh = ut.prepare_TH1D("hPtIncoh", ptbin/3., ptmin, ptmax)
    hPtGG = ut.prepare_TH1D("hPtGG", ptbin, ptmin, ptmax)

    ut.put_yx_tit(hPt, "Events / ({0:.3f}".format(ptbin)+" GeV^{2})", "log_{10}( #it{p}_{T}^{2} ) (GeV^{2})")

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.01, 0.01)

    draw = "TMath::Log10(jRecPt*jRecPt)"

    tree.Draw(draw + " >> hPt", strsel)
    tree_coh.Draw(draw + " >> hPtCoh", strsel)
    tree_incoh.Draw(draw + " >> hPtIncoh", strsel)
    tree_gg.Draw(draw + " >> hPtGG", strsel)
    ut.norm_to_data(hPtCoh, hPt, rt.kBlue, -5., -1.8) # norm for coh
    ut.norm_to_data(hPtIncoh, hPt, rt.kRed, -1.1, 1.) # for incoh
    ut.norm_to_data(hPtGG, hPt, rt.kGreen, -5., -2.4) # for ggel

    hPt.Draw()
    hPtCoh.Draw("same")
    hPtIncoh.Draw("same")
    hPtGG.Draw("same")

    leg = ut.prepare_leg(0.67, 0.79, 0.14, 0.17, 0.03)
    ut.add_leg_mass(leg, mmin, mmax)
    leg.AddEntry(hPt, "Data")
    leg.AddEntry(hPtCoh, "Coherent MC", "l")
    leg.AddEntry(hPtIncoh, "Incoherent MC", "l")
    leg.AddEntry(hPtGG, "#gamma#gamma#rightarrow e^{+}e^{-} MC", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hPt, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    #gPad.SetLogy()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_jpsi_logPt2

#_____________________________________________________________________________
if __name__ == "__main__":

    #data
    basedir = "../../../star-upc-data/ana/muDst/muDst_run1/sel5"
    infile = "ana_muDst_run1_all_sel5z.root"

    #MC
    basedir_mc = "../../../star-upc-data/ana/starsim/slight14e/sel5"
    infile_coh = "ana_slight14e1x1_sel5z.root"
    infile_incoh = "ana_slight14e3_sel5z.root"
    infile_gg = "ana_slight14e2x1_sel5_nzvtx.root"

    interactive = False

    if interactive == False: gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    iplot = 5
    funclist = []
    funclist.append(plot_jpsi_logPt2) # 0
    funclist.append(plot_pt2) # 1
    funclist.append(plot_pt) # 2
    funclist.append(fit_pt_incoh) # 3
    funclist.append(fit_pt2_incoh) # 4
    funclist.append(fit_logPt2_incoh) # 5

    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("jRecTree")

    inp_coh = TFile.Open(basedir_mc+"/"+infile_coh)
    tree_coh = inp_coh.Get("jRecTree")

    inp_incoh = TFile.Open(basedir_mc+"/"+infile_incoh)
    tree_incoh = inp_incoh.Get("jRecTree")

    inp_gg = TFile.Open(basedir_mc+"/"+infile_gg)
    tree_gg = inp_gg.Get("jRecTree")

    #call the plot function
    funclist[iplot]()

    #to prevent 'pure virtual method called'
    gPad.Close()

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")





















