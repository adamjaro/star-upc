#!/usr/bin/python

from ROOT import TFile

#_____________________________________________________________________________
if __name__ == "__main__":

    #all cross sections in microbarn

    #rapidity interval
    ymin = -1
    ymax = 1

    #top folder with starlight data
    top = "/home/jaroslav/sim/starlight_tx/"

    #input for no restriction on Coulomb breakup
    sigma0 = 463.574
    in0 = TFile.Open(top+"slight_AuAu_200GeV_Jpsi_coh_bmod5_6Mevt.root")
    tree0 = in0.Get("slight_tree")

    #input for Xn (abbreviated from XnXn + 0nXn + Xn0n)
    sigma_xn = 244.342
    in_xn = TFile.Open(top+"slight_AuAu_200GeV_Jpsi_coh_Xn_6Mevt.root")
    tree_xn = in_xn.Get("slight_tree")

    #input for XnXn
    sigma_xnxn = 67.958
    in_xnxn = TFile.Open(top+"slight_AuAu_200GeV_Jpsi_coh_6Mevt.root")
    tree_xnxn = in_xnxn.Get("slight_tree")

    #rapidity ratios
    strsel = "rapidity>{0:.3f} && rapidity<{1:.3f}".format(ymin, ymax)
    ry_0 = float(tree0.Draw("", strsel))/float(tree0.GetEntries())
    ry_xn = float(tree_xn.Draw("", strsel))/float(tree_xn.GetEntries())
    ry_xnxn = float(tree_xnxn.Draw("", strsel))/float(tree_xnxn.GetEntries())

    #print ry_0, ry_xn, ry_xnxn

    #scaling to Xn
    k_xn = (sigma_xn*ry_xn)/(sigma0*ry_0)
    print "k_xn: {0:.4f}".format(k_xn)

    #scaling to XnXn
    k_xnxn = (sigma_xnxn*ry_xnxn)/(sigma0*ry_0)
    print "k_xnxn: {0:.4f}".format(k_xnxn)

    #scaling from Xn to XnXn
    k_xn_xnxn = (sigma_xnxn*ry_xnxn)/(sigma_xn*ry_xn)
    print "k_xn_xnxn: {0:.4f}".format(k_xn_xnxn)


















