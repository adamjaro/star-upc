#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TGraphErrors, TF1

import sys
sys.path.append('../')
import plot_utils as ut

from analyze_tree import AnalyzeTree

#_____________________________________________________________________________
def load_starlight():

    #slight = TFile.Open("/home/jaroslav/sim/starlight_data/slight_Jpsi_PbPb_coh.root")
    slight = TFile.Open("/home/jaroslav/sim/starlight_tx/slight_AuAu_200GeV_Jpsi_coh_6Mevt.root")
    slight_tree = slight.Get("slight_tree")

    #hSlight = ut.prepare_TH1D("hSlight", 0.3, -5., 5.)
    #frame = ut.prepare_TH1D("frame", 0.1, -5., 5.)
    hSlight = ut.prepare_TH1D("hSlight", 0.002, 0., 0.12)
    #frame = ut.prepare_TH1D("frame", 0.002, 0., 0.12)

    #slight_tree.Draw("rapidity >> hSlight")
    #ut.norm_to_integral(hSlight, 23.16)
    #slight_tree.Draw("pT*pT >> hSlight")
    nall = float( slight_tree.GetEntries() )
    ny = float( slight_tree.Draw("pT*pT >> hSlight", "rapidity>-1 && rapidity<1") )
    sigma_sl_tot = 67.958 # total Starlight cross section, ub
    sigma_sl = (ny/nall)*sigma_sl_tot/1000. # ub to mb
    #sigma_sl = sigma_sl/2. # rapidity interval
    print "sigma_sl:", sigma_sl
    ut.norm_to_integral(hSlight, sigma_sl)

    gSlight = TGraphErrors(hSlight.GetNbinsX())
    for ibin in xrange(1,hSlight.GetNbinsX()+1):
        gSlight.SetPoint(ibin-1, hSlight.GetBinCenter(ibin), hSlight.GetBinContent(ibin))

    gSlight.SetLineColor(rt.kBlue)
    #gSlight.SetLineStyle(lstyle)
    gSlight.SetLineWidth(3)

    #hSlight.SetMaximum(7.5)
    #frame.SetMaximum(7.5)
    #frame.SetMaximum(20)

    #can = ut.box_canvas()
    #hSlight.Draw()

    #gPad.SetLogy()

    #frame.Draw()
    #gSlight.Draw("cx")
    #ut.invert_col(rt.gPad)
    #can.SaveAs("01fig.pdf")

    return gSlight

#end of load_starlight

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()

    #range and binning
    ptbin = 0.005
    ptmin = 0.
    ptmax = 0.12

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
    basedir_mc = "../../../star-upc-data/ana/starsim/slight14e/sel5"
    infile_coh = "ana_slight14e1x1_sel5z.root"
    infile_gg = "ana_slight14e2x1_sel5_nzvtx.root"

    #predictions
    gSlight = load_starlight()

    #open the inputs
    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("jRecTree")
    inp_gg = TFile.Open(basedir_mc+"/"+infile_gg)
    tree_gg = inp_gg.Get("jRecTree")

    #data and gamma-gamma histograms
    hPt = ut.prepare_TH1D("hPt", ptbin, ptmin, ptmax)
    hPtGG = ut.prepare_TH1D("hPtGG", ptbin, ptmin, ptmax)

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    tree.Draw("jRecPt*jRecPt >> hPt" , strsel)
    tree_gg.Draw("jRecPt*jRecPt >> hPtGG", strsel)

    #incoherent functional shape
    func_incoh_pt2 = TF1("func_incoh", "[0]*exp(-[1]*x)", 0., 10.)
    func_incoh_pt2.SetParameters(873.04, 3.28)

    #fill incoherent histogram from functional shape
    hPtIncoh = ut.prepare_TH1D("hPtIncoh", ptbin, ptmin, ptmax)
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

    #get efficiency
    ana = AnalyzeTree()
    ana.SetMass(mmin, mmax)
    eff = ana.AnalyzeMC(basedir_mc+"/"+infile_coh)
    print "eff: ", eff[0], "+/-", eff[1]

    #denominator in cross section calculation
    den = eff[0]*Reta*br*zdc_acc*trg_eff*bbceff*ratio_tof*lumi_scaled
    den = den*1000. # ub to mb
    print "den:", den

    #calculate the cross section
    sigma_tot = hPt.Integral()/den
    sigma_tot_err = rt.TMath.Sqrt(hPt.Integral())/den
    hPt.Scale(sigma_tot/hPt.Integral("width"))
    print "sigma_tot_dy", sigma_tot/dy, "+/-", sigma_tot_err/dy

    #systematical errors
    err_zdc_acc = 0.1
    err_bemc_eff = 0.03
    sys_err = rt.TMath.Sqrt(err_zdc_acc*err_zdc_acc + err_bemc_eff*err_bemc_eff)
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

    can = ut.box_canvas()
    ut.set_margin_lbtr(gPad, 0.1, 0.09, 0.055, 0.03)

    ytit = "d#it{#sigma}/d#it{t} (mb/GeV^{2})"
    ut.put_yx_tit(hPt, ytit, "|#kern[0.3]{#it{t}}| (GeV^{2})", 1.4, 1.2)

    hPt.SetMaximum(11)
    hPt.Draw()

    hSys.Draw("e2same")
    hPt.Draw("e1same")

    #add Starlight prediction
    gSlight.Draw("lsame")

    gPad.SetLogy()

    cleg = ut.prepare_leg(0.1, 0.96, 0.14, 0.01, 0.035)
    cleg.AddEntry(None, "Au+Au #rightarrow J/#psi + Au+Au + XnXn, #sqrt{#it{s}_{#it{NN}}} = 200 GeV", "")
    cleg.Draw("same")

    leg = ut.prepare_leg(0.65, 0.75, 0.18, 0.16, 0.035)
    leg.AddEntry(None, "#bf{|#kern[0.3]{#it{y}}| < 1}", "")
    leg.AddEntry(hPt, "STAR Preliminary")
    leg.AddEntry(gSlight, "Starlight", "l")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

    #to prevent 'pure virtual method called'
    gPad.Close()

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")






















