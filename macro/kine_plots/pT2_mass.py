#!/usr/bin/python3

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TLine, TMath, TLatex

import sys
sys.path.append('../')
import plot_utils as ut
#from parameter_descriptor import parameter_descriptor as pdesc

#_____________________________________________________________________________
def main():

    iplot = 3

    func = {}
    func[0] = pT_mass
    func[1] = pT2_mass
    func[2] = lpT2_mass
    func[3] = lpT2_mass_mc

    func[iplot]()

#_____________________________________________________________________________
def pT_mass():

    inp = "../../../star-upc-data/ana/muDst/muDst_run1/sel5/ana_muDst_run1_all_sel5z.root"
    #inp = "../../../star-upc-data/ana/muDst/muDst_run1/sel5/ana_muDst_run1_all_sel5z_ls.root"

    #pT
    ybin = 0.02
    ymin = 0
    ymax = 1.5

    #mass
    xbin = 0.05
    xmin = 1.1
    xmax = 5

    infile = TFile.Open(inp)
    tree = infile.Get("jRecTree")

    can = ut.box_canvas()

    hPt2M = ut.prepare_TH2D("hPt2M", xbin, xmin, xmax, ybin, ymin, ymax)

    tree.Draw("jRecPt:jRecM >> hPt2M")

    hPt2M.SetMinimum(0.98)
    hPt2M.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def pT2_mass():

    inp = "../../../star-upc-data/ana/muDst/muDst_run1/sel5/ana_muDst_run1_all_sel5z.root"
    #inp = "../../../star-upc-data/ana/muDst/muDst_run1/sel5/ana_muDst_run1_all_sel5z_ls.root"

    #pT^2
    ybin = 0.02
    ymin = 0
    ymax = 1

    #mass
    xbin = 0.05
    xmin = 1.1
    xmax = 5

    infile = TFile.Open(inp)
    tree = infile.Get("jRecTree")

    can = ut.box_canvas()

    hPt2M = ut.prepare_TH2D("hPt2M", xbin, xmin, xmax, ybin, ymin, ymax)

    tree.Draw("jRecPt*jRecPt:jRecM >> hPt2M")

    hPt2M.SetMinimum(0.98)
    hPt2M.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def lpT2_mass():

    #data
    inp = "../../../star-upc-data/ana/muDst/muDst_run1/sel5/ana_muDst_run1_all_sel5z.root"
    #inp = "../../../star-upc-data/ana/muDst/muDst_run1/sel5/ana_muDst_run1_all_sel5z_ls.root"

    #gamma-gamma
    #inp = "../../../star-upc-data/ana/starsim/slight14e/sel5/ana_slight14e2x1_sel5_nzvtx.root"

    #incoherent
    #inp = "../../../star-upc-data/ana/starsim/slight14e/sel5/ana_slight14e3_sel5z.root"

    #log_10(pT^2)
    ybin = 0.14
    ymin = -5
    ymax = 1

    #mass
    xbin = 0.08
    xmin = 1.2
    xmax = 4.3

    infile = TFile.Open(inp)
    tree = infile.Get("jRecTree")

    can = ut.box_canvas()

    hPt2M = ut.prepare_TH2D("hPt2M", xbin, xmin, xmax, ybin, ymin, ymax)

    tree.Draw("TMath::Log10(jRecPt*jRecPt):jRecM >> hPt2M")

    hPt2M.SetMinimum(0.98)
    hPt2M.SetContour(300)

    ut.put_yx_tit(hPt2M, "log_{10}( #it{p}_{T}^{2} ) (GeV^{2})", "#it{m}_{e^{+}e^{-}} (GeV/c^{2})", 1.4, 1.3)
    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.02, 0.1)

    gPad.SetLogz()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def lpT2_mass_mc():

    #data
    #inp = "../../../star-upc-data/ana/muDst/muDst_run1/sel5/ana_muDst_run1_all_sel5z.root"
    inp_ls = "../../../star-upc-data/ana/muDst/muDst_run1/sel5/ana_muDst_run1_all_sel5z_ls.root"

    #gamma-gamma
    inp_gg = "../../../star-upc-data/ana/starsim/slight14e/sel5/ana_slight14e2x1_sel5_nzvtx.root"

    #incoherent
    inp_inc = "../../../star-upc-data/ana/starsim/slight14e/sel5/ana_slight14e3_sel5z.root"

    #coherent
    inp_coh = "../../../star-upc-data/ana/starsim/slight14e/sel5/ana_slight14e1x3_s6_sel5z.root"

    #log_10(pT^2)
    ybin = 0.14
    ymin = -5
    ymax = 1

    #mass
    xbin = 0.08
    xmin = 1.2
    #xmax = 4.3
    xmax = 4.5

    infile_gg = TFile.Open(inp_gg)
    tree_gg = infile_gg.Get("jRecTree")

    infile_inc = TFile.Open(inp_inc)
    tree_inc = infile_inc.Get("jRecTree")

    infile_coh = TFile.Open(inp_coh)
    tree_coh = infile_coh.Get("jRecTree")

    infile_ls = TFile.Open(inp_ls)
    tree_ls = infile_ls.Get("jRecTree")

    #gamma-gamma MC
    h_gg = ut.prepare_TH2D("h_gg", xbin, xmin, xmax, ybin, ymin, ymax)
    h_gg.SetLineColor(rt.kYellow)
    h_gg.SetFillColor(rt.kYellow)

    tree_gg.Draw("TMath::Log10(jRecPt*jRecPt):jRecM >> h_gg")
    h_gg.Scale(162/h_gg.Integral("width")) # scale the gamma-gamma to the data
    h_gg.SetContour(300)

    #incoherent MC
    h_inc = ut.prepare_TH2D("h_inc", xbin, xmin, xmax, ybin, ymin, ymax)
    h_inc.SetLineColor(rt.kRed)
    h_inc.SetFillColor(rt.kRed)

    tree_inc.Draw("TMath::Log10(jRecPt*jRecPt):jRecM >> h_inc")
    h_inc.Scale(81/h_inc.Integral("width")) # scale the incoherent MC to the data

    #coherent MC
    h_coh = ut.prepare_TH2D("h_coh", xbin, xmin, xmax, ybin, ymin, ymax)
    h_coh.SetLineColor(rt.kGreen)
    h_coh.SetFillColor(rt.kGreen)

    tree_coh.Draw("TMath::Log10(jRecPt*jRecPt):jRecM >> h_coh")
    h_coh.Scale(460/h_coh.Integral("width")) # scale the coherent MC to the data

    #like-sign data
    h_ls = ut.prepare_TH2D("h_ls", xbin, xmin, xmax, ybin, ymin, ymax)
    h_ls.SetLineColor(rt.kMagenta)
    h_ls.SetFillColor(rt.kMagenta)

    tree_ls.Draw("TMath::Log10(jRecPt*jRecPt):jRecM >> h_ls", "", "boxsame")

    #make the plot
    can = ut.box_canvas()

    h_gg.Scale(h_coh.GetMaximum()/h_gg.GetMaximum())# gamma-gamma range to the scale of coherent MC

    h_gg.Draw("colzsame")

    h_coh.Draw("boxsame")

    h_inc.Draw("boxsame")

    h_ls.Draw("boxsame")

    ut.put_yx_tit(h_gg, "log_{10}( #it{p}_{T}^{2} ) (GeV^{2})", "#it{m}_{e^{+}e^{-}} (GeV)", 1.4, 1.3)

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.02, 0.01)

    gPad.SetGrid()

    #vertical line in mass
    msep = 2.8 # GeV
    mlin = TLine(msep, ymin, msep, ymax)
    mlin.SetLineStyle(rt.kDashed)
    mlin.SetLineWidth(4)
    mlin.Draw("same")

    mlin_des = TLatex()
    mlin_des.SetTextSize(0.035)
    mlin_des.DrawLatex(2.82, -4.7, "#it{m}_{e^{+}e^{-}} = 2.8 GeV")

    #horizontal line in pT
    pTsep = 0.18 # GeV
    plin = TLine(xmin, TMath.Log10(pTsep*pTsep), xmax, TMath.Log10(pTsep*pTsep))
    plin.SetLineStyle(rt.kDashed)
    plin.SetLineWidth(4)
    plin.Draw("same")

    plin_des = TLatex()
    plin_des.SetTextSize(0.035)
    plin_des.DrawLatex(1.3, -1.3, "#it{p}_{T} = 0.18 GeV")

    ls_leg = ut.prepare_leg(0.14, 0.9, 0.15, 0.05, 0.035)
    ls_leg.AddEntry(h_ls, "Like-sign data", "f")
    ls_leg.Draw("same")

    inc_leg = ut.prepare_leg(0.72, 0.9, 0.15, 0.05, 0.035)
    inc_leg.AddEntry(h_inc, "Incoherent MC", "f")
    inc_leg.Draw("same")

    coh_leg = ut.prepare_leg(0.72, 0.55, 0.15, 0.05, 0.035)
    coh_leg.AddEntry(h_coh, "Coherent MC", "f")
    coh_leg.Draw("same")

    gg_leg = ut.prepare_leg(0.14, 0.2, 0.15, 0.05, 0.035)
    gg_leg.AddEntry(h_gg, "#gamma#gamma#rightarrow e^{+}e^{-} MC", "f")
    gg_leg.Draw("same")

    #gStyle.SetPalette(56)
    gStyle.SetPalette(53)
    ut.invert_col(rt.gPad)

    #offset in color axis
    gPad.Update()
    palette = h_gg.GetListOfFunctions().FindObject("palette")
    deltx = 0.2
    palette.SetX1NDC( palette.GetX1NDC() + deltx )
    palette.SetX2NDC( palette.GetX2NDC() + deltx )

    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)
    gStyle.SetFrameLineWidth(2)

    main()











