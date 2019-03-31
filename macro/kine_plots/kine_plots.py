#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import RooRealVar, RooDataHist, RooArgList, RooCBShape, RooGaussian
from ROOT import RooNovosibirsk, RooBifurGauss, RooBreitWigner
from ROOT import RooFit as rf

import sys
sys.path.append('../')
import plot_utils as ut
from parameter_descriptor import parameter_descriptor as pdesc

#_____________________________________________________________________________
def plot_rec_gen_track_phi():

    #track azimuthal angle phi resolution as ( phi_track_rec - phi_track_gen )/phi_track_gen

    phibin = 0.0001
    phimin = -0.02
    phimax = 0.02

    #ptlo = 0.
    #pthi = 0.9

    fitran = [-0.01, 0.01]

    mmin = 2.8
    mmax = 3.2

    cbw = rt.kBlue

    #output log file
    out = open("out.txt", "w")
    #log fit parameters
    loglist1 = [(x,eval(x)) for x in ["infile_mc", "phibin", "phimin", "phimax"]]
    loglist2 = [(x,eval(x)) for x in ["fitran", "mmin", "mmax"]]
    strlog = ut.make_log_string(loglist1, loglist2)
    ut.log_results(out, strlog+"\n")

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)
    #strsel += " && jGenPt>{0:.3f}".format(ptlo)
    #strsel += " && jGenPt<{0:.3f}".format(pthi)

    nbins, phimax = ut.get_nbins(phibin, phimin, phimax)
    hPhiRel = ut.prepare_TH1D_n("hPhiRel", nbins, phimin, phimax)

    ytit = "Events / ({0:.4f})".format(phibin)
    xtit = "(#phi_{rec} - #phi_{gen})/#phi_{gen}"

    mctree.Draw("(jT0phi-jGenP0phi)/jGenP0phi >> hPhiRel", strsel) # positive charge
    mctree.Draw("(jT1phi-jGenP1phi)/jGenP1phi >>+hPhiRel", strsel) # add negative charge

    x = RooRealVar("x", "x", phimin, phimax)
    x.setRange("fitran", fitran[0], fitran[1])
    rfPhiRel = RooDataHist("rfPhiRel", "rfPhiRel", RooArgList(x), hPhiRel)

    #Breit-Wigner pdf
    mean = RooRealVar("mean", "mean", 0., -0.1, 0.1)
    sigma = RooRealVar("sigma", "sigma", 0.01, 0., 0.9)
    bwpdf = RooBreitWigner("bwpdf", "bwpdf", x, mean, sigma)

    res = bwpdf.fitTo(rfPhiRel, rf.Range("fitran"), rf.Save())

    #log fit results
    ut.log_results(out, ut.log_fit_result(res))

    can = ut.box_canvas()
    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.05, 0.03)

    frame = x.frame(rf.Bins(nbins), rf.Title(""))
    ut.put_frame_yx_tit(frame, ytit, xtit)

    rfPhiRel.plotOn(frame, rf.Name("data"))

    bwpdf.plotOn(frame, rf.Precision(1e-6), rf.Name("bwpdf"))

    frame.Draw()

    desc = pdesc(frame, 0.12, 0.93, 0.057); #x, y, sep
    desc.set_text_size(0.03)
    desc.itemD("#chi^{2}/ndf", frame.chiSquare("bwpdf", "data", 2), -1, cbw)
    desc.prec = 2
    desc.fmt = "e"
    desc.itemR("mean", mean, cbw)
    desc.itemR("#sigma", sigma, cbw)

    desc.draw()

    leg = ut.make_uo_leg(hPhiRel, 0.5, 0.8, 0.2, 0.2)
    #leg.Draw("same")

    #print "Entries: ", hPhiRel.GetEntries()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def plot_rec_gen_track_eta():

    #track pseudorapidity resolution as ( eta_track_rec - eta_track_gen )/eta_track_gen

    etabin = 0.001
    etamin = -0.1
    etamax = 0.1

    #ptlo = 0.
    #pthi = 0.9

    fitran = [-0.06, 0.06]

    mmin = 2.8
    mmax = 3.2

    cbw = rt.kBlue

    #output log file
    out = open("out.txt", "w")
    #log fit parameters
    loglist1 = [(x,eval(x)) for x in ["infile_mc", "etabin", "etamin", "etamax"]]
    loglist2 = [(x,eval(x)) for x in ["fitran", "mmin", "mmax"]]
    strlog = ut.make_log_string(loglist1, loglist2)
    ut.log_results(out, strlog+"\n")

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)
    #strsel += " && jGenPt>{0:.3f}".format(ptlo)
    #strsel += " && jGenPt<{0:.3f}".format(pthi)

    nbins, etamax = ut.get_nbins(etabin, etamin, etamax)
    hEtaRel = ut.prepare_TH1D_n("hEtaRel", nbins, etamin, etamax)

    ytit = "Events / ({0:.3f})".format(etabin)
    xtit = "(#eta_{rec} - #eta_{gen})/#eta_{gen}"

    mctree.Draw("(jT0eta-jGenP0eta)/jGenP0eta >> hEtaRel", strsel) # positive charge
    mctree.Draw("(jT1eta-jGenP1eta)/jGenP1eta >>+hEtaRel", strsel) # add negative charge

    x = RooRealVar("x", "x", etamin, etamax)
    x.setRange("fitran", fitran[0], fitran[1])
    rfEtaRel = RooDataHist("rfEtaRel", "rfEtaRel", RooArgList(x), hEtaRel)

    #Breit-Wigner pdf
    mean = RooRealVar("mean", "mean", 0., -0.1, 0.1)
    sigma = RooRealVar("sigma", "sigma", 0.01, 0., 0.9)
    bwpdf = RooBreitWigner("bwpdf", "bwpdf", x, mean, sigma)

    res = bwpdf.fitTo(rfEtaRel, rf.Range("fitran"), rf.Save())

    #log fit results
    ut.log_results(out, ut.log_fit_result(res))

    can = ut.box_canvas()
    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.05, 0.03)

    frame = x.frame(rf.Bins(nbins), rf.Title(""))
    ut.put_frame_yx_tit(frame, ytit, xtit)

    rfEtaRel.plotOn(frame, rf.Name("data"))

    bwpdf.plotOn(frame, rf.Precision(1e-6), rf.Name("bwpdf"))

    frame.Draw()

    desc = pdesc(frame, 0.13, 0.9, 0.057); #x, y, sep
    desc.set_text_size(0.03)
    desc.itemD("#chi^{2}/ndf", frame.chiSquare("bwpdf", "data", 2), -1, cbw)
    desc.prec = 2
    desc.fmt = "e"
    desc.itemR("mean", mean, cbw)
    desc.itemR("#sigma", sigma, cbw)

    desc.draw()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_rec_gen_track_eta

#_____________________________________________________________________________
def plot_rec_gen_track_pt():

    #track pT resolution as ( pT_track_rec - pT_track_gen )/pT_track_gen

    ptbin = 0.001
    ptmin = -0.3
    ptmax = 0.1

    #generated dielectron pT selection to input data
    ptlo = 0.2
    pthi = 1

    fitran = [-0.15, 0.018]

    mmin = 2.8
    mmax = 3.2

    ccb = rt.kBlue

    #output log file
    out = open("out.txt", "w")
    #log fit parameters
    loglist1 = [(x,eval(x)) for x in ["infile_mc", "ptbin", "ptmin", "ptmax"]]
    loglist2 = [(x,eval(x)) for x in ["ptlo", "pthi", "fitran", "mmin", "mmax"]]
    strlog = ut.make_log_string(loglist1, loglist2)
    ut.log_results(out, strlog+"\n")

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)
    strsel += " && jGenPt>{0:.3f}".format(ptlo)
    strsel += " && jGenPt<{0:.3f}".format(pthi)
    #strsel = ""

    nbins, ptmax = ut.get_nbins(ptbin, ptmin, ptmax)
    hPtTrackRel = ut.prepare_TH1D_n("hPtTrackRel", nbins, ptmin, ptmax)

    ytit = "Events / ({0:.3f})".format(ptbin)
    xtit = "(#it{p}_{T, rec}^{track} - #it{p}_{T, gen}^{track})/#it{p}_{T, gen}^{track}"

    mctree.Draw("(jT0pT-jGenP0pT)/jGenP0pT >> hPtTrackRel", strsel) # positive charge
    mctree.Draw("(jT1pT-jGenP1pT)/jGenP1pT >>+hPtTrackRel", strsel) # add negative charge

    x = RooRealVar("x", "x", ptmin, ptmax)
    x.setRange("fitran", fitran[0], fitran[1])
    rfPtTrackRel = RooDataHist("rfPtTrackRel", "rfPtTrackRel", RooArgList(x), hPtTrackRel)

    #standard Crystal Ball
    mean = RooRealVar("mean", "mean", -0.003, -0.1, 0.1)
    sigma = RooRealVar("sigma", "sigma", 0.01, 0., 0.9)
    alpha = RooRealVar("alpha", "alpha", 1.2, 0., 10.)
    n = RooRealVar("n", "n", 1.3, 0., 20.)
    cbpdf = RooCBShape("cbpdf", "cbpdf", x, mean, sigma, alpha, n)

    res = cbpdf.fitTo(rfPtTrackRel, rf.Range("fitran"), rf.Save())

    #log fit results
    ut.log_results(out, ut.log_fit_result(res))

    #generate new distribution according to the fit
    gROOT.LoadMacro("cb_gen.h")
    #Crystal Ball generator, min, max, mean, sigma, alpha, n
    #cbgen = rt.cb_gen(-0.18, 0.05, -0.00226, 0.00908, 1.40165, 1.114)  #  -0.18, 0.05  ptmin, ptmax
    cbgen = rt.cb_gen(-0.5, 0.05, -0.00226, 0.00908, 0.2, 2.)  #  -0.18, 0.05  ptmin, ptmax
    hRelGen = ut.prepare_TH1D_n("hRelGen", nbins, ptmin, ptmax)
    ut.set_H1D_col(hRelGen, rt.kBlue)
    #rt.cb_generate_n(cbgen, hRelGen, int(hPtTrackRel.GetEntries()))
    rfRelGen = RooDataHist("rfRelGen", "rfRelGen", RooArgList(x), hRelGen)

    #generate distribution with additional smearing applied
    hRelSmear = ut.prepare_TH1D_n("hRelSmear", nbins, ptmin, ptmax)
    ut.set_H1D_col(hRelSmear, rt.kOrange)
    #tcopy = mctree.CopyTree(strsel)
    #rt.cb_apply_smear(cbgen, mctree, hRelSmear)

    can = ut.box_canvas()
    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.05, 0.03)

    frame = x.frame(rf.Bins(nbins), rf.Title(""))
    ut.put_frame_yx_tit(frame, ytit, xtit)

    rfPtTrackRel.plotOn(frame, rf.Name("data"))

    #rfRelGen.plotOn(frame, rf.Name("data"))

    cbpdf.plotOn(frame, rf.Precision(1e-6), rf.Name("cbpdf"), rf.LineColor(ccb))


    frame.Draw()

    #hRelGen.Draw("e1same")
    #hRelSmear.Draw("e1same")

    desc = pdesc(frame, 0.2, 0.8, 0.057); #x, y, sep
    desc.set_text_size(0.03)

    desc.itemD("#chi^{2}/ndf", frame.chiSquare("cbpdf", "data", 4), -1, ccb)
    desc.prec = 5
    desc.itemR("mean", mean, ccb)
    desc.itemR("#sigma", sigma, ccb)
    desc.itemR("#alpha", alpha, ccb)
    desc.prec = 3
    desc.itemR("#it{n}", n, ccb)
    desc.draw()

    leg = ut.prepare_leg(0.2, 0.82, 0.21, 0.12, 0.03) # x, y, dx, dy, tsiz
    leg.SetMargin(0.05)
    leg.AddEntry(0, "#bf{%.1f < #it{p}_{T}^{pair} < %.1f GeV}" % (ptlo, pthi), "")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_rec_gen_track_pt

#_____________________________________________________________________________
def plot_rec_gen_pt_relative():

    # relative dielectron pT resolution as ( pT_rec - pT_gen )/pT_gen

    ptbin = 0.01
    ptmin = -1.2
    ptmax = 4

    #generated pT selection to input data
    ptlo = 0.2
    pthi = 1.

    fitran = [-0.1, 3]

    mmin = 2.8
    mmax = 3.2

    #output log file
    out = open("out.txt", "w")
    #log fit parameters
    loglist1 = [(x,eval(x)) for x in ["infile_mc", "ptbin", "ptmin", "ptmax"]]
    loglist2 = [(x,eval(x)) for x in ["ptlo", "pthi", "fitran", "mmin", "mmax"]]
    strlog = ut.make_log_string(loglist1, loglist2)
    ut.log_results(out, strlog+"\n")

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)
    strsel += " && jGenPt>{0:.3f}".format(ptlo)
    strsel += " && jGenPt<{0:.3f}".format(pthi)

    nbins, ptmax = ut.get_nbins(ptbin, ptmin, ptmax)
    hPtRel = ut.prepare_TH1D("hPtRel", ptbin, ptmin, ptmax)

    ytit = "Events / ({0:.3f})".format(ptbin)
    xtit = "(#it{p}_{T, rec} - #it{p}_{T, gen})/#it{p}_{T, gen}"

    mctree.Draw("(jRecPt-jGenPt)/jGenPt >> hPtRel", strsel)

    x = RooRealVar("x", "x", ptmin, ptmax)
    x.setRange("fitran", fitran[0], fitran[1])
    rfPtRel = RooDataHist("rfPtRel", "rfPtRel", RooArgList(x), hPtRel)

    #reversed Crystal Ball
    mean = RooRealVar("mean", "mean", 0., -0.1, 0.1)
    sigma = RooRealVar("sigma", "sigma", 0.2, 0., 0.9)
    alpha = RooRealVar("alpha", "alpha", -1.2, -10., 0.)
    n = RooRealVar("n", "n", 1.3, 0., 20.)
    cbpdf = RooCBShape("cbpdf", "cbpdf", x, mean, sigma, alpha, n)

    res = cbpdf.fitTo(rfPtRel, rf.Range("fitran"), rf.Save())

    #log fit results
    ut.log_results(out, ut.log_fit_result(res))

    can = ut.box_canvas()
    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.05, 0.03)

    frame = x.frame(rf.Bins(nbins), rf.Title(""))
    ut.put_frame_yx_tit(frame, ytit, xtit)

    rfPtRel.plotOn(frame, rf.Name("data"))

    cbpdf.plotOn(frame, rf.Precision(1e-6), rf.Name("cbpdf"))

    frame.Draw()

    desc = pdesc(frame, 0.65, 0.8, 0.057); #x, y, sep
    desc.set_text_size(0.03)

    desc.itemD("#chi^{2}/ndf", frame.chiSquare("cbpdf", "data", 4), -1, rt.kBlue)
    desc.prec = 5
    desc.itemR("mean", mean, rt.kBlue)
    desc.prec = 4
    desc.itemR("#sigma", sigma, rt.kBlue)
    desc.itemR("#alpha", alpha, rt.kBlue)
    desc.prec = 3
    desc.itemR("#it{n}", n, rt.kBlue)
    desc.draw()

    leg = ut.prepare_leg(0.6, 0.82, 0.21, 0.12, 0.03) # x, y, dx, dy, tsiz
    leg.SetMargin(0.05)
    leg.AddEntry(0, "#bf{%.1f < #it{p}_{T}^{pair} < %.1f GeV}" % (ptlo, pthi), "")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def plot_rec_minus_gen_pt():

    #reconstructed pT vs. generated pT for resolution

    #distribution range
    ptbin = 0.005
    ptmin = -0.2
    ptmax = 0.4

    #generated pT selection to input data
    ptlo = 0
    pthi = 0.1

    #mass selection
    mmin = 2.8
    mmax = 3.2

    #range for the fit
    fitran = [-0.02, 0.2]

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)
    strsel += " && jGenPt>{0:.3f}".format(ptlo)
    strsel += " && jGenPt<{0:.3f}".format(pthi)

    nbins, ptmax = ut.get_nbins(ptbin, ptmin, ptmax)
    hPtDiff = ut.prepare_TH1D("hPtDiff", ptbin, ptmin, ptmax)

    ytit = "Events / ({0:.3f}".format(ptbin)+" GeV)"
    xtit = "#it{p}_{T, reconstructed} - #it{p}_{T, generated} (GeV)"

    mctree.Draw("jRecPt-jGenPt >> hPtDiff", strsel)

    #roofit binned data
    x = RooRealVar("x", "x", -1, 1)
    x.setRange("fitran", fitran[0], fitran[1])
    rfPt = RooDataHist("rfPt", "rfPt", RooArgList(x), hPtDiff)

    #reversed Crystal Ball
    mean = RooRealVar("mean", "mean", 0., -0.1, 0.1)
    sigma = RooRealVar("sigma", "sigma", 0.01, 0., 0.1)
    alpha = RooRealVar("alpha", "alpha", -1.046, -10., 0.)
    n = RooRealVar("n", "n", 1.403, 0., 20.)
    pdf = RooCBShape("pdf", "pdf", x, mean, sigma, alpha, n)

    #make the fit
    res = pdf.fitTo(rfPt, rf.Range("fitran"), rf.Save())

    can = ut.box_canvas()
    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.05, 0.03)

    frame = x.frame(rf.Bins(nbins), rf.Title(""))
    ut.put_frame_yx_tit(frame, ytit, xtit)

    rfPt.plotOn(frame, rf.Name("data"))

    pdf.plotOn(frame, rf.Precision(1e-6), rf.Name("pdf"))

    frame.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_rec_minus_gen_pt

#_____________________________________________________________________________
def plot_rec_gen_LogPt2():

    #reconstructed log_10(pT^2) vs. generated pT^2 for resolution

    ptbin = 0.05
    ptmin = -6.
    ptmax = 0.

    mmin = 2.8
    mmax = 3.2

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    can = ut.box_canvas()

    hLogPt2 = ut.prepare_TH2D("hLogPt2", ptbin, ptmin, ptmax, ptbin, ptmin, ptmax)

    #tit_str = "#it{p}_{T}"+" / ({0:.3f}".format(ptbin)+" GeV)"
    tit_str = "log_{10}( #it{p}_{T}^{2} )"
    ut.put_yx_tit(hLogPt2, "Reconstructed " + tit_str, "Generated " + tit_str, 1.5, 1.2)

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.015, 0.11)

    draw = "TMath::Log10(jRecPt*jRecPt):TMath::Log10(jGenPt*jGenPt)"

    gPad.SetLogz()

    mctree.Draw(draw + " >> hLogPt2", strsel)

    #line 1:1
    lin = ut.col_lin(rt.kViolet, 4, rt.kDashed)
    lin.SetX1(ptmin)
    lin.SetY1(ptmin)
    lin.SetX2(ptmax)
    lin.SetY2(ptmax)

    lin.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_rec_gen_LogPt2

#_____________________________________________________________________________
def plot_rec_minus_gen_pt2():

    #reconstructed pT^2 vs. generated pT^2 for resolution

    #distribution range
    ptbin = 0.001
    ptmin = -0.1
    ptmax = 0.15

    #generated pT^2 selection to input data
    ptlo = 0.04
    pthi = 0.1

    #mass selection
    mmin = 2.8
    mmax = 3.2

    fitran = [-0.003, 0.05]
    #fitran = [-0.003, 0.003]

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)
    strsel += " && (jGenPt*jGenPt)>{0:.3f}".format(ptlo)
    strsel += " && (jGenPt*jGenPt)<{0:.3f}".format(pthi)

    print strsel

    nbins, ptmax = ut.get_nbins(ptbin, ptmin, ptmax)
    hPt2 = ut.prepare_TH1D("hPt2", ptbin, ptmin, ptmax)

    ytit = "Events / ({0:.3f}".format(ptbin)+" GeV^{2})"
    xtit = "#it{p}_{T, reconstructed}^{2} - #it{p}_{T, generated}^{2} (GeV^{2})"
    ut.put_yx_tit(hPt2, ytit, xtit)

    draw = "(jRecPt*jRecPt)-(jGenPt*jGenPt)"

    mctree.Draw(draw + " >> hPt2", strsel)

    #roofit binned data
    x = RooRealVar("x", "x", -1, 1)
    dataH = RooDataHist("dataH", "dataH", RooArgList(x), hPt2)

    x.setRange("fitran", fitran[0], fitran[1])

    #reversed Crystal Ball
    mean = RooRealVar("mean", "mean", 0., -0.1, 0.1)
    sigma = RooRealVar("sigma", "sigma", 0.0011, 0., 0.1)
    alpha = RooRealVar("alpha", "alpha", -1.046, -10., 0.)
    n = RooRealVar("n", "n", 1.403, 0., 20.)
    pdf = RooCBShape("pdf", "pdf", x, mean, sigma, alpha, n)

    #gaus = RooGaussian("gaus", "gaus", x, mean, sigma)

    #make the fit
    #res = pdf.fitTo(dataH, rf.Range("fitran"), rf.Save())
    #res = gaus.fitTo(dataH, rf.Range("fitran"), rf.Save())

    can = ut.box_canvas()
    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.015, 0.03)

    frame = x.frame(rf.Bins(nbins), rf.Title(""))
    frame.SetTitle("")

    frame.SetYTitle(ytit)
    frame.SetXTitle(xtit)

    frame.GetXaxis().SetTitleOffset(1.2);
    frame.GetYaxis().SetTitleOffset(1.7);

    dataH.plotOn(frame, rf.Name("data"))

    pdf.plotOn(frame, rf.Precision(1e-6), rf.Name("pdf"))
    #gaus.plotOn(frame, rf.Precision(1e-6), rf.Name("gaus"))

    frame.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_rec_minus_gen_pt2

#_____________________________________________________________________________
def plot_rec_gen_pt2():

    #reconstructed pT^2 vs. generated pT^2 for resolution

    #ptbin = 0.005
    ptbin = 0.002
    ptmin = 0.
    #ptmax = 1.
    #ptmax = 0.16
    ptmax = 0.1
    #ptmin = 0.
    #ptmax = 0.2

    mmin = 2.8
    mmax = 3.2

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    can = ut.box_canvas()

    hPt2 = ut.prepare_TH2D("hPt2", ptbin, ptmin, ptmax, ptbin, ptmin, ptmax)

    tit_str = "#it{p}_{T}^{2}"+" / ({0:.3f})".format(ptbin)
    ut.put_yx_tit(hPt2, "Reconstructed " + tit_str, "Generated " + tit_str, 1.5, 1.2)

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.015, 0.11)

    #draw = "jRecPt:jGenPt"
    draw = "jRecPt*jRecPt:jGenPt*jGenPt"

    gPad.SetLogz()

    mctree.Draw(draw + " >> hPt2", strsel)

    #line 1:1
    lin = ut.col_lin(rt.kViolet, 4, rt.kDashed)
    lin.SetX1(ptmin)
    lin.SetY1(ptmin)
    lin.SetX2(ptmax)
    lin.SetY2(ptmax)

    lin.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_rec_gen_pt2

#_____________________________________________________________________________
def plot_jpsi_logPt2():

    #J/psi log_10(pT^2)

    ptbin = 0.12
    ptmin = -5.
    ptmax = 1.

    mmin = 2.8
    mmax = 3.2

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    can = ut.box_canvas()

    hPt = ut.prepare_TH1D("hPt", ptbin, ptmin, ptmax)
    hPtMC = ut.prepare_TH1D("hPtMC", ptbin/3., ptmin, ptmax)

    ut.put_yx_tit(hPt, "Events / ({0:.3f}".format(ptbin)+" GeV^{2})", "#it{p}_{T}^{2} (GeV^{2})")

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.01, 0.01)

    draw = "TMath::Log10(jRecPt*jRecPt)"

    tree.Draw(draw + " >> hPt", strsel)
    mctree.Draw(draw + " >> hPtMC", strsel)
    ut.norm_to_data(hPtMC, hPt, rt.kBlue, -5., -1.8) # norm for coh
    #ut.norm_to_data(hPtMC, hPt, rt.kBlue, -1.1, 1.) # for incoh
    #ut.norm_to_data(hPtMC, hPt, rt.kBlue, -5., -2.4) # for ggel

    hPt.Draw()
    hPtMC.Draw("same")

    leg = ut.prepare_leg(0.67, 0.8, 0.14, 0.16, 0.03)
    ut.add_leg_mass(leg, mmin, mmax)
    leg.AddEntry(hPt, "Data")
    leg.AddEntry(hPtMC, "Coherent MC", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hPt, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_jpsi_logPt2

#_____________________________________________________________________________
def plot_jpsi_pt2():

    #J/psi pT^2

    ptbin = 0.002
    ptmin = 0.
    ptmax = 0.15

    mmin = 2.8
    mmax = 3.2

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    can = ut.box_canvas()

    hPt = ut.prepare_TH1D("hPt", ptbin, ptmin, ptmax)
    hPtMC = ut.prepare_TH1D("hPtMC", ptbin/3., ptmin, ptmax)

    ut.put_yx_tit(hPt, "Events / ({0:.3f}".format(ptbin)+" GeV^{2})", "#it{p}_{T}^{2} (GeV^{2})")

    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.01, 0.02)

    draw = "jRecPt*jRecPt"

    tree.Draw(draw + " >> hPt", strsel)
    mctree.Draw(draw + " >> hPtMC", strsel)
    ut.norm_to_data(hPtMC, hPt, rt.kBlue, 0., 0.015)

    hPt.Draw()
    hPtMC.Draw("same")

    leg = ut.prepare_leg(0.67, 0.8, 0.14, 0.16, 0.03)
    ut.add_leg_mass(leg, mmin, mmax)
    leg.AddEntry(hPt, "Data")
    leg.AddEntry(hPtMC, "Coherent MC", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hPt, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_jpsi_pt2

#_____________________________________________________________________________
def plot_jpsi_pt():

    #J/psi transverse momentum
    ptbin = 0.015
    ptmin = 0.
    ptmax = 1.

    mmin = 2.8
    mmax = 3.2

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    can = ut.box_canvas()

    hPt = ut.prepare_TH1D("hPt", ptbin, ptmin, ptmax)
    hPtMC = ut.prepare_TH1D("hPtMC", ptbin/3., ptmin, ptmax)

    ut.put_yx_tit(hPt, "Events / ({0:.3f} GeV)".format(ptbin), "#it{p}_{T} (GeV)")

    ut.set_margin_lbtr(gPad, 0.1, 0.09, 0.01, 0.01)

    draw = "jRecPt"

    tree.Draw(draw + " >> hPt", strsel)
    mctree.Draw(draw + " >> hPtMC", strsel)
    ut.norm_to_data(hPtMC, hPt, rt.kBlue, 0., 0.14)

    hPt.Draw()
    hPtMC.Draw("same")

    leg = ut.prepare_leg(0.67, 0.8, 0.14, 0.16, 0.03)
    ut.add_leg_mass(leg, mmin, mmax)
    leg.AddEntry(hPt, "Data")
    leg.AddEntry(hPtMC, "Coherent MC", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hPt, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_jpsi_pt

#_____________________________________________________________________________
def plot_dphi_bemc():

    #tracks opening angle at BEMC
    phibin = 0.01
    phimin = 2.4
    phimax = 3.1

    mmin = 1.5
    mmax = 5
    #mmin = 2.8
    #mmax = 3.2

    ptmax = 0.17

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f} && jRecPt<{2:.3f}".format(mmin, mmax, ptmax)

    can = ut.box_canvas()

    hDphi = ut.prepare_TH1D("hDphi", phibin, phimin, phimax)
    hDphiMC = ut.prepare_TH1D("hDphiMC", phibin, phimin, phimax)

    ut.put_yx_tit(hDphi, "Events / {0:.2f}".format(phibin), "Tracks #Delta#phi at BEMC")
    ut.put_yx_tit(hDphiMC, "Events / {0:.2f}".format(phibin), "Tracks #Delta#phi at BEMC")

    ut.set_margin_lbtr(gPad, 0.1, 0.08, 0.014, 0.01)

    tree.Draw("jDeltaPhiBemc >> hDphi", strsel)
    mctree.Draw("jDeltaPhiBemc >> hDphiMC", strsel)
    ut.norm_to_data(hDphiMC, hDphi, rt.kBlue)

    hDphiMC.Draw()
    hDphi.Draw("e1same")
    #hDphi.Draw()
    hDphiMC.Draw("same")

    lin = ut.cut_line(2.618, 0.5, hDphi)
    lin.Draw("same")

    leg = ut.prepare_leg(0.14, 0.71, 0.14, 0.21, 0.03)
    ut.add_leg_pt_mass(leg, ptmax, mmin, mmax)
    leg.AddEntry(hDphi, "Data")
    leg.AddEntry(hDphiMC, "MC", "l")
    leg.AddEntry(lin, "Cut at 2.618", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hDphi, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_dphi_bemc

#_____________________________________________________________________________
def plot_dvtx_mc():

    #difference between reconstructed and generated vertex in MC
    vbin = 0.01
    vmin = -2.
    vmax = 2.

    mmin = 1.5
    mmax = 5.

    ptmax = 0.17

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f} && jRecPt<{2:.3f}".format(mmin, mmax, ptmax)

    can = ut.box_canvas()

    hDv = ut.prepare_TH1D("hDv", vbin, vmin, vmax)

    ut.put_yx_tit(hDv, "Events / ({0:.2f} cm)".format(vbin), "Vtx_{#it{z},rec} - Vtx_{#it{z},gen} (cm)")

    ut.set_margin_lbtr(gPad, 0.12, 0.08, 0.01, 0.01)

    mctree.Draw("jVtxZ-jGenVtxZ >> hDv", strsel)

    hDv.Draw()

    leg = ut.prepare_leg(0.62, 0.8, 0.14, 0.16, 0.03)
    ut.add_leg_pt_mass(leg, ptmax, mmin, mmax)
    leg.AddEntry(None, "Reconstructed - generated", "")
    leg.AddEntry(None, "vertex position along #it{z}", "")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hDv, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_dvtx_mc

#_____________________________________________________________________________
def plot_tracks_nhits():

    #tracks number of hits
    nhbin = 1
    nhmin = 10.
    nhmax = 49.

    mmin = 1.5
    mmax = 5.

    ptmax = 0.17

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f} && jRecPt<{2:.3f}".format(mmin, mmax, ptmax)

    can = ut.box_canvas()

    hNh = ut.prepare_TH1D("hNh", nhbin, nhmin, nhmax)
    hNhMC = ut.prepare_TH1D("hNhMC", nhbin, nhmin, nhmax)

    ut.put_yx_tit(hNhMC, "Events / ({0:.0f} hit)".format(nhbin), "Tracks number of hits", 1.7)

    ut.set_margin_lbtr(gPad, 0.12, 0.08, 0.01, 0.01)

    tree.Draw("jT0nHits >> hNh", strsel)
    tree.Draw("jT1nHits >>+hNh", strsel)
    mctree.Draw("jT0nHits >> hNhMC", strsel)
    mctree.Draw("jT1nHits >>+hNhMC", strsel)
    ut.norm_to_data(hNhMC, hNh, rt.kBlue)

    hNhMC.Draw()
    hNh.Draw("e1same")
    hNhMC.Draw("same")

    leg = ut.prepare_leg(0.57, 0.8, 0.14, 0.16, 0.03)
    ut.add_leg_pt_mass(leg, ptmax, mmin, mmax)
    leg.AddEntry(hNh, "Data")
    leg.AddEntry(hNhMC, "MC", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hNh, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_tracks_nhits

#_____________________________________________________________________________
def plot_tracks_chi2():

    #tracks reduced chi2
    cbin = 0.05
    cmin = 0.
    cmax = 4.

    mmin = 2.8
    mmax = 3.2

    ptmax = 0.17

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f} && jRecPt<{2:.3f}".format(mmin, mmax, ptmax)

    can = ut.box_canvas()

    hChi2 = ut.prepare_TH1D("hChi2", cbin, cmin, cmax)
    hChi2MC = ut.prepare_TH1D("hChi2MC", cbin/3., cmin, cmax)

    ut.put_yx_tit(hChi2MC, "Events / {0:.2f}".format(cbin), "Tracks reduced #chi^{2}")

    ut.set_margin_lbtr(gPad, 0.1, 0.08, 0.01, 0.01)

    tree.Draw("jT0chi2 >> hChi2", strsel)
    tree.Draw("jT1chi2 >>+hChi2", strsel)
    mctree.Draw("jT0chi2 >> hChi2MC", strsel)
    mctree.Draw("jT1chi2 >>+hChi2MC", strsel)
    ut.norm_to_data(hChi2MC, hChi2, rt.kBlue)

    hChi2MC.Draw()
    hChi2.Draw("e1same")
    hChi2MC.Draw("same")

    leg = ut.prepare_leg(0.64, 0.8, 0.14, 0.16, 0.03)
    ut.add_leg_pt_mass(leg, ptmax, mmin, mmax)
    leg.AddEntry(hChi2, "Data")
    leg.AddEntry(hChi2MC, "MC", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hChi2, 0.3, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_tracks_chi2

#_____________________________________________________________________________
def plot_tracks_dca():

    #tracks dca to primary vertex along z
    dcabin = 0.02
    dcamin = -1.
    dcamax = 1.

    mmin = 1.5
    mmax = 5.

    ptmax = 0.17

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f} && jRecPt<{2:.3f}".format(mmin, mmax, ptmax)

    can = ut.box_canvas()

    hDca = ut.prepare_TH1D("hDca", dcabin, dcamin, dcamax)
    hDcaMC = ut.prepare_TH1D("hDcaMC", dcabin/3, dcamin, dcamax)

    ut.put_yx_tit(hDcaMC, "Events / ({0:.2f} cm)".format(dcabin), "Tracks dca in #it{z} to prim. vtx (cm)")

    ut.set_margin_lbtr(gPad, 0.1, 0.08, 0.01, 0.01)

    tree.Draw("jT0dcaZ >> hDca", strsel)
    tree.Draw("jT1dcaZ >>+hDca", strsel)
    mctree.Draw("jT0dcaZ >> hDcaMC", strsel)
    mctree.Draw("jT1dcaZ >>+hDcaMC", strsel)
    ut.norm_to_data(hDcaMC, hDca, rt.kBlue)

    hDcaMC.Draw()
    hDca.Draw("e1same")
    hDcaMC.Draw("same")

    leg = ut.prepare_leg(0.67, 0.8, 0.14, 0.16, 0.03)
    ut.add_leg_pt_mass(leg, ptmax, mmin, mmax)
    leg.AddEntry(hDca, "Data")
    leg.AddEntry(hDcaMC, "MC", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hDca, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_tracks_dca

#_____________________________________________________________________________
def plot_tracks_phi():

    #tracks pseudorapidity
    phibin = 0.8
    phimax = 4.

    mmin = 1.5
    mmax = 5.

    ptmax = 0.17

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f} && jRecPt<{2:.3f}".format(mmin, mmax, ptmax)

    can = ut.box_canvas()

    hPhi = ut.prepare_TH1D("hPhi", phibin, -phimax, phimax)
    hPhiMC = ut.prepare_TH1D("hPhiMC", phibin/3., -phimax, phimax)

    ut.put_yx_tit(hPhi, "Events / {0:.1f}".format(phibin), "Tracks azimuthal angle")

    ut.set_margin_lbtr(gPad, 0.1, 0.08, 0.014, 0.01)

    hPhi.SetMaximum(520)

    tree.Draw("jT0phi >> hPhi", strsel)
    tree.Draw("jT1phi >>+hPhi", strsel)
    mctree.Draw("jT0phi >> hPhiMC", strsel)
    mctree.Draw("jT1phi >>+hPhiMC", strsel)
    ut.norm_to_data(hPhiMC, hPhi, rt.kBlue)

    hPhi.Draw()
    hPhiMC.Draw("same")

    leg = ut.prepare_leg(0.67, 0.8, 0.14, 0.16, 0.03)
    ut.add_leg_pt_mass(leg, ptmax, mmin, mmax)
    leg.AddEntry(hPhi, "Data")
    leg.AddEntry(hPhiMC, "MC", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hPhi, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_tracks_phi

#_____________________________________________________________________________
def plot_tracks_eta():

    #tracks pseudorapidity
    etabin = 0.09
    etamax = 1.1

    mmin = 2.8
    mmax = 3.2

    ptmax = 0.18

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f} && jRecPt<{2:.3f}".format(mmin, mmax, ptmax)

    can = ut.box_canvas()

    hEta = ut.prepare_TH1D("hEta", etabin, -etamax, etamax)
    hEtaMC = ut.prepare_TH1D("hEtaMC", etabin/2., -etamax, etamax)

    ut.put_yx_tit(hEta, "Events / {0:.2f}".format(etabin), "Tracks pseudorapidity")

    ut.set_margin_lbtr(gPad, 0.1, 0.08, 0.014, 0.01)

    hEta.SetMaximum(100) # 220

    tree.Draw("jT0eta >> hEta", strsel)
    tree.Draw("jT1eta >>+hEta", strsel)
    mctree.Draw("jT0eta >> hEtaMC", strsel)
    mctree.Draw("jT1eta >>+hEtaMC", strsel)
    ut.norm_to_data(hEtaMC, hEta, rt.kBlue)

    hEta.Draw()
    hEtaMC.Draw("same")

    leg = ut.prepare_leg(0.64, 0.8, 0.14, 0.16, 0.03)
    ut.add_leg_pt_mass(leg, ptmax, mmin, mmax)
    leg.AddEntry(hEta, "Data")
    leg.AddEntry(hEtaMC, "MC", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hEta, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_tracks_eta

#_____________________________________________________________________________
def plot_y():

    #reconstructed rapidity
    ybin = 0.1
    ymax = 1.3

    mmin = 1.5
    mmax = 5

    ptmax = 0.17

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f} && jRecPt<{2:.3f}".format(mmin, mmax, ptmax)

    can = ut.box_canvas()

    hY = ut.prepare_TH1D("hY", ybin, -ymax, ymax)
    hYMC = ut.prepare_TH1D("hYMC", ybin/2., -ymax, ymax)

    ut.put_yx_tit(hY, "Events / {0:.1f}".format(ybin), "Dilepton rapidity")

    ut.set_margin_lbtr(gPad, 0.1, 0.08, 0.01, 0.01)

    tree.Draw("jRecY >> hY", strsel)
    mctree.Draw("jRecY >> hYMC", strsel)
    ut.norm_to_data(hYMC, hY, rt.kBlue)

    hY.Draw()
    hYMC.Draw("same")

    leg = ut.prepare_leg(0.67, 0.8, 0.14, 0.16, 0.03)
    ut.add_leg_pt_mass(leg, ptmax, mmin, mmax)
    leg.AddEntry(hY, "Data")
    leg.AddEntry(hYMC, "MC", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hY, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_y

#_____________________________________________________________________________
if __name__ == "__main__":

    #data
    basedir = "../../../star-upc-data/ana/muDst/muDst_run1/sel5"
    infile = "ana_muDst_run1_all_sel5z.root"
    #infile = "ana_muDst_run1_all_sel5z_nDphi.root"

    #MC
    #basedir_mc = "../../../star-upc-data/ana/starsim/slight14e/sel5"
    #infile_mc = "ana_slight14e1x1_sel5z.root"
    #infile_mc = "ana_slight14e3_sel5z.root"
    #infile_mc = "ana_slight14e1x1_sel5z_nDphi.root"
    #infile_mc = "ana_slight14e2x1_sel5_nzvtx.root"
    #basedir_mc = "../../../star-upc-data/ana/starsim/sartre14a/sel5"
    #infile_mc = "ana_sartre14a1_sel5z_s6_v2.root"
    #infile_mc = "ana_sartre14a1_sel5z_tof.root"
    #infile_mc = "ana_sartre14a1_sel5z_bemcmc.root"

    #basedir_mc = "../../../star-upc-data/ana/starsim/slight14e/sel5"
    #infile_mc = "ana_slight14e1x2_s6_sel5z.root"

    basedir_mc = "../../../star-upc-data/ana/starsim/bgen14a/sel5"
    infile_mc = "ana_bgen14a1_v0_sel5z_s6.root"

    interactive = False

    if interactive == False: gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    iplot = 11
    funclist = []
    funclist.append(plot_y) # 0
    funclist.append(plot_tracks_eta) # 1
    funclist.append(plot_tracks_phi) # 2
    funclist.append(plot_tracks_dca) # 3
    funclist.append(plot_tracks_chi2) # 4
    funclist.append(plot_tracks_nhits) # 5
    funclist.append(plot_dvtx_mc) # 6
    funclist.append(plot_dphi_bemc) # 7
    funclist.append(plot_jpsi_pt) # 8
    funclist.append(plot_jpsi_pt2) # 9
    funclist.append(plot_jpsi_logPt2) # 10
    funclist.append(plot_rec_gen_pt2) # 11
    funclist.append(plot_rec_minus_gen_pt2) # 12
    funclist.append(plot_rec_gen_LogPt2) # 13
    funclist.append(plot_rec_minus_gen_pt) # 14
    funclist.append(plot_rec_gen_pt_relative) # 15
    funclist.append(plot_rec_gen_track_pt) # 16
    funclist.append(plot_rec_gen_track_eta) # 17
    funclist.append(plot_rec_gen_track_phi) # 18

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


