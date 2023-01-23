#!/usr/bin/python3

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile
from ROOT import TGraphAsymmErrors, TF1

import sys
sys.path.append('../')
import plot_utils as ut

from models import load_starlight_y

#_____________________________________________________________________________
def main():

    #bins in |y|
    #ybins = rt.vector(rt.double)([0, 0.2, 0.5, 1])
    ybins = rt.vector(rt.double)([-1, 1])

    #mass interval
    mmin = 2.8
    mmax = 3.2

    #maximal |t|
    tmax = 0.109

    ngg = 131  # number of gamma-gamma from mass fit

    lumi = 13871.907 # lumi in inv. ub

    #correction to luminosity for ana/triggered events
    ratio_ana = 3420950./3694000

    #scale the lumi for |z| around nominal bunch crossing
    ratio_zdc_vtx = 0.502

    Reta = 0.503 # pseudorapidity preselection
    #Reta = 1.

    trg_eff = 0.67 # bemc trigger efficiency

    ratio_tof = 1.433 # tof correction to efficiency

    bbceff = 0.97 # BBC veto inefficiency

    zdc_acc = 0.49 # ZDC acceptance to XnXn 0.7
    #zdc_acc = 1.

    br = 0.05971 # dielectrons branching ratio

    #double length for |y| bins because of abs value
    #abs_bins = 2.
    abs_bins = 1.

    #Starlight
    gSlight = load_starlight_y()

    #data
    basedir = "../../../star-upc-data/ana/muDst/muDst_run1/sel5"
    infile = "ana_muDst_run1_all_sel5z.root"

    #MC
    basedir_sl = "../../../star-upc-data/ana/starsim/slight14e/sel5"
    infile_sl = "ana_slight14e1x3_s6_sel5z.root"
    #
    basedir_gg = "../../../star-upc-data/ana/starsim/slight14e/sel5"
    infile_gg = "ana_slight14e2x1_sel5_nzvtx.root"

    #open the inputs
    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("jRecTree")
    #
    inp_sl = TFile.Open(basedir_sl+"/"+infile_sl)
    tree_sl_gen = inp_sl.Get("jGenTree")
    #
    inp_gg = TFile.Open(basedir_gg+"/"+infile_gg)
    tree_gg = inp_gg.Get("jRecTree")

    #load the data
    datasel = "jRecM>{0:.3f} && jRecM<{1:.3f} && jRecPt*jRecPt<{2:.3f}".format(mmin, mmax, tmax)
    mcsel = "jGenM>{0:.3f} && jGenM<{1:.3f} && jGenPt*jGenPt<{2:.3f}".format(mmin, mmax, tmax)

    hY = ut.prepare_TH1D_vec("hY", ybins)
    #tree.Draw("TMath::Abs(jRecY) >> hY" , datasel)
    tree.Draw("jRecY >> hY" , datasel)

    #for ibin in range(1, hY.GetNbinsX()+1):
        #print(ibin, hY.GetBinLowEdge(ibin), hY.GetBinLowEdge(ibin)+hY.GetBinWidth(ibin))

    #subtract gamma-gamma and incoherent components
    hY.Sumw2()
    print("Data entries:", hY.Integral())

    #gamma-gamma component
    h_gg = ut.prepare_TH1D_vec("h_gg", ybins)
    #tree_gg.Draw("TMath::Abs(jRecY) >> h_gg" , datasel)
    tree_gg.Draw("jRecY >> h_gg" , datasel)
    ut.norm_to_num(h_gg, ngg)
    print("Gamma-gamma component:", h_gg.Integral())

    #subtract the gamma-gamma component
    hY.Add(h_gg, -1)
    print("Entries after gamma-gamma subtraction:", hY.Integral())

    #incoherent functional shape
    func_incoh_pt2 = TF1("func_incoh", "[0]*exp(-[1]*x)", 0., 10.)
    func_incoh_pt2.SetParameters(873.04, 3.28)

    #load the incoherent shape to retrieve its normalization
    inc_bins = ut.get_bins_vec_2pt(0.004, 0.01, 0, 0.109, 0.06)
    hPtIncoh = ut.prepare_TH1D_vec("hPtIncoh", inc_bins)
    ut.fill_h1_tf(hPtIncoh, func_incoh_pt2, rt.kRed)

    #subtract the incoherent component
    h_inc = hY.Clone()
    ut.norm_to_num(h_inc, hPtIncoh.Integral())
    print("Incoherent entries:", h_inc.Integral())
    hY.Add(h_inc, -1)

    print("Entries after all subtractions:", hY.Integral())

    #AxE for coherent signal
    h_sl_all = ut.prepare_TH1D_vec("h_sl_all", ybins)
    h_sl_sel = ut.prepare_TH1D_vec("h_sl_sel", ybins)
    tree_sl_gen.Draw("jGenY >> h_sl_all")
    tree_sl_gen.Draw("jGenY >> h_sl_sel", "jAccept==1")
    axe = TGraphAsymmErrors(h_sl_sel, h_sl_all)
    h_sl_sel.Sumw2()
    h_sl_sel.Divide(h_sl_all)

    #for i in range(axe.GetN()):
        #print(i, axe.GetPointY(i))
    #for i in range(1, h_sl_sel.GetNbinsX()+1):
        #print(i, h_sl_sel.GetBinContent(i))

    #apply the AxE
    hY.Divide(h_sl_sel)

    #scale the luminosity
    lumi_scaled = lumi*ratio_ana*ratio_zdc_vtx
    #print("lumi_scaled:", lumi_scaled)

    #denominator for the cross section, conversion ub to mb
    den = Reta*br*zdc_acc*trg_eff*bbceff*ratio_tof*lumi_scaled*1000.*abs_bins

    #apply the denominator and bin width
    ut.norm_to_den_w(hY, den)

    print("Integrated sigma from data (mb):", hY.Integral("width"))

    #plot the data (development)
    can = ut.box_canvas()
    hY.Draw()

    gSlight.Draw("lsame")
    #gSlight.Draw("al")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")






#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()

