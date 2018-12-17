#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TH1D
from ROOT import RooDataSet, RooArgSet, RooDataHist, RooArgList
from ROOT import RooAddPdf, RooRealVar
from ROOT import RooAbsReal
from ROOT import RooFit as rf

import sys
sys.path.append('../')
import plot_utils as ut
from parameter_descriptor import parameter_descriptor as pdesc

from fit_functions import m, y, pT, cb, m0, sig, alpha, n
from fit_functions import lam, c1, c2, bkgd

#_____________________________________________________________________________
def fixVal(x, val):

    #fix roofit variable to a constant value
    x.setVal(val)
    x.setConstant()

#_____________________________________________________________________________
if __name__ == "__main__":

    basedir = "../../../star-upc-data/ana/muDst"

    infile = "muDst_run1/sel5/ana_muDst_run1_all_sel5z.root"
    inLS = "muDst_run1/sel5/ana_muDst_run1_all_sel5z_ls.root"

    mbin = 0.045
    mmin = 1.12
    mmax = 5.

    ymin = -1.
    ymax = 1.

    ptmax = 0.18

    alphafix = 0.694
    nfix = 3.743

    fitran = [1.45, mmax]

    binned = False

    #integration range
    #intran = [2.1, 2.6]
    #intran = [3.4, 4.6]
    intran = [2.8, 3.2]

    #cmodel = rt.kMagenta
    cmodel = rt.kBlue
    cbkg = rt.kRed
    #ccb = rt.kYellow
    ccb = rt.kGreen+1

    #-- end of config --


    #get the input
    gROOT.SetBatch()
    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("jRecTree")

    #output log file
    out = open("out.txt", "w")
    #log fit parameters
    loglist1 = [(x,eval(x)) for x in ["infile", "inLS"]]
    loglist2 = [(x,eval(x)) for x in ["mbin", "mmin", "mmax", "ymin", "ymax", "ptmax", "binned"]]
    loglist3 = [(x,eval(x)) for x in ["alphafix", "nfix", "fitran", "intran"]]
    strlog = ut.make_log_string(loglist1, loglist2, loglist3)
    ut.log_results(out, strlog+"\n")

    #unbinned and binned input data
    nbins, mmax = ut.get_nbins(mbin, mmin, mmax)
    strsel = "jRecY>{0:.3f} && jRecY<{1:.3f} && jRecPt<{2:.3f}".format(ymin, ymax, ptmax)
    #unbinned data
    m.setMin(mmin)
    m.setMax(mmax)
    m.setRange("fitran", fitran[0], fitran[1])
    m.setRange("intran", intran[0], intran[1])
    dataIN = RooDataSet("data", "data", tree, RooArgSet(m,y,pT));
    data = dataIN.reduce(strsel);
    #binned data
    hMass = TH1D("hMass", "hMass", nbins, mmin, mmax)
    tree.Draw("jRecM >> hMass", strsel)
    dataH = RooDataHist("dataH", "dataH", RooArgList(m), hMass)

    #like-sign data
    inpLS = TFile.Open(basedir+"/"+inLS)
    treeLS = inpLS.Get("jRecTree")
    hMassLS = TH1D("hMassLS", "hMassLS", nbins, mmin, mmax)
    treeLS.Draw("jRecM >> hMassLS", strsel)
    hMassLS.SetFillColor(rt.kRed)
    hMassLS.SetLineColor(hMassLS.GetFillColor())

    #Crystal Ball
    if nfix > 0.: fixVal(n, nfix)
    if alphafix > 0.: fixVal(alpha, alphafix)

    #Background function
    c1.setVal(fitran[0])

    #composite pdf
    nevt = data.numEntries()
    ncb = RooRealVar("ncb", "ncb", nevt/2, 0, nevt)
    nbkg = RooRealVar("nbkg", "nbkg", nevt/2, 0, nevt)
    model = RooAddPdf("model", "model", RooArgList(cb, bkgd), RooArgList(ncb, nbkg))

    #make the fit
    if binned == True:
        r1 = model.fitTo(dataH, rf.Range("fitran"), rf.Save())
    else:
        r1 = model.fitTo(data, rf.Range("fitran"), rf.Save())

    #log fit results
    ut.log_results(out, ut.log_fit_result(r1))

    #integrate fit functions
    mset = RooArgSet(m)
    icb = cb.createIntegral(mset, rf.NormSet(mset), rf.Range("intran"))
    ibkg = bkgd.createIntegral(mset, rf.NormSet(mset), rf.Range("intran"))
    intCB = RooRealVar("intCB", "intCB", 0, nevt)
    intBkg = RooRealVar("intBkg", "intBkg", 0, nevt)
    intCB.setVal(icb.getVal()*ncb.getVal())
    intCB.setError(icb.getVal()*ncb.getError())
    intBkg.setVal(ibkg.getVal()*nbkg.getVal())
    intBkg.setError(ibkg.getVal()*nbkg.getError())

    ut.log_results(out, "Integration range: ["+str(intran[0])+", "+str(intran[1])+"]")
    ut.log_results(out, "CrystalBall integral: {0:.0f} +/- {1:.0f}".format(intCB.getVal(), intCB.getError()))
    ut.log_results(out, "Background integral: {0:.0f} +/- {1:.0f}".format(intBkg.getVal(), intBkg.getError()))

    #create the plot
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    can = ut.box_canvas()
    gPad.SetRightMargin(0.01)
    gPad.SetTopMargin(0.01)
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

    #plot the fit model
    model.plotOn(frame, rf.Precision(1e-6), rf.Name("Model"), rf.LineColor(cmodel))
    model.plotOn(frame, rf.Name("Background"), rf.Components("Background"), rf.LineColor(cbkg), rf.LineStyle(rt.kDashed))#dashdotted
    model.plotOn(frame, rf.Name("CrystalBall"), rf.Components("cb"), rf.LineColor(ccb), rf.LineStyle(rt.kDashDotted), rf.Precision(1e-6))

    #plot the frame
    frame.Draw()
    #plot like-sing data
    hMassLS.Draw("same")
    frame.Draw("same")

    frame.SetXTitle("#it{m}_{e^{+}e^{-}} (GeV/c^{2})")
    frame.SetYTitle( "Dielectron counts / (%.0f MeV/c^{2})" % (1000.*mbin) )

    #legend for fit functions
    leg = ut.prepare_leg(0.16, 0.85, 0.24, 0.1, 0.03)
    lm = ut.col_lin(cmodel, 3)
    lc = ut.col_lin(ccb, 3, rt.kDashDotted)
    lb = ut.col_lin(cbkg, 3, rt.kDashed)
    leg.AddEntry(lm, "Fit model", "l")
    leg.AddEntry(lc, "Crystal Ball", "l")
    leg.AddEntry(lb, "Background", "l")
    leg.Draw("same")

    #legend for data and kinematics interval
    leg2 = ut.prepare_leg(0.73, 0.78, 0.22, 0.17, 0.03)
    leg2.SetMargin(0.17)
    ut.add_leg_y_pt(leg2, ymin, ymax, ptmax)
    hx = ut.prepare_TH1D("hx", 1, 0, 1)
    hx.Draw("same")
    hxLS = ut.prepare_TH1D("hxLS", 1, 0, 1)
    hxLS.SetMarkerColor(rt.kRed)
    hxLS.SetMarkerStyle(21)
    leg2.AddEntry(hx, "unlike sign")
    leg2.AddEntry(hxLS, "like sign", "p")
    leg2.Draw("same")

    #show fit parameters
    desc = pdesc(frame, 0.15, 0.78, 0.045)
    desc.set_text_size(0.03)
    desc.itemD("#chi^{2}/ndf", frame.chiSquare("Model", "data", 7), -1, cmodel)
    desc.prec = 0
    desc.itemR("#it{N}_{CB}", ncb, ccb)
    desc.itemR("#it{N}_{bkg}", nbkg, cbkg)
    desc.prec = 3
    desc.itemR("#it{m}_{0}", m0, ccb)
    desc.itemR("#sigma", sig, ccb)
    if alphafix > 0.:
        desc.itemD("#alpha", alpha.getVal(), -1, ccb)
    else:
        desc.itemR("#alpha", alpha, ccb)
    if nfix > 0.:
        desc.itemD("#it{n}", n.getVal(), -1, ccb)
    else:
        desc.itemR("#it{n}", n, ccb)
    desc.itemR("#lambda", lam, cbkg)
    desc.itemR("#it{c}_{1}", c1, cbkg)
    desc.itemR("#it{c}_{2}", c2, cbkg)
    desc.draw()

    #integration range
    lin_lo = ut.cut_line(intran[0], 0.33, frame)
    lin_hi = ut.cut_line(intran[1], 0.33, frame)
    lin_lo.Draw("same")
    lin_hi.Draw("same")

    #integration result
    desc2 = pdesc(frame, 0.77, 0.6, 0.045)
    desc2.prec = 0
    desc2.itemD("#int_{%.1f}^{%.1f}#it{#gamma#gamma}" % (intran[0], intran[1]), intBkg.getVal(), intBkg.getError(), cbkg)
    desc2.draw()

    #ut.invert_col(gPad)
    can.SaveAs("01fig.pdf")

    #to prevent 'pure virtual method called'
    gPad.Close()

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")


























