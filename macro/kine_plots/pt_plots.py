#!/usr/bin/python

import math

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TF1, TH1D, TGraphAsymmErrors
from ROOT import RooRealVar, RooDataSet, RooArgSet, RooDataHist, RooArgList, RooGenericPdf
from ROOT import RooFormulaVar, TGaxis, TMath
from ROOT import RooFit as rf

import sys
sys.path.append('../')
import plot_utils as ut
from parameter_descriptor import parameter_descriptor as pdesc

#_____________________________________________________________________________
def plot_pt_gg():

    #pT of gamma-gamma below and above J/psi

    ptbin = 0.02
    #ptbin = 0.03
    ptmin = 0.
    ptmax = 1.1

    mmin = 2.1
    mmax = 2.6
    #mmin = 3.4
    #mmax = 5.

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    can = ut.box_canvas()

    hPt = ut.prepare_TH1D("hPt", ptbin, ptmin, ptmax)
    hPtGG = ut.prepare_TH1D("hPtGG", ptbin, ptmin, ptmax)

    #ut.put_yx_tit(hPt, "Events / ({0:.3f}".format(ptbin)+" GeV)", "#it{p}_{T} (GeV})")
    ytit = "#gamma#gamma#rightarrow e^{+}e^{-} candidates / "+"({0:.3f}".format(ptbin)+" GeV)"
    ut.put_yx_tit(hPt, ytit, "Dielectron #it{p}_{T} (GeV)", 1.5, 1.2)

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.01, 0.02)

    draw = "jRecPt"

    tree.Draw(draw + " >> hPt", strsel)
    tree_gg.Draw(draw + " >> hPtGG", strsel)
    ut.norm_to_data(hPtGG, hPt, rt.kGreen, 0., 0.3)
    #ut.norm_to_data(hPtGG, hPt, rt.kGreen, 0., 0.18)

    hPt.Draw()
    hPtGG.Draw("same")

    leg = ut.prepare_leg(0.67, 0.78, 0.14, 0.18, 0.03)
    leg.AddEntry(None, "#bf{|#kern[0.3]{#it{y}}| < 1}", "")
    ut.add_leg_mass(leg, mmin, mmax)
    leg.AddEntry(hPt, "Data")
    leg.AddEntry(hPtGG, "#gamma#gamma#rightarrow e^{+}e^{-}", "l")
    leg.Draw("same")

    pleg = ut.prepare_leg(0.33, 0.8, 0.01, 0.14, 0.035)
    pleg.AddEntry(None, "STAR Preliminary", "")
    pleg.AddEntry(None, "AuAu@200 GeV", "")
    pleg.AddEntry(None, "UPC sample", "")
    pleg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_pt_gg

#_____________________________________________________________________________
def pdf_logPt2_prelim():

    #PDF fit to log_10(pT^2) for preliminary figure

    #tree_in = tree_incoh
    tree_in = tree

    #ptbin = 0.04
    ptbin = 0.12
    ptmin = -5.
    ptmax = 1.

    mmin = 2.8
    mmax = 3.2

    #fitran = [-5., 1.]
    fitran = [-0.9, 0.1]

    binned = False

    #gamma-gamma 131 evt for pT<0.18

    #input data
    pT = RooRealVar("jRecPt", "pT", 0, 10)
    m = RooRealVar("jRecM", "mass", 0, 10)
    dataIN = RooDataSet("data", "data", tree_in, RooArgSet(pT, m))
    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)
    data = dataIN.reduce(strsel)
    #x is RooRealVar for log(Pt2)
    draw = "TMath::Log10(jRecPt*jRecPt)"
    draw_func = RooFormulaVar("x", "Dielectron log_{10}( #it{p}_{T}^{2} ) ((GeV/c)^{2})", draw, RooArgList(pT))
    x = data.addColumn(draw_func)
    x.setRange("fitran", fitran[0], fitran[1])

    #binned data
    nbins, ptmax = ut.get_nbins(ptbin, ptmin, ptmax)
    hPt = TH1D("hPt", "hPt", nbins, ptmin, ptmax)
    hPtCoh = ut.prepare_TH1D("hPtCoh", ptbin, ptmin, ptmax)
    hPtCoh.SetLineWidth(2)
    #fill in binned data
    tree_in.Draw(draw + " >> hPt", strsel)
    tree_coh.Draw(draw + " >> hPtCoh", strsel)
    dataH = RooDataHist("dataH", "dataH", RooArgList(x), hPt)

    #range for plot
    x.setMin(ptmin)
    x.setMax(ptmax)
    x.setRange("plotran", ptmin, ptmax)

    #create the pdf
    b = RooRealVar("b", "b", 5., 0., 10.)
    pdf_func = "log(10.)*pow(10.,x)*exp(-b*pow(10.,x))"
    pdf_logPt2 = RooGenericPdf("pdf_logPt2", pdf_func, RooArgList(x, b))

    #make the fit
    if binned == True:
        r1 = pdf_logPt2.fitTo(dataH, rf.Range("fitran"), rf.Save())
    else:
        r1 = pdf_logPt2.fitTo(data, rf.Range("fitran"), rf.Save())

    #calculate norm to number of events
    xset = RooArgSet(x)
    ipdf = pdf_logPt2.createIntegral(xset, rf.NormSet(xset), rf.Range("fitran"))
    print "PDF integral:", ipdf.getVal()
    if binned == True:
        nevt = tree_incoh.Draw("", strsel+" && "+draw+">{0:.3f}".format(fitran[0])+" && "+draw+"<{1:.3f}".format(fitran[0], fitran[1]))
    else:
        nevt = data.sumEntries("x", "fitran")

    print "nevt:", nevt
    pdf_logPt2.setNormRange("fitran")
    print "PDF norm:", pdf_logPt2.getNorm(RooArgSet(x))

    #a = nevt/ipdf.getVal()
    a = nevt/pdf_logPt2.getNorm(RooArgSet(x))
    print "a =", a

    #gamma-gamma contribution
    hPtGG = ut.prepare_TH1D("hPtGG", ptbin, ptmin, ptmax)
    tree_gg.Draw(draw + " >> hPtGG", strsel)
    #ut.norm_to_data(hPtGG, hPt, rt.kGreen, -5., -2.9)
    ut.norm_to_num(hPtGG, 131., rt.kGreen+1)

    print "Int GG:", hPtGG.Integral()

    #sum of all contributions
    hSum = ut.prepare_TH1D("hSum", ptbin, ptmin, ptmax)
    hSum.SetLineWidth(3)
    #add ggel to the sum
    hSum.Add(hPtGG)
    #add incoherent contribution
    func_logPt2 = TF1("pdf_logPt2", "[0]*log(10.)*pow(10.,x)*exp(-[1]*pow(10.,x))", -10., 10.)
    func_logPt2.SetParameters(a, b.getVal())
    hInc = ut.prepare_TH1D("hInc", ptbin, ptmin, ptmax)
    ut.fill_h1_tf(hInc, func_logPt2)
    hSum.Add(hInc)
    #add coherent contribution
    ut.norm_to_data(hPtCoh, hPt, rt.kBlue, -5., -2.2) # norm for coh
    hSum.Add(hPtCoh)
    #set to draw as a lines
    ut.line_h1(hSum, rt.kBlack)

    #create canvas frame
    can = ut.box_canvas()
    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.01, 0.01)

    frame = x.frame(rf.Bins(nbins), rf.Title(""))
    frame.SetTitle("")

    frame.SetYTitle("J/#psi candidates / ({0:.3f}".format(ptbin)+" (GeV/c)^{2})")

    frame.GetXaxis().SetTitleOffset(1.2)
    frame.GetYaxis().SetTitleOffset(1.6)

    print "Int data:", hPt.Integral()

    #plot the data
    if binned == True:
        dataH.plotOn(frame, rf.Name("data"))
    else:
        data.plotOn(frame, rf.Name("data"))

    pdf_logPt2.plotOn(frame, rf.Range("fitran"), rf.LineColor(rt.kRed), rf.Name("pdf_logPt2"))
    pdf_logPt2.plotOn(frame, rf.Range("plotran"), rf.LineColor(rt.kRed), rf.Name("pdf_logPt2_full"), rf.LineStyle(rt.kDashed))

    frame.Draw()

    leg = ut.prepare_leg(0.61, 0.77, 0.16, 0.19, 0.03)
    #ut.add_leg_mass(leg, mmin, mmax)
    hx = ut.prepare_TH1D("hx", 1, 0, 1)
    hx.Draw("same")
    ln = ut.col_lin(rt.kRed, 2)
    leg.AddEntry(hx, "Data", "p")
    leg.AddEntry(hSum, "Sum", "l")
    leg.AddEntry(hPtCoh, "Coherent J/#psi", "l")
    leg.AddEntry(ln, "Incoherent parametrization", "l")
    leg.AddEntry(hPtGG, "#gamma#gamma#rightarrow e^{+}e^{-}", "l")
    #leg.AddEntry(ln, "ln(10)*#it{A}*10^{log_{10}#it{p}_{T}^{2}}exp(-#it{b}10^{log_{10}#it{p}_{T}^{2}})", "l")
    leg.Draw("same")

    l0 = ut.cut_line(fitran[0], 0.9, frame)
    l1 = ut.cut_line(fitran[1], 0.9, frame)
    #l0.Draw()
    #l1.Draw()

    pleg = ut.prepare_leg(0.12, 0.75, 0.14, 0.22, 0.03)
    pleg.AddEntry(None, "#bf{|#kern[0.3]{#it{y}}| < 1}", "")
    ut.add_leg_mass(pleg, mmin, mmax)
    pleg.AddEntry(None, "STAR Preliminary", "")
    pleg.AddEntry(None, "AuAu@200 GeV", "")
    pleg.AddEntry(None, "UPC sample", "")
    pleg.Draw("same")

    desc = pdesc(frame, 0.14, 0.9, 0.057)
    desc.set_text_size(0.03)
    desc.itemD("#chi^{2}/ndf", frame.chiSquare("pdf_logPt2", "data", 2), -1, rt.kRed)
    desc.itemD("#it{A}", a, -1, rt.kRed)
    desc.itemR("#it{b}", b, rt.kRed)
    #desc.draw()

    #put the sum
    hSum.Draw("same")

    frame.Draw("same")

    #put gamma-gamma and coherent J/psi
    hPtGG.Draw("same")
    hPtCoh.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of pdf_logPt2_prelim

#_____________________________________________________________________________
def make_eff_pt2():

    #efficiency vs. pT^2

    ptbin = 0.005
    ptmin = 0.
    ptmax = 0.12   # 0.3

    mmin = 2.8
    mmax = 3.2

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    can = ut.box_canvas()

    nbins, ptmax = ut.get_nbins(ptbin, ptmin, ptmax)
    hPtRec = TH1D("hPtRec", "hPtRec", nbins, ptmin, ptmax)
    hPtGen = TH1D("hPtGen", "hPtGen", nbins, ptmin, ptmax)
    #hPtRec = ut.prepare_TH1D("hPtRec", ptbin, ptmin, ptmax)
    #hPtGen = ut.prepare_TH1D("hPtGen", ptbin, ptmin, ptmax)

    hPtRec.Sumw2()
    hPtGen.Sumw2()

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.01, 0.02)

    #generated trees
    tree_coh_gen = inp_coh.Get("jGenTree")
    tree_incoh_gen = inp_incoh.Get("jGenTree")

    tree_coh.Draw("jGenPt*jGenPt >> hPtRec", strsel)
    tree_coh_gen.Draw("jGenPt*jGenPt >> hPtGen")

    #tree_incoh.Draw("jGenPt*jGenPt >>+ hPtRec", strsel)
    #tree_incoh_gen.Draw("jGenPt*jGenPt >>+ hPtGen")

    #tree_incoh.Draw("jGenPt*jGenPt >> hPtRec", strsel)
    #tree_incoh_gen.Draw("jGenPt*jGenPt >> hPtGen")

    #calculate the efficiency
    hEff = TGraphAsymmErrors(hPtRec, hPtGen)

    #hPtRec.Divide(hPtGen)

    #hPtRec.Draw()
    #hPtGen.Draw("same")
    hEff.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

# end of make_eff_pt2

#_____________________________________________________________________________
def subtract_pt2():

    #pT^2 with subtracted incoherent and gamma-gamma components

    ptbin = 0.005
    ptmin = 0.
    ptmax = 0.12   # 0.3

    mmin = 2.8
    mmax = 3.2

    ngg = 131  # number of gamma-gamma from mass fit

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    can = ut.box_canvas()

    hPt = ut.prepare_TH1D("hPt", ptbin, ptmin, ptmax)
    hPtCoh = ut.prepare_TH1D("hPtCoh", ptbin, ptmin, ptmax)
    hPtIncoh = ut.prepare_TH1D("hPtIncoh", ptbin, ptmin, ptmax)
    hPtGG = ut.prepare_TH1D("hPtGG", ptbin, ptmin, ptmax)

    ut.put_yx_tit(hPt, "Events / ({0:.3f}".format(ptbin)+" GeV^{2})", "#it{p}_{T}^{2} (GeV^{2})")

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.01, 0.02)

    draw = "jRecPt*jRecPt"

    tree.Draw(draw + " >> hPt", strsel)
    tree_coh.Draw(draw + " >> hPtCoh", strsel)
    tree_gg.Draw(draw + " >> hPtGG", strsel)

    #incoherent functional shape
    func_incoh_pt2 = TF1("func_incoh", "[0]*exp(-[1]*x)", 0., 10.)
    func_incoh_pt2.SetParameters(873.04, 3.28)

    #fill incoherent histogram from functional shape
    ut.fill_h1_tf(hPtIncoh, func_incoh_pt2, rt.kRed)

    #normalize gamma-gamma component
    ut.norm_to_num(hPtGG, ngg, rt.kGreen)

    #subtract gamma-gamma and incoherent components
    hPt.Sumw2()
    hPt.Add(hPtGG, -1)
    hPt.Add(hPtIncoh, -1)

    #normalize coherent MC to a custom range
    ut.norm_to_data(hPtCoh, hPt, rt.kBlue, 0., 0.015)

    hPt.SetMinimum(1)

    hPt.Draw()
    hPtCoh.Draw("same")
    #hPtIncoh.Draw("same")
    #hPtGG.Draw("same")

    leg = ut.prepare_leg(0.67, 0.78, 0.14, 0.18, 0.03)
    ut.add_leg_mass(leg, mmin, mmax)
    leg.AddEntry(hPt, "Data")
    leg.AddEntry(hPtCoh, "Coherent MC", "l")
    #leg.AddEntry(hPtIncoh, "Incoherent MC", "l")
    #leg.AddEntry(hPtGG, "#gamma#gamma#rightarrow e^{+}e^{-} MC", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hPt, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of subtract_pt2

#_____________________________________________________________________________
def plot_pt2_real():

    #pT^2 with realistic normalization for incoherent and gamma-gamma components

    ptbin = 0.002
    ptmin = 0.
    ptmax = 0.2   # 0.3

    mmin = 2.8
    mmax = 3.2

    ngg = 131  # number of gamma-gamma from mass fit

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    can = ut.box_canvas()

    hPt = ut.prepare_TH1D("hPt", ptbin, ptmin, ptmax)
    hPtCoh = ut.prepare_TH1D("hPtCoh", ptbin, ptmin, ptmax)
    hPtIncoh = ut.prepare_TH1D("hPtIncoh", ptbin, ptmin, ptmax)
    hPtGG = ut.prepare_TH1D("hPtGG", ptbin, ptmin, ptmax)

    ut.put_yx_tit(hPt, "Events / ({0:.3f}".format(ptbin)+" GeV^{2})", "#it{p}_{T}^{2} (GeV^{2})")

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.01, 0.02)

    draw = "jRecPt*jRecPt"

    tree.Draw(draw + " >> hPt", strsel)
    tree_coh.Draw(draw + " >> hPtCoh", strsel)
    tree_gg.Draw(draw + " >> hPtGG", strsel)

    #incoherent functional shape
    func_incoh_pt2 = TF1("func_incoh", "[0]*exp(-[1]*x)", 0., 10.)
    func_incoh_pt2.SetParameters(873.04, 3.28)

    #fill incoherent histogram from functional shape
    ut.fill_h1_tf(hPtIncoh, func_incoh_pt2, rt.kRed)

    ut.norm_to_data(hPtCoh, hPt, rt.kBlue, 0., 0.015)
    ut.norm_to_num(hPtGG, ngg, rt.kGreen)

    hPt.Draw()
    hPtCoh.Draw("same")
    hPtIncoh.Draw("same")
    hPtGG.Draw("same")

    leg = ut.prepare_leg(0.6, 0.78, 0.14, 0.18, 0.03)
    ut.add_leg_mass(leg, mmin, mmax)
    leg.AddEntry(hPt, "Data")
    leg.AddEntry(hPtCoh, "Coherent MC, Sartre", "l")
    leg.AddEntry(hPtIncoh, "Incoherent parametrization", "l")
    leg.AddEntry(hPtGG, "#gamma#gamma#rightarrow e^{+}e^{-} MC", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hPt, 0.14, 0.9, 0.01, 0.1)
    #uoleg.Draw("same")

    gPad.SetLogy()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_pt2_real

#_____________________________________________________________________________
def subtract_pt2_incoh():

    #subtract functional shape from pT^2 incoherent MC

    ptbin = 0.008
    ptmin = 0.
    ptmax = 1.

    mmin = 2.8
    mmax = 3.2

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    can = ut.box_canvas()

    hPt = ut.prepare_TH1D("hPt", ptbin, ptmin, ptmax)

    ut.put_yx_tit(hPt, "Events / ({0:.3f}".format(ptbin)+" GeV^{2})", "#it{p}_{T}^{2} (GeV^{2})")

    tree_incoh.Draw("jRecPt*jRecPt >> hPt", strsel)

    #incoherent functional shape
    func_incoh_pt2 = TF1("func_incoh", "[0]*exp(-[1]*x)", 0., 10.)
    func_incoh_pt2.SetParName(0, "A")
    func_incoh_pt2.SetParName(1, "b")
    func_incoh_pt2.SetNpx(1000)
    func_incoh_pt2.SetLineColor(rt.kRed)

    #values from pdf fit to log(Pt2)
    #func_incoh_pt2.SetParameters(266.3, 3.28)
    func_incoh_pt2.SetParameters(101953.970, 4.810)

    #histogram created from functional values
    hPtFunc = ut.prepare_TH1D("hPtFunc", ptbin, ptmin, ptmax)
    for ibin in xrange(1,hPtFunc.GetNbinsX()+1):
        edge = hPtFunc.GetBinLowEdge(ibin)
        w = hPtFunc.GetBinWidth(ibin)
        hPtFunc.SetBinContent(ibin, func_incoh_pt2.Integral(edge, edge+w))
        hPtFunc.SetBinError(ibin, 0.)

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.01, 0.01)

    hPt.Draw()
    hPtFunc.Draw("same")

    uoleg = ut.make_uo_leg(hPt, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of subtract_pt2_incoh

#_____________________________________________________________________________
def pdf_logPt2_incoh():

    #PDF fit to log_10(pT^2)

    #tree_in = tree_incoh
    tree_in = tree

    #ptbin = 0.04
    ptbin = 0.12
    ptmin = -5.
    ptmax = 1.

    mmin = 2.8
    mmax = 3.2

    #fitran = [-5., 1.]
    fitran = [-0.9, 0.1]

    binned = False

    #gamma-gamma 131 evt for pT<0.18

    #output log file
    out = open("out.txt", "w")
    ut.log_results(out, "in "+infile+" in_coh "+infile_coh+" in_gg "+infile_gg)
    loglist = [(x,eval(x)) for x in ["ptbin", "ptmin", "ptmax", "mmin", "mmax", "fitran", "binned"]]
    strlog = ut.make_log_string(loglist)
    ut.log_results(out, strlog+"\n")

    #input data
    pT = RooRealVar("jRecPt", "pT", 0, 10)
    m = RooRealVar("jRecM", "mass", 0, 10)
    dataIN = RooDataSet("data", "data", tree_in, RooArgSet(pT, m))
    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)
    data = dataIN.reduce(strsel)
    #x is RooRealVar for log(Pt2)
    draw = "TMath::Log10(jRecPt*jRecPt)"
    draw_func = RooFormulaVar("x", "log_{10}( #it{p}_{T}^{2} ) (GeV^{2})", draw, RooArgList(pT))
    x = data.addColumn(draw_func)
    x.setRange("fitran", fitran[0], fitran[1])

    #binned data
    nbins, ptmax = ut.get_nbins(ptbin, ptmin, ptmax)
    hPt = TH1D("hPt", "hPt", nbins, ptmin, ptmax)
    tree_in.Draw(draw + " >> hPt", strsel)
    dataH = RooDataHist("dataH", "dataH", RooArgList(x), hPt)

    #range for plot
    x.setMin(ptmin)
    x.setMax(ptmax)
    x.setRange("plotran", ptmin, ptmax)

    #create the pdf
    b = RooRealVar("b", "b", 5., 0., 10.)
    pdf_func = "log(10.)*pow(10.,x)*exp(-b*pow(10.,x))"
    pdf_logPt2 = RooGenericPdf("pdf_logPt2", pdf_func, RooArgList(x, b))

    #make the fit
    if binned == True:
        r1 = pdf_logPt2.fitTo(dataH, rf.Range("fitran"), rf.Save())
    else:
        r1 = pdf_logPt2.fitTo(data, rf.Range("fitran"), rf.Save())

    ut.log_results(out, ut.log_fit_result(r1))

    #calculate norm to number of events
    xset = RooArgSet(x)
    ipdf = pdf_logPt2.createIntegral(xset, rf.NormSet(xset), rf.Range("fitran"))
    print "PDF integral:", ipdf.getVal()
    if binned == True:
        nevt = tree_incoh.Draw("", strsel+" && "+draw+">{0:.3f}".format(fitran[0])+" && "+draw+"<{1:.3f}".format(fitran[0], fitran[1]))
    else:
        nevt = data.sumEntries("x", "fitran")

    print "nevt:", nevt
    pdf_logPt2.setNormRange("fitran")
    print "PDF norm:", pdf_logPt2.getNorm(RooArgSet(x))

    #a = nevt/ipdf.getVal()
    a = nevt/pdf_logPt2.getNorm(RooArgSet(x))
    ut.log_results(out, "log_10(pT^2) parametrization:")
    ut.log_results(out, "A = {0:.2f}".format(a))
    ut.log_results(out, ut.log_fit_parameters(r1, 0, 2))
    print "a =", a

    #Coherent contribution
    hPtCoh = ut.prepare_TH1D("hPtCoh", ptbin, ptmin, ptmax)
    tree_coh.Draw(draw + " >> hPtCoh", strsel)
    #ut.norm_to_data(hPtCoh, hPt, rt.kBlue, -5., -2.2) # norm for coh
    ut.norm_to_data(hPtCoh, hPt, rt.kBlue, -5, -2.1)

    #Sartre generated coherent shape
    sartre = TFile.Open("/home/jaroslav/sim/sartre_tx/sartre_AuAu_200GeV_Jpsi_coh_2p7Mevt.root")
    sartre_tree = sartre.Get("sartre_tree")
    hSartre = ut.prepare_TH1D("hSartre", ptbin, ptmin, ptmax)
    sartre_tree.Draw("TMath::Log10(pT*pT) >> hSartre", "rapidity>-1 && rapidity<1")
    ut.norm_to_data(hSartre, hPt, rt.kViolet, -5, -2.3) # norm for Sartre

    #gamma-gamma contribution
    hPtGG = ut.prepare_TH1D("hPtGG", ptbin, ptmin, ptmax)
    tree_gg.Draw(draw + " >> hPtGG", strsel)
    #ut.norm_to_data(hPtGG, hPt, rt.kGreen, -5., -2.9)
    ut.norm_to_num(hPtGG, 131., rt.kGreen)

    print "Int GG:", hPtGG.Integral()

    #sum of all contributions
    hSum = ut.prepare_TH1D("hSum", ptbin, ptmin, ptmax)
    hSum.SetLineWidth(3)
    #add ggel to the sum
    hSum.Add(hPtGG)
    #add incoherent contribution
    func_logPt2 = TF1("pdf_logPt2", "[0]*log(10.)*pow(10.,x)*exp(-[1]*pow(10.,x))", -10., 10.)
    func_logPt2.SetParameters(a, b.getVal())
    hInc = ut.prepare_TH1D("hInc", ptbin, ptmin, ptmax)
    ut.fill_h1_tf(hInc, func_logPt2)
    hSum.Add(hInc)
    #add coherent contribution
    hSum.Add(hPtCoh)
    #set to draw as a lines
    ut.line_h1(hSum, rt.kBlack)

    #create canvas frame
    can = ut.box_canvas()
    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.01, 0.01)

    frame = x.frame(rf.Bins(nbins), rf.Title(""))
    frame.SetTitle("")
    frame.SetMaximum(75)

    frame.SetYTitle("Events / ({0:.3f}".format(ptbin)+" GeV^{2})")

    print "Int data:", hPt.Integral()

    #plot the data
    if binned == True:
        dataH.plotOn(frame, rf.Name("data"))
    else:
        data.plotOn(frame, rf.Name("data"))

    pdf_logPt2.plotOn(frame, rf.Range("fitran"), rf.LineColor(rt.kRed), rf.Name("pdf_logPt2"))
    pdf_logPt2.plotOn(frame, rf.Range("plotran"), rf.LineColor(rt.kRed), rf.Name("pdf_logPt2_full"), rf.LineStyle(rt.kDashed))

    frame.Draw()

    amin = TMath.Power(10, ptmin)
    amax = TMath.Power(10, ptmax)-1
    print amin, amax
    pt2func = TF1("f1","TMath::Power(10, x)",amin,amax)#TMath::Power(x, 10)
    aPt2 = TGaxis(-5, 75, 1, 75,"f1",510,"-");
    ut.set_axis(aPt2)
    aPt2.SetTitle("pt2");
    #aPt2.Draw();

    leg = ut.prepare_leg(0.57, 0.78, 0.14, 0.19, 0.03)
    ut.add_leg_mass(leg, mmin, mmax)
    hx = ut.prepare_TH1D("hx", 1, 0, 1)
    hx.Draw("same")
    ln = ut.col_lin(rt.kRed)
    leg.AddEntry(hx, "Data")
    leg.AddEntry(hPtCoh, "Sartre MC", "l")
    leg.AddEntry(hPtGG, "#gamma#gamma#rightarrow e^{+}e^{-} MC", "l")
    #leg.AddEntry(ln, "ln(10)*#it{A}*10^{log_{10}#it{p}_{T}^{2}}exp(-#it{b}10^{log_{10}#it{p}_{T}^{2}})", "l")
    #leg.AddEntry(ln, "Incoherent fit", "l")
    leg.Draw("same")

    l0 = ut.cut_line(fitran[0], 0.9, frame)
    l1 = ut.cut_line(fitran[1], 0.9, frame)
    #l0.Draw()
    #l1.Draw()

    desc = pdesc(frame, 0.14, 0.8, 0.054)
    desc.set_text_size(0.03)
    desc.itemD("#chi^{2}/ndf", frame.chiSquare("pdf_logPt2", "data", 2), -1, rt.kRed)
    desc.itemD("#it{A}", a, -1, rt.kRed)
    desc.itemR("#it{b}", b, rt.kRed)
    desc.draw()

    #put the sum
    hSum.Draw("same")

    #gPad.SetLogy()

    frame.Draw("same")

    #put gamma-gamma
    hPtGG.Draw("same")
    #put coherent J/psi
    hPtCoh.Draw("same")

    #put Sartre generated coherent shape
    #hSartre.Draw("same")

    leg2 = ut.prepare_leg(0.14, 0.9, 0.14, 0.08, 0.03)
    leg2.AddEntry(ln, "ln(10)*#it{A}*10^{log_{10}#it{p}_{T}^{2}}exp(-#it{b}10^{log_{10}#it{p}_{T}^{2}})", "l")
    #leg2.AddEntry(hPtCoh, "Sartre MC reconstructed", "l")
    #leg2.AddEntry(hSartre, "Sartre MC generated", "l")
    leg2.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of pdf_logPt2_incoh

#_____________________________________________________________________________
def fit_logPt2_incoh():

    #fit to incoherent log_10(pT^2)

    ptbin = 0.12
    ptmin = -5.
    ptmax = 1.

    mmin = 2.8
    mmax = 3.2

    fitran = [-1., -0.1]

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

    r1 = (hPtIncoh.Fit(func_incoh_logPt2, "RS", "", fitran[0], fitran[1])).Get()

    #create pdf normalized to number of events
    pdf_logPt2 = TF1("pdf_logPt2", "[0]*log(10.)*pow(10.,x)*exp(-[1]*pow(10.,x))", -10., 10.)
    nevt = tree_incoh.Draw("", strsel+" && "+draw+">{0:.3f}".format(fitran[0])+" && "+draw+"<{1:.3f}".format(fitran[0], fitran[1]))
    k_norm = nevt/func_incoh_logPt2.Integral(fitran[0], fitran[1])
    pdf_logPt2.SetParameter(0, k_norm*func_incoh_logPt2.GetParameter(0))
    pdf_logPt2.SetParameter(1, func_incoh_logPt2.GetParameter(1))
    #verify the normalization:
    print "PDF integral", pdf_logPt2.Integral(-10., 10.)

    hPtIncoh.Draw()
    func_incoh_logPt2.Draw("same")

    leg = ut.prepare_leg(0.18, 0.78, 0.14, 0.15, 0.03)
    ut.add_leg_mass(leg, mmin, mmax)
    leg.AddEntry(hPtIncoh, "Incoherent MC")
    leg.AddEntry(func_incoh_logPt2, "ln(10)*#it{A}*10^{log_{10}#it{p}_{T}^{2}}exp(-#it{b}10^{log_{10}#it{p}_{T}^{2}})", "l")
    leg.Draw("same")

    desc = pdesc(hPtIncoh, 0.18, 0.78, 0.057)
    desc.set_text_size(0.03)
    desc.itemD("#chi^{2}/ndf", r1.Chi2()/r1.Ndf(), -1, rt.kRed)
    desc.itemRes("#it{A}", r1, 0, rt.kRed)
    desc.itemD("#it{A}", pdf_logPt2.GetParameter(0), -1, rt.kRed)
    desc.itemRes("#it{b}", r1, 1, rt.kRed)
    desc.draw()

    uoleg = ut.make_uo_leg(hPtIncoh, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    l0 = ut.cut_line(fitran[0], 0.9, hPtIncoh)
    l1 = ut.cut_line(fitran[1], 0.9, hPtIncoh)
    l0.Draw()
    l1.Draw()

    ut.invert_col(rt.gPad)
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

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of fit_pt2_incoh

#_____________________________________________________________________________
def fit_pt_incoh():

    #fit to incoherent MC pT

    ptbin = 0.015
    #ptbin = math.sqrt(0.005)
    ptmin = 0.
    ptmax = 1.4

    mmin = 2.8
    mmax = 3.2

    fitran = [0.4, 1.]

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    can = ut.box_canvas()

    hPtIncoh = ut.prepare_TH1D("hPtIncoh", ptbin, ptmin, ptmax)
    ut.put_yx_tit(hPtIncoh, "Events / ({0:.3f}".format(ptbin)+" GeV)", "#it{p}_{T} (GeV)")

    tree_incoh.Draw("jRecPt >> hPtIncoh", strsel)

    print "Input events:", hPtIncoh.GetEntries()
    print "Histogram integral:", hPtIncoh.Integral()
    print "Histogram integral (w):", hPtIncoh.Integral("width")

    #hPtIncoh.Sumw2()
    #hPtIncoh.Scale(1./hPtIncoh.Integral("width"))

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.01, 0.02)

    func_incoh = TF1("func_incoh", "2*[0]*x*exp(-[1]*x*x)", 0., 10.)
    func_incoh.SetParName(0, "A")
    func_incoh.SetParName(1, "b")
    func_incoh.SetNpx(1000)
    func_incoh.SetLineColor(rt.kRed)

    func_incoh.SetParameters(3000., 5.)

    r1 = (hPtIncoh.Fit(func_incoh, "RS", "", fitran[0], fitran[1])).Get()

    print "Fit integral:", func_incoh.Integral(0., 10.)

    hPtIncoh.Draw()
    func_incoh.Draw("same")

    #normalize fit function to number of events
    pdf_incoh = TF1("pdf_incoh", "2*[0]*x*exp(-[1]*x*x)", 0., 10.)
    pdf_incoh.SetParName(0, "A")
    pdf_incoh.SetParName(1, "b")
    #    tree_incoh.Draw("jRecPt >> hPtIncoh", strsel)
    #strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)
    nevt = tree_incoh.Draw("", strsel+" && jRecPt>{0:.3f} && jRecPt<{1:.3f}".format(fitran[0], fitran[1]))
    k_norm = nevt/func_incoh.Integral(fitran[0], fitran[1])
    pdf_incoh.SetParameter(0, k_norm*func_incoh.GetParameter(0))
    pdf_incoh.SetParameter(1, func_incoh.GetParameter(1))
    #verify the normalization:
    print "Function integral after norm:", pdf_incoh.Integral(0., 10.)

    #create pdf for pT^2 and verify normalization
    pdf_pt2 = TF1("pdf_pt2", "[0]*exp(-[1]*x)", 0., 10.)
    pdf_pt2.SetParameter(0, pdf_incoh.GetParameter(0))
    pdf_pt2.SetParameter(1, pdf_incoh.GetParameter(1))
    print "PDF for pT^2 integral:", pdf_pt2.Integral(0., 10.)

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
    desc.itemD("#it{A}", pdf_incoh.GetParameter(0), -1, rt.kRed)
    desc.prec = 3
    desc.itemRes("#it{b}", r1, 1, rt.kRed)
    desc.draw()

    l0 = ut.cut_line(fitran[0], 0.9, hPtIncoh)
    l1 = ut.cut_line(fitran[1], 0.9, hPtIncoh)
    l0.Draw()
    l1.Draw()

    uoleg = ut.make_uo_leg(hPtIncoh, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of fit_pt_incoh

#_____________________________________________________________________________
def plot_pt():

    #pT with coherent incoherent and gamma-gamma components

    ptbin = 0.02
    ptmin = 0.
    ptmax = 1.1

    mmin = 2.8
    mmax = 3.2
    #mmin = 3.4
    #mmax = 5.

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    can = ut.box_canvas()

    hPt = ut.prepare_TH1D("hPt", ptbin, ptmin, ptmax)
    hPtCoh = ut.prepare_TH1D("hPtCoh", ptbin, ptmin, ptmax)
    hPtIncoh = ut.prepare_TH1D("hPtIncoh", ptbin, ptmin, ptmax)
    hPtGG = ut.prepare_TH1D("hPtGG", ptbin, ptmin, ptmax)

    #ut.put_yx_tit(hPt, "Events / ({0:.3f}".format(ptbin)+" GeV)", "#it{p}_{T} (GeV})")
    ut.put_yx_tit(hPt, "J/#psi candidates / ({0:.3f}".format(ptbin)+" GeV/c)", "Dielectron #it{p}_{T} (GeV/c)", 1.5, 1.2)

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.01, 0.02)

    draw = "jRecPt"

    tree.Draw(draw + " >> hPt", strsel)
    tree_coh.Draw(draw + " >> hPtCoh", strsel)
    tree_incoh.Draw(draw + " >> hPtIncoh", strsel)
    tree_gg.Draw(draw + " >> hPtGG", strsel)

    ut.norm_to_data(hPtCoh, hPt, rt.kBlue, 0., 0.08)
    ut.norm_to_data(hPtIncoh, hPt, rt.kRed, 0.28, 1.)
    #ut.norm_to_data(hPtGG, hPt, rt.kGreen, 0., 0.03)
    ut.norm_to_num(hPtGG, 131, rt.kGreen+1)

    #sum of all contributions
    hSum = ut.prepare_TH1D("hSum", ptbin, ptmin, ptmax)
    hSum.SetLineWidth(3)
    #add ggel to the sum
    hSum.Add(hPtGG)
    #add incoherent contribution
    hSum.Add(hPtIncoh)
    #add coherent contribution
    hSum.Add(hPtCoh)
    #set to draw as a lines
    ut.line_h1(hSum, rt.kBlack)

    hPt.Draw()
    hSum.Draw("same")
    hPtCoh.Draw("same")
    hPtIncoh.Draw("same")
    hPtGG.Draw("same")

    leg = ut.prepare_leg(0.64, 0.65, 0.14, 0.3, 0.03)
    leg.AddEntry(None, "#bf{|#kern[0.3]{#it{y}}| < 1}", "")
    ut.add_leg_mass(leg, mmin, mmax)
    leg.AddEntry(hPt, "Data", "p")
    leg.AddEntry(hSum, "Sum", "l")
    leg.AddEntry(hPtCoh, "Coherent J/#psi", "l")
    leg.AddEntry(hPtIncoh, "Incoherent J/#psi", "l")
    leg.AddEntry(hPtGG, "#gamma#gamma#rightarrow e^{+}e^{-}", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hPt, 0.14, 0.9, 0.01, 0.1)
    #uoleg.Draw("same")

    pleg = ut.prepare_leg(0.33, 0.8, 0.01, 0.14, 0.035)
    pleg.AddEntry(None, "STAR Preliminary", "")
    pleg.AddEntry(None, "AuAu@200 GeV", "")
    pleg.AddEntry(None, "UPC sample", "")
    pleg.Draw("same")

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
    #mmin = 1.5
    #mmax = 2.6

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

    ut.invert_col(rt.gPad)
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
    ut.norm_to_data(hPtGG, hPt, rt.kGreen, -5., -2.9) # for ggel

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

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_jpsi_logPt2

#_____________________________________________________________________________
if __name__ == "__main__":

    #data
    basedir = "../../../star-upc-data/ana/muDst/muDst_run1/sel5"
    infile = "ana_muDst_run1_all_sel5z.root"

    #MC
    basedir_coh = "../../../star-upc-data/ana/starsim/sartre14a/sel5"
    #infile_coh = "ana_sartre14a1_sel5z.root"
    infile_coh = "ana_sartre14a1_sel5z_s6_v2.root"
    #infile_coh = "ana_sartre14a1_sel5z_s6.root"
    #basedir_coh = "../../../star-upc-data/ana/starsim/slight14e/sel5"
    #infile_coh = "ana_slight14e1x1_sel5z.root"
    basedir_mc = "../../../star-upc-data/ana/starsim/slight14e/sel5"
    infile_incoh = "ana_slight14e3_sel5z.root"
    infile_gg = "ana_slight14e2x1_sel5_nzvtx.root"

    interactive = False

    if interactive == False: gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    iplot = 6
    funclist = []
    funclist.append(plot_jpsi_logPt2) # 0
    funclist.append(plot_pt2) # 1
    funclist.append(plot_pt) # 2
    funclist.append(fit_pt_incoh) # 3
    funclist.append(fit_pt2_incoh) # 4
    funclist.append(fit_logPt2_incoh) # 5
    funclist.append(pdf_logPt2_incoh) # 6
    funclist.append(subtract_pt2_incoh) # 7
    funclist.append(plot_pt2_real) # 8
    funclist.append(subtract_pt2) # 9
    funclist.append(make_eff_pt2) # 10
    funclist.append(pdf_logPt2_prelim) # 11
    funclist.append(plot_pt_gg) # 12

    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("jRecTree")

    inp_coh = TFile.Open(basedir_coh+"/"+infile_coh)
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





















