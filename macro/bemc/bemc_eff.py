#!/usr/bin/python

import math

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TH1D
from ROOT import vector

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def get_input(tree, bnam, bmatch):

    #load tracks momenta to lists for all and matched tracks

    tree.SetBranchStatus("*", 0)
    tree.SetBranchStatus(bnam[0], 1)
    tree.SetBranchStatus(bnam[1], 1)
    tree.SetBranchStatus(bmatch[0], 1)
    tree.SetBranchStatus(bmatch[1], 1)

    valAll = []
    valSel = []

    for i in range(tree.GetEntriesFast()):
        tree.GetEntry(i)
        exec("p0 = tree."+bnam[0])
        exec("p1 = tree."+bnam[1])
        exec("match0 = tree."+bmatch[0])
        exec("match1 = tree."+bmatch[1])
        valAll.append(p0)
        valAll.append(p1)
        if match0 == True: valSel.append(p0)
        if match1 == True: valSel.append(p1)
 
    valAll.sort()
    valSel.sort()

    return valAll, valSel

#_____________________________________________________________________________
def get_eff(nsel, nall):

    #efficiency and Binomial error

    #no input
    if nsel == 0 or nall == 0:
        return 0., 0.

    #equal numbers
    if nsel == nall:
        return 1., 1.

    #make the calculation
    eff = float(nsel)/float(nall)
    err = eff*math.sqrt( float(nall-nsel)/float(nall*nsel) )
    return eff, err

#_____________________________________________________________________________
def get_bins(valAll, valSel, prec, delt, minw, maxw):

    #bin edges

    valAll.sort()
    valSel.sort()

    #range for the edges
    minval = valSel[0]
    maxval = valSel[len(valSel)-1]
    print "Range for bin edges:", minval, maxval

    #move both lists to the start of the range
    while valAll[0] < minval: valAll.pop(0)
    while valSel[0] < minval: valSel.pop(0)

    #initialize current minimum and maximum
    cmin = minval
    cmax = minval + delt

    #bin edges
    bins = []
    bins.append(cmin)

    nall = 0
    nsel = 0
    #find bin edges
    while True:
        while valAll != [] and valAll[0] < cmax:
            nall += 1
            valAll.pop(0)
        while valSel != [] and valSel[0] < cmax:
            nsel += 1
            valSel.pop(0)

        #efficiency, Binomial error and relative error
        eff, err = get_eff(nsel, nall)
        rel = 1.
        if eff > 1.e-4: rel = err/eff

        #test for maximal allowed error
        if rel > 1.e-4 and rel < prec:
            #bin edge found, max relative error satisfied
            bins.append(cmax)
            #move to next bin
            cmin = cmax
            #reset the counters for next bin
            nall = 0
            nsel = 0

        #increment current upper limit
        cmax += delt

        #test for end of momenta interval
        if cmax > maxval:
            #set last found edge to the end of values interval and finish
            bins[len(bins)-1] = maxval
            break

    return bins


#_____________________________________________________________________________
if __name__ == "__main__":

    basedir = "../../../star-upc-data/ana/muDst"

    infile = "muDst_run1a/conv0/ana_muDst_run1a_all_conv0.root"

    precision = 0.06
    delta = 1.e-7
    minw = -0.05
    maxw = -0.8

    logx = True

    #branches with momentum at BEMC and matching information
    bnam = ["jT0bemcP", "jT1bemcP"]
    bmatch = ["jT0matchBemc", "jT1matchBemc"]

    #selection for basic input range
    strsel = bnam[0]+"<5 && "+bnam[1]+"<5"

    #line color for fit
    #clin = rt.kMagenta
    clin = rt.kBlue

    #-- end of config --

    gROOT.SetBatch()

    #output temporary file
    outnam = "tmp.root"
    #input and output
    inp = TFile.Open(basedir+"/"+infile)
    out = TFile.Open(outnam, "recreate")

    #get input tree, apply the selection
    tree = inp.Get("jRecTree").CopyTree(strsel)

    #number of bins and bin edges
    valAll, valSel = get_input(tree, bnam, bmatch)
    bins = get_bins(valAll, valSel, precision, delta, minw, maxw)
    #bins = [0.19127007420789358, 0.6585125741333373, 0.7662370740766359, 0.8353138740402769, 0.9004561740059889, 0.9510194739793746, 1.0171439739636032, 1.0616465739895868, 1.1146149740205133, 1.170406074053088, 1.2332706740897925, 1.2877973741216289, 1.3584872741629024, 1.3911401741819673, 1.4620089742233453, 1.5808449742927297, 1.6722981743461263, 1.7565375743953109, 1.922577274492256, 2.26370917410588, 4.423392334918047]

    vbins = vector(rt.double)()
    for i in xrange(len(bins)):
        vbins.push_back(bins[i])


    #momenta and efficiency histograms
    nbins = len(bins)-1
    hAll = TH1D("hAll", "hAll", nbins, vbins.data())
    hSel = TH1D("hSel", "hSel", nbins, vbins.data())
    hAll.Sumw2()
    hSel.Sumw2()
    tree.Draw(bnam[0]+" >>  hAll")
    tree.Draw(bnam[1]+" >>+ hAll")
    tree.Draw(bnam[0]+" >>  hSel", bmatch[0]+"==1")
    tree.Draw(bnam[1]+" >>+ hSel", bmatch[1]+"==1")

    #calculate the efficiency
    hEff = TH1D("hEff", "hEff", nbins, vbins.data())
    hEff.Divide(hSel, hAll, 1, 1, "B")


    #plot the efficiency
    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)

    can = ut.box_canvas()

    gPad.SetTopMargin(0.01)
    gPad.SetRightMargin(0.01)
    gPad.SetBottomMargin(0.12)
    gPad.SetLeftMargin(0.1)

    ut.set_H1D(hEff)

    hEff.SetTitleOffset(1.4, "Y")
    hEff.SetTitleOffset(1.5, "X")

    hEff.SetXTitle("Track momentum #it{p}_{tot} at BEMC (GeV)")
    hEff.SetYTitle("BEMC efficiency")
    hEff.SetTitle("")

    hEff.GetXaxis().SetMoreLogLabels()

    if logx == True: gPad.SetLogx()

    hEff.Draw()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")


    #to prevent 'pure virtual method called'
    gPad.Close()

    #remove the temporary
    gSystem.Exec("rm -f "+outnam)

    #beep when finished
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")

#    for i in range(12):
#        print valAll[i], valSel[i]

#    print len(valAll), len(valSel)















