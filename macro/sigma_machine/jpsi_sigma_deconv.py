#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TF1, vector, TMath, TGraphAsymmErrors

gSystem.Load("/home/jaroslav/root/RooUnfold_Rev360/libRooUnfold")
from ROOT import RooUnfoldResponse, RooUnfoldBayes, RooUnfoldSvd

import sys
sys.path.append('../')
import plot_utils as ut

from models import *
from get_centers import get_centers_from_toyMC

#_____________________________________________________________________________
def main():

    gROOT.SetBatch()

    #range for |t|
    ptmin = 0.
    ptmax = 0.109  #   0.109  0.01 for interference range

    #default binning
    ptbin = 0.004   # 0.004  0.0005 for interference range

    #long bins at high |t|
    ptmid = 0.06  # 0.08, value > ptmax will switch it off   0.06
    ptlon = 0.01  # 0.01

    #short bins at low |t|
    ptlow = 0.01
    ptshort = 0.0005

    #mass interval
    mmin = 2.8
    mmax = 3.2

    dy = 2. # rapidity interval, for integrated sigma

    ngg = 131  # number of gamma-gamma from mass fit

    lumi = 13871.907 # lumi in inv. ub

    #correction to luminosity for ana/triggered events
    ratio_ana = 3420950./3694000

    #scale the lumi for |z| around nominal bunch crossing
    ratio_zdc_vtx = 0.502

    Reta = 0.503 # pseudorapidity preselection
    #Reta = 1.

    trg_eff = 0.67 # bemc trigger efficiency

    ratio_tof = 1.433 # tof correction to efficiency

    bbceff = 0.97 # BBC veto inefficiency

    zdc_acc = 0.49 # ZDC acceptance to XnXn 0.7

    br = 0.05971 # dielectrons branching ratio

    #data
    basedir = "../../../star-upc-data/ana/muDst/muDst_run1/sel5"
    infile = "ana_muDst_run1_all_sel5z.root"

    #MC
    basedir_sl = "../../../star-upc-data/ana/starsim/slight14e/sel5"
    #infile_sl = "ana_slight14e1x2_s6_sel5z.root"
    infile_sl = "ana_slight14e1x3_s6_sel5z.root"
    #
    basedir_sart = "../../../star-upc-data/ana/starsim/sartre14a/sel5"
    infile_sart = "ana_sartre14a1_sel5z_s6_v2.root"
    #
    basedir_bgen = "../../../star-upc-data/ana/starsim/bgen14a/sel5"
    infile_bgen = "ana_bgen14a1_v0_sel5z_s6.root"
    #infile_bgen = "ana_bgen14a2_sel5z_s6.root"
    #
    basedir_gg = "../../../star-upc-data/ana/starsim/slight14e/sel5"
    infile_gg = "ana_slight14e2x1_sel5_nzvtx.root"

    #model predictions
    gSlight = load_starlight(dy)
    gSartre = load_sartre()
    gFlat = loat_flat_pt2()
    gMS = load_ms()
    gCCK = load_cck()

    #open the inputs
    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("jRecTree")
    #
    inp_gg = TFile.Open(basedir_gg+"/"+infile_gg)
    tree_gg = inp_gg.Get("jRecTree")
    #
    inp_sl = TFile.Open(basedir_sl+"/"+infile_sl)
    tree_sl_gen = inp_sl.Get("jGenTree")
    #
    inp_sart = TFile.Open(basedir_sart+"/"+infile_sart)
    tree_sart_gen = inp_sart.Get("jGenTree")
    #
    inp_bgen = TFile.Open(basedir_bgen+"/"+infile_bgen)
    tree_bgen_gen = inp_bgen.Get("jGenTree")

    #evaluate binning
    #print "bins:", ut.get_nbins(ptbin, ptmin, ptmax)

    bins = ut.get_bins_vec_2pt(ptbin, ptlon, ptmin, ptmax, ptmid)
    #bins = ut.get_bins_vec_3pt(ptshort, ptbin, ptlon, ptmin, ptmax, ptlow, ptmid)
    #print "bins2:", bins.size()-1

    #load the data
    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    hPt = ut.prepare_TH1D_vec("hPt", bins)
    tree.Draw("jRecPt*jRecPt >> hPt" , strsel)

    #distribution for bin centers
    hPtCen = hPt.Clone("hPtCen")

    #gamma-gamma component
    hPtGG = ut.prepare_TH1D_vec("hPtGG", bins)
    tree_gg.Draw("jRecPt*jRecPt >> hPtGG", strsel)

    #normalize the gamma-gamma component
    ut.norm_to_num(hPtGG, ngg, rt.kGreen)

    #incoherent functional shape
    func_incoh_pt2 = TF1("func_incoh", "[0]*exp(-[1]*x)", 0., 10.)
    func_incoh_pt2.SetParameters(873.04, 3.28)

    #fill incoherent histogram from functional shape
    hPtIncoh = ut.prepare_TH1D_vec("hPtIncoh", bins)
    ut.fill_h1_tf(hPtIncoh, func_incoh_pt2, rt.kRed)

    #print "Entries before gamma-gamma and incoherent subtraction:", hPt.GetEntries()

    #subtract gamma-gamma and incoherent components
    hPt.Sumw2()
    hPt.Add(hPtGG, -1)
    #print "Gamma-gamma entries:", hPtGG.Integral()
    #print "Entries after gamma-gamma subtraction:", hPt.Integral()
    #print "Incoherent entries:", hPtIncoh.Integral()
    hPt.Add(hPtIncoh, -1)

    #print "Entries after all subtraction:", hPt.Integral()

    #scale the luminosity
    lumi_scaled = lumi*ratio_ana*ratio_zdc_vtx
    #print "lumi_scaled:", lumi_scaled

    #denominator for deconvoluted distribution, conversion ub to mb
    den = Reta*br*zdc_acc*trg_eff*bbceff*ratio_tof*lumi_scaled*1000.*dy

    #deconvolution
    deconv_min = bins[0]
    deconv_max = bins[bins.size()-1]
    deconv_nbin = bins.size()-1
    gROOT.LoadMacro("fill_response_matrix.C")

    #Starlight response
    #resp_sl = RooUnfoldResponse(deconv_nbin, deconv_min, deconv_max, deconv_nbin, deconv_min, deconv_max)
    resp_sl = RooUnfoldResponse(hPt, hPt)
    rt.fill_response_matrix(tree_sl_gen, resp_sl)
    #
    unfold_sl = RooUnfoldBayes(resp_sl, hPt, 15)
    #unfold_sl = RooUnfoldSvd(resp_sl, hPt, 15)
    hPtSl = unfold_sl.Hreco()
    #ut.set_H1D(hPtSl)
    #apply the denominator and bin width
    ut.norm_to_den_w(hPtSl, den)

    #Sartre response
    #resp_sart = RooUnfoldResponse(deconv_nbin, deconv_min, deconv_max, deconv_nbin, deconv_min, deconv_max)
    #resp_sart = RooUnfoldResponse(hPt, hPt)
    #rt.fill_response_matrix(tree_sart_gen, resp_sart)
    #
    #unfold_sart = RooUnfoldBayes(resp_sart, hPt, 10)
    #hPtSart = unfold_sart.Hreco()
    #ut.set_H1D(hPtSart)
    #hPtSart.SetMarkerStyle(21)

    #Flat pT^2 response
    #resp_bgen = RooUnfoldResponse(deconv_nbin, deconv_min, deconv_max, deconv_nbin, deconv_min, deconv_max)
    resp_bgen = RooUnfoldResponse(hPt, hPt)
    rt.fill_response_matrix(tree_bgen_gen, resp_bgen)
    #
    unfold_bgen = RooUnfoldBayes(resp_bgen, hPt, 14)
    hPtFlat = unfold_bgen.Hreco()
    #ut.set_H1D(hPtFlat)
    #apply the denominator and bin width
    ut.norm_to_den_w(hPtFlat, den)
    #hPtFlat.SetMarkerStyle(22)
    #hPtFlat.SetMarkerSize(1.3)

    #systematical errors
    err_zdc_acc = 0.1
    err_bemc_eff = 0.03
    #sys_err = rt.TMath.Sqrt(err_zdc_acc*err_zdc_acc + err_bemc_eff*err_bemc_eff)
    sys_err = err_zdc_acc*err_zdc_acc + err_bemc_eff*err_bemc_eff
    #print "Total sys err:", sys_err
    hSys = ut.prepare_TH1D_vec("hSys", bins)
    hSys.SetOption("E2")
    hSys.SetFillColor(rt.kOrange+1)
    hSys.SetLineColor(rt.kOrange)
    for ibin in xrange(1,hPtFlat.GetNbinsX()+1):
        hSys.SetBinContent(ibin, hPtFlat.GetBinContent(ibin))
        sig_sl = hPtSl.GetBinContent(ibin)
        sig_fl = hPtFlat.GetBinContent(ibin)
        err_deconv = TMath.Abs(sig_fl-sig_sl)/sig_fl
        #print "err_deconv", err_deconv
        #sys_err += err_deconv*err_deconv
        sys_err_sq = sys_err + err_deconv*err_deconv
        sys_err_bin = TMath.Sqrt(sys_err_sq)
        stat_err = hPtFlat.GetBinError(ibin)/hPtFlat.GetBinContent(ibin)
        tot_err = TMath.Sqrt(stat_err*stat_err + sys_err_sq)
        #hSys.SetBinError(ibin, hPtFlat.GetBinContent(ibin)*err_deconv)
        hSys.SetBinError(ibin, hPtFlat.GetBinContent(ibin)*sys_err_bin)
        #hPtFlat.SetBinError(ibin, hPtFlat.GetBinContent(ibin)*tot_err)

    #draw the results
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    #frame for models plot only
    frame = ut.prepare_TH1D("frame", ptbin, ptmin, ptmax)

    can = ut.box_canvas()
    #ut.set_margin_lbtr(gPad, 0.1, 0.09, 0.03, 0.03)
    ut.set_margin_lbtr(gPad, 0.1, 0.09, 0.055, 0.01)

    ytit = "d#it{#sigma}/d#it{t}d#it{y} (mb/(GeV/c)^{2})"
    xtit = "|#kern[0.3]{#it{t}}| ((GeV/c)^{2})"

    ut.put_yx_tit(frame, ytit, xtit, 1.4, 1.2)
    frame.SetMaximum(11)
    #frame.SetMinimum(1.e-6)
    #frame.SetMinimum(2e-4)
    frame.SetMinimum(1e-5)  # 3e-5
    frame.Draw()

    #hSys.Draw("e2same")

    #bin center points from data
    gSig = apply_centers(hPtFlat, hPtCen)
    ut.set_graph(gSig)

    #hPtSl.Draw("e1same")
    #hPtSart.Draw("e1same")
    #hPtFlat.Draw("e1same")

    #put model predictions
    #gSartre.Draw("lsame")
    #gFlat.Draw("lsame")
    gMS.Draw("lsame")
    gCCK.Draw("lsame")
    gSlight.Draw("lsame")

    gSig.Draw("P")

    frame.Draw("same")

    gPad.SetLogy()

    cleg = ut.prepare_leg(0.1, 0.96, 0.14, 0.01, 0.035)
    cleg.AddEntry(None, "Au+Au #rightarrow J/#psi + Au+Au + XnXn, #sqrt{#it{s}_{#it{NN}}} = 200 GeV", "")
    cleg.Draw("same")

    leg = ut.prepare_leg(0.45, 0.82, 0.18, 0.1, 0.035)
    leg.AddEntry(None, "#bf{|#kern[0.3]{#it{y}}| < 1}", "")
    hx = ut.prepare_TH1D("hx", 1, 0, 1)
    leg.AddEntry(hx, "STAR")
    hx.Draw("same")
    leg.Draw("same")

    #legend for models
    mleg = ut.prepare_leg(0.68, 0.76, 0.3, 0.16, 0.035)
    #mleg = ut.prepare_leg(0.68, 0.8, 0.3, 0.12, 0.035)
    mleg.AddEntry(gSlight, "STARLIGHT", "l")
    mleg.AddEntry(gMS, "MS", "l")
    mleg.AddEntry(gCCK, "CCK-hs", "l")
    #mleg.AddEntry(gSartre, "Sartre", "l")
    #mleg.AddEntry(gFlat, "Flat #it{p}_{T}^{2}", "l")
    mleg.Draw("same")

    #legend for deconvolution method
    dleg = ut.prepare_leg(0.3, 0.75, 0.2, 0.18, 0.035)
    #dleg = ut.prepare_leg(0.3, 0.83, 0.2, 0.1, 0.035)
    dleg.AddEntry(None, "Unfolding with:", "")
    dleg.AddEntry(hPtSl, "Starlight", "p")
    #dleg.AddEntry(hPtSart, "Sartre", "p")
    dleg.AddEntry(hPtFlat, "Flat #it{p}_{T}^{2}", "p")
    #dleg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

    #to prevent 'pure virtual method called'
    gPad.Close()

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")


#_____________________________________________________________________________
def apply_centers(hPt, hCen):

    #bin center points according to the data

    cen = get_centers_from_toyMC(hCen)

    gSig = TGraphAsymmErrors(hPt.GetNbinsX())

    for i in xrange(hPt.GetNbinsX()):

        #center point
        #xcen = hPt.GetBinCenter(i+1)
        xcen = cen[i]["val"]

        #cross section value
        gSig.SetPoint(i, xcen, hPt.GetBinContent(i+1))

        #vertical error
        gSig.SetPointEYlow(i, hPt.GetBinErrorLow(i+1))
        gSig.SetPointEYhigh(i, hPt.GetBinErrorUp(i+1))

        #horizontal error
        gSig.SetPointEXlow(i, cen[i]["err"])
        gSig.SetPointEXhigh(i, cen[i]["err"])

    return gSig

#_____________________________________________________________________________
def get_centers(bins):

    #bin center points according to the data

    print bins

#_____________________________________________________________________________
if __name__ == "__main__":

    main()












