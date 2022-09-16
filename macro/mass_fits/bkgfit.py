#!/usr/bin/python3

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TH1D
from ROOT import RooDataSet, RooArgSet, RooDataHist, RooArgList
from ROOT import RooFit as rf

import sys
sys.path.append('../')
import plot_utils as ut
from parameter_descriptor import parameter_descriptor as pdesc

from fit_functions import m, y, pT
from fit_functions import lam, c1, c2, bkgd
from fit_functions import lamF, c1f, c2f, bkgd_f

#_____________________________________________________________________________
if __name__ == "__main__":

    basedir = "../../../star-upc-data/ana/starsim"

    #infile = "slight14d/sel3/ana_slight14d2_sel3.root"
    #infile = "slight14d/sel3/ana_slight14d2_sel3b.root"
    infile = "slight14e/sel5/ana_slight14e2x1_sel5_nzvtx.root"
    #infile = "slight14e/sel5/ana_slight14e2x1_s6_sel5z.root"

    mbin = 0.08
    mmin = 0.9
    mmax = 5.

    fitran = [1.4, mmax] # 1.4  2

    ymin = -1.
    ymax = 1.

    ptmax = 0.18

    binned = False

    #cbkg = rt.kMagenta
    cbkg = rt.kBlue

    #-- end of config --


    #load the input
    gROOT.SetBatch()
    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("jRecTree")

    #output log file
    out = open("out.txt", "w")
    #log fit parameters
    loglist1 = [(x,eval(x)) for x in ["infile", "mbin", "mmin", "mmax"]]
    loglist2 = [(x,eval(x)) for x in ["ymin", "ymax", "ptmax", "fitran", "binned"]]
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
    c1.setVal(fitran[0])
    if binned == True:
        r1 = bkgd.fitTo(dataH, rf.Range("fitran"), rf.Save())
    else:
        r1 = bkgd.fitTo(data, rf.Range("fitran"), rf.Save())

    #log fit results
    ut.log_results(out, ut.log_fit_result(r1))
    ut.log_results(out, "Fit parameters in 3-digits:")
    ut.log_results(out, ut.log_fit_parameters(r1, 0))

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

    #plot the data
    if binned == True:
        dataH.plotOn(frame, rf.Name("data"))
    else:
        data.plotOn(frame, rf.Name("data"))

    #plot background function as determined from the fit
    bkgd.plotOn(frame, rf.Range("fitran"), rf.LineColor(cbkg), rf.Name("Background"))

    #background function from the data
    #lamF.setVal(-1.055)
    #c1f.setVal(1.338)
    #c2f.setVal(0.172)
    lamF.setVal(-1.0517)
    c1f.setVal(1.3399)
    c2f.setVal(0.16973)
    bkgd_f.plotOn(frame, rf.Range("fitran"), rf.LineColor(rt.kRed), rf.Name("Background_f"))

    frame.Draw()

    frame.SetXTitle("#it{m}_{e^{+}e^{-}} (GeV/#it{c}^{2})")
    frame.SetYTitle( "Dielectron counts / (%.0f MeV/#it{c}^{2})" % (1000.*mbin) )

    #fit parameters on the plot
    desc = pdesc(frame, 0.75, 0.78, 0.045); #x, y, sep
    desc.set_text_size(0.03)
    desc.itemD("#chi^{2}/ndf", frame.chiSquare("Background", "data", 3), -1, cbkg)
    desc.itemR("#lambda", lam, cbkg)
    desc.itemR("#it{c}_{1}", c1, cbkg)
    desc.itemR("#it{c}_{2}", c2, cbkg)
    desc.draw()

    #legend for data and fit function
    bkgfunc = "(#it{m}-#it{c}_{1})#it{e}^{#lambda(#it{m}-#it{c}_{1})^{2}+#it{c}_{2}(#it{m}-#it{c}_{1})^{3}}"
    hx = ut.prepare_TH1D("hx", 1, 0, 1)
    lx = ut.col_lin(cbkg)
    leg = ut.prepare_leg(0.58, 0.82, 0.39, 0.1, 0.029) # x, y, dx, dy, tsiz
    leg.SetMargin(0.1)
    leg.AddEntry(hx, "MC #gamma#gamma#rightarrow e^{+}e^{-}") # , "lp"
    leg.AddEntry(lx, "#it{f}_{#gamma#gamma}(#it{m}) = "+bkgfunc, "l")
    leg.Draw("same")

    #legend for shape from the data
    leg2 = ut.prepare_leg(0.7, 0.55, 0.25, 0.04, 0.029)
    leg2.SetMargin(0.17)
    lx2 = ut.col_lin(rt.kRed)
    leg2.AddEntry(lx2, "Shape from data", "l")
    leg2.Draw("same")

    #ut.invert_col(gPad)
    can.SaveAs("01fig.pdf")

    #to prevent 'pure virtual method called'
    gPad.Close()

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")






















