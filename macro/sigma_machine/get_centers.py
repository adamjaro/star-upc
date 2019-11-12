#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TF1, vector, TMath, TGraphErrors

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    #testing macro for bin centers from the data

    gROOT.SetBatch()

    #range for |t|
    ptmin = 0.
    ptmax = 0.109  #   0.109  0.01 for interference range

    #default binning
    ptbin = 0.004   # 0.004  0.0005 for interference range

    #long bins at high |t|
    ptmid = 0.06  # 0.08, value > ptmax will switch it off   0.06
    ptlon = 0.01  # 0.01

    #mass interval
    mmin = 2.8
    mmax = 3.2

    #data
    basedir = "../../../star-upc-data/ana/muDst/muDst_run1/sel5"
    infile = "ana_muDst_run1_all_sel5z.root"

    #open the inputs
    inp = TFile.Open(basedir+"/"+infile)
    tree = inp.Get("jRecTree")

    #evaluate binning
    bins = ut.get_bins_vec_2pt(ptbin, ptlon, ptmin, ptmax, ptmid)

    #load the data
    strsel = "jRecM>{0:.3f} && jRecM<{1:.3f}".format(mmin, mmax)

    #input pT^2
    hPt = ut.prepare_TH1D_vec("hPt", bins)
    tree.Draw("jRecPt*jRecPt >> hPt" , strsel)

    #bin centers from the data
    cen_tree = get_centers_from_tree(hPt, tree, strsel)
    #print
    cen_toyMC = get_centers_from_toyMC(hPt)

    for i in xrange(len(cen_tree)):
        #print i, cen_tree[i], cen_toyMC[i], cen_tree[i] - cen_toyMC[i]
        pass

    #gr = get_data_graph(hPt, cen_tree)
    gr = get_data_graph(hPt, cen_toyMC)

    #plot the distribution
    can = ut.box_canvas()
    frame = ut.prepare_TH1D("frame", ptbin, ptmin, ptmax)
    #ut.set_margin_lbtr(gPad, 0.1, 0.09, 0.03, 0.03)
    ut.set_margin_lbtr(gPad, 0.1, 0.09, 0.055, 0.03)
    gPad.SetLogy()

    frame.SetMaximum(310)
    #frame.SetMinimum(1.e-6)
    frame.SetMinimum(3)
    #frame.SetMinimum(1e-5)  # 3e-5
    frame.Draw()

    #hPt.Draw("e1same")
    gr.Draw("epsame")

    ut.invert_col(gPad)
    can.SaveAs("01fig.pdf")

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")

#_____________________________________________________________________________
def get_centers_from_tree(hPt, tree, strsel):

    #bin center points according to the data in existing input tree

    centers = []

    #apply selection to the input data
    inp = tree.CopyTree(strsel)

    #get the pT values in the tree
    gROOT.ProcessLine("struct pTval {Double_t val;};")
    pT = rt.pTval()

    inp.SetBranchStatus("*", 0)
    inp.SetBranchStatus("jRecPt", 1)
    inp.SetBranchAddress("jRecPt", rt.AddressOf(pT, "val"))

    for i in xrange(1, hPt.GetNbinsX()+1):

        pt2mean = 0.
        npt = 0
        pt2min = hPt.GetBinLowEdge(i)
        pt2max = hPt.GetBinLowEdge(i) + hPt.GetBinWidth(i)

        for j in xrange(inp.GetEntriesFast()):
            inp.GetEntry(j)
            pt2 = pT.val**2
            if pt2 < pt2min or pt2 > pt2max: continue
            pt2mean += pt2
            npt += 1
            #print pt2, pt2mean, npt

        if npt > 0:
            pt2mean = pt2mean/npt
        else:
            pt2mean = 999.

        centers.append({"val":pt2mean, "err":0})

        #print i, hPt.GetBinCenter(i), pt2mean, hPt.GetBinCenter(i) - pt2mean
        #print i, hPt.GetBinCenter(i) - pt2mean

    return centers


#_____________________________________________________________________________
def get_centers_from_toyMC(hPt):

    #bin center points according using the input distribution as a toyMC

    centers = []

    #generate the toyMC
    pt2val = []
    for i in xrange(int(1e5)):
        pt2val.append( hPt.GetRandom() )

    #get mean values from the toyMC
    for i in xrange(1, hPt.GetNbinsX()+1):

        pt2mean = 0.
        npt = 0
        pt2min = hPt.GetBinLowEdge(i)
        pt2max = hPt.GetBinLowEdge(i) + hPt.GetBinWidth(i)

        #calculate the mean for a given bin
        for pt2 in pt2val:

            if pt2 < pt2min or pt2 > pt2max: continue
            pt2mean += pt2
            npt += 1
            #print pt2, pt2mean, npt

        if npt > 0:
            pt2mean = pt2mean/npt
        else:
            pt2mean = 999.

        #horizontal error from number of events in a given bin
        nev = int(hPt.GetBinContent(i))
        #print nev
        means = []
        j = -1
        #repeat mean calculation for samples of 'nev' events from toyMC data
        while True:
            mval = 0
            i = 0
            while i < nev:
            #for i in xrange(nev):
                j += 1
                if j >= len(pt2val):
                    mval = -999;
                    break

                pt2 = pt2val[j]
                if pt2 < pt2min or pt2 > pt2max: continue
                mval += pt2
                i += 1

            if mval > 0:
                means.append(mval/nev)

            if j < len(pt2val): continue
            break

        #calculate mean of differences partial means as the horizontal error
        #merr = 0
        #for m in means:
            #merr += m
        #merr = merr/len(means)

        #calculate RMS of partial means relative to the full mean as the horizontal error
        rms = 0.
        for m in means:
            rms += (pt2mean - m)**2
        rms = rms/len(means)
        rms = TMath.Sqrt(rms)

        print pt2mean, rms

        centers.append({"val":pt2mean, "err":rms})

        #print i, hPt.GetBinCenter(i), pt2mean, hPt.GetBinCenter(i) - pt2mean

    return centers


#_____________________________________________________________________________
def get_data_graph(hx, centers):

    #make graph erros from input distribution and bin centers
    gr = TGraphErrors(hx.GetNbinsX())

    for i in xrange(hx.GetNbinsX()):
        gr.SetPoint(i, centers[i]["val"], hx.GetBinContent(i+1))
        gr.SetPointError(i, centers[i]["err"], hx.GetBinError(i+1))

    return gr



#_____________________________________________________________________________
if __name__ == "__main__":

    main()























