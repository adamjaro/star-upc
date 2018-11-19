#!/usr/bin/python

#gamma-gamma -> e+e- cross section and starlight prediction

from analyze_tree import AnalyzeTree

#_____________________________________________________________________________
if __name__ == "__main__":

    #rapidity, mass and max pT
    ymin = -1.
    ymax = 1.

    #mass
    mmin = 2.1
    mmax = 2.6

    #pT
    ptmax = 0.17

    #number of gamma-gamma from mass fit
    Ngg = 324
    nggerr = 11

    #fraction of 1n1n events
    ratio_1n1n = 0.136

    #lumi in inv. ub
    lumi = 13871.907

    #correction to luminosity for ana/triggered events
    ratio_ana = 3420950./3694000

    #scale the lumi for |z| around nominal bunch crossing
    ratio_zdc_vtx = 0.502

    #tof correction to efficiency
    ratio_tof = 1.433

    #BBC veto inefficiency
    bbceff = 0.97

    #data
    basedir_data = "../../../star-upc-data/ana/muDst/muDst_run1/sel5/"
    datatree = basedir_data + "ana_muDst_run1_all_sel5z.root"

    #gamma-gamma mc
    basedir = "../../../star-upc-data/ana/starsim/"
    mctree = basedir + "slight14e/sel5/ana_slight14e2x1_sel5_nzvtx.root"

    #starlight total cross section of gamma-gamma -> e+e- and corresponding file
    sigma_starlight = 2.063
    starlight = "/home/jaroslav/sim/starlight_tx/slight_AuAu_200GeV_ggel_1n1n_m1p1_5p3_pT0p4_eta1p2_4Mevt.root"


    #configure the tree analyzer
    ana = AnalyzeTree()
    ana.SetMass(mmin, mmax)
    ana.SetY(ymin, ymax)
    ana.SetPt(ptmax)

    print "Mass: [", mmin, ",", mmax, "]"
    print "Ngg:", Ngg, "+/-", nggerr

    #scale the luminosity
    lumi_scaled = lumi*ratio_ana*ratio_zdc_vtx
    print "lumi_scaled:", lumi_scaled

    #get the efficiency
    eff = ana.AnalyzeMC(mctree)
    print "eff: ", eff[0], "+/-", eff[1]

    #calculate the cross section
    sigma = float(Ngg*ratio_1n1n)/(eff[0]*bbceff*ratio_tof*lumi_scaled)
    sigma_err = float(nggerr*ratio_1n1n)/(eff[0]*bbceff*ratio_tof*lumi_scaled)
    print "sigma:", sigma, "+/-", sigma_err

    #Starlight correction R_ym
    Rym = ana.AnalyzeStarlight(starlight, 4)
    print "R_ym: ", Rym

    #theoretical prediction from Starlight
    sigma_sta = sigma_starlight*Rym
    print "sigma_sta: ", sigma_sta

    #ratio data/mc
    datamc = sigma/sigma_sta
    print "data/mc:", datamc




















