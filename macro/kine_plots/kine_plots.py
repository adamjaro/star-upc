#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append('../')
import plot_utils as ut


#_____________________________________________________________________________
def plot_dvtx_mc():

    #difference between reconstructed and generated vertex in MC
    vbin = 0.01
    vmin = -2.
    vmax = 2.

    mmin = 1.5
    mmax = 5.

    ptmax = 0.17

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f} && jRecPt<{2:.3f}".format(mmin, mmax, ptmax)

    can = ut.box_canvas()

    hDv = ut.prepare_TH1D("hDv", vbin, vmin, vmax)

    ut.put_yx_tit(hDv, "Events / ({0:.2f} cm)".format(vbin), "Vtx_{#it{z},rec} - Vtx_{#it{z},gen} (cm)")

    ut.set_margin_lbtr(gPad, 0.12, 0.08, 0.01, 0.01)

    mctree.Draw("jVtxZ-jGenVtxZ >> hDv", strsel)

    hDv.Draw()

    leg = ut.prepare_leg(0.62, 0.8, 0.14, 0.16, 0.03)
    ut.add_leg_pt_mass(leg, ptmax, mmin, mmax)
    leg.AddEntry(None, "Reconstructed - generated", "")
    leg.AddEntry(None, "vertex position along #it{z}", "")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hDv, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_dvtx_mc

#_____________________________________________________________________________
def plot_tracks_nhits():

    #tracks number of hits
    nhbin = 1
    nhmin = 10.
    nhmax = 49.

    mmin = 1.5
    mmax = 5.

    ptmax = 0.17

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f} && jRecPt<{2:.3f}".format(mmin, mmax, ptmax)

    can = ut.box_canvas()

    hNh = ut.prepare_TH1D("hNh", nhbin, nhmin, nhmax)
    hNhMC = ut.prepare_TH1D("hNhMC", nhbin, nhmin, nhmax)

    ut.put_yx_tit(hNhMC, "Events / ({0:.0f} hit)".format(nhbin), "Tracks number of hits", 1.7)

    ut.set_margin_lbtr(gPad, 0.12, 0.08, 0.01, 0.01)

    tree.Draw("jT0nHits >> hNh", strsel)
    tree.Draw("jT1nHits >>+hNh", strsel)
    mctree.Draw("jT0nHits >> hNhMC", strsel)
    mctree.Draw("jT1nHits >>+hNhMC", strsel)
    ut.norm_to_data(hNhMC, hNh, rt.kBlue)

    hNhMC.Draw()
    hNh.Draw("e1same")
    hNhMC.Draw("same")

    leg = ut.prepare_leg(0.57, 0.8, 0.14, 0.16, 0.03)
    ut.add_leg_pt_mass(leg, ptmax, mmin, mmax)
    leg.AddEntry(hNh, "Data")
    leg.AddEntry(hNhMC, "MC", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hNh, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_tracks_nhits

#_____________________________________________________________________________
def plot_tracks_chi2():

    #tracks reduced chi2
    cbin = 0.05
    cmin = 0.
    cmax = 4.

    mmin = 1.5
    mmax = 5.

    ptmax = 0.17

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f} && jRecPt<{2:.3f}".format(mmin, mmax, ptmax)

    can = ut.box_canvas()

    hChi2 = ut.prepare_TH1D("hChi2", cbin, cmin, cmax)
    hChi2MC = ut.prepare_TH1D("hChi2MC", cbin/3., cmin, cmax)

    ut.put_yx_tit(hChi2MC, "Events / {0:.2f}".format(cbin), "Tracks reduced #chi^{2}")

    ut.set_margin_lbtr(gPad, 0.1, 0.08, 0.01, 0.01)

    tree.Draw("jT0chi2 >> hChi2", strsel)
    tree.Draw("jT1chi2 >>+hChi2", strsel)
    mctree.Draw("jT0chi2 >> hChi2MC", strsel)
    mctree.Draw("jT1chi2 >>+hChi2MC", strsel)
    ut.norm_to_data(hChi2MC, hChi2, rt.kBlue)

    hChi2MC.Draw()
    hChi2.Draw("e1same")
    hChi2MC.Draw("same")

    leg = ut.prepare_leg(0.67, 0.8, 0.14, 0.16, 0.03)
    ut.add_leg_pt_mass(leg, ptmax, mmin, mmax)
    leg.AddEntry(hChi2, "Data")
    leg.AddEntry(hChi2MC, "MC", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hChi2, 0.3, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_tracks_chi2

#_____________________________________________________________________________
def plot_tracks_dca():

    #tracks dca to primary vertex along z
    dcabin = 0.02
    dcamin = -1.
    dcamax = 1.

    mmin = 1.5
    mmax = 5.

    ptmax = 0.17

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f} && jRecPt<{2:.3f}".format(mmin, mmax, ptmax)

    can = ut.box_canvas()

    hDca = ut.prepare_TH1D("hDca", dcabin, dcamin, dcamax)
    hDcaMC = ut.prepare_TH1D("hDcaMC", dcabin/3, dcamin, dcamax)

    ut.put_yx_tit(hDcaMC, "Events / ({0:.2f} cm)".format(dcabin), "Tracks dca in #it{z} to prim. vtx (cm)")

    ut.set_margin_lbtr(gPad, 0.1, 0.08, 0.01, 0.01)

    tree.Draw("jT0dcaZ >> hDca", strsel)
    tree.Draw("jT1dcaZ >>+hDca", strsel)
    mctree.Draw("jT0dcaZ >> hDcaMC", strsel)
    mctree.Draw("jT1dcaZ >>+hDcaMC", strsel)
    ut.norm_to_data(hDcaMC, hDca, rt.kBlue)

    hDcaMC.Draw()
    hDca.Draw("e1same")
    hDcaMC.Draw("same")

    leg = ut.prepare_leg(0.67, 0.8, 0.14, 0.16, 0.03)
    ut.add_leg_pt_mass(leg, ptmax, mmin, mmax)
    leg.AddEntry(hDca, "Data")
    leg.AddEntry(hDcaMC, "MC", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hDca, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_tracks_dca

#_____________________________________________________________________________
def plot_tracks_phi():

    #tracks pseudorapidity
    phibin = 0.8
    phimax = 4.

    mmin = 1.5
    mmax = 5.

    ptmax = 0.17

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f} && jRecPt<{2:.3f}".format(mmin, mmax, ptmax)

    can = ut.box_canvas()

    hPhi = ut.prepare_TH1D("hPhi", phibin, -phimax, phimax)
    hPhiMC = ut.prepare_TH1D("hPhiMC", phibin/3., -phimax, phimax)

    ut.put_yx_tit(hPhi, "Events / {0:.1f}".format(phibin), "Tracks azimuthal angle")

    ut.set_margin_lbtr(gPad, 0.1, 0.08, 0.014, 0.01)

    hPhi.SetMaximum(520)

    tree.Draw("jT0phi >> hPhi", strsel)
    tree.Draw("jT1phi >>+hPhi", strsel)
    mctree.Draw("jT0phi >> hPhiMC", strsel)
    mctree.Draw("jT1phi >>+hPhiMC", strsel)
    ut.norm_to_data(hPhiMC, hPhi, rt.kBlue)

    hPhi.Draw()
    hPhiMC.Draw("same")

    leg = ut.prepare_leg(0.67, 0.8, 0.14, 0.16, 0.03)
    ut.add_leg_pt_mass(leg, ptmax, mmin, mmax)
    leg.AddEntry(hPhi, "Data")
    leg.AddEntry(hPhiMC, "MC", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hPhi, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_tracks_phi

#_____________________________________________________________________________
def plot_tracks_eta():

    #tracks pseudorapidity
    etabin = 0.09
    etamax = 1.1

    mmin = 1.5
    mmax = 5

    ptmax = 0.17

    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f} && jRecPt<{2:.3f}".format(mmin, mmax, ptmax)

    can = ut.box_canvas()

    hEta = ut.prepare_TH1D("hEta", etabin, -etamax, etamax)
    hEtaMC = ut.prepare_TH1D("hEtaMC", etabin/2., -etamax, etamax)

    ut.put_yx_tit(hEta, "Events / {0:.2f}".format(etabin), "Tracks pseudorapidity")

    ut.set_margin_lbtr(gPad, 0.1, 0.08, 0.014, 0.01)

    hEta.SetMaximum(220)

    tree.Draw("jT0eta >> hEta", strsel)
    tree.Draw("jT1eta >>+hEta", strsel)
    mctree.Draw("jT0eta >> hEtaMC", strsel)
    mctree.Draw("jT1eta >>+hEtaMC", strsel)
    ut.norm_to_data(hEtaMC, hEta, rt.kBlue)

    hEta.Draw()
    hEtaMC.Draw("same")

    leg = ut.prepare_leg(0.67, 0.8, 0.14, 0.16, 0.03)
    ut.add_leg_pt_mass(leg, ptmax, mmin, mmax)
    leg.AddEntry(hEta, "Data")
    leg.AddEntry(hEtaMC, "MC", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hEta, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#end of plot_tracks_eta

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

    ut.put_yx_tit(hY, "Events / {0:.1f}".format(ybin), "Dilepton rapidity")

    ut.set_margin_lbtr(gPad, 0.1, 0.08, 0.01, 0.01)

    tree.Draw("jRecY >> hY", strsel)
    mctree.Draw("jRecY >> hYMC", strsel)
    ut.norm_to_data(hYMC, hY, rt.kBlue)

    hY.Draw()
    hYMC.Draw("same")

    leg = ut.prepare_leg(0.67, 0.8, 0.14, 0.16, 0.03)
    ut.add_leg_pt_mass(leg, ptmax, mmin, mmax)
    leg.AddEntry(hY, "Data")
    leg.AddEntry(hYMC, "MC", "l")
    leg.Draw("same")

    uoleg = ut.make_uo_leg(hY, 0.14, 0.9, 0.01, 0.1)
    uoleg.Draw("same")

    #ut.invert_col(rt.gPad)
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
    #infile_mc = "ana_slight14e2x1_sel5_nzvtx.root"

    interactive = False

    if interactive == False: gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    iplot = 6
    funclist = []
    funclist.append(plot_y) # 0
    funclist.append(plot_tracks_eta) # 1
    funclist.append(plot_tracks_phi) # 2
    funclist.append(plot_tracks_dca) # 3
    funclist.append(plot_tracks_chi2) # 4
    funclist.append(plot_tracks_nhits) # 5
    funclist.append(plot_dvtx_mc) # 6

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


