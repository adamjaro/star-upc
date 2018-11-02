#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TH1D
from ROOT import RooDataSet, RooArgSet, RooDataHist, RooArgList
from ROOT import RooFit as rf

import sys
sys.path.append('../')
import plot_utils as ut
from parameter_descriptor import parameter_descriptor as pdesc

from fit_functions import m, y, pT, cb, m0, sig, alpha, n

#_____________________________________________________________________________
if __name__ == "__main__":

    basedir = "../../../star-upc-data/ana/starsim"

    #infile = "slight14d/sel5/ana_slight14d1_sel5a.root"
    infile = "slight14e/sel5/ana_slight14e1x1_sel5.root"

    mbin = 0.004
    mmin = 2.
    mmax = 3.6

    fitran = [2., 3.22]

    ymin = -1.
    ymax = 1.

    ptmax = 0.17; # 0.17

    binned = False

    #ccb = rt.kMagenta;
    ccb = rt.kBlue
    lmg = 4; # left margin in text output

    #strdat = "MC coherent #it{J}/#it{#psi}#rightarrow e^{+}e^{-}"
    strdat = "Embedding MC coherent #it{J}/#it{#psi}"

    #-- end of config --


    #get input
    gROOT.SetBatch()
    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("jRecTree")

    #output log file
    out = open("out.txt", "w")
    #log fit parameters
    loglist1 = [(x,eval(x)) for x in ["infile", "mbin", "mmin", "mmax"]]
    loglist2 = [(x,eval(x)) for x in ["ymin", "ymax", "ptmax", "binned", "fitran[0]", "fitran[1]"]]
    strlog = ut.make_log_string(loglist1, loglist2)
    ut.log_results(out, strlog+"\n")

    #unbinned and binned input data
    nbins, mmax = ut.get_nbins(mbin, mmin, mmax)
    strsel = "jRecY>{0:.3f} && jRecY<{1:.3f} && jRecPt<{2:.3f}".format(ymin, ymax, ptmax)
    #unbinned data
    m.setMin(mmin)
    m.setMax(mmax)
    m.setRange("fitran", fitran[0], fitran[1])
    dataIN = RooDataSet("data", "data", tree, RooArgSet(m,y,pT));
    data = dataIN.reduce(strsel);
    #binned data
    hMass = TH1D("hMass", "hMass", nbins, mmin, mmax)
    tree.Draw("jRecM >> hMass", strsel)
    dataH = RooDataHist("dataH", "dataH", RooArgList(m), hMass)

    #make the fit
    if binned == True:
        r1 = cb.fitTo(dataH, rf.Range("fitran"), rf.Save())
    else:
        r1 = cb.fitTo(data, rf.Range("fitran"), rf.Save())

    #log fit results
    ut.log_results(out, ut.log_fit_result(r1))
    ut.log_results(out, "Alpha and n in 3-digits:")
    ut.log_results(out, "{0:6} {1:.3f} +/- {2:.3f}".format("alpha:", alpha.getVal(), alpha.getError()))
    ut.log_results(out, "{0:6} {1:.3f} +/- {2:.3f}".format("n:", n.getVal(), n.getError()))

    #create the plot
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    can = ut.box_canvas()
    gPad.SetRightMargin(0.02)
    gPad.SetTopMargin(0.04)
    gPad.SetBottomMargin(0.09)
    gPad.SetLeftMargin(0.11)

    frame = m.frame(rf.Bins(nbins), rf.Title(""))
    frame.SetTitle("")
    frame.GetXaxis().SetTitleOffset(1.2);
    frame.GetYaxis().SetTitleOffset(1.6);

    if binned == True:
        dataH.plotOn(frame, rf.Name("data"))
    else:
        data.plotOn(frame, rf.Name("data"))

    cb.plotOn(frame, rf.Precision(1e-6), rf.Name("CrystalBall"), rf.LineColor(ccb))
    frame.Draw()

    frame.SetXTitle("#it{m}_{e^{+}e^{-}} (GeV)")
    frame.SetYTitle( "Dielectron counts / ({0:.0f} MeV)".format(1000.*mbin) )

    #fit parameters on the plot
    desc = pdesc(frame, 0.18, 0.8, 0.057); #x, y, sep
    desc.set_text_size(0.03)

    desc.itemD("#chi^{2}/ndf", frame.chiSquare("CrystalBall", "data", 4), -1, ccb)
    desc.prec = 4
    desc.itemR("#it{m}_{0}", m0, ccb)
    desc.itemR("#sigma", sig, ccb)
    desc.prec = 3
    desc.itemR("#alpha", alpha, ccb)
    desc.itemR("#it{n}", n, ccb)
    desc.draw()

    leg = ut.prepare_leg(0.16, 0.85, 0.35, 0.08, 0.029) # x, y, dx, dy, tsiz
    leg.SetMargin(0.14)
    hx = ut.prepare_TH1D("hx", 1, 0, 1)
    leg.AddEntry(hx, strdat)
    leg.Draw("same")

    leg2 = ut.prepare_leg(0.75, 0.8, 0.21, 0.12, 0.03) # x, y, dx, dy, tsiz
    leg2.SetMargin(0.05)
    leg2.AddEntry(0, "#bf{%2.1f < #it{y} < %2.1f}" % (ymin, ymax), "")
    leg2.AddEntry(0, "#bf{#it{p}_{T} < %.3f GeV}" % ptmax, "")
    leg2.Draw("same")

    #ut.invert_col(gPad)
    can.SaveAs("01fig.pdf")

    #to prevent 'pure virtual method called'
    gPad.Close()

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")














