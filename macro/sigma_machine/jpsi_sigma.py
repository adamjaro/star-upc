#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TGraphErrors, TF1, vector, cout

gSystem.Load("/home/jaroslav/root/RooUnfold_Rev360/libRooUnfold")
from ROOT import RooUnfoldResponse, RooUnfoldBayes

import sys
sys.path.append('../')
import plot_utils as ut

from analyze_tree import AnalyzeTree

from models import load_starlight, load_ms, load_cck

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    #range and binning
    ptbin = 0.005   # 0.005 0.003
    ptmin = 0.

    ptmid = 0.08  # 0.08, value > ptmax will switch it off
    ptlon = 0.01

    ptmax = 0.109  # 0.11  0.109

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

    zdc_acc = 0.7 # ZDC acceptance to XnXn

    br = 0.05971 # dielectrons branching ratio

    #data
    basedir = "../../../star-upc-data/ana/muDst/muDst_run1/sel5"
    infile = "ana_muDst_run1_all_sel5z.root"

    #MC
    basedir_coh = "../../../star-upc-data/ana/starsim/slight14e/sel5"
    infile_coh = "ana_slight14e1x1_sel5z.root"
    #
    #basedir_coh = "../../../star-upc-data/ana/starsim/sartre14a/sel5"
    #infile_coh = "ana_sartre14a1_sel5z_s6_v2.root"
    #
    #basedir_coh = "../../../star-upc-data/ana/starsim/slight14e/sel5"
    #infile_coh = "ana_slight14e1x2_v0_s6_sel5z.root"
    # 
    basedir_gg = "../../../star-upc-data/ana/starsim/slight14e/sel5"
    infile_gg = "ana_slight14e2x1_sel5_nzvtx.root"

    #predictions
    gSlight = load_starlight(dy)
    gMS = load_ms()
    gCCK = load_cck()
    #gSartre = load_sartre()

    #open the inputs
    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("jRecTree")
    inp_gg = TFile.Open(basedir_gg+"/"+infile_gg)
    tree_gg = inp_gg.Get("jRecTree")
    inp_coh = TFile.Open(basedir_coh+"/"+infile_coh)
    tree_coh_gen = inp_coh.Get("jGenTree")

    #evaluate binning
    print "bins:", ut.get_nbins(ptbin, ptmin, ptmax)
    bins = vector(rt.double)()
    #bins.push_back(ptmin)
    #while True:
    #    if bins[bins.size()-1] < ptmid:
    #        increment = ptbin
    #    else:
    #        increment = ptlon
    #    bins.push_back( bins[bins.size()-1] + increment )
    #    if bins[bins.size()-1] > ptmax: break

    bins = ut.get_bins_vec_2pt(ptbin, ptlon, ptmin, ptmax, ptmid)

    print "bins2:", bins.size()-1

    #data and gamma-gamma histograms
    #hPt = ut.prepare_TH1D("hPt", ptbin, ptmin, ptmax)
    #hPtGG = ut.prepare_TH1D("hPtGG", ptbin, ptmin, ptmax)
    hPt = ut.prepare_TH1D_vec("hPt", bins)
    hPtGG = ut.prepare_TH1D_vec("hPtGG", bins)

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    tree.Draw("jRecPt*jRecPt >> hPt" , strsel)
    tree_gg.Draw("jRecPt*jRecPt >> hPtGG", strsel)

    #incoherent functional shape
    func_incoh_pt2 = TF1("func_incoh", "[0]*exp(-[1]*x)", 0., 10.)
    func_incoh_pt2.SetParameters(873.04, 3.28)

    #fill incoherent histogram from functional shape
    #hPtIncoh = ut.prepare_TH1D("hPtIncoh", ptbin, ptmin, ptmax)
    hPtIncoh = ut.prepare_TH1D_vec("hPtIncoh", bins)
    ut.fill_h1_tf(hPtIncoh, func_incoh_pt2, rt.kRed)

    #normalize gamma-gamma component
    ut.norm_to_num(hPtGG, ngg, rt.kGreen)

    #subtract gamma-gamma and incoherent components
    hPt.Sumw2()
    hPt.Add(hPtGG, -1)
    hPt.Add(hPtIncoh, -1)

    #scale the luminosity
    lumi_scaled = lumi*ratio_ana*ratio_zdc_vtx
    print "lumi_scaled:", lumi_scaled

    #deconvolution
    #deconv_min = bins[0]
    #deconv_max = bins[bins.size()-1]
    #deconv_nbin = bins.size()-1
    #response = RooUnfoldResponse(deconv_nbin, deconv_min, deconv_max, deconv_nbin/2, deconv_min, deconv_max)
    #gROOT.LoadMacro("fill_response_matrix.C")
    #rt.fill_response_matrix(tree_coh_gen, response)
    #response.Print()

    #unfold = RooUnfoldBayes(response, hPt, 15)
    #hPtRec = unfold.Hreco()
    #ut.set_H1D(hPtRec)
    #hPtRec.SetTitle("")

    #denominator for deconvoluted distribution, conversion ub to mb
    #den = 0.85*Reta*br*zdc_acc*trg_eff*bbceff*ratio_tof*lumi_scaled*1000.*dy
    # 

    #cross section after deconvolution
    #sigma_tot = hPtRec.Integral()/den
    #hPtRec.Scale(sigma_tot/hPtRec.Integral("width"))
    #print "sigma_tot_dy, deconvoluted", sigma_tot

    #get efficiency
    ana = AnalyzeTree()
    ana.SetMass(mmin, mmax)
    eff = ana.AnalyzeMC(basedir_coh+"/"+infile_coh)
    print "eff: ", eff[0], "+/-", eff[1]

    #denominator in cross section calculation
    den = eff[0]*Reta*br*zdc_acc*trg_eff*bbceff*ratio_tof*lumi_scaled*dy
    den = den*1000. # ub to mb
    print "den:", den

    #calculate the cross section
    sigma_tot = hPt.Integral()/den
    sigma_tot_err = rt.TMath.Sqrt(hPt.Integral())/den
    hPt.Scale(sigma_tot/hPt.Integral("width"))
    print "sigma_tot_dy", sigma_tot, "+/-", sigma_tot_err

    #systematical errors
    err_zdc_acc = 0.1
    err_bemc_eff = 0.03
    sys_err = rt.TMath.Sqrt(err_zdc_acc*err_zdc_acc + err_bemc_eff*err_bemc_eff)
    print "Total sys err:", sys_err
    hSys = ut.prepare_TH1D("hSys", ptbin, ptmin, ptmax)
    hSys.SetOption("E2")
    hSys.SetFillColor(rt.kOrange+1)
    hSys.SetLineColor(rt.kOrange)
    for ibin in xrange(1,hPt.GetNbinsX()+1):
        hSys.SetBinContent(ibin, hPt.GetBinContent(ibin))
        hSys.SetBinError(ibin, hPt.GetBinContent(ibin)*sys_err)
        #print ibin, hPt.GetBinError(ibin)/hPt.GetBinContent(ibin)

    #draw the results
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    #frame for models plot only
    frame = ut.prepare_TH1D("frame", ptbin, ptmin, ptmax)

    can = ut.box_canvas()
    ut.set_margin_lbtr(gPad, 0.1, 0.09, 0.055, 0.03)

    ytit = "d#it{#sigma}/d#it{t}d#it{y} (mb/(GeV/c)^{2})"
    xtit = "|#kern[0.3]{#it{t}}| ((GeV/c)^{2})"
    ut.put_yx_tit(hPt, ytit, xtit, 1.4, 1.2)
    #ut.put_yx_tit(hPtRec, ytit, xtit, 1.4, 1.2)

    hPt.SetMaximum(11)
    #hPt.SetMaximum(80)
    hPt.SetMinimum(0.0002)
    hPt.Draw()

    #hPtRec.SetMaximum(11)
    #hPtRec.SetMinimum(0.0002)
    #hPtRec.Draw()

    #hSys.Draw("e2same")
    #hPt.Draw("e1same")

    ut.put_yx_tit(frame, ytit, xtit, 1.4, 1.2)
    frame.SetMaximum(11)
    frame.SetMinimum(1.e-5)
    #frame.Draw()

    #add Starlight prediction
    gMS.Draw("lsame")
    gCCK.Draw("lsame")
    gSlight.Draw("lsame")
    #gSartre.Draw("lsame")

    gPad.SetLogy()

    cleg = ut.prepare_leg(0.1, 0.96, 0.14, 0.01, 0.035)
    cleg.AddEntry(None, "Au+Au #rightarrow J/#psi + Au+Au + XnXn, #sqrt{#it{s}_{#it{NN}}} = 200 GeV", "")
    cleg.Draw("same")

    leg = ut.prepare_leg(0.2, 0.82, 0.18, 0.1, 0.035)
    leg.AddEntry(None, "#bf{|#kern[0.3]{#it{y}}| < 1}", "")
    leg.AddEntry(hPt, "STAR Preliminary")
    leg.Draw("same")

    #legend about systematic error
    eleg = ut.prepare_leg(0.2, 0.76, 0.18, 0.06, 0.028)
    eleg.AddEntry(None, "10% normalization error", "")
    eleg.AddEntry(None, "not shown", "")
    eleg.Draw("same")

    #legend for models
    mleg = ut.prepare_leg(0.68, 0.75, 0.3, 0.16, 0.035)
    mleg.AddEntry(gSlight, "STARLIGHT", "l")
    mleg.AddEntry(gMS, "MS", "l")
    mleg.AddEntry(gCCK, "CCK-hs", "l")
    #mleg.AddEntry(gSartre, "Sartre", "l")
    mleg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

    #to prevent 'pure virtual method called'
    gPad.Close()

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")






















