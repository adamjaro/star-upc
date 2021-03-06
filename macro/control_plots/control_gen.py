#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TClonesArray, TMath

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    #infile = "/home/jaroslav/sim/starlight_nOOn_data/run2/slight_PbPb_Pb208_100kevt.root"
    #infile = "/home/jaroslav/sim/starlight_nOOn_data/run2/slight_PbPb_100kevt.root"
    #infile = "/home/jaroslav/sim/starlight_nOOn_data/run2/slight_AuAu_100kevt.root"
    #infile = "/home/jaroslav/sim/starlight_nOOn_data/run2/slight_AuAu_Glauber_100kevt.root"
    infile = "/home/jaroslav/sim/starlight_nOOn_data/run2/slight_AuAu_XnXn_Glauber_100kevt.root"

    in_sl = "/home/jaroslav/sim/noon-master/SLoutput_100k.root"

    iplot = 8
    funclist = []
    funclist.append( gen_y ) # 0
    funclist.append( gen_phot_k ) # 1
    funclist.append( gen_ay ) # 2
    funclist.append( gen_nmult ) # 3
    funclist.append( read_particles ) # 4
    funclist.append( neut_en ) # 5
    funclist.append( neut_eta ) # 6
    funclist.append( neut_abs_eta ) # 7
    funclist.append( neut_en_pn ) # 8

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
    kmax = 10
    #kmax = 150

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
    #tree_sl.Draw("photonK >> hKsl", "", "", 100000)
    ut.line_h1(hKsl)

    ut.put_yx_tit(hK, "Events", "k", 1.4, 1.2)

    hK.Draw()
    #hKsl.Draw("same")

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

    #nev = tree.GetEntriesFast()
    nev = 12
    for iev in xrange(nev):
        tree.GetEntry(iev)

        print iev

        nmc = particles.GetEntriesFast()

        for imc in xrange(nmc):

            part = particles.At(imc)

            print " ", imc, part.GetPdgCode(), part.Px(), part.Py(), part.Pz(), part.Energy()

#read_particles

#_____________________________________________________________________________
def neut_en():

    #neutron energy

    ebin = 0.5
    emin = 50
    #emax = 200
    emax = 1000
    #ebin = 10
    #emin = 500
    #emax = 3000

    hE = ut.prepare_TH1D("hE", ebin, emin, emax)

    can = ut.box_canvas()

    particles = TClonesArray("TParticle", 200)
    tree.SetBranchAddress("particles", particles)

    nev = tree.GetEntriesFast()
    #nev = 24
    for iev in xrange(nev):
        tree.GetEntry(iev)

        esum = 0.

        for imc in xrange(particles.GetEntriesFast()):

            part = particles.At(imc)
            if part.GetPdgCode() != 2112: continue

            esum += part.Energy()

        hE.Fill( esum )

    ut.put_yx_tit(hE, "Events", "E (GeV)", 1.4, 1.2)

    hE.Draw()

    gPad.SetGrid()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#neut_en

#_____________________________________________________________________________
def neut_eta():

    #neutron pseudorapidity

    etabin = 0.05
    etamin = -20
    etamax = 20

    hEta = ut.prepare_TH1D("hEta", etabin, etamin, etamax)

    can = ut.box_canvas()

    particles = TClonesArray("TParticle", 200)
    tree.SetBranchAddress("particles", particles)

    nev = tree.GetEntriesFast()
    #nev = 24
    for iev in xrange(nev):
        tree.GetEntry(iev)
        for imc in xrange(particles.GetEntriesFast()):
            part = particles.At(imc)
            if part.GetPdgCode() != 2112: continue
            hEta.Fill( part.Eta() )

    ut.put_yx_tit(hEta, "Events", "#eta", 1.4, 1.2)

    hEta.Draw()

    gPad.SetGrid()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#neut_eta

#_____________________________________________________________________________
def neut_abs_eta():

    #neutron absolute pseudorapidity

    etabin = 0.05
    etamin = 5
    etamax = 20

    hEta = ut.prepare_TH1D("hEta", etabin, etamin, etamax)

    can = ut.box_canvas()

    particles = TClonesArray("TParticle", 200)
    tree.SetBranchAddress("particles", particles)

    nev = tree.GetEntriesFast()
    #nev = 24
    for iev in xrange(nev):
        tree.GetEntry(iev)
        for imc in xrange(particles.GetEntriesFast()):
            part = particles.At(imc)
            if part.GetPdgCode() != 2112: continue
            #hEta.Fill( TMath.Abs(part.Eta()) )
            hEta.Fill( abs(part.Eta()) )

    ytit = "Events / {0:.2f}".format(etabin)
    ut.put_yx_tit(hEta, ytit, "Neutron |#kern[0.3]{#eta}|", 1.4, 1.2)

    ut.set_H1D_col(hEta, rt.kRed)

    ut.set_margin_lbtr(gPad, 0.1, 0.09, 0.01, 0.02)

    hEta.Draw()

    gPad.SetGrid()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#neut_abs_eta

#_____________________________________________________________________________
def neut_en_pn():

    #neutron energy and positive and negative rapidity

    #plot range
    ebin = 3
    #emin = 1
    emin = 30
    #emax = 1400
    emax = 710

    #analysis cuts
    eta_max = 6.6 # absolute eta
    en_max = 1250 # energy
    en_min = 20

    hE = ut.prepare_TH2D("hE", ebin, emin, emax, ebin, emin, emax)

    can = ut.box_canvas()

    particles = TClonesArray("TParticle", 200)
    tree.SetBranchAddress("particles", particles)

    nev = tree.GetEntriesFast()
    #nev = int(1e4)

    nall = 0.
    nsel = 0.

    for iev in xrange(nev):
        tree.GetEntry(iev)

        epos = 0.
        eneg = 0.

        for imc in xrange(particles.GetEntriesFast()):

            part = particles.At(imc)
            if part.GetPdgCode() != 2112: continue

            #ZDC eta
            if abs(part.Eta()) < eta_max: continue

            if part.Eta() > 0:
                epos += part.Energy()
            else:
                eneg += part.Energy()

        if epos < en_min or eneg < en_min: continue

        nall += 1.

        if epos > en_max or eneg > en_max: continue

        #if epos < en_min or epos > en_max: continue
        #if eneg < en_min or eneg > en_max: continue

        nsel += 1.

        hE.Fill(eneg, epos)

    print nall, nsel, nsel/nall

    ut.put_yx_tit(hE, "#it{E}_{#it{n}} (GeV),  #it{#eta} > 0", "#it{E}_{#it{n}} (GeV), #it{#eta} < 0", 1.7, 1.2)
    ut.set_margin_lbtr(gPad, 0.12, 0.09, 0.02, 0.11)

    hE.SetMinimum(0.98)
    hE.SetContour(300)

    hE.Draw()

    gPad.SetGrid()

    gPad.SetLogz()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#neut_en_pn

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()











