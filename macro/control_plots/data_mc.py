#!/usr/bin/python

import ROOT as rt
from ROOT import TF1, gPad, gROOT, gStyle, TFile

import sys
sys.path.append('../')
import plot_utils as ut
from parameter_descriptor import parameter_descriptor as pdesc

#_____________________________________________________________________________
def main():

    #data
    basedir = "../../../star-upc-data/ana/muDst/muDst_run1/sel5"
    infile = "ana_muDst_run1_all_sel5z.root"

    #MC
    basedir_coh = "../../../star-upc-data/ana/starsim/slight14e/sel5"
    infile_coh = "ana_slight14e1x3_s6_sel5z.root"

    ymin = -1
    ymax = 1

    mmin = 1.5
    mmax = 5

    ptmax = 0.17

    iplot = 0
    funclist = []
    funclist.append( tracks_eta ) # 0

    inp = TFile.Open(basedir+"/"+infile)
    global tree
    tree = inp.Get("jRecTree")

    inp_coh = TFile.Open(basedir_coh+"/"+infile_coh)
    global tree_coh
    tree_coh = inp_coh.Get("jRecTree")

    global gsel
    gsel = "jRecM>"+str(mmin)+" && jRecM<"+str(mmax)+" && jRecY>"+str(ymin)+" && jRecY<"+str(ymax)+" && jRecPt<"+str(ptmax)

    funclist[iplot]()

#main

#_____________________________________________________________________________
def tracks_eta():

    #bins in eta
    ebin = 0.2
    emin = -1.2
    emax = 1.2

    hEta = ut.prepare_TH1D("hEta", ebin, emin, emax)
    hEtaMC = ut.prepare_TH1D("hEtaMC", ebin, emin, emax)

    can = ut.box_canvas()

    tree.Draw("jT0eta >> hEta", gsel)
    tree.Draw("jT1eta >>+ hEta", gsel)

    tree_coh.Draw("jT0eta >> hEtaMC", gsel)
    tree_coh.Draw("jT1eta >>+ hEtaMC", gsel)

    ut.norm_to_data(hEtaMC, hEta)

    #gPad.SetLogy()

    hEta.Draw()
    hEtaMC.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#tracks_eta

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()

