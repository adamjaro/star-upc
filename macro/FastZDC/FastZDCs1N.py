#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, TTree, AddressOf
from ROOT import TMath, TRandom3

from STnOOnRead import STnOOnRead

#_____________________________________________________________________________
def main():

    #starlight_nOOn input
    infile = "/home/jaroslav/sim/starlight_nOOn_data/run2/slight_AuAu_XnXn_Glauber_100kevt.root"
    inp = STnOOnRead(infile)

    #target number of XnXn events
    nev = 10000

    #output file
    outfile = "FastZDC.root"

    #resolution sigma_E/E, east and west
    sigE = 0.217
    sigW = 0.306

    s2E = 0.1
    s2W = 0.005

    #difference in mean for ADC, east and west
    deltE = 25.2
    deltW = 11.5

    #simulation Gaussian
    #gsig = TF1("FastZDC", "gaus", -12*sigE, 12*sigE)
    #gsig.SetParameters(1, 0, sigE)
    rnd = TRandom3()

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

    jRecM.v = 3.
    jRecY.v = 0.
    jRecPt.v = 0.1

    #input loop
    iev = 0
    nXX = 0
    while True:

        #load the event
        if not inp.read(iev): break
        iev += 1

        #select the XnXn
        if not inp.is_XnXn: continue
        nXX += 1

        #generated energy and multiplicity
        epos.v = inp.epos
        eneg.v = inp.eneg
        npos.v = inp.npos
        nneg.v = inp.nneg

        #energy resolution

        #adcE.v = inp.eneg + rnd.Gaus(0, 0.2*inp.eneg)
        #adcW.v = inp.epos + rnd.Gaus(0, 0.2*inp.epos)

        #adcE.v = get_adc(inp.eneg, sigE, deltE, rnd)
        #adcW.v = get_adc(inp.epos, sigW, deltW, rnd)

        adcE.v = get_adc(inp.eneg, sigE, s2E, deltE, rnd)
        adcW.v = get_adc(inp.epos, sigW, s2W, deltW, rnd)

        #print get_adc(inp.eneg, 0.2, 0, rnd)

        #print gsig.GetRandom()
        #print rnd.Gaus(0, sigE)
        #print

        tree_out.Fill()

        #target XnXn reached
        if nXX >= nev: break

    #input loop


    print "Events read:", iev
    print "XnXn events:", nXX

    tree_out.Write()
    out.Close()

#main

#_____________________________________________________________________________
def get_adc(en, sig, s2, delt, rnd):

    #convert energy to ADC

    #sigma = en*TMath.Sqrt( ((0.05**2)/en) + 0.2**2 )
    #sigma = en*TMath.Sqrt( ((0.01**2)/en) + sig**2 )
    #sigma = en*TMath.Sqrt( (0.1/en)**2 + sig**2 )
    #sigma = en*sig
    #sigma = 100.*sig
    #sigma = en*TMath.Sqrt( (sig**2) )
    #sigma = 100*sig + 0.1*(en-100) # works for east
    #sigma = 100*sig + 0.005*(en-100) # works for west

    sigma = 100*sig + s2*(en-100)

    adc = -1.

    while adc < 0.:
        #adc = en + rnd.Gaus(0, sig*en)
        #adc = en + rnd.Gaus(0, sig*100.)
        adc = en + rnd.Gaus(0, sigma)
        adc -= delt

    #if adc<0.: print adc

    return adc

#get_adc

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()



















