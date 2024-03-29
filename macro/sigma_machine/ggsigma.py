#!/usr/bin/python3

#gamma-gamma -> e+e- cross section and starlight prediction

from math import sqrt

from analyze_tree import AnalyzeTree

#_____________________________________________________________________________
if __name__ == "__main__":

    #rapidity, mass and max pT
    ymin = -1.
    ymax = 1.

    #mass
    #mmin = 2.1
    #mmax = 2.6
    mmin = 3.4
    mmax = 4.6

    #pT
    ptmax = 0.18

    #number of gamma-gamma from mass fit
    #Ngg = 332
    #nggerr = 11
    Ngg = 89
    nggerr = 3

    #fraction of 1n1n events
    #ratio_1n1n = 0.135
    #ratio_1n1n_err = 0.018
    ratio_1n1n = 0.168
    ratio_1n1n_err = 0.038
    #ratio_1n1n = 1.

    #lumi in inv. ub
    lumi = 13871.907

    #correction to luminosity for ana/triggered events
    ratio_ana = 3420950./3694000

    #scale the lumi for |z| around nominal bunch crossing
    ratio_zdc_vtx = 0.502

    #bemc trigger efficiency
    trg_eff = 0.67

    #tof correction to efficiency
    ratio_tof = 1.433

    #BBC veto inefficiency
    bbceff = 0.97

    #data
    #basedir_data = "../../../star-upc-data/ana/muDst/muDst_run1/sel5/"
    #datatree = basedir_data + "ana_muDst_run1_all_sel5z.root"

    #gamma-gamma mc
    basedir = "../../../star-upc-data/ana/starsim/"
    mctree = basedir + "slight14e/sel5/ana_slight14e2x1_sel5_nzvtx.root"
    #mctree = basedir + "slight14e/sel5/ana_slight14e2x1_s6_sel5z.root"

    #starlight total cross section of gamma-gamma -> e+e- and corresponding file
    sigma_starlight = 2.063
    starlight = "/home/jaroslav/sim/starlight_tx/slight_AuAu_200GeV_ggel_1n1n_m1p1_5p3_pT0p4_eta1p2_4Mevt.root"
    #sigma_starlight = 22.801
    #starlight = "/home/jaroslav/sim/starlight_tx/slight_AuAu_200GeV_ggel_m1p1_5p3_pT0p4_eta1p2_4Mevt.root"


    #configure the tree analyzer
    ana = AnalyzeTree()
    ana.SetMass(mmin, mmax)
    ana.SetY(ymin, ymax)
    ana.SetPt(ptmax)

    print("Mass: [", mmin, ",", mmax, "]")
    print("Ngg:", Ngg, "+/-", nggerr)

    print("ratio_1n1n:", ratio_1n1n, "+/-", ratio_1n1n_err)

    #scale the luminosity, explicit precision
    #lumi_scaled = lumi*ratio_ana*ratio_zdc_vtx
    lumi_scaled = float("{0:.3f}".format(lumi*ratio_ana*ratio_zdc_vtx))
    print("lumi_scaled:", lumi_scaled)

    #get the efficiency
    eff = ana.AnalyzeMC(mctree)
    print("eff: ", eff[0], "+/-", eff[1])

    #efficiency components
    print("trg_eff:", trg_eff)
    print("bbceff:", bbceff)
    print("ratio_tof:", ratio_tof)

    #calculate the cross section, nb
    sigma = float(1e3*Ngg*ratio_1n1n)/(eff[0]*trg_eff*bbceff*ratio_tof*lumi_scaled)

    #statistical error
    sigma_err = float(1e3*nggerr*ratio_1n1n)/(eff[0]*trg_eff*bbceff*ratio_tof*lumi_scaled)

    #systematic error
    sigma_sys = float(1e3*Ngg*ratio_1n1n_err)/(eff[0]*trg_eff*bbceff*ratio_tof*lumi_scaled)

    print("sigma:", sigma, "+/-", sigma_err, "+/-", sigma_sys)
    print("sigma:", sigma, "+/-", sqrt(sigma_err**2 + sigma_sys**2))

    #Starlight correction R_ym
    Rym = ana.AnalyzeStarlight(starlight, 4)
    print("R_ym: ", Rym)

    #theoretical prediction from Starlight, nb
    sigma_sta = sigma_starlight*Rym*1e3
    print("sigma_sta: ", sigma_sta)

    #ratio data/mc
    datamc = sigma/sigma_sta
    print("data/mc:", datamc)




















