
// c++ headers
#include <iostream>
#include <fstream>
#include <sys/ioctl.h>
#include <sstream>
#include <time.h>
#include <vector>

// root headers
#include "TFile.h"
#include "TChain.h"
#include "TTree.h"
#include "TIterator.h"
#include "TMath.h"
#include "TLorentzVector.h"
#include "TDatabasePDG.h"
#include "TParticle.h"
#include "TH1I.h"
#include "TH2I.h"
#include "TList.h"
#include "TVector3.h"

// local headers
#include "StUPCEvent.h"
#include "StUPCTrack.h"
#include "StUPCBemcCluster.h"
#include "StUPCVertex.h"
#include "THB1D.h"

using namespace std;

//output trees
TTree *jRecTree;
Double_t jT0pT, jT0eta, jT0phi, jT0pTBemc, jT0etaBemc, jT0phiBemc;
Double_t jT1pT, jT1eta, jT1phi, jT1pTBemc, jT1etaBemc, jT1phiBemc;
Double_t jT0sigEl, jT0chi2, jT0dEdxSig, jT0beta, jT0dcaXY, jT0dcaZ;
Double_t jT1sigEl, jT1chi2, jT1dEdxSig, jT1beta, jT1dcaXY, jT1dcaZ;
Double_t jT0bemcE, jT1bemcE, jT0EnAtBemc, jT1EnAtBemc, jT0bemcP, jT1bemcP;
Int_t jT0charge, jT0nHits, jT0nHitsFit;
Int_t jT1charge, jT1nHits, jT1nHitsFit;
Bool_t jT0matchBemc, jT1matchBemc;
Double_t jT0Deta, jT0Dphi, jT1Deta, jT1Dphi;
Double_t jDeltaDip, jRecPt, jRecY, jRecM;
Double_t jVtxX, jVtxY, jVtxZ;
Int_t jNselTrk, jRunNum;
Long64_t jEvtNum;

const Double_t kInf=9.e9; // infinity representations
const Int_t kIntInf=9999;

//selection criteria
Short_t sign=0;
UShort_t minNhits=0;
Double_t maxAbsEta=kInf, maxNsigPID=kInf;
Double_t minTrkPt=-kInf;
Bool_t matchTof=0, projBemc=0;
Float_t maxAbsZvtx=kInf;
Double_t maxDeltaDip=kInf, maxM=kInf;
Int_t maxSelTrk=kIntInf;

//trigger IDs, same as in StUPCFilterMaker.h
enum {kUPCJpsiB_1=0, kUPCJpsiB_2, kUPCmain_1, kUPCmain_2};

//analysis variables
TFile *infile;
TChain *inchain;
StUPCEvent *upcEvt;
Bool_t isMC;
Double_t trackMass;
TH1I *hEvtCount, *hTrkCount, *hRunCount;
enum evtCnt {kAnaL=1, kTrg, kMaxTrk, kPair, kVtx, kZvtx, kPID, kMaxM, kDip, kSign, kMaxCnt};
enum trkCnt {kTrkAll=1, kTof, kBemcProj, kTPChits, kEta, kPt, kMaxTrkCnt};
THB1D *hPt;

//functions
void RunTracks();
void FilterTracks(vector<Bool_t>& filterMap);
Bool_t selectPair(const StUPCTrack *trk0, const StUPCTrack *trk1);
inline Bool_t selectTrack(const StUPCTrack *trk);
void FillRecTree(const StUPCTrack *trk0, const StUPCTrack *trk1);
TTree *ConnectInput(const string& in);
TFile *CreateOutputTree(const string& out);
void PrintStat(ostream& out, const string& innam, const string& outnam, Int_t lmg=4);
void statMsg(stringstream& st, string msg, evtCnt cnt, Int_t wdt=15);
void ShowProggress(Double_t xi, Double_t xall, const string& in, const string& out);

//_____________________________________________________________________________
int main(void) {

  string basedir = "/home/jaroslav/analyza/star-upc/"; // local
  //string basedir = "/home/tmp/jaroslav/"; // rcf


  //string in = "trees/convel/test0/StUPC_conv.root";
  string in = "trees/test/muDst_test0/StUPC_muDst_test0_all.root";
  //string in = "/home/jaroslav/analyza/StUPCLib/ver1/ana/muDst_run1_prod.txt";
  //string in = "StUPC_muDst_run3_all.root";
  //string in = "trees/starsim/slight14a/StUPC_slight14a6.root";

  string out = "build/output.root";
  //string out = "sel/test/muDst_test0/conv/sel0/ana_muDst_test0_all_conv_sel0.root";

  //selection criteria
  sign = -1;            // sign of dilepton pair, -1: unlike-sign, +1: like-sign, 0: no sign selection
  minNhits = 14;        // min number of track hits
  //maxAbsEta = 1.;       // max track pseudorapidity, absolute value
  maxNsigPID = 3;       // max number of sigmas for TPC dE/dx PID
  //minTrkPt = 0.4;       // minimal track pT at DCA
  matchTof = 1;         // track - TOF matching, 1: required, 0: not required
  projBemc = 1;         // projection to BEMC, 1: required, 0: not required, redundant with matchBemc
  maxAbsZvtx = 100.;    // maximal Z position of vertex, absolute value
  maxDeltaDip = 0.03;   // max delta dip angle
  maxM = 0.1;           // maximal invariant mass
  maxSelTrk = 50;       // max num of selected tracks

  //overrides to selection criteria
  //maxNsigPID = kInf;
  //maxM = kInf;
  //maxDeltaDip = kInf;


  //input
  TTree *upcTree = ConnectInput(basedir+in);
  if(!upcTree) {cout << "No input." << endl; return 1;}

  //output
  TFile *outfile = CreateOutputTree(basedir+out);
  if(!outfile) {cout << "Can not open output file." << endl; return -1;}

  //analysis init
  trackMass = TDatabasePDG::Instance()->GetParticle( 11 )->Mass(); // track mass from PDG
  hEvtCount = new TH1I("hEvtCount", "hEvtCount", kMaxCnt-1, 1, kMaxCnt);
  hTrkCount = new TH1I("hTrkCount", "hTrkCount", kMaxTrkCnt-1, 1, kMaxTrkCnt);
  const Int_t runFirst = 15040000; // 15078000
  const Int_t runLast = 15190000; // 15167100
  hRunCount = new TH1I("hRunCount", "hRunCount", runLast-runFirst, runFirst, runLast);
  clock_t cdelta = CLOCKS_PER_SEC*0.5; //clock ticks per 0.5 sec
  hPt = new THB1D("hPt", "hPt", 70, 0., 2);
  struct winsize size;
  ioctl(STDOUT_FILENO, TIOCGWINSZ, &size);
  hPt->SetTotalHeight( size.ws_row-3 ); // full terminal is size.ws_row-1

  Long64_t nev = upcTree->GetEntries();
  cout << "Starting the analysis, events: " << nev << endl;

  clock_t ctim = clock();
  //event loop
  for(Long64_t iev=0; iev<nev; iev++) {
    if( (clock()-ctim) > cdelta ) {
      ShowProggress(iev, nev, in, out);
      ctim = clock();
    }

    hEvtCount->Fill( kAnaL );

    //get the event
    upcTree->GetEntry(iev);

    //trigger
    //if( !isMC && !upcEvt->getTrigger(kUPCJpsiB_1) && !upcEvt->getTrigger(kUPCJpsiB_2) ) continue;
    if( !isMC && !upcEvt->getTrigger(kUPCmain_1) && !upcEvt->getTrigger(kUPCmain_2) ) continue;
    hEvtCount->Fill( kTrg );

    jEvtNum = iev;
    RunTracks();

  }//event loop

  hPt->SetTotalHeight( hPt->GetTotalHeight()-1 );
  ShowProggress(nev, nev, in, out);
  cout << endl;

  ofstream out1("out.txt");
  PrintStat(out1, in, out, 6);

  jRecTree->Write();
  hEvtCount->Write();
  hTrkCount->Write();
  hRunCount->Write();
  outfile->Close();
  if(infile) infile->Close();

  return 0;

}//main

//_____________________________________________________________________________
void RunTracks() {

  Int_t ntrk = upcEvt->getNumberOfTracks();

  //vector to filter selected tracks
  vector<Bool_t> filterMap(ntrk, kFALSE);
  FilterTracks(filterMap);

  if( jNselTrk > maxSelTrk ) return;
  hEvtCount->Fill( kMaxTrk );

  //pairs loop
  for(Int_t i=0; i<ntrk; i++) {
    StUPCTrack *trk0 = upcEvt->getTrack(i);
    if( !filterMap[i] ) continue;

    for(Int_t j=i+1; j<ntrk; j++) {
      StUPCTrack *trk1 = upcEvt->getTrack(j);
      if( !filterMap[j] ) continue;

      hEvtCount->Fill( kPair );

      if( !selectPair(trk0, trk1) ) continue;

      FillRecTree(trk0, trk1);
    }
  }//pairs loop

}//RunTracks

//_____________________________________________________________________________
void FilterTracks(vector<Bool_t>& filterMap) {

  Int_t ntrk = upcEvt->getNumberOfTracks();

  jNselTrk = 0;
  //tracks loop
  for(Int_t i=0; i<ntrk; i++) {
    StUPCTrack *trk = upcEvt->getTrack(i);
    if(!trk) continue;

    hTrkCount->Fill( kTrkAll );

    if( !selectTrack(trk) ) continue;

    //track selected
    filterMap[i] = kTRUE;
    jNselTrk++;

  }//tracks loop

}//FilterTracks

//_____________________________________________________________________________
Bool_t selectPair(const StUPCTrack *trk0, const StUPCTrack *trk1) {

  //same vertex
  if( trk0->getVertexId() != trk1->getVertexId() ) return kFALSE;
  hEvtCount->Fill( kVtx );

  //z_vtx, tracks in pair already from same vertex
  if( TMath::Abs(trk0->getVertex()->getPosZ()) > maxAbsZvtx ) return kFALSE;
  hEvtCount->Fill( kZvtx );

  //electron PID
  Double_t pid0 = trk0->getNSigmasTPCElectron();
  Double_t pid1 = trk1->getNSigmasTPCElectron();
  //accept pairs with nsig0^2 + nsig1^2 < maxsig^2
  if( pid0*pid0 + pid1*pid1 > maxNsigPID*maxNsigPID ) return kFALSE;
  hEvtCount->Fill( kPID );

  //maximal mass
  TLorentzVector v0, v1;
  trk0->getLorentzVector(v0, trackMass);
  trk1->getLorentzVector(v1, trackMass);
  TLorentzVector vpair = v0 + v1;
  if( vpair.M() > maxM ) return kFALSE;
  hEvtCount->Fill( kMaxM );

  //delta-dip-angle, Eq. 2 in PHYSICAL REVIEW C 79, 064903 (2009)
  TVector3 vec0, vec1;
  trk0->getMomentum(vec0);
  trk1->getMomentum(vec1);
  jDeltaDip = TMath::ACos( (vec0.Pt()*vec1.Pt() + vec0.Pz()*vec1.Pz())/(vec0.Mag()*vec1.Mag()) );

  if( jDeltaDip > maxDeltaDip ) return kFALSE;
  hEvtCount->Fill( kDip );

  //sign selection
  Short_t qTrk0 = trk0->getCharge();
  Short_t qTrk1 = trk1->getCharge();
  if( qTrk0*qTrk1*sign < 0 ) return kFALSE;
  hEvtCount->Fill( kSign );

  return kTRUE;

}//selectPair

//_____________________________________________________________________________
inline Bool_t selectTrack(const StUPCTrack *trk) {

  //TOF match
  if( matchTof && !trk->getFlag( StUPCTrack::kTof ) ) return kFALSE;
  //if( matchTof ) {
    //if( !trk->getFlag( StUPCTrack::kTof ) || trk->getTofBeta() < -998 ) return kFALSE;
  //}
  hTrkCount->Fill( kTof );

  //BEMC projection
  if( projBemc && !trk->getFlag( StUPCTrack::kBemcProj ) ) return kFALSE;
  hTrkCount->Fill( kBemcProj );

  //min hits in TPC
  if( trk->getNhits() < minNhits ) return kFALSE;
  hTrkCount->Fill( kTPChits );

  //max |eta|
  if( TMath::Abs( trk->getEta() ) > maxAbsEta ) return kFALSE;
  hTrkCount->Fill( kEta );

  //min pT
  if( trk->getPt() < minTrkPt ) return kFALSE;
  hTrkCount->Fill( kPt );

  return kTRUE;

}//selectTrack

//_____________________________________________________________________________
void FillRecTree(const StUPCTrack *trk0, const StUPCTrack *trk1) {

  //tracks kinematics at PV
  jT0pT = trk0->getPt();
  jT0eta = trk0->getEta();
  jT0phi = trk0->getPhi();
  jT1pT = trk1->getPt();
  jT1eta = trk1->getEta();
  jT1phi = trk1->getPhi();

  //dE/dx PID and signal
  jT0sigEl = trk0->getNSigmasTPCElectron();
  jT1sigEl = trk1->getNSigmasTPCElectron();
  jT0dEdxSig  = trk0->getDEdxSignal();
  jT1dEdxSig  = trk1->getDEdxSignal();

  //TOF beta
  jT0beta = trk0->getTofBeta();
  jT1beta = trk1->getTofBeta();

  //DCA to vertex
  jT0dcaXY = trk0->getDcaXY();
  jT0dcaZ = trk0->getDcaZ();
  jT1dcaXY = trk1->getDcaXY();
  jT1dcaZ = trk1->getDcaZ();

  //chi2
  jT0chi2 = trk0->getChi2();
  jT1chi2 = trk1->getChi2();

  //charge
  jT0charge = trk0->getCharge();
  jT1charge = trk1->getCharge();

  //tracks hits
  jT0nHits = trk0->getNhits();
  jT1nHits = trk1->getNhits();
  jT0nHitsFit = trk0->getNhitsFit();
  jT1nHitsFit = trk1->getNhitsFit();

  //kinematics at BEMC
  trk0->getBemcPtEtaPhi(jT0pTBemc, jT0etaBemc, jT0phiBemc);
  trk1->getBemcPtEtaPhi(jT1pTBemc, jT1etaBemc, jT1phiBemc);
  //momentum at BEMC
  TVector3 v0b, v1b;
  v0b.SetPtEtaPhi(jT0pTBemc, jT0etaBemc, jT0phiBemc);
  v1b.SetPtEtaPhi(jT1pTBemc, jT1etaBemc, jT1phiBemc);
  jT0bemcP = v0b.Mag();
  jT1bemcP = v1b.Mag();

  //BEMC clusters energy
  StUPCBemcCluster *cls0 = trk0->getBemcCluster();
  StUPCBemcCluster *cls1 = trk1->getBemcCluster();
  jT0bemcE=-kInf; jT1bemcE=-kInf;
  if(cls0) jT0bemcE = cls0->getEnergy();
  if(cls1) jT1bemcE = cls1->getEnergy();

  //tracks energy at BEMC
  jT0EnAtBemc = -kInf;
  jT1EnAtBemc = -kInf;
  if( trk0->getFlag( StUPCTrack::kBemcProj ) ) {
    TLorentzVector bv0;
    trk0->getBemcLorentzVector(bv0, trackMass);
    jT0EnAtBemc = bv0.E();
  }
  if( trk1->getFlag( StUPCTrack::kBemcProj ) ) {
    TLorentzVector bv1;
    trk1->getBemcLorentzVector(bv1, trackMass);
    jT1EnAtBemc = bv1.E();
  }

  //eta and phi difference between cluster and track at BEMC
  jT0Deta=-kInf; jT0Dphi=-kInf; jT1Deta=-kInf; jT1Dphi=-kInf;
  if( cls0 ) {
    jT0Deta = cls0->getEta() - jT0etaBemc;
    jT0Dphi = cls0->getPhi() - jT0phiBemc;
  }
  if( cls1 ) {
    jT1Deta = cls1->getEta() - jT1etaBemc;
    jT1Dphi = cls1->getPhi() - jT1phiBemc;
  }

  //BEMC match
  jT0matchBemc = trk0->getFlag( StUPCTrack::kBemc );
  jT1matchBemc = trk1->getFlag( StUPCTrack::kBemc );

  if( jT0matchBemc ) hPt->Fill( jT0pTBemc );
  if( jT1matchBemc ) hPt->Fill( jT1pTBemc );

  //pair kinematics
  TLorentzVector v0, v1;
  trk0->getLorentzVector(v0, trackMass);
  trk1->getLorentzVector(v1, trackMass);
  TLorentzVector vpair = v0 + v1; //sum of tracks 4-vectors
  jRecPt = vpair.Pt();
  jRecY  = vpair.Rapidity();
  jRecM  = vpair.M();

  //vertex position, both tracks come from the same vertex at this point
  StUPCVertex *vtx = trk0->getVertex();
  jVtxX = vtx->getPosX();
  jVtxY = vtx->getPosY();
  jVtxZ = vtx->getPosZ();

  //run number
  jRunNum = upcEvt->getRunNumber();
  hRunCount->Fill( jRunNum );

  jRecTree->Fill();

}//FillRecTree

//_____________________________________________________________________________
TFile *CreateOutputTree(const string& out) {

  TFile *outfile = TFile::Open(out.c_str(), "recreate");
  if(!outfile) return 0x0;

  //standard reconstructed tree
  jRecTree = new TTree("jRecTree", "jRecTree");
  jRecTree ->Branch("jT0pT", &jT0pT, "jT0pT/D");
  jRecTree ->Branch("jT0eta", &jT0eta, "jT0eta/D");
  jRecTree ->Branch("jT0phi", &jT0phi, "jT0phi/D");
  jRecTree ->Branch("jT0pTBemc", &jT0pTBemc, "jT0pTBemc/D");
  jRecTree ->Branch("jT0etaBemc", &jT0etaBemc, "jT0etaBemc/D");
  jRecTree ->Branch("jT0phiBemc", &jT0phiBemc, "jT0phiBemc/D");
  jRecTree ->Branch("jT1pT", &jT1pT, "jT1pT/D");
  jRecTree ->Branch("jT1eta", &jT1eta, "jT1eta/D");
  jRecTree ->Branch("jT1phi", &jT1phi, "jT1phi/D");
  jRecTree ->Branch("jT1pTBemc", &jT1pTBemc, "jT1pTBemc/D");
  jRecTree ->Branch("jT1etaBemc", &jT1etaBemc, "jT1etaBemc/D");
  jRecTree ->Branch("jT1phiBemc", &jT1phiBemc, "jT1phiBemc/D");
  jRecTree ->Branch("jT0sigEl", &jT0sigEl, "jT0sigEl/D");
  jRecTree ->Branch("jT0chi2", &jT0chi2, "jT0chi2/D");
  jRecTree ->Branch("jT0dEdxSig", &jT0dEdxSig, "jT0dEdxSig/D");
  jRecTree ->Branch("jT0beta", &jT0beta, "jT0beta/D");
  jRecTree ->Branch("jT0dcaXY", &jT0dcaXY, "jT0dcaXY/D");
  jRecTree ->Branch("jT0dcaZ", &jT0dcaZ, "jT0dcaZ/D");
  jRecTree ->Branch("jT1sigEl", &jT1sigEl, "jT1sigEl/D");
  jRecTree ->Branch("jT1chi2", &jT1chi2, "jT1chi2/D");
  jRecTree ->Branch("jT1dEdxSig", &jT1dEdxSig, "jT1dEdxSig/D");
  jRecTree ->Branch("jT1beta", &jT1beta, "jT1beta/D");
  jRecTree ->Branch("jT1dcaXY", &jT1dcaXY, "jT1dcaXY/D");
  jRecTree ->Branch("jT1dcaZ", &jT1dcaZ, "jT1dcaZ/D");
  jRecTree ->Branch("jT0bemcE", &jT0bemcE, "jT0bemcE/D");
  jRecTree ->Branch("jT1bemcE", &jT1bemcE, "jT1bemcE/D");
  jRecTree ->Branch("jT0EnAtBemc", &jT0EnAtBemc, "jT0EnAtBemc/D");
  jRecTree ->Branch("jT1EnAtBemc", &jT1EnAtBemc, "jT1EnAtBemc/D");
  jRecTree ->Branch("jT0bemcP", &jT0bemcP, "jT0bemcP/D");
  jRecTree ->Branch("jT1bemcP", &jT1bemcP, "jT1bemcP/D");
  jRecTree ->Branch("jT0charge", &jT0charge, "jT0charge/I");
  jRecTree ->Branch("jT0nHits", &jT0nHits, "jT0nHits/I");
  jRecTree ->Branch("jT0nHitsFit", &jT0nHitsFit, "jT0nHitsFit/I");
  jRecTree ->Branch("jT1charge", &jT1charge, "jT1charge/I");
  jRecTree ->Branch("jT1nHits", &jT1nHits, "jT1nHits/I");
  jRecTree ->Branch("jT1nHitsFit", &jT1nHitsFit, "jT1nHitsFit/I");
  jRecTree ->Branch("jDeltaDip", &jDeltaDip, "jDeltaDip/D");
  jRecTree ->Branch("jT0matchBemc", &jT0matchBemc, "jT0matchBemc/O");
  jRecTree ->Branch("jT1matchBemc", &jT1matchBemc, "jT1matchBemc/O");
  jRecTree ->Branch("jT0Deta", &jT0Deta, "jT0Deta/D");
  jRecTree ->Branch("jT0Dphi", &jT0Dphi, "jT0Dphi/D");
  jRecTree ->Branch("jT1Deta", &jT1Deta, "jT1Deta/D");
  jRecTree ->Branch("jT1Dphi", &jT1Dphi, "jT1Dphi/D");
  jRecTree ->Branch("jRecPt", &jRecPt, "jRecPt/D");
  jRecTree ->Branch("jRecY", &jRecY, "jRecY/D");
  jRecTree ->Branch("jRecM", &jRecM, "jRecM/D");
  jRecTree ->Branch("jVtxX", &jVtxX, "jVtxX/D");
  jRecTree ->Branch("jVtxY", &jVtxY, "jVtxY/D");
  jRecTree ->Branch("jVtxZ", &jVtxZ, "jVtxZ/D");
  jRecTree ->Branch("jNselTrk", &jNselTrk, "jNselTrk/I");
  jRecTree ->Branch("jRunNum", &jRunNum, "jRunNum/I");
  jRecTree ->Branch("jEvtNum", &jEvtNum, "jEvtNum/L");

  //selection criteria in output reconstructed tree
  jRecTree ->Branch("sign", &sign, "sign/S");
  jRecTree ->Branch("minNhits", &minNhits, "minNhits/s");
  jRecTree ->Branch("maxAbsEta", &maxAbsEta, "maxAbsEta/D");
  jRecTree ->Branch("maxNsigPID", &maxNsigPID, "maxNsigPID/D");
  jRecTree ->Branch("minTrkPt", &minTrkPt, "minTrkPt/D");
  jRecTree ->Branch("matchTof", &matchTof, "matchTof/O");
  jRecTree ->Branch("projBemc", &projBemc, "projBemc/O");
  jRecTree ->Branch("maxAbsZvtx", &maxAbsZvtx, "maxAbsZvtx/F");
  jRecTree ->Branch("maxDeltaDip", &maxDeltaDip, "maxDeltaDip/D");
  jRecTree ->Branch("maxSelTrk", &maxSelTrk, "maxSelTrk/I");
  jRecTree ->Branch("maxM", &maxM, "maxM/D");


  return outfile;

}//CreateOutputTree

//_____________________________________________________________________________
TTree *ConnectInput(const string& in) {

  TTree *upcTree = 0x0;
  //input from file or chain
  if( in.find(".root") != string::npos ) {
    cout << "Input from root file" << endl;
    infile = TFile::Open(in.c_str(), "read");
    if(!infile) return 0x0;
    upcTree = dynamic_cast<TTree*>( infile->Get("mUPCTree") );
  } else {
    cout << "Input from chain" << endl;
    inchain = new TChain("mUPCTree");
    ifstream instr(in.c_str());
    string line;
    while(getline(instr, line)) {
      inchain->AddFile(line.c_str());
    }
    instr.close();
    upcTree = dynamic_cast<TTree*>( inchain );
  }

  if(!upcTree) return 0x0;

  upcTree->SetBranchAddress("mUPCEvent", &upcEvt);
  upcTree->GetEntry(0);
  isMC = upcEvt->getIsMC(); // MC or data

  return upcTree;

}//ConnectInput

//_____________________________________________________________________________
void PrintStat(ostream& out, const string& innam, const string& outnam, Int_t lmg) {

  stringstream st;
  //input and output
  st.width(8); st << left << "Input:" << innam << endl << endl;
  st.width(8); st << left << "Output:" << outnam << endl << endl;

  //analysis counter
  //Int_t wdt=15;
  st << "------------------------" << endl;
  st.precision(0);
  statMsg(st, "Local ana: ", kAnaL);
  statMsg(st, "Triggers: ", kTrg);
  st << "------------------------" << endl;
  statMsg(st, "Max mult: ", kMaxTrk);
  statMsg(st, "Pairs: ", kPair);
  statMsg(st, "Same vtx: ", kVtx);
  statMsg(st, "z_vtx: ", kZvtx);
  statMsg(st, "PID: ", kPID);
  statMsg(st, "Max mass: ", kMaxM);
  statMsg(st, "Delta dip: ", kDip);
  statMsg(st, "Sign: ", kSign);
  st << "------------------------" << endl;

  //pT histogram
  st << hPt;

  //put left margin
  string line;
  Int_t ilin=0;
  while( getline(st, line) ) {
    if( ++ilin == 4 ) lmg += 2;
    if(!line.empty()) {
      out.width(lmg);
      out << "";
    }
    out << line << endl;
  }

}//PrintStat

//_____________________________________________________________________________
void statMsg(stringstream& st, string msg, evtCnt cnt, Int_t wdt) {

  st.width(wdt); st << left << msg << fixed << hEvtCount->GetBinContent( cnt ) << endl;

}//statMsg

//_____________________________________________________________________________
void ShowProggress(Double_t xi, Double_t xall, const string& in, const string& out) {

  if( xall < 0.1 ) return;
  if( xi > xall ) return;

  cout << endl;
  cout.width(10);
  cout << "Input: " << in << endl;
  cout.width(10);
  cout << "Output: " << out << endl;
  cout << hPt;

  Int_t pbar = 35;

  Double_t prog = xi/xall;
  Int_t pos = prog*pbar;

  string pdone = "\u2588"; //full block
  string phead = "\u2591"; //light shade
  string prem = "\u2591"; //light shade
  cout<<" [";
  //proggress loop
  for(Int_t i=0; i<pbar; ++i) {
    if( i < pos ) {
      cout << pdone;
    } else {
      if( i == pos ) {
        cout << phead;
      } else {
        cout << prem;
      }
    }
  }//proggress loop
  //cout<<"] "<<Form("%.1f", prog*100.)<<" %\r";
  cout << Form("] %.1f", prog*100.)<<" %\r";
  cout.flush();

  // std::cout<<"Event: "<<i<<"\r"; std::cout.flush();

}//ShowProggress

















