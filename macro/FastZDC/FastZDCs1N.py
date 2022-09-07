#!/usr/bin/python3

import sys
sys.path.append("./models")

import ROOT as rt
from ROOT import gPad, gROOT, gSystem, gStyle, TFile, TTree, AddressOf
from ROOT import TMath, TRandom3

from STnOOnRead import STnOOnRead

from Linear import Linear
from Quad import Quad
from Poisson import Poisson
from HCal import HCal
from Grupen import Grupen

#_____________________________________________________________________________
def main():

    #starlight_nOOn input
    #infile = "/home/jaroslav/sim/starlight_nOOn_data/run2/slight_AuAu_XnXn_Glauber_100kevt.root"
    infile = "/home/jaroslav/sim/starlight_nOOn_data/slight_AuAu_200GeV_XnXn_JpsiCoh_eta1p2_Glauber_1Mevt.root"
    inp = STnOOnRead(infile)

    #target number of XnXn events, negative for all
    nev = 120000
    #nev = -1

    #output file
    outfile = "FastZDC.root"
    #outfile = "/home/jaroslav/analyza/star-upc-data/ana/FastZDC/STnOOn_eta1p2_1Mevt/FastZDC_HCal_allADC.root"
    #outfile = "/home/jaroslav/analyza/star-upc-data/ana/FastZDC/STnOOn_eta1p2_1Mevt/FastZDC_Grupen_allADC.root"
    #outfile = "/home/jaroslav/analyza/star-upc-data/ana/FastZDC/STnOOn_eta1p2_1Mevt/FastZDC_HCal_run16.root"
    #outfile = "/home/jaroslav/analyza/star-upc-data/ana/FastZDC/STnOOn_eta1p2_1Mevt/FastZDC_Grupen_run16.root"

    #ZDC model
    #mod = Linear()
    #mod = Quad()
    #mod = Poisson()
    #mod = HCal()
    mod = Grupen()

    #trigger limit on ACD
    #adc_trg_max_east = 1200.
    #adc_trg_max_west = 1200.
    #adc_trg_max = 999999.
    adc_trg_max_east = 854.758
    adc_trg_max_west = 747.1381

    #create the output
    out = TFile.Open(outfile, "recreate")
    tree_out = TTree("jRecTree", "jRecTree")
    gROOT.ProcessLine("struct EntD{Double_t v;}; struct EntI{Int_t v;};")
    epos = rt.EntD()
    eneg = rt.EntD()
    npos = rt.EntI()
    nneg = rt.EntI()
    adcE = rt.EntD()
    adcW = rt.EntD()
    jRecM = rt.EntD()
    jRecY = rt.EntD()
    jRecPt = rt.EntD()
    tree_out.Branch("epos", AddressOf(epos, "v"), "epos/D")
    tree_out.Branch("eneg", AddressOf(eneg, "v"), "eneg/D")
    tree_out.Branch("npos", AddressOf(npos, "v"), "npos/I")
    tree_out.Branch("nneg", AddressOf(nneg, "v"), "nneg/I")
    tree_out.Branch("jZDCUnAttEast", AddressOf(adcE, "v"), "jZDCUnAttEast/D")
    tree_out.Branch("jZDCUnAttWest", AddressOf(adcW, "v"), "jZDCUnAttWest/D")
    tree_out.Branch("jRecM", AddressOf(jRecM, "v"), "jRecM/D")
    tree_out.Branch("jRecY", AddressOf(jRecY, "v"), "jRecY/D")
    tree_out.Branch("jRecPt", AddressOf(jRecPt, "v"), "jRecPt/D")

    #inp.read(0)

    inp.tree.GetEntry(0)

    return

    #input loop
    iev = 0
    nXX = 0
    nCen = 0
    nTrig = 0
    while True:

        #load the event
        if not inp.read(iev): break
        iev += 1

        #central trigger
        if not inp.is_Cen: continue
        nCen += 1

        #select the XnXn
        if not inp.is_XnXn: continue
        nXX += 1

        #ADC from energy by the model
        adcE.v, adcW.v = mod(inp.eneg, inp.epos)

        #trigger condition on ADC
        if adcE.v > adc_trg_max_east or adcW.v > adc_trg_max_west:
            continue

        #accepted by the trigger
        nTrig += 1

        #generated energy and multiplicity
        epos.v = inp.epos
        eneg.v = inp.eneg
        npos.v = inp.npos
        nneg.v = inp.nneg

        #J/psi kinematics
        jRecM.v = inp.m
        jRecY.v = inp.y
        jRecPt.v = inp.pT

        #fill the output
        tree_out.Fill()

        #target XnXn reached
        if nev > 0 and nTrig >= nev: break

    #input loop

    #event statistics
    print("Events read:", iev)
    print("Central trg:", nCen)
    print("XnXn events:", nXX)
    print("Trig events:", nTrig)

    #ratio of triggers to all XnXn events
    xtrig = float(nTrig)
    xall = float(nXX)
    rto = xtrig/xall
    sigma_rto = rto*TMath.Sqrt( (xall-xtrig)/(xall*xtrig) )
    print("Trig/XnXn  :", rto, "+/-", sigma_rto)

    tree_out.Write()
    out.Close()

#main

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()

    #beep when finished
    #gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")
    gSystem.Exec("mplayer ../input_ok_3_clean.mp3 > /dev/null 2>&1")

















