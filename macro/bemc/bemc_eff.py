#!/usr/bin/python

import math
from time import time

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TH1D
from ROOT import TGraphAsymmErrors, TMath, TF1
from ROOT import vector, double, AddressOf

import sys
sys.path.append('../')
import plot_utils as ut
from parameter_descriptor import parameter_descriptor as pdesc

#_____________________________________________________________________________
def get_bins(tree, bnam, bmatch, prec, ons, delt):

    #load tracks momenta to lists for all and matched tracks

    tree.SetBranchStatus("*", 0)
    tree.SetBranchStatus(bnam[0], 1)
    tree.SetBranchStatus(bnam[1], 1)
    tree.SetBranchStatus(bmatch[0], 1)
    tree.SetBranchStatus(bmatch[1], 1)

    #C++ structure for tree entry
    gROOT.ProcessLine("struct Entry {Double_t p0, p1; Bool_t match0, match1;};")
    entry = rt.Entry()
    tree.SetBranchAddress(bnam[0], AddressOf(entry, "p0"))
    tree.SetBranchAddress(bnam[1], AddressOf(entry, "p1"))
    tree.SetBranchAddress(bmatch[0], AddressOf(entry, "match0"))
    tree.SetBranchAddress(bmatch[1], AddressOf(entry, "match1"))

    #momenta values for all and matched tracks
    valAll = rt.list(double)()
    valSel = rt.list(double)()

    for i in xrange(tree.GetEntriesFast()):
        tree.GetEntry(i)
        valAll.push_back(entry.p0)
        valAll.push_back(entry.p1)
        if entry.match0 == 1: valSel.push_back(entry.p0)
        if entry.match1 == 1: valSel.push_back(entry.p1)

    tree.ResetBranchAddresses()

    #bin edges
    bins = vector(rt.double)()

    t0 = time()

    #runs faster when the algorithm is in plain ROOT
    gROOT.LoadMacro("get_bins.C")
    rt.get_bins(bins, valAll, valSel, prec, ons, delt)

    t1 = time()
    print "Time to calculate the bins (sec):", t1-t0

    return bins

#_____________________________________________________________________________
def fitFuncErf(xVal, par):

    return par[3]+par[0]*(1.+TMath.Erf((xVal[0]-par[1])/par[2]/TMath.Sqrt(2.)))


#_____________________________________________________________________________
if __name__ == "__main__":

    basedir = "../../../star-upc-data/ana/muDst"
    #basedir = "../../../star-upc-data/ana/starsim"

    infile = "muDst_run1a/conv0/ana_muDst_run1a_all_conv0.root"
    #infile = "slight14d/sel3/ana_slight14d2_sel3a.root"

    precision = 0.06   # 0.06  0.01
    onset = -0.03
    delta = 1.e-7

    logx = True

    #branches with momentum at BEMC and matching information
    bnam = ["jT0bemcP", "jT1bemcP"]
    bmatch = ["jT0matchBemc", "jT1matchBemc"]

    #selection for basic input range
    strsel = ""
    #strsel = bnam[0]+"<5 && "+bnam[1]+"<5"
    #strsel += " && "+bnam[0]+">0.4 && "+bnam[1]+">0.4"

    #line color for fit
    #clin = rt.kMagenta
    clin = rt.kBlue

    #-- end of config --


    gROOT.SetBatch()

    #output temporary file
    outnam = "tmp.root"
    #input and output
    inp = TFile.Open(basedir+"/"+infile)
    outfile = TFile.Open(outnam, "recreate")

    #output log file
    out = open("out.txt", "w")
    strlog = "in "+infile+" precision "+str(precision)+" onset "+str(onset)
    strlog += " delta "+str(delta)
    ut.log_results(out, strlog+"\n")

    #get input tree, apply the selection
    tree = inp.Get("jRecTree").CopyTree(strsel)

    # bin edges
    bins = get_bins(tree, bnam, bmatch, precision, onset, delta)

    #momenta and efficiency histograms
    nbins = len(bins)-1
    hAll = TH1D("hAll", "hAll", nbins, bins.data())
    hSel = TH1D("hSel", "hSel", nbins, bins.data())
    hAll.Sumw2()
    hSel.Sumw2()
    tree.Draw(bnam[0]+" >>  hAll")
    tree.Draw(bnam[1]+" >>+ hAll")
    tree.Draw(bnam[0]+" >>  hSel", bmatch[0]+"==1")
    tree.Draw(bnam[1]+" >>+ hSel", bmatch[1]+"==1")

    #calculate the efficiency
    hEff = TGraphAsymmErrors(hSel, hAll)
    #hEff = TH1D("hEffBemc", "", nbins, bins.data());
    #hEff.Divide(hSel, hAll, 1, 1, "B");

    fitFunc = TF1("fitFunc", fitFuncErf, 0., 10. , 4)
    fitFunc.SetParNames("n", "pthr", "sigma", "e0")
    fitFunc.SetParameters(0.45, 1., 0.3, 0.01)
    fitFunc.FixParameter(3, 0.)

    fitFunc.SetLineColor(clin)
    fitFunc.SetLineWidth(2)
    fitFunc.SetNpx(1000)

    #make the fit
    r1 = ( hEff.Fit(fitFunc, "RS") ).Get()
    out.write(ut.log_tfit_result(r1))

    #log fit parameters in 3-digit precision
    ut.log_results(out, "Fit parameters in 3-digit precision:")
    chistr = "chi2/ndf: {0:.3f}".format(r1.Chi2()/r1.Ndf())
    ut.log_results(out, chistr)
    for ipar in xrange(3):
        nam = fitFunc.GetParName(ipar)
        val = fitFunc.GetParameter(ipar)
        err = fitFunc.GetParError(ipar)
        ut.log_results(out, "{0:9} {1:.3f} +/- {2:.3f}".format(nam+":", val, err))

    #plot the efficiency
    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)

    can = ut.box_canvas()

    if logx == True: gPad.SetLogx()

    gPad.SetTopMargin(0.01)
    gPad.SetRightMargin(0.01)
    gPad.SetBottomMargin(0.12)
    gPad.SetLeftMargin(0.1)

    ut.set_graph(hEff)

    hEff.GetYaxis().SetTitleOffset(1.4)
    hEff.GetXaxis().SetTitleOffset(1.5)

    hEff.GetXaxis().SetTitle("Track momentum #it{p}_{tot} at BEMC (GeV)")
    hEff.GetYaxis().SetTitle("BEMC efficiency")
    hEff.SetTitle("")

    hEff.GetXaxis().SetMoreLogLabels()

    leg = ut.prepare_leg(0.15, 0.82, 0.34, 0.12, 0.03)
    leg.SetMargin(0.17)
    #fitform = "#epsilon_{0} + #it{n}#left[1 + erf#left(#frac{#it{p}_{tot} - #it{p}_{tot}^{thr}}{#sqrt{2}#sigma}#right)#right]"
    fitform = "#it{n}#left[1 + erf#left(#frac{#it{p}_{tot} - #it{p}_{tot}^{thr}}{#sqrt{2}#sigma}#right)#right]"
    leg.AddEntry(fitFunc, fitform, "l")

    #fit parameters on the plot
    desc = pdesc(hEff, 0.035, 0.7, 0.05, 0.002)
    desc.set_text_size(0.03)
    desc.itemD("#chi^{2}/ndf", r1.Chi2()/r1.Ndf(), -1, clin)
    desc.itemRes("#it{n}", r1, 0, clin)
    desc.itemRes("#it{p}_{tot}^{thr}", r1, 1, clin)
    desc.itemRes("#sigma", r1, 2, clin)
    #desc.itemRes("#epsilon_{0}", r1, 3, clin)

    #print "#####", fitFunc.Eval(0.7)

    hEff.Draw("AP")
    #hEff.Draw()
    fitFunc.Draw("same")
    desc.draw()
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

    #to prevent 'pure virtual method called'
    gPad.Close()

    #remove the temporary
    outfile.Close()
    gSystem.Exec("rm -f "+outnam)

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")























