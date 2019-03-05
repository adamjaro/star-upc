#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TF1
from ROOT import TArrow, TLatex, TLine
from ROOT import TEveManager, gEve, TEveArrow, TGMainFrame
import code
import math as ma

import sys
sys.path.append('../')
import plot_utils as ut
from parameter_descriptor import parameter_descriptor as pdesc

#_____________________________________________________________________________
def plot_zdc_vtx_alltrg():

    #ZDC vertex from all triggered events

    vbin = 0.01
    #vmin = -20.
    #vmax = 20.
    #vmin = -26
    #vmax = -12
    vmin = -800
    vmax = 800

    can = ut.box_canvas()

    #make the histogram
    hZdcVtx = ut.prepare_TH1D("hZdcVtxAll", vbin, vmin, vmax)
    hZdcVtx.SetOption("L")

    #convert to meters for plot
    treeAll = inp.Get("jAllTree")
    print "Number of all trg events:", treeAll.GetEntries()
    treeAll.Draw("jZDCVtxZ/100. >> hZdcVtxAll")

    hZdcVtx.SetYTitle("Events / {0:.0f} cm".format(vbin*100.))
    hZdcVtx.SetXTitle("ZDC vertex along #it{z} (meters)")

    hZdcVtx.SetTitleOffset(1.5, "Y")
    hZdcVtx.SetTitleOffset(1.1, "X")

    gPad.SetTopMargin(0.04)
    gPad.SetRightMargin(0.04)
    gPad.SetBottomMargin(0.08)
    gPad.SetLeftMargin(0.1)

    leg = ut.prepare_leg(0.67, 0.8, 0.28, 0.14, 0.025)
    leg.SetMargin(0.17)
    #leg.AddEntry(None, "UPC-JpsiB 2014", "")
    #leg.AddEntry(None, "UPC-main 2010+2011", "")
    #leg.AddEntry(None, "UPC-main 2014", "")
    leg.AddEntry(None, "Zero bias 2014", "")
    #leg.AddEntry(None, "VPD-ZDC-novtx-mon", "")

    #gPad.SetLogy()

    hZdcVtx.Draw()
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_zdc_vtx_alltrg

#_____________________________________________________________________________
def plot_zdc_tpc_vtx_diff():

    #difference between TPC and ZDC vertex

    dbin = 2.5
    dmin = -90
    dmax = 130
    #dmin = -1500
    #dmax = 2000

    mmin = 1.5
    mmax = 5.

    fitcol = rt.kBlue

    out = open("out.txt", "w")
    ut.log_results(out, "in "+infile)
    strlog = "dbin "+str(dbin)+" dmin "+str(dmin)+" dmax "+str(dmax)
    strlog += " mmin "+str(mmin)+" mmax "+str(mmax)+"\n"
    ut.log_results(out, strlog)

    can = ut.box_canvas()

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    hDVtx = ut.prepare_TH1D("hDVtx", dbin, dmin, dmax)

    tree.Draw("jZDCVtxZ-jVtxZ >> hDVtx", strsel)

    #fit function
    f1 = TF1("f1", "gaus+[3]", -50, 105)
    f1.SetNpx(1000)
    f1.SetLineColor(fitcol)
    f1.SetParameter(0, 77)
    f1.SetParameter(1, 25)
    f1.SetParameter(2, 13)
    f1.SetParameter(3, 5)
    f1.SetParName(0, "norm")
    f1.SetParName(1, "mean")
    f1.SetParName(2, "sigma")
    f1.SetParName(3, "ofs")

    #make the fit
    r1 = (hDVtx.Fit(f1, "RS")).Get()
    out.write(ut.log_tfit_result(r1))

    #r1.Print()

    #fraction of events within +/- 4 sigma
    t1 = tree.CopyTree(strsel)
    nall = t1.GetEntries()
    lo = f1.GetParameter(1) - 4.*f1.GetParameter(2)
    hi = f1.GetParameter(1) + 4.*f1.GetParameter(2)
    nsel = t1.Draw("", "(jZDCVtxZ-jVtxZ)>{0:.3f} && (jZDCVtxZ-jVtxZ)<{1:.3f}".format(lo, hi))
    fraction = float(nsel)/float(nall)
    err = fraction*ma.sqrt(float(nall-nsel)/(nall*nsel))
    ut.log_results(out, "Fraction of events within +/- 4 sigma")
    ut.log_results(out, "4sigma interval: "+str(lo)+" "+str(hi))
    ut.log_results(out, "nall: "+str(nall))
    ut.log_results(out, "nsel: "+str(nsel))
    ut.log_results(out, "f_4s: {0:.3f} +/- {1:.3f}".format(fraction, err))
    print "4sigma interval:", lo, hi
    print "nall:", nall
    print "nsel:", nsel
    print "f_4s: {0:.3f} +/- {1:.3f}".format(fraction, err)


    hDVtx.SetYTitle("Events / {0:.1f} cm".format(dbin))
    hDVtx.SetXTitle("Vertex #it{z}_{ZDC} - #it{z}_{TPC} (cm)")

    hDVtx.SetTitleOffset(1.5, "Y")
    hDVtx.SetTitleOffset(1.3, "X")

    gPad.SetTopMargin(0.012)
    gPad.SetRightMargin(0.04)
    gPad.SetBottomMargin(0.1)
    gPad.SetLeftMargin(0.1)

    #fit parameters on the plot
    desc = pdesc(hDVtx, 0.16, 0.84, 0.057)
    desc.set_text_size(0.03)
    desc.itemD("#chi^{2}/ndf", r1.Chi2()/r1.Ndf(), -1, fitcol)
    desc.prec = 2
    desc.itemRes("norm", r1, 0, fitcol)
    desc.itemRes("mean", r1, 1, fitcol)
    desc.itemRes("#it{#sigma}", r1, 2, fitcol)
    desc.itemRes("ofs", r1, 3, fitcol)

    #cut lines at mean +/- 4sigma
    #cut_lo = ut.cut_line(-20, 0.5, hDVtx)
    #cut_hi = ut.cut_line(70, 0.5, hDVtx)

    leg = ut.prepare_leg(0.14, 0.82, 0.28, 0.136, 0.025)
    leg.SetMargin(0.17)
    ut.add_leg_mass(leg, mmin, mmax)
    leg.AddEntry(hDVtx, "Data")
    leg.AddEntry(f1, "Gaussian + offset", "l")
    #leg.AddEntry(cut_lo, "4#it{#sigma} at -20 and 70 cm", "l")

    hDVtx.Draw()
    leg.Draw("same")
    desc.draw()
    #cut_lo.Draw("same")
    #cut_hi.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_zdc_tpc_vtx_diff

#_____________________________________________________________________________
def plot_zdc_tpc_vtx():

    #2D ZDC and TPC vertices

    zbin = 2.
    #zmin = -50.
    #zmax = 100.
    zmin = -100
    zmax = 150

    tbin = 2.
    #tmin = -55.
    #tmax = 55.
    tmin = -110
    tmax = 110

    mmin = 1.5
    mmax = 5.

    can = ut.box_canvas()

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    hVtx = ut.prepare_TH2D("hVtx", tbin, tmin, tmax, zbin, zmin, zmax)

    tree.Draw("jZDCVtxZ:jVtxZ >> hVtx", strsel)
    hVtx.SetXTitle("TPC vertex along #it{z} / "+"{0:.0f} cm".format(zbin))
    hVtx.SetYTitle("ZDC vertex along #it{z} / "+"{0:.0f} cm".format(zbin))

    hVtx.SetTitleOffset(1.5, "Y")
    hVtx.SetTitleOffset(1.1, "X")

    gPad.SetTopMargin(0.02)
    gPad.SetRightMargin(0.09)
    gPad.SetBottomMargin(0.08)
    gPad.SetLeftMargin(0.11)

    leg = ut.prepare_leg(0.16, 0.82, 0.23, 0.05, 0.025)
    leg.SetMargin(0.02)
    leg.SetBorderSize(1)
    ut.add_leg_mass(leg, mmin, mmax)

    hVtx.Draw()
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_zdc_tpc_vtx

#_____________________________________________________________________________
def plot_zdc_vtx():

    #ZDC vertex from selected events and from all triggered events

    vbin = 0.1
    vmin = -5.
    vmax = 7.

    mmin = 1.5
    mmax = 5.

    can = ut.box_canvas()

    #selection string
    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    #make the histograms
    hZdcVtx = ut.prepare_TH1D("hZdcVtx", vbin, vmin, vmax)
    hZdcVtxAll = ut.prepare_TH1D("hZdcVtxAll", vbin/10., vmin, vmax)

    #convert to meters for plot
    tree.Draw("jZDCVtxZ/100. >> hZdcVtx", strsel)
    treeAll = inp.Get("jAllTree")
    treeAll.Draw("jZDCVtxZ/100. >> hZdcVtxAll")
    ut.norm_to_data(hZdcVtxAll, hZdcVtx, rt.kRed)

    hZdcVtx.SetYTitle("Events / {0:.0f} cm".format(vbin*100.))
    hZdcVtx.SetXTitle("ZDC vertex along #it{z} (meters)")

    hZdcVtx.SetTitleOffset(1.5, "Y")
    hZdcVtx.SetTitleOffset(1.1, "X")

    gPad.SetTopMargin(0.01)
    gPad.SetRightMargin(0.04)
    gPad.SetBottomMargin(0.08)
    gPad.SetLeftMargin(0.1)

    leg = ut.prepare_leg(0.67, 0.8, 0.28, 0.14, 0.025)
    leg.SetMargin(0.17)
    ut.add_leg_mass(leg, mmin, mmax)
    leg.AddEntry(hZdcVtx, "Selected events")
    leg.AddEntry(hZdcVtxAll, "All UPC-JpsiB triggers", "l")

    #gPad.SetLogy()

    hZdcVtx.Draw()
    hZdcVtxAll.Draw("same")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_zdc_vtx

#_____________________________________________________________________________
def plot_zdc_2d():

    #ZDC ADC counts east vs. west 2D

    zbin = 18.
    zmin = 0.
    zmax = 700.

    ptmax = 0.17
    mmin = 1.5
    mmax = 5.

    znam = ["jZDCUnAttEast", "jZDCUnAttWest"]
    xtit = ["ZDC East ADC", "ZDC West ADC"]

    can = ut.box_canvas()

    strsel = "jRecPt<{0:.3f}".format(ptmax)
    strsel += " && jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)
    #print strsel
    #return

    hZdc = ut.prepare_TH2D("hZdc", zbin, zmin, zmax, zbin, zmin, zmax)
    tree.Draw(znam[1]+":"+znam[0]+" >> hZdc", strsel) # y:x
    #treeAll = inp.Get("jAllTree")
    #treeAll.Draw(znam[1]+":"+znam[0]+" >> hZdc") # y:x
    hZdc.SetXTitle(xtit[0])
    hZdc.SetYTitle(xtit[1])
    hZdc.SetZTitle("Events / {0:.1f}".format(zbin))

    hZdc.SetTitleOffset(2., "X")
    hZdc.SetTitleOffset(1.7, "Y")
    hZdc.SetTitleOffset(1.4, "Z")

    gPad.SetTopMargin(0.01)
    gPad.SetRightMargin(0.05)
    #gPad.SetBottomMargin(0.08)
    #gPad.SetLeftMargin(0.1)

    hZdc.SetOption("lego2")
    #hZdc.SetOption("colz")

    hZdc.Draw()

    #gPad.SetTheta(30.)
    gPad.SetPhi(-125.)  # -125  -135
    #gPad.SetPhi(-160.)
    gPad.Update()

    leg = ut.prepare_leg(0., 0.9, 0.29, 0.1, 0.03)
    leg.SetMargin(0.05)
    leg.AddEntry(None, "#bf{#it{p}_{T} < "+"{0:.2f}".format(ptmax)+" GeV}", "")
    mmin_fmt = "{0:.1f}".format(mmin)
    mmax_fmt = "{0:.1f}".format(mmax)
    leg.AddEntry(None, "#bf{"+mmin_fmt+" < #it{m}_{e^{+}e^{-}} < "+mmax_fmt+" GeV}", "")
    leg.Draw("same")

    #ut.invert_col(gPad)
    can.SaveAs("01fig.pdf")

    if interactive == True: start_interactive()

#end of plot_zdc_2d

#_____________________________________________________________________________
def plot_zdc():

    #ZDC ADC counts east or west 1D

    ew = 0

    zbin = 10.
    zmin = 0.
    zmax = 1300.

    znam = ["jZDCUnAttEast", "jZDCUnAttWest"]
    xtit = ["ZDC East ADC", "ZDC West ADC"]
    lhead = ["East ZDC", "West ZDC"]

    #global gPad
    can = ut.box_canvas()

    hZdc = ut.prepare_TH1D("hZdc", zbin, zmin, zmax)
    hZdcAll = ut.prepare_TH1D("hZdcAll", zbin, zmin, zmax)

    tree.Draw(znam[ew]+" >> hZdc")
    treeAll = inp.Get("jAllTree")
    treeAll.Draw(znam[ew]+" >> hZdcAll")
    ut.norm_to_data(hZdcAll, hZdc, rt.kRed)

    hZdc.SetYTitle("Events / {0:.1f}".format(zbin))
    hZdc.SetXTitle(xtit[ew])

    hZdc.SetTitleOffset(1.5, "Y")
    hZdc.SetTitleOffset(1.1, "X")

    gPad.SetTopMargin(0.01)
    gPad.SetRightMargin(0.08)
    gPad.SetBottomMargin(0.08)
    gPad.SetLeftMargin(0.1)

    leg = ut.prepare_leg(0.5, 0.76, 0.39, 0.16, 0.035)
    leg.SetMargin(0.17)
    leg.AddEntry(None, lhead[ew], "")
    leg.AddEntry(hZdc, "Selected events")
    leg.AddEntry(hZdcAll, "All UPC-JpsiB triggers", "l")

    hZdc.Draw()
    hZdcAll.Draw("same")
    leg.Draw("same")

    #ut.print_pad(rt.gPad)
    ut.invert_col(rt.gPad)

    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def start_interactive():

    vars = globals()
    vars.update(locals())
    shell = code.InteractiveConsole(vars)
    shell.interact()

#_____________________________________________________________________________
if __name__ == "__main__":

    basedir = "../../../star-upc-data/ana/muDst/muDst_run1/sel5"
    #infile = "ana_muDst_run1_all_sel5.root"
    infile = "ana_muDst_run1_all_sel5z.root"
    #infile = "ana_muDst_run1a_all_sel5_tof.root"

    #basedir = "../../../star-upc-data/ana/muDst/muDst_run2a/gg0"
    #infile = "ana_muDst_run2a_all_gg0_v2.root"

    #basedir = "../../../star-upc-data/ana/muDst/muDst_run3/sel5"
    #infile = "ana_muDst_run3_all_sel5z.root"

    #basedir = "../../../star-upc-data/ana/muDst/muDst_VPDZDCmon1/sel5"
    #infile = "ana_VPDZDCmon1_sel5z.root"

    interactive = False

    if interactive == False: gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    iplot = 4
    funclist = []
    funclist.append(plot_zdc) # 0
    funclist.append(plot_zdc_2d) # 1
    funclist.append(plot_zdc_vtx) # 2
    funclist.append(plot_zdc_tpc_vtx) # 3
    funclist.append(plot_zdc_tpc_vtx_diff) # 4
    funclist.append(plot_zdc_vtx_alltrg) # 5

    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("jRecTree")

    funclist[iplot]()

    #to prevent 'pure virtual method called'
    gPad.Close()

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")



























