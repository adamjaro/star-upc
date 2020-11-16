
//plot routines to compare data and MC

//local headers
#include "plotUtils.h"

TCanvas *c3;
TCanvas *c4;
TCanvas *can;
TTree *dataTree; TTree *mcrecTree; TTree *mcgenTree;
TLegend *leg; TLegend *leg1; TLegend *leg2;
string basedir, datainp, mcinp;

Double_t ymin=-9999., ymax=9999., mmin=-9999., mmax=9999., ptmax=9999.;
Int_t nMCbin=-1;
Double_t yspace;
string *glrec; string *gxtit;
Double_t *gxbin; Double_t *gxmin; Double_t *gxmax;

void Init();
Double_t GetMax(Double_t x1, Double_t x2, Double_t x3);
Double_t GetMin(Double_t x1, Double_t x2, Double_t x3);

//_____________________________________________________________________________
void ControlPlotsDataMC() {

  basedir = "../../../star-upc-data/ana/";

  datainp = "muDst/muDst_run1/sel5/ana_muDst_run1_all_sel5z.root";
  //datainp = "st/sel0/ana_muDst_run0_all_sel0a.root";
  mcinp = "starsim/slight14e/sel5/ana_slight14e1x3_s6_sel5z.root";
  //mcinp = "st/sel0/ana_muDst_run0_all_sel0.root";



  ymin = -1.; ymax = 1.;

  //mmin = 2.1; mmax = 2.6;
  mmin = 2.8; mmax = 3.2;
  //mmin = 1.5; mmax = 5.;

  ptmax = 0.18;

  Init();

  Int_t set   = 2;
  Int_t iplot = 5;

  Int_t trkCharge = 0; // track charge to plot, 0 = both, -1 = negative, 1 = positive

  //nMCbin = 100; // set bins for MC manually

  Bool_t logY = 0;
  Double_t vmin = 0.8; // minimum with log scale

  yspace = 1.2; // 1.2  30  1.4

  string datalabel = "Data";
  //string mclabel = "MC rec";
  string mclabel = "MC";

  if(set == 0) {
  // set 0, z of PV, deltaPhi
  // iplot                     0          1               2               3         4           5         6          7
  //                       z of PV  opening angle   BEMC energy / p   rapidity  delta eta    delta phi  trk phi   trk eta
  static string lrec[] = {  "jVtxZ", "jDeltaPhi", "jT0bemcE/jT0bemcP", "jRecY", "jT0Deta",  "jT0Dphi",  "jT0phi", "jT0eta"};
  static Double_t xbin[] = {   6.,      0.01,             0.05,         0.15,     0.005,      0.008,      0.9,      0.2};
  static Double_t xmin[] = { -110.,     2.5,              0.,           -1.3,    -0.10,       -0.1,       -4.,      -1.2};
  static Double_t xmax[] = {  110.,     3.42,             2.,           1.3,      0.10,       0.1,        4.,       1.2};
  static string xtit[] = {
    "#it{z} of primary vertex (cm)",
    "Tracks opening angle",
    "#it{E}/#it{p} in BEMC",
    "Dielectron rapidity",
    "#eta_{emc_cluster} - #eta_{track_projected}",
    "#phi_{emc_cluster} - #phi_{track_projected}",
    "Tracks azimuthal angle",
    "Tracks pseudorapidity"
  };
    glrec=lrec; gxbin=xbin; gxmin=xmin; gxmax=xmax; gxtit=xtit;
  }

  if(set == 1) {
  // set 1
  // iplot                      0           1         2            3            4          5             6
  //                        BEMC energy  trk pT   trk energy   pT at BEMC   trk chi^2   trk nhits   trk hits fit
  static string lrec[] = {  "jT0bemcE",  "jT0pT",  "jT0eng",  "jT0pTBemc",  "jT0chi2", "jT0nHits", "jT0nHitsFit" };
  static Double_t xbin[] = {   0.05,       0.07,      0.09,       0.03,        0.1,         1,           1 };
  static Double_t xmin[] = {   0.,         0.4,       1.3,        0.,          0,           0,           0 };
  static Double_t xmax[] = {   5.,         2.6,       3.2,        4.5,         4,          50,          50 };
  static string xtit[] = {
    "Energy in BEMC",
    "Tracks #it{p}_{T} (GeV)",
    "Tracks energy (GeV)",
    "Track #it{p}_{T} at BEMC (GeV)",
    "Track #chi^{2}",
    "Track number of hits",
    "Track number of hits for fit"
  };
    glrec=lrec; gxbin=xbin; gxmin=xmin; gxmax=xmax; gxtit=xtit;
  }

  if(set == 2) {
  // set 2
  // iplot                      0           1           2               3            4            5
  //                         dca in z   dca in xy  en at bemc proj   n sig el   sig for dEdx   p at BEMC
  static string lrec[] = {  "jT0dcaZ", "jT0dcaXY", "jT0EnAtBemc",   "jT0sigEl", "jT0dEdxSig", "jT0bemcP" };
  static Double_t xbin[] = {   0.01,      0.01,         0.1,            0.1,         1e-7,        0.1 };
  static Double_t xmin[] = {   -2,         0,           0.5,            -4,         0,            0 };
  static Double_t xmax[] = {   2,          4,           4,              4,           1e-5,        6 };
  static string xtit[] = {
    "DCA along #it{z}",
    "DCA in #it{xy} plane",
    "Track energy at BEMC projection",
    "N sigma electron",
    "dE/dx signal",
    "Track momentum #it{p}_{tot} at BEMC"
  };
    glrec=lrec; gxbin=xbin; gxmin=xmin; gxmax=xmax; gxtit=xtit;
  }

  //create the histograms
  TH1D *pdata = PrepareTH1D("pdata", gxbin[iplot], gxmin[iplot], gxmax[iplot]);
  //TH1D *pmcrec = PrepareTH1D("pmcrec", gxbin[iplot], gxmin[iplot], gxmax[iplot]);
  TH1D *pmcrec = 0x0;
  if( nMCbin > 0 ) {
    pmcrec = PrepareTH1D("pmcrec", nMCbin, gxmin[iplot], gxmax[iplot]);
  } else {
    pmcrec = PrepareTH1D("pmcrec", gxbin[iplot], gxmin[iplot], gxmax[iplot]);
  }

  //fill the histograms, selection string
  string selform = Form("jRecM>%f && jRecM<%f && jRecY>%f && jRecY<%f && jRecPt<%f", mmin, mmax, ymin, ymax, ptmax);
  //add custom selection
  //selform += " && jVtxZ>-30. && jVtxZ<30.";
  //string selform = "";
  mcrecTree ->Draw( Form("%s >> pmcrec", glrec[iplot].c_str()), selform.c_str() );
  dataTree  ->Draw( Form("%s >> pdata",  glrec[iplot].c_str()), selform.c_str() );

  //put also the second track by replacing 'jT0' by 'jT1'
  string posTrk("jT0"); // T0 is positive
  string negTrk("jT1"); // T1 is negative
  string pnam(glrec[iplot]);
  Int_t ipos = pnam.find(posTrk, 0);
  Bool_t negFound = ipos>=0 ? kTRUE : kFALSE;
  while (ipos >= 0) {
    pnam.replace(ipos, negTrk.size(), negTrk);
    ipos = pnam.find(posTrk, ++ipos);
  }
  //put also tracks of negative charge, if requested
  string trkChargeLab = " , positive tracks";
  if ( negFound && trkCharge != 1 ) {
    //store the data for track0
    TH1D *hdattmp = (TH1D*) pdata->Clone(); TH1D *hmctmp = (TH1D*) pmcrec->Clone();
    //fill the histograms for track1
    dataTree  ->Draw( Form("%s >> pdata", pnam.c_str())  , selform.c_str() );
    mcrecTree ->Draw( Form("%s >> pmcrec", pnam.c_str()) , selform.c_str() );
    trkChargeLab = " , negative tracks";
    if( trkCharge == 0 ) {
      //add results for track0
      pdata->Add(hdattmp); pmcrec->Add(hmctmp); delete hdattmp; delete hmctmp;
      trkChargeLab = " , tracks of both charges";
    }
  }


  cout << "Data entries: " << pdata->GetEntries() << " , MC entries: " << pmcrec->GetEntries() << endl;

  //normalize mc to the data
  normToData(pmcrec, pdata);
  TH1D *pmc = pmcrec;
/*
  pmcrec->Sumw2();
  pmcrec->Scale(pdata->Integral()/pmcrec->Integral());

  //make a clear histogram for normalized mc plot
  TH1D *pmc = new TH1D("pmc", "pmc", pmcrec->GetNbinsX(), gxmin[iplot], gxmax[iplot]);
  for(Int_t i=0; i<pmc->GetNbinsX()+1; i++) pmc->SetBinContent(i, pmcrec->GetBinContent(i));
*/
  pmc->SetMaximum( GetMax(
    pmcrec->GetMaximum() + pmcrec->GetBinError(pmcrec->GetMaximumBin()),
    pdata->GetMaximum() + pdata->GetBinError(pdata->GetMaximumBin()), 0.
  ));
  pmc->SetMinimum( GetMin(
    pmcrec->GetMinimum() - pmcrec->GetBinError(pmcrec->GetMinimumBin()),
    pdata->GetMinimum() - pdata->GetBinError(pdata->GetMinimumBin()), 0.
  ));

  //make the plots
  if(logY) {
    can->cd(1)->SetLogy();
    pmc->SetMinimum(vmin);
  }

  pmc->SetLineColor(kMagenta);
  pmc->SetLineWidth(3);
  pmc->SetTitle("");
  if( negFound ) gxtit[iplot] += trkChargeLab; // tracks plot
  pmc->SetXTitle(gxtit[iplot].c_str());
  pmc->SetYTitle( Form("Events / (%.3f)", gxbin[iplot]) );
  pmc->SetTitleOffset(1.4,"X");
  pmc->SetTitleOffset(1.6,"Y");

  //legend for input selection
  leg = PrepareLeg(0.7, 0.84, 0.1, 0.14, 0.03); // x, y, dx, dy, tsiz
  leg->AddEntry((TObject*)0, Form("%2.1f < #it{y} < %2.1f", ymin, ymax), "");
  leg->AddEntry((TObject*)0, Form("%2.1f < #it{m}_{e^{+}e^{-}} < %2.1f GeV", mmin, mmax), "");
  leg->AddEntry((TObject*)0, Form("#it{p}_{T}^{e^{+}e^{-}} < %.3f GeV", ptmax), "");

  //legend for data
  leg1 = PrepareLeg(0.84, 0.74, 0.12, 0.07, 0.03); // x, y, dx, dy, tsiz
  leg1->AddEntry(pdata, datalabel.c_str(), "pl");
  leg1->AddEntry(pmc, mclabel.c_str(), "l");

  //legend for underflow and overflow
  leg2 = PrepareLeg(0.15, 0.94, 0.1, 0.04, 0.03);
  string ovfstr = Form("Underflow: %.0f, overflow: %.0f", pdata->GetBinContent(0), pdata->GetBinContent(pdata->GetNbinsX()+1));
  leg2->AddEntry((TObject*)0, ovfstr.c_str(), "");

  pmc->Draw();
  pdata->Draw("e1same");

  leg->Draw("same");
  leg1->Draw("same");
  leg2->Draw("same");

  invertCol(gPad);

  can->SaveAs( "01fig.pdf" );

  //beep when finished
  gSystem->Exec("mplayer computerbeep_1.mp3 > /dev/null 2>&1");

}//ControlPlotsDataMC

//_____________________________________________________________________________
void Init() {

  gStyle->SetOptStat("");//nemruo
  gStyle->SetPalette(1);
  gStyle->SetLineWidth(2);      //axis line
  gStyle->SetFrameLineWidth(2); //frame line
  TGaxis::SetMaxDigits(3);

  c3 = new TCanvas("c3", "Analysis", 768., 768.);
  c4 = new TCanvas("c4", "Analysis", 2048., 600.);
  AdjustCanvas(c3, 1, 1, 0.12, 0.14);// bmg, lmg
  AdjustCanvas(c4, 1, 1, 0.12, 0.14);// bmg, lmg
  can = c3;
  can->cd(1);
  gPad->SetRightMargin(0.01);
  gPad->SetTopMargin(0.01);
  gPad->SetLeftMargin(0.11);
  gPad->SetBottomMargin(0.1);

  //input
  TFile *datafile = TFile::Open((basedir+datainp).c_str(), "READ");
  TFile *mcfile   = TFile::Open((basedir+mcinp).c_str(), "READ");

  dataTree  = (TTree*) datafile->Get("jRecTree");
  mcrecTree = (TTree*) mcfile->Get("jRecTree");
  mcgenTree = (TTree*) mcfile->Get("jGenTree");

}//Init

//_____________________________________________________________________________
Double_t GetMax(Double_t x1, Double_t x2, Double_t x3) {

  Double_t x4 = -1.;
  if( x1 > x4 ) x4 = x1;
  if( x2 > x4 ) x4 = x2;
  if( x3 > x4 ) x4 = x3;

  return x4*yspace;

}//GetMax

//_____________________________________________________________________________
Double_t GetMin(Double_t x1, Double_t x2, Double_t x3) {

  Double_t x4 = 9999.;
  if( x1 < x4 ) x4 = x1;
  if( x2 < x4 ) x4 = x2;
  if( x3 < x4 ) x4 = x3;
  x4-=x4*0.2;
  if( x4 < 0. ) x4 = 0.;

  return x4;

}//GetMin













