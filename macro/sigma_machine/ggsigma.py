#!/usr/bin/python

#gamma-gamma -> e+e- cross section and starlight prediction

from analyze_tree import AnalyzeTree

#_____________________________________________________________________________
if __name__ == "__main__":

    #rapidity, mass and max pT
    ymin = -1.
    ymax = 1.

    #mass
    mmin = 3.4
    mmax = 4.6

    #pT
    ptmax = 0.17

    ##number of gamma-gamma from mass fit
    #number of 1n1n events from ZDC fit
    Ngg = 16
    nggerr = 5

    #lumi in inv. ub
    lumi = 13871.907

    #correction to luminosity for ana/triggered events, dl-201810.01
    ratio_ana = 3420950./3694000

    #scale the lumi for |z| around nominal bunch crossing, dl-201810.02
    ratio_zdc = 0.205

    #embedding correction to starsim efficiency
    ratio_emb = 1.6

    #trigger efficiency
    trgeff = 0.673

    #BBC veto inefficiency
    bbceff = 0.97

    #gamma-gamma mc
    basedir = "../../../star-upc-data/ana/starsim/"
    mctree = basedir + "slight14d/sel5/ana_slight14d2_sel5a.root"

    #starlight total cross section of gamma-gamma -> e+e- and corresponding file
    sigma_starlight = 2.063
    starlight = "/home/jaroslav/sim/starlight_tx/slight_AuAu_200GeV_ggel_1n1n_m1p1_5p3_pT0p4_eta1p2_4Mevt.root"

    #configure the tree analyzer
    ana = AnalyzeTree()
    ana.SetMass(mmin, mmax)
    ana.SetY(ymin, ymax)
    ana.SetPt(ptmax)

    #scale the luminosity
    lumi_scaled = lumi*ratio_ana*ratio_zdc
    print "lumi_scaled:", lumi_scaled

    #get the efficiency
    eff = ana.AnalyzeMC(mctree)
    print "eff: ", eff[0], "+/-", eff[1]

    #Starlight correction R_ym
    Rym = ana.AnalyzeStarlight(starlight, 4)
    print "R_ym: ", Rym

    #calculate the cross section
    sigma = float(Ngg)/(eff[0]*trgeff*bbceff*ratio_emb*lumi_scaled)
    sigma_err = float(nggerr)/(eff[0]*trgeff*bbceff*ratio_emb*lumi_scaled)
    print "sigma:", sigma, "+/-", sigma_err

    #theoretical prediction from Starlight
    sigma_sta = sigma_starlight*Rym
    print "sigma_sta: ", sigma_sta

    #ratio data/mc
    datamc = sigma/sigma_sta
    print "data/mc:", datamc




















