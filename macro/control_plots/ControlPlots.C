
//plot routines

//local headers
#include "cutLine.h"
#include "plotUtils.h"

TCanvas *c3;
TCanvas *c4;
TCanvas *can;
TTree *jRecTree;
TTree *jLSTree;
TH1D *htmp;
TLegend *leg;
TLegend *leg1;
Double_t xl, dxl, yl, dyl;
string strjpsi, strgg;

Double_t mmin=-9999., mmax=9999.;

TFile *infile;
TFile *infile_ls;

const Int_t nplots = 100;
void(*MakePlot[nplots])();
void MakeMass();
void MakePt();
void MakeBBCLargeBEMC();
void MakeBBCLarge();
void MakeDEtaBEMC();
void MakeDPhiBEMC();
void MakeAnaVsRun();
void MakeTracksPt();
void MakeTracksEta();
void MakeTracksPhi();
void MakeVtxZ();
void MakePIDdEdx();
void MakeDeltaPhi();
void MakeEnOverP();
void MakeTracksChi2();
void MakeTracksPhiBEMC();
void MakePtMC();
void MakeRapidityMC();
void MakeTracksGenPtMC();
void MakePt2();
void MakePtGG();
void MakeEffM();
void MakeEffTrkPt();
void MakeGGsigma();
void MakePIDdEdx1D();
void MakeDeltaDip();
void MakeEtaPhiBemc();
void MakeTracksEnBEMC();
void MakeTracksBemcHitE();
void MakeTracksBemcHitFractionE();
void MakeEnTrackClsBemc();
void MakePtotBemc();
void MakeZdc();


//_____________________________________________________________________________
void ControlPlots() {

  //string basedir = "../../../star-upc-data/ana/starsim/slight14e/sel5/";
  string basedir = "../../../star-upc-data/ana/muDst/muDst_run1/sel5/";

  //string in = "muDst_run1/sel2/ana_muDst_run1_all_sel2.root";
  //string in = "muDst_dev0/sel3/ana_muDst_dev0_all_sel3.root";
  string in = "ana_muDst_run1_all_sel5z.root";
  //string in = "muDst_run3/conv/sel0/ana_muDst_run3_all_conv_sel0.root";
  //string in = "muDst_run2/conv/sel0/ana_muDst_run2_all_conv_sel0b_v2.root";
  //string in = "starsim/sel2/ana_slight14a1_v2.root";
  //string in = "starsim/sel2/ana_slight14b1.root";
  //string in = "starsim/sel2/ana_slight14b1_sel2b.root";
  //string in = "starsim/sel2/ana_slight14b1_sel2c.root";
  //string in = "starsim/sel2/ana_slight14b1_v3.root";
  //string in = "../bin/output.root";
  //string in = "ana_slight14e1x3_s6_sel5z.root";

  //string in_ls = "ana_muDst_run1_all_sel5z_ls.root";
  string in_ls = "../../../star-upc-data/ana/muDst/muDst_run1/sel5/ana_muDst_run1_all_sel5z_ls.root";

  //Init();

  Int_t iplot = 11;

  MakePlot[0] = MakeMass;
  MakePlot[1] = MakePt;
  MakePlot[2] = MakeBBCLargeBEMC;
  MakePlot[3] = MakeBBCLarge;
  MakePlot[4] = MakeDEtaBEMC;
  MakePlot[5] = MakeDPhiBEMC;
  MakePlot[6] = MakeAnaVsRun;
  MakePlot[7] = MakeTracksPt;
  MakePlot[8] = MakeTracksEta;
  MakePlot[9] = MakeTracksPhi;
  MakePlot[10] = MakeVtxZ;
  MakePlot[11] = MakePIDdEdx;
  MakePlot[12] = MakeDeltaPhi;
  MakePlot[13] = MakeEnOverP;
  MakePlot[14] = MakeTracksChi2;
  MakePlot[15] = MakeTracksPhiBEMC;
  MakePlot[16] = MakePtMC;
  MakePlot[17] = MakeRapidityMC;
  MakePlot[18] = MakeTracksGenPtMC;
  MakePlot[19] = MakePt2;
  MakePlot[20] = MakePtGG;
  MakePlot[21] = MakeEffM;
  MakePlot[22] = MakeEffTrkPt;
  MakePlot[23] = MakeGGsigma;
  MakePlot[24] = MakePIDdEdx1D;
  MakePlot[25] = MakeDeltaDip;
  MakePlot[26] = MakeEtaPhiBemc;
  MakePlot[27] = MakeTracksEnBEMC;
  MakePlot[28] = MakeTracksBemcHitE;
  MakePlot[29] = MakeTracksBemcHitFractionE;
  MakePlot[30] = MakeEnTrackClsBemc;
  MakePlot[31] = MakePtotBemc;
  MakePlot[32] = MakeZdc;


  infile = TFile::Open( (basedir+in).c_str() );
  if(!infile) {cout << "No input." << endl; return;}
  jRecTree = (TTree*) infile->Get("jRecTree");

  infile_ls = TFile::Open( (in_ls).c_str() );
  //infile_ls = TFile::Open( (basedir+in_ls).c_str() );
  jLSTree = (TTree*) infile_ls->Get("jRecTree");

  strjpsi = "#it{J}/#it{#psi}";
  strgg = "#it{#gamma#gamma}#rightarrow#it{e}^{+}#it{e}^{-}";

  gStyle->SetOptStat("");//nemruo
  gStyle->SetPalette(1);
  gStyle->SetLineWidth(2);      //axis line
  gStyle->SetFrameLineWidth(2); //frame line
  TGaxis::SetMaxDigits(3);
  gStyle->SetPadTickX(1);

  c3 = boxCanvas();
  c4 = new TCanvas("c4", "Analysis", 2048., 600.);
  //AdjustCanvas(c3, 1, 1, 0.12, 0.14);// bmg, lmg
  AdjustCanvas(c4, 1, 1, 0.12, 0.14);// bmg, lmg
  //c5 = boxCanvas(768, 500);
  //AdjustCanvas(c5, 1, 1, 0.12, 0.14);
  //c3->SetGrid();
  can = c3;
  can->cd(1);
  gPad->SetRightMargin(0.03);
  gPad->SetTopMargin(0.03);



  //legends
  xl = 0.45, dxl = 0.4;
  yl = 0.7, dyl = 0.17;

  MakePlot[iplot]();




  can->SaveAs("01fig.pdf");

  //beep when finished
  gSystem->Exec("mplayer computerbeep_1.mp3 > /dev/null 2>&1");

}//ControlPlots

//_____________________________________________________________________________
void MakeMass() {

  //mass
  Double_t mbin = 0.02; // 0.005
  mmin = 0.; // 0.
  mmax = 0.5; // 0.12

  Bool_t logy = 1;

  TH1D *hMass = PrepareTH1D("hMass", mbin, mmin, mmax);
  TH1D *hMassLS = PrepareTH1D("hMassLS", mbin, mmin, mmax);
  SetLineMarkerColor(hMassLS, kRed);
  hMass->SetTitle("");
  hMass->SetXTitle("#it{m}_{e^{+}e^{-}} (GeV/#it{c}^{2})");
  hMass->SetYTitle( Form("Dielectron counts / (%.0f MeV)", 1000.*mbin) );
  //hMass->SetMaximum(256);

  jRecTree->Draw("jRecM >> hMass");
  jLSTree->Draw("jRecM >> hMassLS");

  hMass->SetTitleOffset(1.5, "Y");
  hMass->SetTitleOffset(1.3, "X");

  gPad->SetTopMargin(0.01);
  gPad->SetRightMargin(0.03);
  gPad->SetLeftMargin(0.1);
  gPad->SetBottomMargin(0.09);

  leg = PrepareLeg(0.75, 0.87, 0.2, 0.09, 0.04);
  leg->AddEntry(hMass, "Unlike-sign");
  leg->AddEntry(hMassLS, "Like-sign", "l");

  //legend for underflow and overflow
  leg1 = UoLegLin(hMass, 0.56, 0.87, 0.2, 0.09, 0.03);

  cutLine *msel = new cutLine(0.1, 0.8, hMass, logy);

  hMass->Draw();
  //hMassLS->Draw("same");

  //leg->Draw("same");
  leg1->Draw("same");

  msel->Draw("same");

  if(logy) gPad->SetLogy();

  invertCol(gPad);

}//MakeMass

//_____________________________________________________________________________
void MakePt() {

  //pT
  Double_t ptbin = 0.024;
  Double_t ptmax = 2;//0.8
  Double_t mran[2] = {2.9, -3.2}; //mass range for the plot

  TH1D *hPt = PrepareTH1D("hPt", ptbin, 0., ptmax);
  TH1D *hPtLS = PrepareTH1D("hPtLS", ptbin, 0., ptmax);
  hPtLS->SetLineColor(kRed);
  hPt->SetTitle("");
  hPt->SetXTitle("Dielectron #it{p}_{T} (GeV/#it{c})");
  hPt->SetYTitle( Form("Dielectron counts / (%.0f MeV/#it{c})", 1000.*ptbin) );

  if( mran[1] < 0. ) {
    jRecTree->Draw("jRecPt >> hPt");
    jLSTree->Draw("jRecPt >> hPtLS");
  } else {
    jRecTree->Draw("jRecPt >> hPt", Form("jRecM>%f && jRecM<%f", mran[0], mran[1]));
    jLSTree->Draw("jRecPt >> hPtLS", Form("jRecM>%f && jRecM<%f", mran[0], mran[1]));
  }

  hPt->SetTitleOffset(1.5, "Y");
  hPt->SetTitleOffset(1.3, "X");

  gPad->SetTopMargin(0.01);
  gPad->SetRightMargin(0.01);
  gPad->SetLeftMargin(0.15);
  gPad->SetBottomMargin(0.14);

  leg = PrepareLeg(0.55, 0.84, 0.2, 0.13, 0.04);
  leg->AddEntry(hPt, "Unlike-sign");
  leg->AddEntry(hPtLS, "Like-sign", "l");
  if( mran[1] > 0. ) {
    leg->AddEntry((TObject*)0, Form("%.1f < #it{m}_{e^{+}e^{-}} < %.1f GeV/#it{c}^{2}", mran[0], mran[1]), "");
  }
  //leg->AddEntry((TObject*)0, Form("# of events: %.0f", hPt->GetEntries()), "");

  gPad->SetLogy();
  hPt->Draw();
  //hPtLS->Draw("same");
  //leg->Draw("same");

  invertCol(gPad);

}//MakePt

//_____________________________________________________________________________
void MakeBBCLargeBEMC() {

  //BEMC multiplicity vs. BBC large tiles east and west

  Int_t bbcmin = 0;
  Int_t bbcmax = 1000;
  //Int_t nbinsXY = bbcmax-bbcmin;
  Int_t nbinsXY = (bbcmax-bbcmin)/100;

  Int_t emcmin = 0;
  Int_t emcmax = 6;
  Int_t nemc = emcmax-emcmin;

  TH3F *hBBC = PrepareTH3F("hBBC", nbinsXY, bbcmin, bbcmax, nbinsXY, bbcmin, bbcmax, nemc, emcmin, emcmax);
  //TH3F *hBBC = PrepareTH3F("hBBC", nemc, emcmin, emcmax, nemc, emcmin, emcmax, nemc, emcmin, emcmax);
  //hBBC->SetXTitle("BBC Large East");
  //hBBC->SetYTitle("BBC Large West");
  //hBBC->SetZTitle("BEMC multiplicity");
  //hBBC->SetOption("surf");

  //jRecTree->Draw("jBEMCMult:jBBCLargeWest:jBBCLargeEast >> hBBC", Form("jRecM>%f && jRecM<%f", mmin, mmax));
  //jRecTree->Draw("jBEMCMult:jBEMCMult:jBEMCMult >> hBBC", Form("jRecM>%f && jRecM<%f", mmin, mmax));

  //jRecTree->Draw("jBBCLargeEast:jBBCLargeWest:jBEMCMult >> hBBC", "jBEMCMult>-1");

  //TPolyMarker3D *pm = new TPolyMarker3D(10000, 21);

  //jRecTree->Draw("jBBCLargeEast:jBBCLargeWest:jBEMCMult >> pm", "jBEMCMult>-1");

  //                      z               y       x
  //jRecTree->Draw("jBBCLargeEast:jBBCLargeWest:jBEMCMult", "jBEMCMult>-1");
  //jRecTree->Draw("jBEMCMult:jBBCLargeWest:jBBCLargeEast >> pmbbc", "jBEMCMult>-1");
  jRecTree->Draw("jBEMCMult:jBBCLargeWest:jBBCLargeEast >> hBBC");

  //TPolyMarker3D *pm = dynamic_cast<TPolyMarker3D*>( gDirectory->Get("pmbbc") );
  //TGraph *pm = dynamic_cast<T2D*>( gDirectory->Get("pmbbc") );
  //TPolyMarker3D *pm = dynamic_cast<TPolyMarker3D*>( gDirectory->Get("pmbbc") );
  cout << dynamic_cast<TH3F*>( gDirectory->Get("pmbbc") ) << endl;

  //gPad->SetLogx();
  //gPad->SetLogz();
  //hBBC->Draw("iso");
  hBBC->Draw("box");
  //hBBC->Draw();

  //pm->Draw("AP");

}//MakeBBCLargeBEMC

//_____________________________________________________________________________
void MakeBBCLarge() {

  //BBC large tiles east and west

  Int_t bbcmin = 0;
  //Int_t bbcmax = 900;
  Int_t bbcmax = 190;
  //Int_t nbinsXY = bbcmax-bbcmin;
  Int_t nbinsXY = (bbcmax-bbcmin)/10;

  TH2D *hBBC = PrepareTH2D("hBBC", nbinsXY, bbcmin, bbcmax, nbinsXY, bbcmin, bbcmax);
  hBBC->SetXTitle("BBC Large East");
  hBBC->SetYTitle("BBC Large West");


  jRecTree->Draw("jBBCLargeEast:jBBCLargeWest >> hBBC");

  gPad->SetTopMargin(0.05);
  //gPad->SetRightMargin(0.15);
  gPad->SetRightMargin(0.13);

  hBBC->SetTitleOffset(1.1, "X");
  hBBC->SetTitleOffset(1.4, "Y");

  //hBBC->SetMinimum(0.0001);
  gPad->SetLogz();

  //gPad->SetLogx();
  //gPad->SetLogy();

  hBBC->Draw();
  //hBBC->Draw("scat");

}//MakeBBCLarge

//_____________________________________________________________________________
void MakeDEtaBEMC() {

  //BEMC matching, delta eta

  Double_t detabin = 0.005; // 0.005  0.01
  Double_t detamax = 0.101; // 0.101

  TH1D *hDetaPos = PrepareTH1D("hDetaPos", detabin, -1.*detamax, detamax);
  TH1D *hDetaNeg = PrepareTH1D("hDetaNeg", detabin, -1.*detamax, detamax);
  SetLineMarkerColor(hDetaPos, kRed);
  SetLineMarkerColor(hDetaNeg, kBlue);

  jRecTree->Draw("jT0Deta >> hDetaPos");
  jRecTree->Draw("jT1Deta >> hDetaNeg");

  //htmp = (TH1D*) hDeta->Clone(); //store the data for track0
  //jRecTree->Draw("jT1Deta >> hDeta"); //fill the histogram for track1
  //hDeta->Add(htmp); delete htmp; //add results for track0

  hDetaPos->SetYTitle(Form("Dielectron counts / (%.3f)", detabin));
  hDetaPos->SetXTitle("#eta_{emc_cluster} - #eta_{track_projected}");

  hDetaPos->SetTitleOffset(1.5, "Y");
  hDetaPos->SetTitleOffset(1.3, "X");

  gPad->SetTopMargin(0.06);//0.02
  gPad->SetRightMargin(0.01);
  gPad->SetBottomMargin(0.14);
  gPad->SetLeftMargin(0.15);

  leg = PrepareLeg(0.7, 0.84, 0.2, 0.09, 0.04);
  leg->AddEntry(hDetaPos, "Positive track");
  leg->AddEntry(hDetaNeg, "Negative track");

  hDetaPos->Draw();
  hDetaNeg->Draw("e1same");
  leg->Draw("same");



}//MakeDEtaBEMC

//_____________________________________________________________________________
void MakeDPhiBEMC(){

  //BEMC matching, delta phi

  Double_t dphibin = 0.008; // 0.008  0.014
  Double_t dphimax = 0.1; // 0.101
  Double_t mran[2] = {2.9, 3.2}; //mass range for the plot

  TH1D *hDphiPos = PrepareTH1D("hDphiPos", dphibin, -1.*dphimax, dphimax);
  TH1D *hDphiNeg = PrepareTH1D("hDphiNeg", dphibin, -1.*dphimax, dphimax);
  SetLineMarkerColor(hDphiPos, kRed);
  SetLineMarkerColor(hDphiNeg, kBlue);

  if( mran[1] < 0. ) {
    jRecTree->Draw("jT0Dphi >> hDphiPos");
    jRecTree->Draw("jT1Dphi >> hDphiNeg");
  } else {
    jRecTree->Draw("jT0Dphi >> hDphiPos", Form("jRecM>%f && jRecM<%f", mran[0], mran[1]));
    jRecTree->Draw("jT1Dphi >> hDphiNeg", Form("jRecM>%f && jRecM<%f", mran[0], mran[1]));
  }

  hDphiPos->SetYTitle(Form("Dielectron counts / (%.3f)", dphibin));
  hDphiPos->SetXTitle("#phi_{emc_cluster} - #phi_{track_projected}");

  hDphiPos->SetTitleOffset(1.5, "Y");
  hDphiPos->SetTitleOffset(1.3, "X");

  gPad->SetTopMargin(0.07);//0.02
  gPad->SetRightMargin(0.01);
  gPad->SetBottomMargin(0.14);
  gPad->SetLeftMargin(0.15);

  leg = PrepareLeg(0.7, 0.84, 0.2, 0.09, 0.04);
  leg->AddEntry(hDphiPos, "Positive track");
  leg->AddEntry(hDphiNeg, "Negative track");
  if( mran[1] > 0. ) {
    leg->AddEntry((TObject*)0, Form("%.1f < #it{m}_{e^{+}e^{-}} < %.1f GeV/#it{c}^{2}", mran[0], mran[1]), "");
  }

  hDphiPos->Draw();
  hDphiNeg->Draw("e1same");
  leg->Draw("same");



}//MakeDPhiBEMC

//_____________________________________________________________________________
void MakeAnaVsRun() {

  //analyzed and selected events per run

  TH1I *hAnaPerRun = dynamic_cast<TH1I*>( infile->Get("hAnaPerRun") );
  TH1I *hSelPerRun = dynamic_cast<TH1I*>( infile->Get("hSelPerRun") );

  //get number of runs in histograms
  Int_t nrunsHist=0;

  for(Int_t ibin=-1; ibin<hAnaPerRun->GetNbinsX()+1; ibin++) {
    if( hAnaPerRun->GetBinContent(ibin) <= 0 ) continue;
    nrunsHist++;
  }
  cout << "Number of runs hist: " << nrunsHist << endl;

  //lumi per run
  ifstream lumifile("lum_perrun_UPC-jpsi-B.txt");
  string line;
  Int_t nrunsLumi=0;
  Int_t runFirst = (Int_t) 1e9; // first run in lumi file
  Double_t lumitot=0; // total luminosity
  struct runAndLumi {
    Int_t runnum;
    Double_t lumi;
  } runlumi;
  vector<runAndLumi> runlumiVec; // vector with runs and lumi to fill the histogram
  //lumi file loop
  while( getline(lumifile, line) ) {
    if( line.empty() ) continue;

    istringstream ist(line);
    istream_iterator<string> it(ist);

    Int_t runnum = stoi(*it);

    for(Int_t i=0; i<4; i++) it++; // move iterator 4 places to reach lumi value
    Double_t lumi = stof(*it);
    lumitot += lumi;

    if( runnum < runFirst ) runFirst = runnum; // determine first run number

    //put current run and lumi to vector
    runlumi.runnum = runnum;
    runlumi.lumi = lumi;
    runlumiVec.push_back(runlumi);

    if(nrunsLumi > 2650) {
      cout << runnum << " " << fixed << setprecision(5) << lumi << endl;
    }

    nrunsLumi++;
  }//lumi file loop

  cout << "Number of runs lumi: " << nrunsLumi << endl;
  if( nrunsLumi < nrunsHist ) cout << "Warning missing runs with lumi" << endl;
  cout << "First run lumi: " << runFirst << endl;
  cout << "Total lumi: " << lumitot << " inv. micro barn" << endl;

  //histograms to print ana and sel events per run
  //Int_t nruns = nrunsLumi; // for extension to runs from lumi
  Int_t nruns = 2680; // to be able to divide by 20 or 40 and rebin
  TH1I *hAnaRun = new TH1I(); // analyzed events in run
  TH1I *hSelRun = new TH1I(); // selected events in each run
  TH1D *hLumiRun = new TH1D(); // luminosity for each run
  hAnaRun->SetNameTitle("hAnaRun", "hAnaRun");
  hSelRun->SetNameTitle("hSelRun", "hSelRun");
  hLumiRun->SetNameTitle("hLumiRun", "hLumiRun");
  hAnaRun->SetBins(nruns, 0, nruns);
  hSelRun->SetBins(nruns, 0, nruns);
  hLumiRun->SetBins(nruns, 0, nruns);

  //lookup table between run number and bin number
  map<Int_t, Int_t> runbin; //run number, bin number

  //fill lumi per run histogram and set lookup table
  //run loop
  for(Int_t irun=0; irun<nruns; irun++) {
    hLumiRun->SetBinContent( irun+1, runlumiVec[irun].lumi ); // ibin and lumi
    runbin.insert( std::make_pair( runlumiVec[irun].runnum, irun) ); // runnum and ibin
  }//run loop


  //ratio of selected per analyzed events
  TH1D *hSelAna = PrepareTH1D("hSelAna", nruns, 0, nruns);
  //ratio of selected events per luminosity
  TH1D *hSelLumi = PrepareTH1D("hSelLumi", nruns, 0, nruns);

  //fill print versions of histograms

  Int_t nallAna=0, nallSel=0; // sum of all ana and sel events for consistency check
  //ana histograms loop
  for(Int_t ibin=0; ibin<hAnaPerRun->GetNbinsX(); ibin++) {
    if( hAnaPerRun->GetBinContent(ibin) <= 0 ) continue;

    Int_t runnum = hAnaPerRun->GetBinLowEdge(ibin); // run number from original analysis histogram

    Double_t anarun = hAnaPerRun->GetBinContent(ibin); // analyzed and selected events from analysis
    Double_t selrun = hSelPerRun->GetBinContent(ibin);
    nallAna += (Int_t) anarun;
    nallSel += (Int_t) selrun;

    Int_t binnum = runbin[runnum]; // bin number from run number

    hAnaRun->SetBinContent(binnum+1, anarun);
    hSelRun->SetBinContent(binnum+1, selrun);

    //ratio selected to analyzed events
    hSelAna->SetBinContent(binnum+1, selrun/anarun);
    //hSelAna->SetBinError(irun, sqrt( (anarun-selrun)/(anarun*selrun) )*selrun/anarun);
    hSelAna->SetBinError(binnum+1, 0);

    //ratio selected events to lumi
    Double_t lumi = hLumiRun->GetBinContent(binnum);
    hSelLumi->SetBinContent(binnum+1, selrun/lumi);
    hSelLumi->SetBinError(binnum+1, 0);

  }//ana histograms loop
  cout << "All ana: " << nallAna << ", all sel: " << nallSel << endl;

  //group histograms

  Int_t rebin = 40; // rebin constant 20  40

  TH1D *hSelLumiGroup = PrepareTH1D("hSelLumiGroup", nruns/rebin, 0, nruns/rebin);
  TH1D *hSelAnaGroup = PrepareTH1D("hSelAnaGroup", nruns/rebin, 0, nruns/rebin);

  Double_t gana=0., gsel=0., glumi=0.; // group sums
  Int_t igroup=0, gcnt=0;
  Int_t nrunAna=0, nrunSel=0; // sum of all ana and sel events for consistency check
  //run histograms loop
  for(Int_t ibin=0; ibin<hAnaRun->GetNbinsX()+1; ibin++) {

    Double_t anarun = hAnaRun->GetBinContent(ibin); // analyzed and selected events from analysis
    Double_t selrun = hSelRun->GetBinContent(ibin);
    Double_t lumi = hLumiRun->GetBinContent(ibin);
    nrunAna += (Int_t) anarun;
    nrunSel += (Int_t) selrun;

    //group histograms
    gana += anarun;
    gsel += selrun;
    glumi += lumi;

    //group done
    if( ++gcnt >= rebin ) {
      gcnt = 0;
      if( glumi > 1e-5 ) hSelLumiGroup->SetBinContent(igroup+1, gsel/glumi);
      hSelLumiGroup->SetBinError(igroup+1, 0);
      if( gana > 1e-5 ) {
        Double_t rto = gsel/gana;
        Double_t err = rto*sqrt( (gana-gsel) / (gana*gsel) );
        hSelAnaGroup->SetBinContent(igroup+1, rto);
        hSelAnaGroup->SetBinError(igroup+1, err);
      }
      //cout << "################### " << gana << " " << gsel << " " << glumi << endl;
      gana = 0.;
      gsel = 0.;
      glumi = 0.;
      igroup++;
    }

  }//run histograms loop
  cout << "Run all ana: " << nrunAna << ", run all sel: " << nrunSel << endl;

  //bin labels loop
  for(Int_t ibin=0; ibin<hSelAnaGroup->GetNbinsX(); ibin++) {
    hSelLumiGroup->GetXaxis()->SetBinLabel(ibin+1, "");
    hSelAnaGroup->GetXaxis()->SetBinLabel(ibin+1, "");

    if(ibin%5 != 0) continue;

    hSelLumiGroup->GetXaxis()->SetBinLabel(ibin+1, Form("%d", ibin));
    hSelAnaGroup->GetXaxis()->SetBinLabel(ibin+1, Form("%d", ibin));

  }//bin labels loop
  //hSelLumiGroup->LabelsOption("v","X");
  //hSelAnaGroup->LabelsOption("v","X");

  can = c4;
  can->cd(1);

  gPad->SetTopMargin(0.1);//0.01
  gPad->SetLeftMargin(0.05);
  gPad->SetRightMargin(0.05);

  hSelAnaGroup->SetXTitle("Run group");
  hSelAnaGroup->SetYTitle("Selected / analyzed events");

  hSelAnaGroup->SetAxisColor(kBlue, "Y");
  hSelAnaGroup->SetLabelColor(kBlue, "Y");
  hSelAnaGroup->SetTitleOffset(1.2, "X");
  hSelAnaGroup->SetTitleOffset(0.55, "Y");
  hSelAnaGroup->GetXaxis()->SetLabelSize(0.07);
  //hSelAnaGroup->GetYaxis()->SetLabelSize(0.05);

  hSelAnaGroup->GetYaxis()->SetTitleColor(kBlue);

  hSelAnaGroup->Draw("e");
  can->Update();

  //scale selected per lumi to the pad
  Float_t rmax = 1.1*hSelLumiGroup->GetMaximum();
  Float_t scale = gPad->GetUymax()/rmax;
  hSelLumiGroup->Scale(scale);
  hSelLumiGroup->SetLineColor(kRed);
  hSelLumiGroup->Draw("same");

  //axis for sel per lumi
  TGaxis *lumiaxis = new TGaxis(gPad->GetUxmax(),gPad->GetUymin(), gPad->GetUxmax(),gPad->GetUymax(), 0,rmax,510,"+L");
  lumiaxis->SetLineColor(kRed);
  lumiaxis->SetLabelColor(kRed);
  lumiaxis->SetTitle("Selected events / luminosity");
  lumiaxis->SetTitleOffset(0.5);
  lumiaxis->SetTitleSize(0.05);
  lumiaxis->SetTitleColor(kRed);
  lumiaxis->SetLabelSize(0.05);
  lumiaxis->Draw();

  hSelAnaGroup->Draw("same");

  //hAnaRun->Draw();
  //hSelRun->Draw();
  //hLumiRun->Draw();
  //hSelAna->Draw();
  //hAnaPerRun->Draw();
  //hSelLumi->Draw();



  //hSelLumiGroup->Draw();


}//MakeAnaVsRun

//_____________________________________________________________________________
void MakeTracksPt() {

  //tracks pT

  Double_t ptbin = 0.1;
  Double_t ptmax = 3.3;//0.8
  Double_t mran[2] = {1.2, -5.};

  TH1D *hPtPos = PrepareTH1D("hPtPos", ptbin, 0., ptmax);
  TH1D *hPtNeg = PrepareTH1D("hPtNeg", ptbin, 0., ptmax);
  SetLineMarkerColor(hPtPos, kRed);
  SetLineMarkerColor(hPtNeg, kBlue);

  //
  if( mran[1] < 0. ) {
    //jRecTree->Draw("jT0pT >> hPtPos");
    //jRecTree->Draw("jT1pT >> hPtNeg");
    jRecTree->Draw("jT0pT >> hPtPos", "jT0matchBemc==1");
    jRecTree->Draw("jT1pT >> hPtNeg", "jT1matchBemc==1");
  } else {
    jRecTree->Draw("jT0pT >> hPtPos", Form("jRecM>%f && jRecM<%f", mran[0], mran[1]));
    jRecTree->Draw("jT1pT >> hPtNeg", Form("jRecM>%f && jRecM<%f", mran[0], mran[1]));
  }

  hPtPos->SetYTitle(Form("Dielectron counts / (%.0f MeV/#it{c})", 1000.*ptbin));
  hPtPos->SetXTitle("Tracks #it{p}_{T} (GeV/#it{c})");

  hPtPos->SetTitleOffset(1.5, "Y");
  hPtPos->SetTitleOffset(1.1, "X");

  gPad->SetTopMargin(0.05);
  gPad->SetRightMargin(0.01);

  leg = PrepareLeg(0.7, 0.84, 0.2, 0.09, 0.04);
  leg->AddEntry(hPtPos, "Positive track");
  leg->AddEntry(hPtNeg, "Negative track");
  if( mran[1] > 0. ) leg->AddEntry((TObject*)0, Form("%.1f < #it{m}_{e^{+}e^{-}} < %.1f GeV/#it{c}^{2}", mran[0], mran[1]), "");

  hPtPos->Draw();
  hPtNeg->Draw("e1same");
  leg->Draw("same");

  invertCol(gPad);

}//MakeTracksPt

//_____________________________________________________________________________
void MakeTracksEta() {

  //tracks pseudorapidity

  Double_t etabin = 0.1;//0.1
  Double_t etamax = 1.5;//0.8

  TH1D *hEtaPos = PrepareTH1D("hEtaPos", etabin, -1.*etamax, etamax);
  TH1D *hEtaNeg = PrepareTH1D("hEtaNeg", etabin, -1.*etamax, etamax);
  SetLineMarkerColor(hEtaPos, kRed);
  SetLineMarkerColor(hEtaNeg, kBlue);

  jRecTree->Draw("jT0eta >> hEtaPos");
  jRecTree->Draw("jT1eta >> hEtaNeg");
  //jRecTree->Draw("jGenP0eta >> hEtaPos");
  //jRecTree->Draw("jGenP1eta >> hEtaNeg");

  hEtaPos->SetYTitle(Form("Dielectron counts / (%.1f)", etabin));
  hEtaPos->SetXTitle("Tracks pseudorapidity");

  hEtaPos->SetTitleOffset(1.5, "Y");
  hEtaPos->SetTitleOffset(1.1, "X");

  gPad->SetTopMargin(0.01);
  gPad->SetRightMargin(0.01);
  gPad->SetLeftMargin(0.11);
  gPad->SetBottomMargin(0.09);

  leg = PrepareLeg(0.75, 0.9, 0.2, 0.08, 0.03);
  leg->AddEntry(hEtaPos, "Positive track", "p");
  leg->AddEntry(hEtaNeg, "Negative track", "p");

  hEtaPos->Draw();
  hEtaNeg->Draw("e1same");
  leg->Draw("same");

  invertCol(gPad);

}//MakeTracksEta

//_____________________________________________________________________________
void MakeTracksPhi() {

  //tracks azimuthal angle

  Double_t phibin = 0.9;
  Double_t phimax = 4.;//0.8

  TH1D *hPhiPos = PrepareTH1D("hPhiPos", phibin, -1.*phimax, phimax);
  TH1D *hPhiNeg = PrepareTH1D("hPhiNeg", phibin, -1.*phimax, phimax);
  SetLineMarkerColor(hPhiPos, kRed);
  SetLineMarkerColor(hPhiNeg, kBlue);

  jRecTree->Draw("jT0phi >> hPhiPos");
  jRecTree->Draw("jT1phi >> hPhiNeg");

  hPhiPos->SetYTitle(Form("Dielectron counts / (%.1f)", phibin));
  hPhiPos->SetXTitle("Tracks azimuthal angle");
  hPhiNeg->SetYTitle(Form("Dielectron counts / (%.1f)", phibin));
  hPhiNeg->SetXTitle("Tracks azimuthal angle");

  hPhiPos->SetTitleOffset(1.5, "Y");
  hPhiPos->SetTitleOffset(1.1, "X");
  hPhiNeg->SetTitleOffset(1.5, "Y");
  hPhiNeg->SetTitleOffset(1.1, "X");

  gPad->SetTopMargin(0.01);
  gPad->SetRightMargin(0.01);

  leg = PrepareLeg(0.7, 0.3, 0.2, 0.09, 0.04);
  leg->AddEntry(hPhiPos, "Positive track");
  leg->AddEntry(hPhiNeg, "Negative track");

  hPhiPos->Draw("e1same");
  //hPhiPos->Draw();
  hPhiPos->Draw("e1same");
  hPhiNeg->Draw("e1same");
  leg->Draw("same");

}//MakeTracksPhi

//_____________________________________________________________________________
void MakeVtxZ() {

  //vertex Z-position

  Double_t vtxbin = 4;
  Double_t vtxmax = 110.;//0.8

  TH1D *hVtxZ = PrepareTH1D("hVtxZ", vtxbin, -1.*vtxmax, vtxmax);
  SetLineMarkerColor(hVtxZ, kBlue);

  jRecTree->Draw("jVtxZ >> hVtxZ");

  hVtxZ->SetYTitle(Form("Dielectron counts / (%.0f cm)", vtxbin));
  hVtxZ->SetXTitle("#it{z} of primary vertex (cm)");

  hVtxZ->SetTitleOffset(1.5, "Y");
  hVtxZ->SetTitleOffset(1.1, "X");

  gPad->SetTopMargin(0.01);
  gPad->SetRightMargin(0.01);

  hVtxZ->Draw();

}//MakeVtxZ

//_____________________________________________________________________________
void MakePIDdEdx() {

  // n sigmas for electrons from dE/dx, positive track vs. negative

  Double_t pbin = 0.2;
  //Double_t pidmax = 10.;
  Double_t pidmax = 4.;
  //Double_t mran[2] = {2.9, -3.2}; // upper negative to set off
  Double_t mran[2] = {2.8, 3.2};

  TH2D *hpid = PrepareTH2D("hpid", pbin, -pidmax, pidmax, pbin, -pidmax, pidmax);

  if( mran[1] > 0. ) {
    jRecTree->Draw("jT0sigEl:jT1sigEl >> hpid", Form("jRecM>%f && jRecM<%f", mran[0], mran[1]));
  } else {
    jRecTree->Draw("jT0sigEl:jT1sigEl >> hpid"); // y:x
  }

  hpid->SetYTitle("#it{n}#sigma (electron) for positive track");
  hpid->SetXTitle("#it{n}#sigma (electron) for negative track");

  // circle of 3-sigmas
  TCrown *circle = new TCrown(0., 0., 3., 3.);
  circle->SetLineStyle(2);
  circle->SetLineWidth(4);

  leg = PrepareLeg(0.43, 0.87, 0.2, 0.09, 0.04);
  leg->AddEntry((TObject*)0, Form("%.1f < #it{m}_{e^{+}e^{-}} < %.1f GeV/#it{c}^{2}", mran[0], mran[1]), "");

  hpid->SetTitleOffset(1.2, "Y");
  hpid->SetTitleOffset(1.3, "X");

  gPad->SetRightMargin(0.11);
  gPad->SetLeftMargin(0.08);
  gPad->SetTopMargin(0.02);
  gPad->SetBottomMargin(0.1);

  //gPad->SetLogz();

  hpid->Draw();
  //circle->Draw("same");
  if( mran[1] > 0. ) leg->Draw("same");

  //invertCol(gPad);

}//MakePIDdEdx

//_____________________________________________________________________________
void MakeDeltaPhi() {

  //tracks opening angle

  Double_t deltbin = 0.01;
  Double_t deltmin = 2.3;
  Double_t deltmax = TMath::Pi()+1.e-4;//0.8
  //Double_t mran[2] = {2.8, 3.2};
  Double_t mran[2] = {1.5, 5.};
  Double_t ptmax = 0.17;

  Bool_t logy = 1;

  TH1D *hDeltaPhi = PrepareTH1D("hDeltaPhi", deltbin, deltmin, deltmax);
  //SetLineMarkerColor(hDeltaPhi, kBlue);

  jRecTree->Draw("jDeltaPhiBemc >> hDeltaPhi", Form("jRecM>%f && jRecM<%f && jRecPt<%f", mran[0], mran[1], ptmax));


  hDeltaPhi->SetYTitle(Form("Dielectron counts / (%.3f)", deltbin));
  hDeltaPhi->SetXTitle("Tracks opening angle at BEMC, #Delta#it{#phi}_{BEMC}");

  hDeltaPhi->SetTitleOffset(1.5, "Y");
  hDeltaPhi->SetTitleOffset(1.1, "X");

  gPad->SetTopMargin(0.01);
  gPad->SetRightMargin(0.01);

  if(logy) gPad->SetLogy();

  Double_t trgval = 2.618; // half of a sextant, pi-2pi/(2*6)
  cutLine *dsel = new cutLine(trgval, 0.8, hDeltaPhi, logy);

  leg = PrepareLeg(0.15, 0.85, 0.2, 0.12, 0.03);
  leg->AddEntry((TObject*)0, Form("%.1f < #it{m}_{e^{+}e^{-}} < %.1f GeV", mran[0], mran[1]), "");
  leg->AddEntry((TObject*)0, Form("#it{p}_{T} < %.3f GeV", ptmax), "");
  leg->AddEntry(dsel, Form("#Delta#it{#phi}_{BEMC} = %.3f (sextant/2)", trgval), "l");


  hDeltaPhi->Draw();
  leg->Draw("same");
  dsel->Draw("same");

  invertCol(gPad);

}//MakeDeltaPhi

//_____________________________________________________________________________
void MakeEnOverP() {

  //BEMC cluster energy over track momentum at BEMC

  Double_t epbin = 0.1;
  Double_t epmax = 3.4; //3.4  40
  Double_t mran[2] = {2.9, -3.2};

  TH1D *hEPpos = PrepareTH1D("hEPpos", epbin, 0., epmax);
  TH1D *hEPneg = PrepareTH1D("hEPneg", epbin, 0., epmax);
  SetLineMarkerColor(hEPpos, kRed);
  SetLineMarkerColor(hEPneg, kBlue);

  if( mran[1] < 0. ) {
    jRecTree->Draw("jT0bemcE/jT0bemcP >> hEPpos");
    jRecTree->Draw("jT1bemcE/jT1bemcP >> hEPneg");
  } else {
    jRecTree->Draw("jT0bemcE/jT0bemcP >> hEPpos", Form("jRecM>%f && jRecM<%f", mran[0], mran[1]));
    jRecTree->Draw("jT1bemcE/jT1bemcP >> hEPneg", Form("jRecM>%f && jRecM<%f", mran[0], mran[1]));
  }

  hEPpos->SetYTitle(Form("Dielectron counts / (%.1f)", epbin));
  hEPpos->SetXTitle("#it{E}/#it{p} at BEMC");

  hEPpos->SetTitleOffset(1.45, "Y");
  hEPpos->SetTitleOffset(1.1, "X");

  gPad->SetTopMargin(0.05);
  gPad->SetRightMargin(0.01);

  leg = PrepareLeg(0.55, 0.8, 0.17, 0.14, 0.04);
  leg->AddEntry(hEPpos, "Positive track");
  leg->AddEntry(hEPneg, "Negative track");
  if( mran[1] > 0. ) leg->AddEntry((TObject*)0, Form("%.1f < #it{m}_{e^{+}e^{-}} < %.1f GeV/#it{c}^{2}", mran[0], mran[1]), "");

  hEPpos->Draw();
  hEPneg->Draw("e1same");
  leg->Draw("same");

}//MakeEnOverP

//_____________________________________________________________________________
void MakeTracksChi2() {

  //tracks chi2

  Double_t chi2bin = 0.1;
  Double_t chi2max = 4.;

  TH1D *hChi2pos = PrepareTH1D("hChi2pos", chi2bin, 0., chi2max);
  TH1D *hChi2neg = PrepareTH1D("hChi2neg", chi2bin, 0., chi2max);
  SetLineMarkerColor(hChi2pos, kRed);
  SetLineMarkerColor(hChi2neg, kBlue);

  jRecTree->Draw("jT0chi2 >> hChi2pos");
  jRecTree->Draw("jT1chi2 >> hChi2neg");

  hChi2pos->SetYTitle(Form("Dielectron counts / (%.1f)", chi2bin));
  hChi2pos->SetXTitle("#chi^{2}/NDF");

  hChi2pos->SetTitleOffset(1.45, "Y");
  hChi2pos->SetTitleOffset(1.1, "X");

  gPad->SetTopMargin(0.01);
  gPad->SetRightMargin(0.01);

  leg = PrepareLeg(0.7, 0.87, 0.2, 0.09, 0.04);
  leg->AddEntry(hChi2pos, "Positive track");
  leg->AddEntry(hChi2neg, "Negative track");

  hChi2pos->Draw();
  hChi2neg->Draw("e1same");
  leg->Draw("same");

}//MakeTracksChi2

//_____________________________________________________________________________
void MakeTracksPhiBEMC() {

  //tracks azimuthal angle at BEMC position

  Double_t phibin = 0.9; // 0.9
  Double_t phimax = 4.;//0.8

  TH1D *hPhiPos = PrepareTH1D("hPhiPos", phibin, -1.*phimax, phimax);
  TH1D *hPhiNeg = PrepareTH1D("hPhiNeg", phibin, -1.*phimax, phimax);
  SetLineMarkerColor(hPhiPos, kRed);
  SetLineMarkerColor(hPhiNeg, kBlue);

  jRecTree->Draw("jT0phiBemc >> hPhiPos");
  jRecTree->Draw("jT1phiBemc >> hPhiNeg");

  hPhiPos->SetYTitle(Form("Dielectron counts / (%.1f)", phibin));
  hPhiPos->SetXTitle("Tracks #phi at BEMC position");
  hPhiNeg->SetYTitle(Form("Dielectron counts / (%.1f)", phibin));
  hPhiNeg->SetXTitle("Tracks #phi at BEMC position");

  hPhiPos->SetTitleOffset(1.5, "Y");
  hPhiPos->SetTitleOffset(1.1, "X");
  hPhiNeg->SetTitleOffset(1.5, "Y");
  hPhiNeg->SetTitleOffset(1.1, "X");

  gPad->SetTopMargin(0.01);
  gPad->SetRightMargin(0.01);

  leg = PrepareLeg(0.7, 0.3, 0.2, 0.09, 0.04);
  leg->AddEntry(hPhiPos, "Positive track");
  leg->AddEntry(hPhiNeg, "Negative track");

  hPhiPos->Draw("e1same");
  //hPhiPos->Draw();
  hPhiPos->Draw("e1same");
  hPhiNeg->Draw("e1same");
  leg->Draw("same");

}//MakeTracksPhiBEMC

//_____________________________________________________________________________
void MakePtMC() {

  //pT in MC

  Double_t ptbin = 0.03;
  Double_t ptmax = 1.57;//0.8  0.69
  Double_t mran[2] = {2.9, -3.2}; //mass range for the plot

  TTree *jGenTree = (TTree*) infile->Get("jGenTree");
  if( !jGenTree ) {cout << "No MC" << endl; return;}

  TH1D *hPt = PrepareTH1D("hPt", ptbin, 0., ptmax);
  TH1D *hPtMC = PrepareTH1D("hPtMC", ptbin, 0., ptmax);
  hPt->SetMarkerColor(kBlack); hPt->SetLineColor(kBlack);
  hPtMC->SetLineColor(kBlue);
  hPt->SetTitle("");
  hPt->SetXTitle("Dielectron #it{p}_{T} (GeV/#it{c})");
  hPt->SetYTitle( Form("Dielectron counts / (%.0f MeV/#it{c})", 1000.*ptbin) );

  if( mran[1] < 0. ) {
    jRecTree->Draw("jRecPt >> hPt");
    jGenTree->Draw("jGenPt >> hPtMC");
  } else {
    jRecTree->Draw("jRecPt >> hPt", Form("jRecM>%f && jRecM<%f", mran[0], mran[1]));
    jGenTree->Draw("jGenPt >> hPtMC", Form("jRecM>%f && jRecM<%f", mran[0], mran[1]));
  }

  //normalize generated to reconstructed
  hPtMC->Sumw2();
  hPtMC->Scale(hPt->Integral()/hPtMC->Integral());
  for(Int_t ibin=0; ibin<hPtMC->GetNbinsX()+1; ibin++) hPtMC->SetBinError(ibin, 0);


  hPt->SetTitleOffset(1.5, "Y");
  hPt->SetTitleOffset(1.3, "X");

  gPad->SetTopMargin(0.02);
  gPad->SetRightMargin(0.01);
  gPad->SetLeftMargin(0.15);
  gPad->SetBottomMargin(0.14);

  leg = PrepareLeg(0.55, 0.84, 0.2, 0.13, 0.04);
  leg->AddEntry(hPt, "Reconstructed");
  leg->AddEntry(hPtMC, "Generated", "l");
  if( mran[1] > 0. ) {
    leg->AddEntry((TObject*)0, Form("%.1f < #it{m}_{e^{+}e^{-}} < %.1f GeV/#it{c}^{2}", mran[0], mran[1]), "");
  }
  //leg->AddEntry((TObject*)0, Form("# of events: %.0f", hPt->GetEntries()), "");

  gPad->SetLogy();
  //hPtMC->Draw();
  hPt->Draw();
  hPtMC->Draw("same");
  leg->Draw("same");

}//MakePt

//_____________________________________________________________________________
void MakeRapidityMC() {

  //rapidity in MC

  Double_t ybin = 0.1;
  Double_t ymax = 1.1;//0.8
  Double_t mran[2] = {2.9, -3.2}; //mass range for the plot

  TTree *jGenTree = (TTree*) infile->Get("jGenTree");
  if( !jGenTree ) {cout << "No MC" << endl; return;}

  TH1D *hY = PrepareTH1D("hY", ybin, -1.*ymax, ymax);
  TH1D *hYMC = PrepareTH1D("hYMC", ybin, -1.*ymax, ymax);
  hY->SetMarkerColor(kBlack); hY->SetLineColor(kBlack);
  hYMC->SetLineColor(kBlue);
  hY->SetTitle("");
  hY->SetXTitle("Dielectron rapidity");
  hY->SetYTitle( Form("Dielectron counts / (%.1f)", ybin) );

  if( mran[1] < 0. ) {
    jRecTree->Draw("jRecY >> hY");
    jGenTree->Draw("jGenY >> hYMC");
  } else {
    jRecTree->Draw("jRecY >> hY", Form("jRecM>%f && jRecM<%f", mran[0], mran[1]));
    jGenTree->Draw("jGenY >> hYMC", Form("jRecM>%f && jRecM<%f", mran[0], mran[1]));
  }

  //normalize generated to reconstructed
  hYMC->Sumw2();
  hYMC->Scale(hY->Integral()/hYMC->Integral());
  for(Int_t ibin=0; ibin<hYMC->GetNbinsX()+1; ibin++) hYMC->SetBinError(ibin, 0);


  hY->SetTitleOffset(1.5, "Y");
  hY->SetTitleOffset(1.3, "X");

  gPad->SetTopMargin(0.02);
  gPad->SetRightMargin(0.01);
  gPad->SetLeftMargin(0.15);
  gPad->SetBottomMargin(0.14);

  leg = PrepareLeg(0.7, 0.88, 0.2, 0.08, 0.04);
  leg->AddEntry(hY, "Reconstructed");
  leg->AddEntry(hYMC, "Generated", "l");
  if( mran[1] > 0. ) {
    leg->AddEntry((TObject*)0, Form("%.1f < #it{m}_{e^{+}e^{-}} < %.1f GeV/#it{c}^{2}", mran[0], mran[1]), "");
  }
  //leg->AddEntry((TObject*)0, Form("# of events: %.0f", hPt->GetEntries()), "");

  gPad->SetLogy();
  //hPtMC->Draw();
  hY->Draw();
  hYMC->Draw("same");
  leg->Draw("same");

}//MakeRapidityMC

//_____________________________________________________________________________
void MakeTracksGenPtMC() {

  //generated tracks pT in gen tree and in rec tree
  //to make educated guess on minimal gen e+ and e- pT

  Double_t pTbin = 0.07;
  Double_t pTmin = 0.; // 0.05
  Double_t pTmax = 3.;
  Bool_t logy = kTRUE;

  Double_t mran[2] = {2.8, 3.2}; //mass range for the plot

  TTree *jGenTree = (TTree*) infile->Get("jGenTree");
  TTree *jRecTree = (TTree*) infile->Get("jRecTree");
  if( !jGenTree || !jRecTree ) {cout << "No input" << endl; return;}

  TH1D *hPt = PrepareTH1D("hPt", pTbin, pTmin, pTmax);
  TH1D *hPtMC = PrepareTH1D("hPtMC", pTbin, pTmin, pTmax);
  hPt->SetMarkerColor(kBlack); hPt->SetLineColor(kBlack);
  hPtMC->SetLineColor(kBlue);

  //pT of positive particles (P0) and negative (P1)
  string strsel = Form("jRecM>%f && jRecM<%f", mran[0], mran[1]);
  string strselmc = Form("jGenM>%f && jGenM<%f", mran[0], mran[1]);
  jRecTree->Draw("jGenP0pT >> hPt", strsel.c_str());    //gen particle pT from rec tree
  jGenTree->Draw("jGenP0pT >> hPtMC", strselmc.c_str());  //the same from gen tree
  jRecTree->Draw("jGenP1pT >>+ hPt", strsel.c_str());
  jGenTree->Draw("jGenP1pT >>+ hPtMC", strselmc.c_str());

  cout << "gen entries: " << hPtMC->GetEntries() << " rec entries: " << hPt->GetEntries() << endl;

  //normalize pT from gen tree to distribution from rec tree
  hPtMC->Sumw2();
  hPtMC->Scale(hPt->Integral()/hPtMC->Integral());
  for(Int_t ibin=0; ibin<hPtMC->GetNbinsX()+1; ibin++) hPtMC->SetBinError(ibin, 0);

  //hPtMC->SetMinimum(0.01); //for log scale

  //selection line, cut value on x, line length along y, histogram and log scale
  cutLine *tsel = new cutLine(0.6, 0.97, hPtMC, logy);
  //tsel->SetLineColor(kRed);

  gPad->SetTopMargin(0.02);
  gPad->SetRightMargin(0.01);
  gPad->SetLeftMargin(0.11);
  gPad->SetBottomMargin(0.11);

  hPtMC->SetXTitle("Tracks p_{T} (GeV)");

  hPtMC->SetTitleOffset(1.5, "Y");
  hPtMC->SetTitleOffset(1.3, "X");

  leg = PrepareLeg(0.68, 0.88, 0.2, 0.09, 0.03);
  leg->AddEntry(hPt, "Rec MC");
  leg->AddEntry(hPtMC, "Gen MC", "l");
  leg->AddEntry((TObject*)0, Form("%.1f < #it{m}_{e^{+}e^{-}} < %.1f GeV", mran[0], mran[1]), "");

  if(logy) gPad->SetLogy();

  hPtMC->Draw();
  hPt->Draw("esame");
  hPtMC->Draw("same");
  tsel->Draw();

  leg->Draw("same");

  invertCol(gPad);

}//MakeTracksGenPtMC

//_____________________________________________________________________________
void MakePt2() {

  //pT^2 (or pT) from data and coherent and incoherent MC

  //values to plot, pT^2 or pT
  string ptval = "jRecPt2";

  //plot limits
  Double_t ptbin = 0.005; //0.005  0.02
  Double_t ptmax = 0.3;//0.8 0.3  1.4

  //mass range for the plot
  Double_t mran[] = {2.8, 3.2};

  //position of cut line
  Double_t cutval = 0.035; //0.17
  //cutval = cutval*cutval;
  //cout << cutval << endl;

  //mc inputs, need to load before creating the histograms
  TFile *infileMC1 = TFile::Open( "/home/jaroslav/analyza/StUPCLib/ver1/ana/sel/sel0/starsim/slight14a/ana_slight14a1_v2.root");
  TTree *jRecTreeMC1 = (TTree*) infileMC1->Get("jRecTree");

  TFile *infileMC2 = TFile::Open( "/home/jaroslav/analyza/StUPCLib/ver1/ana/sel/sel0/starsim/slight14a/ana_slight14a2_v2.root" );
  TTree *jRecTreeMC2 = (TTree*) infileMC2->Get("jRecTree");

  TH1D *hPt2 = PrepareTH1D("hPt2", ptbin, 0., ptmax);
  SetLineMarkerColor(hPt2, kBlack);
  TH1D *hPt2mcCoh = PrepareTH1D("hPt2mcCoh", ptbin, 0., ptmax);
  TH1D *hPt2mcInc = PrepareTH1D("hPt2mcInc", ptbin, 0., ptmax);
  TH1D *hPtLS = PrepareTH1D("hPtLS", ptbin, 0., ptmax);
  hPtLS->SetLineColor(kRed);
  hPt2->SetTitle("");
  if( ptval == "jRecPt2" ) {
    hPt2->SetXTitle("Dielectron #it{p}_{T}^{2} (GeV)^{2}");
    hPt2->SetYTitle( Form("Dielectron counts / (%.3f GeV^{2})", ptbin) );
  } else {
    hPt2->SetXTitle("Dielectron #it{p}_{T} GeV/#it{c}");
    hPt2->SetYTitle( Form("Dielectron counts / (%.0f MeV/#it{c})", 1000.*ptbin) );
  }

  //fill the histograms
  string selstr = Form("jRecM>%f && jRecM<%f", mran[0], mran[1]);

  //jRecTree->Draw("jRecPt2 >> hPt2", selstr.c_str());
  jRecTree->Draw((ptval+" >> hPt2").c_str(), selstr.c_str());
  jLSTree->Draw((ptval+" >> hPtLS").c_str(), selstr.c_str());

  jRecTreeMC1->Draw((ptval+" >> hPt2mcCoh").c_str(), selstr.c_str());
  jRecTreeMC2->Draw((ptval+" >> hPt2mcInc").c_str(), selstr.c_str());

  //normalize pT from MC to data
  normToData(hPt2mcCoh, hPt2, kMagenta);
  normToData(hPt2mcInc, hPt2, kRed);

  hPt2->SetTitleOffset(1.6, "Y");
  hPt2->SetTitleOffset(1.3, "X");

  gPad->SetTopMargin(0.01);
  gPad->SetRightMargin(0.03);
  gPad->SetLeftMargin(0.11);
  gPad->SetBottomMargin(0.11);

  cutLine *clin = new cutLine(cutval, 0.98, hPt2, kTRUE);
  clin->SetLineColor(kYellow);

  leg = PrepareLeg(0.6, 0.76, 0.2, 0.21, 0.03);
  leg->AddEntry(hPt2, "Data");
  //leg->AddEntry(hPtLS, "Like-sign", "l");
  leg->AddEntry((TObject*)0, Form("%.1f < #it{m}_{e^{+}e^{-}} < %.1f GeV/#it{c}^{2}", mran[0], mran[1]), "");
  leg->AddEntry(hPt2mcCoh, (string("MC coherent ")+strjpsi).c_str(), "l");
  leg->AddEntry(hPt2mcInc, (string("MC incoherent ")+strjpsi).c_str(), "l");
  if( cutval > 0. && ptval == "jRecPt2" ) {
    leg->AddEntry(clin, Form("#it{p}_{T}^{2} = %.3f GeV^{2}", cutval), "l");
  }



  gPad->SetLogy();
  hPt2->Draw();
  //hPtLS->Draw("same");
  if(cutval > 0.) clin->Draw("same");
  hPt2mcCoh->Draw("same");
  hPt2mcInc->Draw("same");
  leg->Draw("same");
  gPad->RedrawAxis();

  invertCol(gPad);




}//MakePt2

//_____________________________________________________________________________
void MakePtGG() {

  //pT for gamma-gamma -> e+e-

  //values to plot
  string ptval = "jRecPt";

  //plot limits
  Double_t ptbin = 0.025;
  Double_t ptmax = 1.3;

  //mass range for the plot
  Double_t mran[] = {2.1, 2.6};

  //position of cut line
  Double_t cutval = 0.17; // 0.17

  //mc inputs, need to load before creating the histograms
  TFile *infileMC1 = TFile::Open( "/home/jaroslav/analyza/StUPCLib/ver1/ana/sel/sel0/starsim/slight14a/ana_slight14a4_v2.root");
  TTree *jRecTreeMC1 = (TTree*) infileMC1->Get("jRecTree");

  TH1D *hPt = PrepareTH1D("hPt", ptbin, 0., ptmax);
  SetLineMarkerColor(hPt, kBlack);
  TH1D *hPtmcGG = PrepareTH1D("hPtmcGG", ptbin, 0., ptmax);
  TH1D *hPtLS = PrepareTH1D("hPtLS", ptbin, 0., ptmax);
  hPtLS->SetLineColor(kRed);
  hPt->SetTitle("");
  hPt->SetXTitle("Dielectron #it{p}_{T} (GeV)");
  hPt->SetYTitle( Form("Dielectron counts / (%.0f MeV)", 1000.*ptbin) );


  //fill the histograms
  string selstr = Form("jRecM>%f && jRecM<%f", mran[0], mran[1]);

  jRecTree->Draw((ptval+" >> hPt").c_str(), selstr.c_str());
  jLSTree->Draw((ptval+" >> hPtLS").c_str(), selstr.c_str());

  jRecTreeMC1->Draw((ptval+" >> hPtmcGG").c_str(), selstr.c_str());

  //normalize pT from MC to data
  normToData(hPtmcGG, hPt, kMagenta);

  hPt->SetTitleOffset(1.6, "Y");
  hPt->SetTitleOffset(1.3, "X");

  gPad->SetTopMargin(0.01);
  gPad->SetRightMargin(0.01);
  gPad->SetLeftMargin(0.11);
  gPad->SetBottomMargin(0.11);

  cutLine *clin = new cutLine(cutval, 0.98, hPt, kTRUE);
  clin->SetLineColor(kYellow);

  leg = PrepareLeg(0.6, 0.76, 0.2, 0.21, 0.03);
  leg->AddEntry(hPt, "Data");
  //leg->AddEntry(hPtLS, "Like-sign", "l");
  leg->AddEntry((TObject*)0, Form("%.1f < #it{m}_{e^{+}e^{-}} < %.1f GeV/#it{c}^{2}", mran[0], mran[1]), "");
  leg->AddEntry(hPtmcGG, (string("MC ")+strgg).c_str(), "l");
  leg->AddEntry(hPtLS, "Like-sign data", "l");
  leg->AddEntry(clin, Form("#it{p}_{T} = %.3f GeV", cutval), "l");
  if( cutval > 0. && ptval == "jRecPt2" ) {
    leg->AddEntry(clin, Form("#it{p}_{T}^{2} = %.3f GeV^{2}", cutval), "l");
  }



  gPad->SetLogy();
  hPt->Draw();
  hPtLS->Draw("same");
  if(cutval > 0.) clin->Draw("same");
  hPtmcGG->Draw("same");
  leg->Draw("same");
  gPad->RedrawAxis();

  invertCol(gPad);




}//MakePtGG

//_____________________________________________________________________________
void MakeEffM() {

  //efficiency as a function of mass

  Double_t mbin = 0.1;
  Double_t mmin = 1.5;
  Double_t mmax = 5.;

  TTree *jGenTree = (TTree*) infile->Get("jGenTree");
  TTree *jRecTree = (TTree*) infile->Get("jRecTree");
  if( !jGenTree || !jRecTree ) {cout << "No input" << endl; return;}

  TH1D *hMass = PrepareTH1D("hMass", mbin, mmin, mmax);
  TH1D *hMassGen = PrepareTH1D("hMassGen", mbin, mmin, mmax);

  string strsel = Form("jRecM>%f && jRecM<%f", mmin, mmax);
  string strselgen = Form("jGenM>%f && jGenM<%f", mmin, mmax);

  jRecTree->Draw("jRecM >> hMass", strsel.c_str());
  jGenTree->Draw("jGenM >> hMassGen", strselgen.c_str());

  TH1D *hEff = (TH1D*) divHist(hMass, hMassGen);

  normToData(hMass, hEff);
  normToData(hMassGen, hEff);

  hEff->SetTitle("");
  hEff->SetXTitle("#it{m}_{e^{+}e^{-}} (GeV)");
  hEff->SetYTitle( Form("Efficiency / (%.0f MeV)", 1000.*mbin) );

  hEff->SetTitleOffset(1.6, "Y");
  hEff->SetTitleOffset(1.3, "X");

  gPad->SetTopMargin(0.01);
  gPad->SetRightMargin(0.01);
  gPad->SetLeftMargin(0.11);
  gPad->SetBottomMargin(0.11);

  leg = PrepareLeg(0.17, 0.85, 0.2, 0.09, 0.03);
  leg->AddEntry((TObject*)0, strgg.c_str(), "");
  leg->AddEntry(hEff, "MC rec/gen");

  //hMassGen->Draw();
  //hMass->Draw("same");
  //hEff->Draw("same");

  hEff->Draw();

  leg->Draw("asme");

  //gPad->SetLogy();

  invertCol(gPad);

}//MakeEffM

//_____________________________________________________________________________
void MakeEffTrkPt() {

  //efficiency as a function of track pT

  Double_t pTbin = 0.07;
  Double_t pTmin = 0.6; // 0.05
  Double_t pTmax = 1.8;

  Double_t mran[2] = {2.8, 3.2}; //mass range for the plot

  Bool_t logy = 1;

  TTree *jGenTree = (TTree*) infile->Get("jGenTree");
  TTree *jRecTree = (TTree*) infile->Get("jRecTree");
  if( !jGenTree || !jRecTree ) {cout << "No input" << endl; return;}

  TH1D *hPt = PrepareTH1D("hPt", pTbin, pTmin, pTmax);
  TH1D *hPtGen = PrepareTH1D("hPtGen", pTbin, pTmin, pTmax);

  //pT of positive particles (P0) and negative (P1)
  string strsel = Form("jRecM>%f && jRecM<%f", mran[0], mran[1]);
  string strselgen = Form("jGenM>%f && jGenM<%f", mran[0], mran[1]);
  jRecTree->Draw("jT0pT >> hPt", strsel.c_str());
  jGenTree->Draw("jGenP0pT >> hPtGen", strselgen.c_str());
  jRecTree->Draw("jT1pT >>+ hPt", strsel.c_str());
  jGenTree->Draw("jGenP1pT >>+ hPtGen", strselgen.c_str());

  TH1D *hEff = (TH1D*) divHist(hPt, hPtGen);

  hEff->SetTitle("");
  hEff->SetXTitle("Tracks #it{p}_{T} (GeV)");
  hEff->SetYTitle( Form("Efficiency / (%.0f MeV)", 1000.*pTbin) );

  hEff->SetTitleOffset(1.6, "Y");
  hEff->SetTitleOffset(1.3, "X");

  gPad->SetTopMargin(0.01);
  gPad->SetRightMargin(0.01);
  gPad->SetLeftMargin(0.11);
  gPad->SetBottomMargin(0.11);

  hEff->Draw();
  //hPt->Draw();
  //hPtGen->Draw();

  if(logy) gPad->SetLogy();

  invertCol(gPad);

}//MakeEffTrkPt

//_____________________________________________________________________________
void MakeGGsigma() {

  //sigma(gamma-gamma), data/starlight vs. mass interval

  const Int_t n = 6;
  Double_t x[n]; for(Int_t i=0; i<n; i++) x[i] = (Double_t) i+0.5;

  //cross section ratio and error
  Double_t y1[n]     = {1.20, 0.91, 0.70, 0.59, 0.54, 0.16};
  Double_t y1err[n]  = {0.05, 0.04, 0.03, 0.02, 0.02, 0.01};

  string labels[n] = {"[2.1, 2.2]", "[2.2, 2.3]", "[2.3, 2.4]", "[2.4, 2.5]", "[2.5, 2.6]", "[3.4, 5.0]"};

  TGraphErrors *gXY = new TGraphErrors(n, x, y1, NULL, y1err);
  SetGraphStyle(gXY, kBlack  ,kFullCircle      ,1.8,kBlack   , 1,2);

  TH1F *frame = gPad->DrawFrame(0.7, 0.1, 6.3, 1.3);//xmin, ymin, xmax, ymax
  frame->SetBins(n, 0., (Double_t) n);
  frame->SetXTitle("#it{m}_{e^{+}e^{-}} interval (GeV)");
  frame->SetYTitle("#it{#sigma}_{#gamma#gamma},  data/Starlight");
  for(Int_t i=0; i<n; i++) frame->GetXaxis()->SetBinLabel(i+1, labels[i].data());
  frame->SetTitleOffset(3.3, "X");
  frame->SetTitleOffset(1.3, "Y");
  frame->SetLabelSize(0.06, "X");
  frame->SetLabelSize(0.04, "Y");
  frame->LabelsOption("v", "X"); // put labels perpendicular to the x-axis
  frame->SetTitleSize(0.04, "Y");
  frame->SetTitleSize(0.04, "X");

  gPad->SetTopMargin(0.01);
  gPad->SetRightMargin(0.01);
  gPad->SetLeftMargin(0.11);
  gPad->SetBottomMargin(0.23);

  TLine *lin = new TLine(0.3, 1., 5.7, 1.);
  lin->SetLineColor(kViolet);
  lin->SetLineStyle(kDashed);
  lin->SetLineWidth(4);

  leg = PrepareLeg(0.6, 0.88, 0.2, 0.09, 0.03);
  leg->AddEntry(gXY, "data/Starlight");
  leg->AddEntry(lin, "= 1", "l");

  gXY->Draw("e1p");
  lin->Draw("same");
  leg->Draw("same");

  invertCol(gPad);

}//MakeGGsigma

//_____________________________________________________________________________
void MakePIDdEdx1D() {

  // n sigmas for electrons from dE/dx, 1D histogram for both tracks

  Double_t pbin = 0.05;
  Double_t pidmax = 10.;

  TH1D *hpid = PrepareTH1D("hpid", pbin, -1.*pidmax, pidmax);

  jRecTree->Draw("jT0sigEl >> hpid");
  jRecTree->Draw("jT1sigEl >>+hpid");

  hpid->SetYTitle(Form("Dielectron counts / (%.1f)", pbin));
  hpid->SetXTitle("#it{n}#sigma (electron)");

  hpid->SetTitleOffset(1.5, "Y");
  hpid->SetTitleOffset(1.1, "X");

  gPad->SetTopMargin(0.05);
  gPad->SetRightMargin(0.01);
  gPad->SetBottomMargin(0.08);
  gPad->SetLeftMargin(0.1);

  hpid->Draw();

  invertCol(gPad);

}//MakePIDdEdx1D

//_____________________________________________________________________________
void MakeDeltaDip() {

  // delta-dip-angle according to Phys.Rev. C79 (2009) 064903, http://inspirehep.net/record/797805

  Double_t pdip = 0.001;
  Double_t dipmax = 0.55;

  Bool_t logy = 1;

  TH1D *hdip = PrepareTH1D("hdip", pdip, 0., dipmax);

  jRecTree->Draw("jDeltaDip >> hdip");

  hdip->SetYTitle(Form("Dielectron counts / (%.3f)", pdip));
  hdip->SetXTitle("#delta-dip-angle");

  hdip->SetTitleOffset(1.5, "Y");
  hdip->SetTitleOffset(1.1, "X");

  gPad->SetTopMargin(0.05);
  gPad->SetRightMargin(0.08);
  gPad->SetBottomMargin(0.08);
  gPad->SetLeftMargin(0.1);

  if(logy) gPad->SetLogy();

  //delta-dip-angle formula
  string dipform =
  "#delta-dip-angle = cos^{-1} #left[#frac{#it{p}_{T1} #it{p}_{T2} + #it{p}_{z1} #it{p}_{z2}}{#it{p}_{1} #it{p}_{2}}#right}";
  leg = PrepareLeg(0.37, 0.82, 0.2, 0.09, 0.031);
  leg->AddEntry((TObject*)0, dipform.c_str(), "");

  //legend for underflow and overflow
  leg1 = UoLegLin(hdip, 0.55, 0.74, 0.1, 0.04, 0.03);

  cutLine *dsel = new cutLine(0.03, 0.8, hdip, logy);

  hdip->Draw();
  leg->Draw("same");
  dsel->Draw("same");
  leg1->Draw("same");

  invertCol(gPad);

}//MakeDeltaDip

//_____________________________________________________________________________
void MakeEtaPhiBemc() {

  Double_t etabin = 0.05;
  Double_t etamax = 1.1;

  Double_t phibin = 0.1;
  Double_t phimax = 3.5;

  TH2D *hEtaPhi = PrepareTH2D("hEtaPhi", etabin, -1.*etamax, etamax, phibin, -1.*phimax, phimax);
  hEtaPhi->SetXTitle(Form("Tracks #eta at BEMC / (%.2f)", etabin));
  hEtaPhi->SetYTitle(Form("Tracks #phi at BEMC / (%.2f)", phibin));

  jRecTree->Draw("jT0phiBemc:jT0etaBemc >> hEtaPhi"); // y:x
  jRecTree->Draw("jT1phiBemc:jT1etaBemc >>+hEtaPhi"); 

  hEtaPhi->SetTitleOffset(1.2, "Y");
  hEtaPhi->SetTitleOffset(1.2, "X");

  gPad->SetTopMargin(0.01);
  gPad->SetRightMargin(0.09);
  gPad->SetBottomMargin(0.09);
  gPad->SetLeftMargin(0.09);

  hEtaPhi->Draw();

  invertCol(gPad);

}//MakeEtaPhiBemc

//_____________________________________________________________________________
void MakeTracksEnBEMC() {

  // tracks energy at BEMC position

  Double_t ebin = 0.03;
  Double_t emin = 0.;
  Double_t emax = 3.5;

  Double_t msel[] = {2.8, 3.2};

  TH1D *hEnBemc = PrepareTH1D("hEnBemc", ebin, emin, emax);

  string strsel = Form("jRecM>%f && jRecM<%f", msel[0], msel[1]);

  jRecTree->Draw("jT0EnAtBemc >> hEnBemc", strsel.c_str());
  jRecTree->Draw("jT1EnAtBemc >>+hEnBemc", strsel.c_str());

  hEnBemc->SetYTitle(Form("Dielectron counts / (%.3f)", ebin));
  hEnBemc->SetXTitle("Track energy at BEMC (GeV)");

  hEnBemc->SetTitleOffset(1.5, "Y");
  hEnBemc->SetTitleOffset(1.1, "X");

  gPad->SetTopMargin(0.05);
  gPad->SetRightMargin(0.08);
  gPad->SetBottomMargin(0.08);
  gPad->SetLeftMargin(0.1);

  //legend for mass selection
  leg = PrepareLeg(0.5, 0.76, 0.2, 0.21, 0.035);
  leg->AddEntry((TObject*)0, Form("%.1f < #it{m}_{e^{+}e^{-}} < %.1f GeV/#it{c}^{2}", msel[0], msel[1]), "");

  hEnBemc->Draw();
  leg->Draw("same");

  invertCol(gPad);

}//MakeTracksEnBEMC

//_____________________________________________________________________________
void MakeTracksBemcHitE() {

  // energy of BEMC hit to which the tracks are matched to

  Double_t ebin = 0.03;
  Double_t emin = 0.;
  Double_t emax = 3.5;

  Double_t msel[] = {2.8, 3.2};

  TH1D *hHitEnBemc = PrepareTH1D("hHitEnBemc", ebin, emin, emax);

  string strsel = Form("jRecM>%f && jRecM<%f", msel[0], msel[1]);

  jRecTree->Draw("jT0bemcHitE >> hHitEnBemc", strsel.c_str());
  jRecTree->Draw("jT1bemcHitE >>+hHitEnBemc", strsel.c_str());

  hHitEnBemc->SetYTitle(Form("Dielectron counts / (%.3f)", ebin));
  hHitEnBemc->SetXTitle("BEMC hit energy (GeV)");

  hHitEnBemc->SetTitleOffset(1.5, "Y");
  hHitEnBemc->SetTitleOffset(1.1, "X");

  gPad->SetTopMargin(0.05);
  gPad->SetRightMargin(0.08);
  gPad->SetBottomMargin(0.08);
  gPad->SetLeftMargin(0.1);

  //legend for mass selection
  leg = PrepareLeg(0.5, 0.76, 0.2, 0.21, 0.035);
  leg->AddEntry((TObject*)0, Form("%.1f < #it{m}_{e^{+}e^{-}} < %.1f GeV/#it{c}^{2}", msel[0], msel[1]), "");

  hHitEnBemc->Draw();
  leg->Draw("same");

  invertCol(gPad);

}//MakeTracksBemcHitE

//_____________________________________________________________________________
void MakeTracksBemcHitFractionE() {

  // fraction of BEMC hit energy to cluster energy

  Double_t ebin = 0.03;
  Double_t fracmin = 0.;
  Double_t fracmax = 2.;

  Double_t msel[] = {2.8, 3.2};

  TH1D *hHitFrac = PrepareTH1D("hHitFrac", ebin, fracmin, fracmax);

  string strsel = Form("jRecM>%f && jRecM<%f", msel[0], msel[1]);

  jRecTree->Draw("jT0bemcHitE/jT0bemcE >> hHitFrac", strsel.c_str());
  jRecTree->Draw("jT1bemcHitE/jT1bemcE >>+hHitFrac", strsel.c_str());

  hHitFrac->SetYTitle(Form("Dielectron counts / (%.3f)", ebin));
  hHitFrac->SetXTitle("BEMC hit energy / cluster energy");

  hHitFrac->SetTitleOffset(1.5, "Y");
  hHitFrac->SetTitleOffset(1.1, "X");

  gPad->SetTopMargin(0.05);
  gPad->SetRightMargin(0.08);
  gPad->SetBottomMargin(0.08);
  gPad->SetLeftMargin(0.1);

  //legend for mass selection
  leg = PrepareLeg(0.5, 0.76, 0.2, 0.21, 0.035);
  leg->AddEntry((TObject*)0, Form("%.1f < #it{m}_{e^{+}e^{-}} < %.1f GeV/#it{c}^{2}", msel[0], msel[1]), "");

  hHitFrac->Draw();
  leg->Draw("same");

  invertCol(gPad);

}//MakeTracksBemcHitFractionE

//_____________________________________________________________________________
void MakeEnTrackClsBemc() {

  // track energy at BEMC and cluster energy, 2D

  Double_t ebinCls = 0.05;
  Double_t eclsMin = 0.;
  Double_t eclsMax = 3.5;

  Double_t ebinTrk = 0.05;
  Double_t etrkMin = 0.5;
  Double_t etrkMax = 3.5;

  Double_t msel[] = {2.8, 3.2};
  Double_t ptmax = 0.17;

  TH2D *hEn = PrepareTH2D("hEn", ebinCls, eclsMin, eclsMax, ebinTrk, etrkMin, etrkMax);
  hEn->SetXTitle(Form("BEMC cluster energy (GeV) / (%.2f)", ebinCls));
  hEn->SetYTitle(Form("Tracks energy at BEMC (GeV) / (%.2f)", ebinTrk));

  string strsel = Form("jRecM>%f && jRecM<%f && jRecPt<%f", msel[0], msel[1], ptmax);

  jRecTree->Draw("jT0EnAtBemc:jT0bemcE >> hEn", strsel.c_str()); // y:x
  jRecTree->Draw("jT1EnAtBemc:jT1bemcE >>+hEn", strsel.c_str()); 

  hEn->SetTitleOffset(1.3, "Y");
  hEn->SetTitleOffset(1.3, "X");

  gPad->SetTopMargin(0.012);
  gPad->SetRightMargin(0.11);
  gPad->SetBottomMargin(0.09);
  gPad->SetLeftMargin(0.09);

  //legend for mass selection
  leg = PrepareLeg(0.1, 0.85, 0.2, 0.11, 0.035);
  leg->AddEntry((TObject*)0, Form("%.1f < #it{m}_{e^{+}e^{-}} < %.1f GeV", msel[0], msel[1]), "");
  leg->AddEntry((TObject*)0, Form("p_{#it{T}}^{e^{+}e^{-}} < %.2f GeV", ptmax), "");

  gPad->SetGrid();

  hEn->Draw();
  leg->Draw("same");

  invertCol(gPad);

}//MakeEnTrackClsBemc

//_____________________________________________________________________________
void MakePtotBemc() {

  //tracks momentum at BEMC for all tracks and with BEMC match

  Double_t pbin = 0.025;
  Double_t pmax = 3.3;

  TH1D *hPtot = PrepareTH1D("hPtot", pbin, 0., pmax);
  TH1D *hPtotBemc = PrepareTH1D("hPtotBemc", pbin, 0., pmax);
  //hPtLS->SetLineColor(kRed);
  hPtot->SetTitle("");
  hPtot->SetXTitle("Tracks momentum #it{p}_{tot} at BEMC (GeV)");
  hPtot->SetYTitle( Form("Counts / (%.0f MeV)", 1000.*pbin) );

  jRecTree->Draw("jT0bemcP >> hPtot");
  jRecTree->Draw("jT1bemcP >>+ hPtot");

  jRecTree->Draw("jT0bemcP >> hPtotBemc", "jT0matchBemc==1");
  jRecTree->Draw("jT1bemcP >>+ hPtotBemc", "jT1matchBemc==1");

  hPtot->SetTitleOffset(1.5, "Y");
  hPtot->SetTitleOffset(1.3, "X");

  gPad->SetTopMargin(0.01);
  gPad->SetRightMargin(0.01);
  gPad->SetLeftMargin(0.1);
  gPad->SetBottomMargin(0.1);

  setH1Col(hPtotBemc, kRed);

  leg = PrepareLeg(0.7, 0.84, 0.2, 0.1, 0.035);
  leg->AddEntry(hPtot, "All tracks");
  leg->AddEntry(hPtotBemc, "BEMC match");

  gPad->SetLogy();
  hPtot->Draw();
  hPtotBemc->Draw("e1same");
  //hPtot->Draw("e1same");
  leg->Draw("same");

  invertCol(gPad);

}//MakePtotBemc

//_____________________________________________________________________________
void MakeZdc() {

  //ZDC ADC distributions

  Bool_t ew = 0; // 0 - east,  1 - west

  Double_t zbin = 10.;
  Double_t zmin = 0.;
  Double_t zmax = 1300.;

  string znam[2] = {"jZDCUnAttEast", "jZDCUnAttWest"};
  string xtit[2] = {"ZDC East ADC", "ZDC West ADC"};
  string lhead[2] = {"East ZDC", "West ZDC"};

  TH1D *hZdc = PrepareTH1D("hZdc", zbin, zmin, zmax);
  TH1D *hZdcAll = PrepareTH1D("hZdcAll", zbin, zmin, zmax);

  jRecTree->Draw((znam[ew]+" >> hZdc").c_str());

  TTree *jAllTree = (TTree*) infile->Get("jAllTree");
  jAllTree->Draw((znam[ew]+" >> hZdcAll").c_str());
  normToData(hZdcAll, hZdc, kRed);

  hZdc->SetYTitle(Form("Events / (%.1f)", zbin));
  hZdc->SetXTitle(xtit[ew].c_str());

  hZdc->SetTitleOffset(1.5, "Y");
  hZdc->SetTitleOffset(1.1, "X");

  gPad->SetTopMargin(0.01);
  gPad->SetRightMargin(0.08);
  gPad->SetBottomMargin(0.08);
  gPad->SetLeftMargin(0.1);

  //legend for ZDC description
  leg = PrepareLeg(0.5, 0.76, 0.2, 0.16, 0.035);
  leg->AddEntry((TObject*)0, lhead[ew].c_str(), "");
  leg->AddEntry(hZdc, "Selected events");
  //leg->AddEntry(hZdcAll, "All UPC-JpsiB triggers", "l");
  leg->AddEntry(colLin(kRed,2), "All UPC-JpsiB triggers", "l");


  hZdc->Draw();
  hZdcAll->Draw("same");
  leg->Draw("same");

  printPad(gPad);

  //invertCol(gPad);



}//MakeZdc



















