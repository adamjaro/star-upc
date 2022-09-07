
import ROOT as rt
from ROOT import TFile, TGraphErrors

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def load_starlight(dy):

    slight = TFile.Open("/home/jaroslav/sim/starlight_tx/slight_AuAu_200GeV_Jpsi_coh_intmax0p34_6Mevt.root")
    slight_tree = slight.Get("slight_tree")

    #hSlight = ut.prepare_TH1D("hSlight", 0.002, 0., 0.12)
    hSlight = ut.prepare_TH1D_vec("hSlight", ut.get_bins_vec_2pt(0.0002, 0.002, 0, 0.12, 0.004))

    nall = float( slight_tree.GetEntries() )
    ny = float( slight_tree.Draw("pT*pT >> hSlight", "rapidity>-1 && rapidity<1") )

    #normalize to the width of each bin, necessary for variable binning
    for ibin in range(hSlight.GetNbinsX()+1):
        hSlight.SetBinContent(ibin, hSlight.GetBinContent(ibin)/hSlight.GetBinWidth(ibin))

    sigma_sl_tot = 67.958 # total Starlight cross section, ub
    sigma_sl = (ny/nall)*sigma_sl_tot/1000. # ub to mb
    sigma_sl = sigma_sl/dy # rapidity interval
    print("sigma_sl:", sigma_sl)

    #normalize to Starlight total cross section
    ut.norm_to_integral(hSlight, sigma_sl)

    #convert to graph
    gSlight = ut.h1_to_graph(hSlight)

    gSlight.SetLineColor(rt.kBlue)
    gSlight.SetLineWidth(3)
    gSlight.SetLineStyle(9) # kDashDotted

    return gSlight

#end of load_starlight

#_____________________________________________________________________________
def load_ms():

    #model by Heikki and Bjorn
    f = open("data/to_star_ms.txt", "r")
    t_sigma = []
    for line in f:
        if line[0] == "#": continue
        point = line.split(" ")
        t_sigma.append([float(point[0]), float(point[1])])

    #scaling to XnXn
    kx = 0.1702

    gMS = TGraphErrors(len(t_sigma))
    for i in range(len(t_sigma)):
        gMS.SetPoint(i, t_sigma[i][0], t_sigma[i][1]*kx)

    gMS.SetLineColor(rt.kViolet)
    gMS.SetLineWidth(3)
    gMS.SetLineStyle(rt.kDashDotted) # kDashed

    return gMS

#end of load_ms

#_____________________________________________________________________________
def load_cck():

    #model by Guillermo at. al.
    f = open("data/data-dtdy-y_0-RHIC-clean_CCK.dat", "r")
    sigma = []
    for line in f:
        if line[0] == "#": continue
        p = line.split("\t")
        t = float(p[3])
        nucl = float(p[4])
        hs = float(p[8])
        sigma.append({ "t":t, "nucl":nucl, "hs":hs })

    #correction from gamma-Au to AuAu by Michal
    k_auau = 9.0296

    #scaling to XnXn
    kx = 0.1702

    gCCK = TGraphErrors(len(sigma))
    for i in range(len(sigma)):
        gCCK.SetPoint(i, sigma[i]["t"], sigma[i]["hs"]*k_auau*kx)

    gCCK.SetLineColor(rt.kRed)
    gCCK.SetLineWidth(3)
    gCCK.SetLineStyle(rt.kDashed) # 9

    return gCCK

#end of load_cck

#_____________________________________________________________________________
def load_sartre():

    sartre = TFile.Open("/home/jaroslav/sim/sartre_tx/sartre_AuAu_200GeV_Jpsi_coh_2p7Mevt.root")
    sartre_tree = sartre.Get("sartre_tree")

    hSartre = ut.prepare_TH1D("hSartre", 0.002, 0., 0.12)
    sartre_tree.Draw("-tval >> hSartre", "rapidity>-1 && rapidity<1")

    ut.norm_to_integral(hSartre, 0.025) # now same as Starlight

    gSartre = TGraphErrors(hSartre.GetNbinsX())
    for ibin in range(1,hSartre.GetNbinsX()+1):
        gSartre.SetPoint(ibin-1, hSartre.GetBinCenter(ibin), hSartre.GetBinContent(ibin))

    gSartre.SetLineColor(rt.kYellow+1)
    gSartre.SetLineWidth(3)
    #gSartre.SetLineStyle(rt.kDashDotted)

    return gSartre

#end of load_sartre

#_____________________________________________________________________________
def loat_flat_pt2():

    bgen = TFile.Open("/home/jaroslav/sim/bgen_tx/bgen_pTsq0p14_eta1p2_6Mevt.root")
    bgen_tree = bgen.Get("bgen_tree")

    hFlat = ut.prepare_TH1D("hFlat", 0.002, 0., 0.12)
    bgen_tree.Draw("pT2rec >> hFlat")

    ut.norm_to_integral(hFlat, 0.025) # norm to Starlight

    gFlat = ut.h1_to_graph(hFlat)

    gFlat.SetLineColor(rt.kViolet)
    gFlat.SetLineWidth(3)
    gFlat.SetLineStyle(rt.kDashed)

    return gFlat

#end of loat_flat_pt2


















