#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TF1
from ROOT import RooFit as rf
from ROOT import RooRealVar, RooDataSet, RooFormulaVar, RooArgSet, RooArgList
from ROOT import RooDataHist, RooHistPdf, RooAddPdf, RooGenericPdf, RooGaussian

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def fit():

    #fit to log_10(pT^2) with components

    ptbin = 0.12
    ptmin = -5.
    ptmax = 1.

    mmin = 2.8
    mmax = 3.2

    #input data
    pT = RooRealVar("jRecPt", "pT", 0, 10)
    m = RooRealVar("jRecM", "mass", 0, 10)
    data_all = RooDataSet("data", "data", tree, RooArgSet(pT, m))
    #select for mass range
    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)
    data = data_all.reduce( strsel )

    #create log(pT^2) from pT
    logPtSq_draw = "TMath::Log10(jRecPt*jRecPt)"
    logPtSq_form = RooFormulaVar("logPtSq", "logPtSq", logPtSq_draw, RooArgList(pT))
    logPtSq = data.addColumn( logPtSq_form )

    #bins and range for the plot
    nbins, ptmax = ut.get_nbins(ptbin, ptmin, ptmax)
    logPtSq.setMin(ptmin)
    logPtSq.setMax(ptmax)

    #gamma-gamma -> e+e- hist pdf
    hGG = ut.prepare_TH1D("hGG", ptbin, ptmin, ptmax)
    tree_gg.Draw( logPtSq_draw+" >> hGG", strsel )
    dhGG = RooDataHist("dhGG", "dhGG", RooArgList(logPtSq), hGG)
    ggpdf = RooHistPdf("ggpdf", "ggpdf", RooArgSet(logPtSq), dhGG, 0)
    ngg = RooRealVar("ngg", "ngg", 130, 0, 1e4)
    ngg.setVal(131)
    ngg.setConstant()

    #incoherent parametrization
    bval = RooRealVar("bval", "bval", 3.3, 0, 10)
    #bval.setVal(3.3)
    bval.setConstant()
    inc_form = "log(10.)*pow(10.,logPtSq)*exp(-bval*pow(10.,logPtSq))"
    incpdf = RooGenericPdf("incpdf", inc_form, RooArgList(logPtSq, bval))
    ninc = RooRealVar("ninc", "ninc", 100, 0, 1e4)

    #signal ansatz
    sig1_mean = RooRealVar("sig1_mean", "sig1_mean", -2.3, -5, 1)
    sig1_mean.setConstant()
    sig1_sig = RooRealVar("sig1_sig", "sig1_sig", 0.4, 0, 5)
    sig1_sig.setConstant()
    sig1_pdf = RooGaussian("sig1_pdf", "sig1_pdf", logPtSq, sig1_mean, sig1_sig)
    nsig1 = RooRealVar("nsig1", "nsig1", 100, 0, 1e4)

    sig2_mean = RooRealVar("sig2_mean", "sig2_mean", -1.5, -5, 1)
    #sig2_mean.setConstant()
    sig2_sig = RooRealVar("sig2_sig", "sig2_sig", 0.2, 0, 5)
    sig2_sig.setConstant()
    sig2_pdf = RooGaussian("sig2_pdf", "sig2_pdf", logPtSq, sig2_mean, sig2_sig)
    nsig2 = RooRealVar("nsig2", "nsig2", 50, 0, 1e4)


    #fit model
    model = RooAddPdf("model", "model", RooArgList(ggpdf, incpdf, sig1_pdf, sig2_pdf), RooArgList(ngg, ninc, nsig1, nsig2))

    #make the fit
    res = model.fitTo(data, rf.Save())

    #create canvas frame
    can = ut.box_canvas()
    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.01, 0.01)

    frame = logPtSq.frame(rf.Bins(nbins), rf.Title(""))
    frame.SetTitle("")
    frame.SetMaximum(75)

    frame.SetYTitle("Events / ({0:.3f}".format(ptbin)+" GeV^{2})")
    frame.SetXTitle("log_{10}( #it{p}_{T}^{2} ) (GeV^{2})")

    frame.GetXaxis().SetTitleOffset(1.2)
    frame.GetYaxis().SetTitleOffset(1.6)

    #plot the data
    data.plotOn(frame, rf.Name("data"))

    #plot the model
    model.plotOn(frame, rf.Name("model"), rf.LineColor(rt.kOrange-3))

    model.plotOn(frame, rf.Name("gg"), rf.Components("ggpdf"), rf.LineColor(rt.kGreen))
    model.plotOn(frame, rf.Name("inc"), rf.Components("incpdf"), rf.LineColor(rt.kRed))
    model.plotOn(frame, rf.Name("sig1"), rf.Components("sig1_pdf"), rf.LineColor(rt.kBlue))
    model.plotOn(frame, rf.Name("sig2"), rf.Components("sig2_pdf"), rf.LineColor(rt.kBlue))

    frame.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")


#_____________________________________________________________________________
def plot():

    #plot of log_10(pT^2) with components

    ptbin = 0.12
    ptmin = -5.
    ptmax = 1.

    mmin = 2.8  #  2.8   2.4 for ls
    mmax = 3.2

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)
    strsel_ls = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(2.3, mmax)

    can = ut.box_canvas()

    hPt = ut.prepare_TH1D("hPt", ptbin, ptmin, ptmax)
    hPtLS = ut.prepare_TH1D("hPtLS", ptbin, ptmin, ptmax)
    hPtGG = ut.prepare_TH1D("hPtGG", ptbin, ptmin, ptmax)
    hPtInc = ut.prepare_TH1D("hPtInc", ptbin, ptmin, ptmax)

    ut.put_yx_tit(hPt, "Events / ({0:.3f}".format(ptbin)+" GeV^{2})", "log_{10}( #it{p}_{T}^{2} ) (GeV^{2})")
    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.01, 0.01)

    #data
    draw = "TMath::Log10(jRecPt*jRecPt)"
    tree.Draw(draw + " >> hPt", strsel)

    #like-sign data
    tree_ls.Draw(draw + " >> hPtLS", strsel_ls)
    ut.set_H1D_col(hPtLS, rt.kRed)
    print hPtLS.GetEntries()

    #gamma-gamma
    tree_gg.Draw(draw + " >> hPtGG", strsel)
    ut.norm_to_num(hPtGG, 131., rt.kGreen)

    #incoherent contribution
    tree_inc.Draw(draw + " >> hPtInc", strsel)
    ut.norm_to_num(hPtInc, 270., rt.kRed) # 270  100

    #psi' contribution
    psiP = TFile.Open(basedir_mc+"/ana_slight14e4x1_s6_sel5z.root")
    psiP_tree = psiP.Get("jRecTree")
    hPtPsiP = ut.prepare_TH1D("hPtPsiP", ptbin, ptmin, ptmax)
    psiP_tree.Draw(draw + " >> hPtPsiP", strsel)
    ut.norm_to_num(hPtPsiP, 30, rt.kViolet)

    #incoherent parametrization
    func_incoh_logPt2 = TF1("func_incoh_logPt2", "[0]*log(10.)*pow(10.,x)*exp(-[1]*pow(10.,x))", -10., 10.)
    func_incoh_logPt2.SetParName(0, "A")
    func_incoh_logPt2.SetParName(1, "b")
    func_incoh_logPt2.SetNpx(1000)
    func_incoh_logPt2.SetLineColor(rt.kRed)
    func_incoh_logPt2.SetParameters(80, 3) # 4.9 from incoherent mc, 3.3 from data fit

    #signal empirical shape
    sig1 = TF1("sig1", "gaus", -10, 10)
    sig1.SetParameters(40, -2.3, 0.4) # const, mean, sigma
    sig2 = TF1("sig2", "gaus", -10, 10)
    sig2.SetParameters(35, -1.35, 0.2)

    #add like-sign to incoherent MC
    #hPtInc.Add(hPtLS)

    #subtract the individual components
    hPt.Add(hPtGG, -1)
    hPt.Add(sig1, -1)
    hPt.Add(sig2, -1)
    hPt.Add(hPtPsiP, -1)
    hPt.Add(func_incoh_logPt2, -1)

    hPt.Draw()
    #hPtLS.Draw("same")
    #hPtGG.Draw("same")
    #func_incoh_logPt2.Draw("same")
    #hPtPsiP.Draw("same")
    #hPtInc.Draw("same")

    #sig1.Draw("same")
    #sig2.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")


#_____________________________________________________________________________
if __name__ == "__main__":

    #data
    basedir = "../../../star-upc-data/ana/muDst/muDst_run1/sel5"
    infile = "ana_muDst_run1_all_sel5z.root"
    infile_ls = "ana_muDst_run1_all_sel5z_ls.root"

    #MC
    basedir_mc = "../../../star-upc-data/ana/starsim/slight14e/sel5"
    infile_gg = "ana_slight14e2x1_sel5_nzvtx.root"
    infile_incoh = "ana_slight14e3_sel5z.root"

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    iplot = 1
    funclist = []
    funclist.append(plot) # 0
    funclist.append(fit) # 0

    #open the inputs
    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("jRecTree")

    inp_ls = TFile.Open(basedir+"/"+infile_ls)
    tree_ls = inp_ls.Get("jRecTree")

    inp_gg = TFile.Open(basedir_mc+"/"+infile_gg)
    tree_gg = inp_gg.Get("jRecTree")

    inp_inc = TFile.Open(basedir_mc+"/"+infile_incoh)
    tree_inc = inp_inc.Get("jRecTree")

    #call the plot function
    funclist[iplot]()

    #to prevent 'pure virtual method called'
    #gPad.Close()

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")































