#!/usr/bin/python3

import sys
sys.path.append("./models")

from ctypes import c_double, c_int

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
    epos = c_double(0)
    eneg = c_double(0)
    npos = c_int(0)
    nneg = c_int(0)
    adcE = c_double(0)
    adcW = c_double(0)
    jRecM = c_double(0)
    jRecY = c_double(0)
    jRecPt = c_double(0)

    tree_out.Branch("epos", epos, "epos/D")
    tree_out.Branch("eneg", eneg, "eneg/D")
    tree_out.Branch("npos", npos, "npos/I")
    tree_out.Branch("nneg", nneg, "nneg/I")
    tree_out.Branch("jZDCUnAttEast", adcE, "jZDCUnAttEast/D")
    tree_out.Branch("jZDCUnAttWest", adcW, "jZDCUnAttWest/D")
    tree_out.Branch("jRecM", jRecM, "jRecM/D")
    tree_out.Branch("jRecY", jRecY, "jRecY/D")
    tree_out.Branch("jRecPt", jRecPt, "jRecPt/D")

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
        adcE.value, adcW.value = mod(inp.eneg, inp.epos)

        #trigger condition on ADC
        if adcE.value > adc_trg_max_east or adcW.value > adc_trg_max_west:
            continue

        #accepted by the trigger
        nTrig += 1

        #generated energy and multiplicity
        epos.value = inp.epos
        eneg.value = inp.eneg
        npos.value = inp.npos
        nneg.value = inp.nneg

        #J/psi kinematics
        jRecM.value = inp.m
        jRecY.value = inp.y
        jRecPt.value = inp.pT

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

















