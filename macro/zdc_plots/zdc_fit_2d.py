#!/usr/bin/python

import code

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import RooRealVar, RooDataSet, RooArgSet
from ROOT import RooDataHist
from ROOT import TBuffer3D
from ROOT import RooFit as rf

import sys
sys.path.append('../')
import plot_utils as ut

from fit_func import Model2D
from plot_pdf import PlotPdf

#_____________________________________________________________________________
def plot_projection(frame, ew):

    xtit = ["ZDC East ADC", "ZDC West ADC"]

    frame.SetXTitle(xtit[ew])

    frame.GetXaxis().SetTitleOffset(1.2)
    frame.GetYaxis().SetTitleOffset(1.4)

    gPad.SetTopMargin(0.01)
    gPad.SetRightMargin(0.01)
    gPad.SetBottomMargin(0.1)
    gPad.SetLeftMargin(0.1)

    frame.Draw()

#_____________________________________________________________________________
def plot_2d(plot_pdf):

    plot_pdf.pdf.GetXaxis().SetTitleOffset(2.3)
    plot_pdf.pdf.GetYaxis().SetTitleOffset(1.9)
    plot_pdf.pdf.GetZaxis().SetTitleOffset(1.7)

    gPad.SetTopMargin(0.01)
    gPad.SetRightMargin(0.05)
    gPad.SetBottomMargin(0.11)
    gPad.SetLeftMargin(0.12)

    plot_pdf.plot()

    gPad.SetPhi(-125.)
    gPad.Update()

#_____________________________________________________________________________
def make_fit():

    adc_bin = 18  #18 for low-m gg, 20 for jpsi
    adc_min = 10.
    adc_max = 700.

    ptmax = 0.17
    #mmin = 1.6
    #mmax = 2.6
    mmin = 1.5
    mmax = 5.

    #east/west projections and 2D plot
    ew = 0
    p2d = 1

    #plot colors
    model_col = rt.kMagenta
    model_col = rt.kBlue

    out = open("out.txt", "w")
    lmg = 6
    ut.log_results(out, "in "+infile, lmg)
    strlog = "adc_bin " + str(adc_bin) + " adc_min " + str(adc_min) + " adc_max " + str(adc_max)
    strlog += " ptmax " + str(ptmax) + " mmin " + str(mmin) + " mmax " + str(mmax)
    ut.log_results(out, strlog, lmg)

    #adc distributions
    adc_east = RooRealVar("jZDCUnAttEast", "ZDC ADC east", adc_min, adc_max)
    adc_west = RooRealVar("jZDCUnAttWest", "ZDC ADC west", adc_min, adc_max)
    #kinematics variables
    m = RooRealVar("jRecM", "e^{+}e^{-} mass (GeV)", 0., 10.)
    y = RooRealVar("jRecY", "rapidity", -1., 1.)
    pT = RooRealVar("jRecPt", "pT", 0., 10.)

    strsel = "jRecPt<{0:.3f} && jRecM>{1:.3f} && jRecM<{2:.3f}".format(ptmax, mmin, mmax)
    data_all = RooDataSet("data", "data", tree, RooArgSet(adc_east, adc_west, m, y, pT))
    data = data_all.reduce(strsel)

    model = Model2D(adc_east, adc_west)

    r1 = model.model.fitTo(data, rf.Save())

    ut.log_results(out, ut.log_fit_result(r1), lmg)
    ut.log_results(out, "Fit parameters:\n", lmg)
    out.write(ut.log_fit_parameters(r1, lmg+2)+"\n")
    #out.write(ut.table_fit_parameters(r1))

    #print ut.table_fit_parameters(r1)

    #create the plot
    can = ut.box_canvas()

    nbins, adc_max = ut.get_nbins(adc_bin, adc_min, adc_max)
    adc_east.setMax(adc_max)
    adc_west.setMax(adc_max)
    frame_east = adc_east.frame(rf.Bins(nbins), rf.Title(""))
    frame_west = adc_west.frame(rf.Bins(nbins), rf.Title(""))

    data.plotOn(frame_east, rf.Name("data"))
    model.model.plotOn(frame_east, rf.Precision(1e-6), rf.Name("model"), rf.LineColor(model_col))

    data.plotOn(frame_west, rf.Name("data"))
    model.model.plotOn(frame_west, rf.Precision(1e-6), rf.Name("model"), rf.LineColor(model_col))

    ytit = "Events / ({0:.0f} ADC units)".format(adc_bin)
    frame_east.SetYTitle(ytit)
    frame_west.SetYTitle(ytit)
    frame_east.SetTitle("")
    frame_west.SetTitle("")

    frame = [frame_east, frame_west]
    if p2d == 0: plot_projection(frame[ew], ew)

    plot_pdf = PlotPdf(model, adc_east, adc_west)
    if p2d == 1: plot_2d(plot_pdf)

    lhead = ["east ZDC", "west ZDC"]
    if p2d == 1:
        leg = ut.prepare_leg(0.01, 0.9, 0.3, 0.1, 0.03)
    else:
        leg = ut.prepare_leg(0.66, 0.8, 0.32, 0.13, 0.03)
    if p2d == 0: leg.AddEntry(None, "#bf{Projection to "+lhead[ew]+"}", "")
    leg.SetMargin(0.05)
    leg.AddEntry(None, "#bf{#it{p}_{T} < "+"{0:.2f}".format(ptmax)+" GeV}", "")
    mmin_fmt = "{0:.1f}".format(mmin)
    mmax_fmt = "{0:.1f}".format(mmax)
    leg.AddEntry(None, "#bf{"+mmin_fmt+" < #it{m}_{e^{+}e^{-}} < "+mmax_fmt+" GeV}", "")
    leg.Draw("same")

    #ut.print_pad(gPad)

    #b3d = TBuffer3D(0)
    #b3d = None
    #gPad.GetViewer3D().OpenComposite(b3d)
    #print b3d

    #print "All input: ", data.numEntries()
    #print "All input: 858"
    #all input data
    nall = float(tree.Draw("", strsel))
    print "All input: ", nall
    print "1n1n events: ", model.num_1n1n.getVal()
    ratio_1n1n = float(model.num_1n1n.getVal())/nall
    print "Ratio 1n1n / all: ", ratio_1n1n
    ut.log_results(out, "Fraction of 1n1n events:\n", lmg)
    ut.log_results(out, "All input: "+str(nall), lmg)
    ut.log_results(out, "1n1n events: "+str(model.num_1n1n.getVal()), lmg)
    ut.log_results(out, "Ratio 1n1n / all: "+str(ratio_1n1n), lmg)

    #ut.invert_col(gPad)
    can.SaveAs("01fig.pdf")

    if interactive == True: start_interactive()

#_____________________________________________________________________________
def start_interactive():

    vars = globals()
    vars.update(locals())
    shell = code.InteractiveConsole(vars)
    shell.interact()

#_____________________________________________________________________________
if __name__ == "__main__":

    #basedir = "../../ana/muDst/muDst_run1/sel3"
    #infile = "ana_muDst_run1_all_sel3z.root"

    basedir = "../../../star-upc-data/ana/muDst/muDst_run1/sel5"
    infile = "ana_muDst_run1_all_sel5z.root"
    #infile = "ana_muDst_run1_all_sel5.root"

    interactive = False

    if interactive == False: gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("jRecTree")

    make_fit()

    #to prevent 'pure virtual method called'
    gPad.Close()

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")














