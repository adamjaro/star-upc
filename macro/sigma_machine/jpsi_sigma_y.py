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
    #ybins = rt.vector(rt.double)([-1, 1])

    #|y| interval
    aymin = 0
    aymax = 1
    #aymax = 0.2
    #aymin = 0.2
    #aymax = 0.5
    #aymin = 0.5
    #aymax = 1

    #number of gamma-gamma from mass fit
    ngg = 162 # |y| < 1
    #ngg = 74 # |y| < 0.2
    #ngg = 62 # 0.2 < |y| < 0.5
    #ngg = 27 # 0.5 < |y| < 1

    #incoherent shape
    inc1 = 873.04 # |y| < 1  80.6/2 = 40.3
    inc2 = 3.28
    #inc1 = 270.8 # |y| < 0.2    24.4/0.4 = 61
    #inc2 = 3.77
    #inc1 = 328.35 # 0.2 < |y| < 0.5   30.9/0.6 = 51.5
    #inc2 = 2.92
    #inc1 = 285.88 # 0.5 < |y| < 1     26.2/1 = 26.2
    #inc2 = 3.43

    #maximal |t|
    tmax = 0.109

    #mass interval
    mmin = 2.8
    mmax = 3.2

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

    #Starlight
    gSlight = load_starlight_y()

    #data
    basedir = "../../../star-upc-data/ana/muDst/muDst_run1/sel5"
    infile = "ana_muDst_run1_all_sel5z.root"

    #MC
    basedir_sl = "../../../star-upc-data/ana/starsim/slight14e/sel5"
    infile_sl = "ana_slight14e1x3_s6_sel5z.root"
    #
    basedir_bgen = "../../../star-upc-data/ana/starsim/bgen14a/sel5"
    infile_bgen = "ana_bgen14a1_v0_sel5z_s6.root"
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
    #
    inp_bgen = TFile.Open(basedir_bgen+"/"+infile_bgen)
    tree_bgen_gen = inp_bgen.Get("jGenTree")

    #load the data
    mcsel = "jGenPt*jGenPt<{0:.3f}".format(tmax)
    mcsel += "&& TMath::Abs(jGenY)>{0:.3f} && TMath::Abs(jGenY)<{1:.3f}".format(aymin, aymax)
    datasel = "jRecM>{0:.3f} && jRecM<{1:.3f} && jRecPt*jRecPt<{2:.3f}".format(mmin, mmax, tmax)
    datasel += "&& TMath::Abs(jRecY)>{0:.3f} && TMath::Abs(jRecY)<{1:.3f}".format(aymin, aymax)

    #hY = ut.prepare_TH1D_vec("hY", ybins)
    hY = ut.prepare_TH1D_n("hY", 1, aymin, aymax)

    #tree.Draw("jRecY >> hY" , datasel)
    tree.Draw("TMath::Abs(jRecY) >> hY" , datasel)

    #for ibin in range(1, hY.GetNbinsX()+1):
        #print(ibin, hY.GetBinLowEdge(ibin), hY.GetBinLowEdge(ibin)+hY.GetBinWidth(ibin))

    #subtract gamma-gamma and incoherent components
    hY.Sumw2()
    print("Data entries:", hY.Integral())

    #gamma-gamma component
    #h_gg = ut.prepare_TH1D_vec("h_gg", ybins)
    h_gg = ut.prepare_TH1D_n("h_gg", 1, aymin, aymax)
    #tree_gg.Draw("jRecY >> h_gg" , datasel)
    tree_gg.Draw("TMath::Abs(jRecY) >> h_gg" , datasel)
    ut.norm_to_num(h_gg, ngg)
    print("Gamma-gamma component:", h_gg.Integral())

    #subtract the gamma-gamma component
    hY.Add(h_gg, -1)
    print("Entries after gamma-gamma subtraction:", hY.Integral())

    #incoherent functional shape
    func_incoh_pt2 = TF1("func_incoh", "[0]*exp(-[1]*x)", 0., 10.)
    func_incoh_pt2.SetParameters(inc1, inc2)

    #load the incoherent shape to retrieve its normalization
    inc_bins = ut.get_bins_vec_2pt(0.004, 0.01, 0, 0.109, 0.06)
    hPtIncoh = ut.prepare_TH1D_vec("hPtIncoh", inc_bins)
    ut.fill_h1_tf(hPtIncoh, func_incoh_pt2, rt.kRed)

    #subtract the incoherent component
    h_inc = hY.Clone()
    ut.norm_to_num(h_inc, hPtIncoh.Integral())
    print("Incoherent entries:", h_inc.Integral())
    hY.Add(h_inc, -1)

    print("Entries after all subtractions:", hY.GetBinContent(1), "+/-", hY.GetBinError(1))

    #AxE for coherent signal
    tree_mc = tree_sl_gen
    #tree_mc = tree_bgen_gen
    nall = tree_mc.Draw("", mcsel)
    nsel = tree_mc.Draw("", "jAccept==1"+"&&"+datasel)

    #selections to reproduce the deconv method:
    # "(jGenPt*jGenPt<{0:.3f})".format(tmax)
    # "jAccept==1"+"&&(jRecPt*jRecPt<{0:.3f})".format(tmax)

    axe = nsel/nall
    print("Numeric AxE:", axe)

    #scale the luminosity
    lumi_scaled = lumi*ratio_ana*ratio_zdc_vtx
    #print("lumi_scaled:", lumi_scaled)

    #denominator for the cross section in micro barn
    den = Reta*br*zdc_acc*trg_eff*bbceff*ratio_tof*lumi_scaled


    #calculate the cross section
    sigma = hY.GetBinContent(1)/(axe*den*hY.GetBinWidth(1)*2)
    sigma_err = hY.GetBinError(1)/(axe*den*hY.GetBinWidth(1)*2)
    print("Sigma (micro barn):", sigma, "+/-", sigma_err)

    return

    #apply the denominator and bin width
    #ut.norm_to_den_w(hY, den)
    #print("Integrated sigma from data (mb):", hY.GetBinContent(1), hY.GetBinError(1)) # hY.Integral("width")



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

