#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TArrow, TLatex, TLine
from ROOT import TEveManager, gEve, TEveArrow, TGMainFrame
import code

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def plot_zdc_vtx():

    vbin = 0.01
    vmin = -1800.
    vmax = 1800.

    ptmax = 0.17
    mmin = 1.5
    mmax = 5


#end of plot_zdc_vtx

#_____________________________________________________________________________
def plot_zdc_2d():

    zbin = 18.
    zmin = 0.
    zmax = 700.

    ptmax = 0.17
    mmin = 1.5
    mmax = 5

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

    hZdc.Draw()

    #gPad.SetTheta(30.)
    gPad.SetPhi(-125.)
    #gPad.SetPhi(-160.)
    gPad.Update()

    leg = ut.prepare_leg(0., 0.9, 0.29, 0.1, 0.03)
    leg.SetMargin(0.05)
    leg.AddEntry(None, "#bf{#it{p}_{T} < "+"{0:.2f}".format(ptmax)+" GeV}", "")
    mmin_fmt = "{0:.1f}".format(mmin)
    mmax_fmt = "{0:.1f}".format(mmax)
    leg.AddEntry(None, "#bf{"+mmin_fmt+" < #it{m}_{e^{+}e^{-}} < "+mmax_fmt+" GeV}", "")
    leg.Draw("same")

    ut.invert_col(gPad)
    can.SaveAs("01fig.pdf")

    if interactive == True: start_interactive()

#end of plot_zdc_2d

#_____________________________________________________________________________
def plot_zdc():

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

    basedir = "../../ana/muDst/muDst_run0/sel3"

    infile = "ana_muDst_run0_all_sel3_alltree.root"

    interactive = False

    if interactive == False: gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    iplot = 0
    funclist = []
    funclist.append(plot_zdc) # 0
    funclist.append(plot_zdc_2d) # 1

    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("jRecTree")

    funclist[iplot]()

    #to prevent 'pure virtual method called'
    gPad.Close()

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")



























