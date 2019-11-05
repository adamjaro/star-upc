#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TF1, TGaxis
from ROOT import RooFit as rf
from ROOT import RooRealVar, RooDataSet, RooFormulaVar, RooArgSet, RooArgList
from ROOT import RooDataHist, RooHistPdf, RooAddPdf, RooGenericPdf, RooGaussian

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def fit():

    #fit to log_10(pT^2) with components and plot of plain pT^2

    #range in log_10(pT^2)
    ptbin = 0.12
    ptmin = -5.
    ptmax = 1.01

    #range in pT^2
    ptsq_bin = 0.03
    ptsq_min = 1e-5
    ptsq_max = 1

    mmin = 2.8
    mmax = 3.2

    #range for incoherent fit
    fitran = [-0.9, 0.1]

    #number of gamma-gamma events
    ngg = 131

    #number of psi' events
    npsiP = 20

    #input data
    pT = RooRealVar("jRecPt", "pT", 0, 10)
    m = RooRealVar("jRecM", "mass", 0, 10)
    data_all = RooDataSet("data", "data", tree, RooArgSet(pT, m))
    #select for mass range
    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)
    data = data_all.reduce( strsel )

    #create log(pT^2) from pT
    ptsq_draw = "jRecPt*jRecPt" # will be used for pT^2
    logPtSq_draw = "TMath::Log10("+ptsq_draw+")"
    logPtSq_form = RooFormulaVar("logPtSq", "logPtSq", logPtSq_draw, RooArgList(pT))
    logPtSq = data.addColumn( logPtSq_form )
    logPtSq.setRange("fitran", fitran[0], fitran[1])

    #bins and range for the plot
    nbins, ptmax = ut.get_nbins(ptbin, ptmin, ptmax)
    logPtSq.setMin(ptmin)
    logPtSq.setMax(ptmax)
    logPtSq.setRange("plotran", ptmin, ptmax)

    #range for pT^2
    ptsq_nbins, ptsq_max = ut.get_nbins(ptsq_bin, ptsq_min, ptsq_max)

    #incoherent parametrization
    bval = RooRealVar("bval", "bval", 3.3, 0, 10)
    inc_form = "log(10.)*pow(10.,logPtSq)*exp(-bval*pow(10.,logPtSq))"
    incpdf = RooGenericPdf("incpdf", inc_form, RooArgList(logPtSq, bval))

    #make the incoherent fit
    res = incpdf.fitTo(data, rf.Range("fitran"), rf.Save())

    #get incoherent norm to the number of events
    lset = RooArgSet(logPtSq)
    iinc = incpdf.createIntegral(lset, rf.NormSet(lset), rf.Range("fitran"))
    inc_nevt = data.sumEntries("logPtSq", "fitran")
    incpdf.setNormRange("fitran")
    aval = RooRealVar("aval", "aval", inc_nevt/incpdf.getNorm(lset))
    #print "A =", aval.getVal()
    #print "b =", bval.getVal()

    #gamma-gamma contribution
    hGG = ut.prepare_TH1D_n("hGG", nbins, ptmin, ptmax)
    tree_gg.Draw( logPtSq_draw+" >> hGG", strsel )
    ut.norm_to_num(hGG, ngg, rt.kGreen)

    #gamma-gamma in pT^2
    hGG_ptsq = ut.prepare_TH1D_n("hGG_ptsq", ptsq_nbins, ptsq_min, ptsq_max)
    tree_gg.Draw( ptsq_draw+" >> hGG_ptsq", strsel )
    ut.norm_to_num(hGG_ptsq, ngg, rt.kGreen)

    #psi' contribution
    psiP_file = TFile.Open(basedir_mc+"/ana_slight14e4x1_s6_sel5z.root")
    psiP_tree = psiP_file.Get("jRecTree")
    hPsiP = ut.prepare_TH1D_n("hPsiP", nbins, ptmin, ptmax)
    psiP_tree.Draw(logPtSq_draw+" >> hPsiP", strsel)
    ut.norm_to_num(hPsiP, npsiP, rt.kViolet)

    #psi' in pT^2
    hPsiP_ptsq = ut.prepare_TH1D_n("hPsiP_ptsq", ptsq_nbins, ptsq_min, ptsq_max)
    psiP_tree.Draw(ptsq_draw+" >> hPsiP_ptsq", strsel)
    ut.norm_to_num(hPsiP_ptsq, npsiP, rt.kViolet)

    #create canvas frame
    gStyle.SetPadTickY(1)
    can = ut.box_canvas(1086, 543) # square area is still 768^2
    can.SetMargin(0, 0, 0, 0)
    can.Divide(2, 1, 0, 0)
    gStyle.SetLineWidth(1)

    can.cd(1)
    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.01, 0)

    frame = logPtSq.frame(rf.Bins(nbins))
    frame.SetTitle("")
    frame.SetMaximum(75)

    frame.SetYTitle("Events / ({0:.3f}".format(ptbin)+" GeV^{2})")
    frame.SetXTitle("log_{10}( #it{p}_{T}^{2} ) (GeV^{2})")

    frame.GetXaxis().SetTitleOffset(1.2)
    frame.GetYaxis().SetTitleOffset(1.6)

    #plot the data
    data.plotOn(frame, rf.Name("data"), rf.LineWidth(2))

    #incoherent parametrization
    incpdf.plotOn(frame, rf.Range("fitran"), rf.LineColor(rt.kRed), rf.Name("incpdf"), rf.LineWidth(2))
    incpdf.plotOn(frame, rf.Range("plotran"), rf.LineColor(rt.kRed), rf.Name("incpdf_full"), rf.LineStyle(rt.kDashed), rf.LineWidth(2))

    frame.Draw()

    #add gamma-gamma contribution
    hGG.Draw("same")

    #add psi'
    #hPsiP.Draw("same")

    #plot pT^2 on the right

    #pT^2 variable from pT
    ptsq_form = RooFormulaVar("ptsq", "ptsq", ptsq_draw, RooArgList(pT))
    ptsq = data.addColumn( ptsq_form )

    #range for pT^2 plot
    ptsq.setMin(ptsq_min)
    ptsq.setMax(ptsq_max)

    #make the pT^2 plot
    can.cd(2)
    gPad.SetLogy()
    #gPad.SetLineWidth(3)
    #gPad.SetFrameLineWidth(1)
    ut.set_margin_lbtr(gPad, 0, 0.1, 0.01, 0.15)

    ptsq_frame = ptsq.frame(rf.Bins(ptsq_nbins), rf.Title(""))

    ptsq_frame.SetTitle("")

    ptsq_frame.SetXTitle("#it{p}_{T}^{2} (GeV^{2})")
    ptsq_frame.GetXaxis().SetTitleOffset(1.2)

    data.plotOn(ptsq_frame, rf.Name("data"), rf.LineWidth(2))

    ptsq_frame.SetMaximum(600)
    ptsq_frame.SetMinimum(0.8) # 0.101

    ptsq_frame.Draw()

    #incoherent parametrization in pT^2, scaled to the plot
    inc_ptsq = TF1("inc_ptsq", "[0]*exp(-[1]*x)", 0., 10.)
    inc_ptsq.SetParameters(aval.getVal()*ptsq_bin, bval.getVal())

    inc_ptsq.Draw("same")

    #add gamma-gamma in pT^2
    hGG_ptsq.Draw("same")

    #add psi' in pT^2
    #hPsiP_ptsq.Draw("same")

    #redraw the frame
    #ptsq_frame.Draw("same")

    #vertical axis for pT^2 plot
    xpos = ptsq_frame.GetXaxis().GetXmax()
    ypos = ptsq_frame.GetMaximum()
    ymin = ptsq_frame.GetMinimum()

    ptsq_axis = TGaxis(xpos, 0, xpos, ypos, ymin, ypos, 510, "+GL")
    ut.set_axis(ptsq_axis)
    ptsq_axis.SetMoreLogLabels()

    ptsq_axis.SetTitle("Events / ({0:.3f}".format(ptsq_bin)+" GeV^{2})")
    ptsq_axis.SetTitleOffset(2.2)

    ptsq_axis.Draw()

    ut.invert_col_can(can)
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































