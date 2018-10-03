#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TH1D
from ROOT import RooRealVar, RooDataSet, RooArgSet, RooArgList, RooDataHist
from ROOT import RooGaussian, RooAddPdf
from ROOT import RooFit as rf

import sys
sys.path.append('../')
import plot_utils as ut
from parameter_descriptor import parameter_descriptor as pdesc

#_____________________________________________________________________________
if __name__ == "__main__":

    basedir = "../../../star-upc-data/ana/muDst/muDst_run1/sel5"
    infile = "ana_muDst_run1_all_sel5.root"

    vbin = 2.5
    vmin = -160
    vmax = 210

    fitran = [-60, 110]

    binned = True

    #fraction of events with valid ZDC vertex
    f_4s = 0.575

    #colM = rt.kMagenta
    colM = rt.kBlue
    col0 = rt.kRed
    #colLR = rt.kGreen
    colLR = rt.kGreen+1

    #get input
    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("jAllTree")

    gROOT.SetBatch()

    #output log file
    out = open("out.txt", "w")
    #log fit parameters
    loglist1 = [(x,eval(x)) for x in ["infile", "vbin", "vmin", "vmax"]]
    loglist2 = [(x,eval(x)) for x in ["fitran", "binned", "f_4s"]]
    strlog = ut.make_log_string(loglist1, loglist2)
    ut.log_results(out, strlog+"\n")

    #input data
    nbins, vmax = ut.get_nbins(vbin, vmin, vmax)
    z = RooRealVar("jZDCVtxZ", "z", vmin, vmax)
    z.setRange("fitran", fitran[0], fitran[1])
    data = RooDataSet("data", "data", tree, RooArgSet(z))
    hZdc = TH1D("hZdc", "hZdc", nbins, vmin, vmax)
    tree.Draw("jZDCVtxZ >> hZdc")
    dataH = RooDataHist("dataH", "dataH", RooArgList(z), hZdc)

    #fit model
    #middle Gaussian
    m0 = RooRealVar("m0", "m0", 27, vmin, vmax)
    sig0 = RooRealVar("sig0", "sig0", 20, vmin, vmax)
    g0 = RooGaussian("g0", "g0", z, m0, sig0)
    #left Gaussian
    mL = RooRealVar("mL", "mL", -36, vmin, vmax)
    sigL = RooRealVar("sigL", "sigL", 25, vmin, vmax)
    gL = RooGaussian("gL", "gL", z, mL, sigL)
    #right Gaussian
    mR = RooRealVar("mR", "mR", 88, vmin, vmax)
    sigR = RooRealVar("sigR", "sigR", 27, vmin, vmax)
    gR = RooGaussian("gR", "gR", z, mR, sigR)
    #model from the Gaussians
    ndat = data.reduce("jZDCVtxZ>{0:.3f} && jZDCVtxZ<{1:.3f}".format(fitran[0], fitran[1])).numEntries()
    n0 = RooRealVar("n0", "n0", ndat/2.1, 0, ndat)
    nL = RooRealVar("nL", "nL", ndat/2.7, 0, ndat)
    nR = RooRealVar("nR", "nR", ndat/3., 0, ndat)
    model = RooAddPdf("model", "model", RooArgList(g0, gL, gR), RooArgList(n0, nL, nR))
    #model = RooAddPdf("model", "model", RooArgList(g0, gL), RooArgList(n0, nL))
    #model = RooAddPdf("model", "model", RooArgList(g0, gR), RooArgList(n0, nR))

    #make the fit
    if binned == True:
        r1 = model.fitTo(dataH, rf.Range("fitran"), rf.Save())
    else:
        r1 = model.fitTo(data, rf.Range("fitran"), rf.Save())

    #log fit results
    ut.log_results(out, ut.log_fit_result(r1))

    #fraction of all events in the middle Gaussian
    nall = float(tree.GetEntries())*f_4s
    ut.log_results(out, "Fraction of all events in the middle Gaussian:")
    ut.log_results(out, "nall, uncorrected: "+str(tree.GetEntries()))
    ut.log_results(out, "nall: "+str(nall))
    ut.log_results(out, "n0: "+str(n0.getVal()))
    ut.log_results(out, "n0/nall: {0:.3f}".format(n0.getVal()/nall))
    print "nall:", nall
    print "n0:", n0.getVal()
    print "n0/nall", n0.getVal()/nall

    #make the plot
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    can = ut.box_canvas()
    gPad.SetRightMargin(0.02)
    gPad.SetTopMargin(0.04)
    gPad.SetBottomMargin(0.09)
    gPad.SetLeftMargin(0.1)

    frame = z.frame(rf.Bins(nbins), rf.Title(""))
    frame.SetTitle("")
    frame.GetXaxis().SetTitleOffset(1.2);
    frame.GetYaxis().SetTitleOffset(1.4);

    if binned == True:
        dataH.plotOn(frame, rf.Name("data"))
    else:
        data.plotOn(frame, rf.Name("data"))

    model.plotOn(frame, rf.Name("g0"), rf.Components("g0"), rf.LineColor(col0))
    model.plotOn(frame, rf.Name("gL"), rf.Components("gL"), rf.LineColor(colLR))
    model.plotOn(frame, rf.Name("gR"), rf.Components("gR"), rf.LineColor(colLR))
    model.plotOn(frame, rf.Name("Model"), rf.LineColor(colM))

    frame.SetXTitle("ZDC vertex along #it{z} (cm)")
    frame.SetYTitle("Events / {0:.1f} cm".format(vbin))

    print "chi2/ndf:", frame.chiSquare("Model", "data", 9)

    frame.Draw()

    #put fit parameters
    desc = pdesc(frame, 0.15, 0.85, 0.045)
    desc.set_text_size(0.03)
    desc.itemD("#chi^{2}/ndf", frame.chiSquare("Model", "data", 9), -1, colM)
    desc.prec = 0
    desc.itemR("norm", n0, col0)
    desc.prec = 3
    desc.itemR("#it{#mu}", m0, col0)
    desc.itemR("#it{#sigma}", sig0, col0)
    desc.draw()

    ut.invert_col(gPad)
    can.SaveAs("01fig.pdf")

    #to prevent 'pure virtual method called'
    gPad.Close()

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")













