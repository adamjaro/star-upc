#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TClonesArray

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    #infile = "/home/jaroslav/sim/starlight_data/slight_Jpsi_PbPb_coh.root"
    infile = "/home/jaroslav/sim/starlight_nOOn/build/slight.root"
    #infile = "/home/jaroslav/sim/starlight_nOOn_data/run1/slight_PbPb_seed1_100kevt.root"

    in_sl = "/home/jaroslav/sim/noon-master/SLoutput_100k.root"

    iplot = 4
    funclist = []
    funclist.append( gen_y ) # 0
    funclist.append( gen_phot_k ) # 1
    funclist.append( gen_ay ) # 2
    funclist.append( gen_nmult ) # 3
    funclist.append( read_particles ) # 4

    inp = TFile.Open(infile)
    inp_sl = TFile.Open(in_sl)
    global tree, tree_sl
    tree = inp.Get("slight_tree")
    tree_sl = inp_sl.Get("fEventTree")

    funclist[iplot]()

#main

#_____________________________________________________________________________
def gen_y():

    #rapidity from Starlight

    #rapidity range
    nbin = 200
    ymin = -6
    ymax = 6

    hY = ut.prepare_TH1D_n("hY", nbin, ymin, ymax)
    hYsl = ut.prepare_TH1D_n("hYsl", nbin, ymin, ymax)

    can = ut.box_canvas()

    tree.Draw("rapidity >> hY", "", "", 100000)
    tree_sl.Draw("VMrapidity >> hYsl", "", "", 100000)
    ut.line_h1(hYsl)

    ut.put_yx_tit(hY, "Events", "y", 1.4, 1.2)

    hY.Draw()
    hYsl.Draw("same")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_y

#_____________________________________________________________________________
def gen_phot_k():

    #photon energy k from rapidity

    #energy range
    kmin = 0
    kmax = 150

    #bins
    nbin = 100

    hK = ut.prepare_TH1D_n("hK", nbin, kmin, kmax)
    hKsl = ut.prepare_TH1D_n("hKsl", nbin, kmin, kmax)

    can = ut.box_canvas()

    #energy by rapidity and mass
    #form = "0.5*mass*TMath::Exp(rapidity)"
    #form = "0.5*3.09*TMath::Exp(TMath::Abs(rapidity))"
    #form = "0.5*3.09*TMath::Exp(rapidity)"
    #form = "0.5*3.09*TMath::Exp(TMath::Abs(rapidity))"
    #form = "0.5*3.09*TMath::Exp(VMrapidity)"
    #form = "photK_from_y"
    form = "photonK"

    tree.Draw(form+" >> hK", "", "", 100000)
    #tree_sl.Draw("photK_from_y >> hKsl", "", "", 100000)
    tree_sl.Draw("photonK >> hKsl", "", "", 100000)
    ut.line_h1(hKsl)

    ut.put_yx_tit(hK, "Events", "k", 1.4, 1.2)

    hK.Draw()
    hKsl.Draw("same")

    #photons directly from Starlight
    #sl = TFile.Open("/home/jaroslav/sim/noon-master/SLoutput.root")
    #hSLk = sl.Get("hPhotK")
    #hSLk.Draw("same")

    gPad.SetGrid()
    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_phot_k

#_____________________________________________________________________________
def gen_ay():

    #abs(y)

    nbin = 100
    ymax = 6

    hAY = ut.prepare_TH1D_n("hAY", nbin, 0, ymax)

    can = ut.box_canvas()

    tree.Draw("TMath::Abs(rapidity) >> hAY", "", "", 100000)

    ut.put_yx_tit(hAY, "Events", "|y|", 1.4, 1.2)

    hAY.Draw()

    #absolute rapidity directly from Starlight
    sl = TFile.Open("/home/jaroslav/sim/noon-master/SLoutput.root")
    hSLy = sl.Get("hAY")
    hSLy.Draw("same")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_ay

#_____________________________________________________________________________
def gen_nmult():

    #neutron multiplicity

    xbin = 1
    xmin = 0
    xmax = 100

    hN = ut.prepare_TH1D("hN", xbin, xmin, xmax)

    can = ut.box_canvas()

    tree.Draw("nmult >> hN")

    ut.put_yx_tit(hN, "Events", "nmult", 1.4, 1.2)

    hN.Draw()

    gPad.SetGrid()
    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_nmult

#_____________________________________________________________________________
def read_particles():

    #particles clones array

    #tree.Print()

    particles = TClonesArray("TParticle", 200)
    tree.SetBranchAddress("particles", particles)

    nev = tree.GetEntriesFast()
    #nev = 3
    for iev in xrange(nev):
        tree.GetEntry(iev)

        print iev

        nmc = particles.GetEntriesFast()

        for imc in xrange(nmc):

            part = particles.At(imc)

            print " ", imc, part.GetPdgCode(), part.Px(), part.Py(), part.Pz(), part.Energy()

#read_particles

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()











