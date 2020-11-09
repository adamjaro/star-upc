#!/usr/bin/python

import sys
sys.path.append("./models")

import ROOT as rt
from ROOT import gPad, gROOT, gSystem, gStyle, TFile, TTree, AddressOf
from ROOT import TMath, TRandom3

from STnOOnRead import STnOOnRead

from Linear import Linear
from Quad import Quad

#_____________________________________________________________________________
def main():

    #starlight_nOOn input
    infile = "/home/jaroslav/sim/starlight_nOOn_data/run2/slight_AuAu_XnXn_Glauber_100kevt.root"
    inp = STnOOnRead(infile)

    #target number of XnXn events
    nev = 10000

    #output file
    outfile = "FastZDC.root"

    #ZDC model
    #mod = Linear()
    mod = Quad()

    #trigger limit on ACD
    adc_trg_max = 1200.

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

    #implicit J/psi kinematics
    jRecM.v = 3.
    jRecY.v = 0.
    jRecPt.v = 0.1

    #input loop
    iev = 0
    nXX = 0
    nTrig = 0
    while True:

        #load the event
        if not inp.read(iev): break
        iev += 1

        #select the XnXn
        if not inp.is_XnXn: continue
        nXX += 1

        #ADC from energy by the model
        adcE.v, adcW.v = mod(inp.eneg, inp.epos)

        #trigger condition on ADC
        if adcE.v > adc_trg_max or adcW.v > adc_trg_max:
            continue

        #accepted by the trigger
        nTrig += 1

        #generated energy and multiplicity
        epos.v = inp.epos
        eneg.v = inp.eneg
        npos.v = inp.npos
        nneg.v = inp.nneg

        #fill the output
        tree_out.Fill()

        #target XnXn reached
        if nTrig >= nev: break

    #input loop


    print "Events read:", iev
    print "XnXn events:", nXX
    print "Trig events:", nTrig
    print "Trig/XnXn  :", float(nTrig)/nXX

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
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")

















