#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append('../')
import plot_utils as ut

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

    tree.Draw("jRecY >> hY", strsel)
    mctree.Draw("jRecY >> hYMC", strsel)
    ut.norm_to_data(hYMC, hY, rt.kBlue)

    hY.Draw()
    hYMC.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_y

#_____________________________________________________________________________
if __name__ == "__main__":

    #data
    basedir = "../../../star-upc-data/ana/muDst/muDst_run1/sel5"
    infile = "ana_muDst_run1_all_sel5z.root"

    #MC
    basedir_mc = "../../../star-upc-data/ana/starsim/slight14e/sel5"
    infile_mc = "ana_slight14e1x1_sel5z.root"

    interactive = False

    if interactive == False: gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    iplot = 0
    funclist = []
    funclist.append(plot_y) # 0

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


