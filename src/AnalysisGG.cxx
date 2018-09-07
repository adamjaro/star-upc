
// c++ headers
#include <iostream>
#include <fstream>
#include <sys/ioctl.h>
#include <sstream>
#include <time.h>

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
#include "TRandom3.h"

// local headers
#include "StUPCEvent.h"
#include "StUPCTrack.h"
#include "StUPCBemcCluster.h"
#include "StUPCVertex.h"
#include "THB1D.h"
#include "ArgumentParser.h"

using namespace std;

//output trees
TTree *jRecTree, *jAllTree;
Double_t jRecPt, jRecY, jRecM;
Int_t jBBCSmallEast, jBBCSmallWest, jBBCLargeEast, jBBCLargeWest;
Int_t jZDCUnAttEast, jZDCUnAttWest, jTOFMult;
Int_t jVPDSumEast, jVPDSumWest;
Double_t jZDCVtxZ;
Double_t jT0pT, jT0eta, jT0phi, jT1pT, jT1eta, jT1phi;
Double_t jT0sigEl, jT1sigEl;
Double_t jT0dEdxSig, jT1dEdxSig, jT0beta, jT1beta;
Double_t jVtxX, jVtxY, jVtxZ;
Int_t jNPrimInVtx, jNPrimVtxUsed;
Double_t jT0dcaXY, jT0dcaZ, jT1dcaXY, jT1dcaZ;
Double_t jT0chi2, jT1chi2;
Bool_t jT0matchTof, jT1matchTof;
Int_t jT0charge, jT1charge, jT0nHits, jT1nHits, jT0nHitsFit, jT1nHitsFit;

const Double_t kUdf=-9.e9;//default for undefined
const Double_t kInf=9.e9; // infinity representation
const Int_t kIntInf=9999;

//selection criteria
Int_t sign=0;
Int_t maxNPrim=kIntInf;
Int_t minNhits=0;
Double_t maxAbsEta=kInf, maxNsigPID=kInf;
Bool_t matchTof=0;
Double_t maxAbsZvtx=kInf;
Double_t maxAbsY=kInf;
const Int_t npairSel=2;
enum {kV0=0, kV1};
Int_t pairSel=kV0;
Int_t trgProfile=0;

//trigger IDs, same as in StUPCFilterMaker.h
enum {kUPCJpsiB_1=0, kUPCJpsiB_2, kUPCmain_1, kUPCmain_2, kZero_bias, kMain10_1, kMain10_2, kMain11_1, kMain11_2, kMain11_3};

//analysis variables
TFile *infile;
TChain *inchain;
StUPCEvent *upcEvt;
Bool_t isMC;
Double_t trackMass;
Bool_t (*RunTracks[npairSel])(StUPCTrack *pair[]); // pointers to pair selection functions
TH1I *hEvtCount;
enum{kAnaL=1, kPair, kVtxId, kPID, kZvtx, kSign, kUPCJpsiB, kMaxCnt};
enum EvtCount{ kAna=1, kTrg, kDatBEMC, kWritten }; // counter from StUPCFilterMaker.h
THB1D *hMass;

//functions
Bool_t RunTracksV0(StUPCTrack *pair[]);
inline Bool_t selectTrack(const StUPCTrack *trk);
void FillRecTree(StUPCTrack *pair[], const TLorentzVector &vpair, const TLorentzVector &v0, const TLorentzVector &v1);
void SortTracks(StUPCTrack *pair[]);
void Init();
TTree *ConnectInput(const string& in);
TFile *CreateOutputTree(const string& out);
void PrintStat(ostream& out, const string& innam, const string& outnam, Int_t lmg=4);
void ShowProggress(Double_t xi, Double_t xall, const string& in, const string& out);

//_____________________________________________________________________________
int main(int argc, char* argv[]) {

  if( argc != 2 ) {
    cout << "No configuration file specified." << endl;
    return -1;
  }

  //register selection criteria for argument parser
  ArgumentParser parser;
  parser.AddDouble("maxAbsEta", &maxAbsEta);
  parser.AddDouble("maxNsigPID", &maxNsigPID);
  parser.AddDouble("maxAbsZvtx", &maxAbsZvtx);
  parser.AddDouble("maxAbsY", &maxAbsY);
  parser.AddInt("sign", &sign);
  parser.AddInt("maxNPrim", &maxNPrim);
  parser.AddInt("minNhits", &minNhits);
  parser.AddInt("pairSel", &pairSel);
  parser.AddInt("trgProfile", &trgProfile);
  parser.AddBool("matchTof", &matchTof);

  string basedir_in, in_name, basedir_out, out_name;
  parser.AddString("basedir_in", &basedir_in);
  parser.AddString("in_name", &in_name);
  parser.AddString("basedir_out", &basedir_out);
  parser.AddString("out_name", &out_name);

  //read the configuration file
  parser.SetConfigDirectory("../config");
  if( !parser.Parse(argv[1]) ) return -1;

  //input
  TTree *upcTree = ConnectInput(basedir_in + "/" + in_name);
  if(!upcTree) {cout << "No input." << endl; return 1;}

  //output
  TFile *outfile = CreateOutputTree(basedir_out + "/" + out_name);
  if(!outfile) {cout << "Can not open output file." << endl; return -1;}

  //analysis init
  Init();

  Long64_t nev = upcTree->GetEntries();
  cout << "Starting the analysis, events: " << nev << endl;
  cout<<"Input:   "<<in_name<<endl;
  cout<<"Output:  "<<out_name<<endl;

  clock_t cdelta = CLOCKS_PER_SEC*0.5; //clock ticks per 0.5 sec
  clock_t ctim = clock();
  //event loop
  for(Long64_t iev=0; iev<nev; iev++) {
    if( (clock()-ctim) > cdelta ) {
      ShowProggress(iev, nev, in_name, out_name);
      ctim = clock();
    }
    //get the event
    upcTree->GetEntry(iev);

    //trigger
    if( !isMC && trgProfile==3 ) {
      if( !upcEvt->getTrigger(kMain10_1) && !upcEvt->getTrigger(kMain10_2)
          && !upcEvt->getTrigger(kMain11_1) && !upcEvt->getTrigger(kMain11_2) && !upcEvt->getTrigger(kMain11_3) ) continue;
    }
    hEvtCount->Fill( kAnaL );

    //tracks
    StUPCTrack *pair[2] = {0,0};
    if( !(*RunTracks[pairSel])(pair) ) continue;
    SortTracks(pair); //put positive track first

    //electron PID
    Double_t pid0 = pair[0]->getNSigmasTPCElectron();
    Double_t pid1 = pair[1]->getNSigmasTPCElectron();
    //accept pairs with nsig0^2 + nsig1^2 < maxsig^2
    if( pid0*pid0 + pid1*pid1 > maxNsigPID*maxNsigPID ) continue;
    hEvtCount->Fill( kPID );

    //z_vtx, tracks in pair are already from same vtx, track 0 used to get vtx object
    if( TMath::Abs(pair[0]->getVertex()->getPosZ()) > maxAbsZvtx ) continue;
    hEvtCount->Fill( kZvtx );

    //pair rapidity
    TLorentzVector v0, v1; //4-vectors for tracks
    pair[0]->getLorentzVector(v0, trackMass);
    pair[1]->getLorentzVector(v1, trackMass);
    TLorentzVector vpair = v0 + v1; //sum of tracks 4-vectors
    //if( TMath::Abs( vpair.Rapidity() ) > maxAbsY ) continue;
    //hEvtCount->Fill( kRap );

    //sign selection
    Short_t qTrk0 = pair[0]->getCharge();
    Short_t qTrk1 = pair[1]->getCharge();
    if( qTrk0*qTrk1*sign < 0 ) continue;
    hEvtCount->Fill( kSign );

    //event selected

    //fill output tree
    FillRecTree(pair, vpair, v0, v1);

  }//event loop

  hMass->SetTotalHeight( hMass->GetTotalHeight()-1 );
  ShowProggress(nev, nev, in_name, out_name);
  cout << endl;
  ofstream out1("out.txt");
  PrintStat(out1, in_name, out_name, 6);

  //write the outputs
  jRecTree->Write();
  hEvtCount->Write();
  outfile->Close();
  if(infile) infile->Close();

  return 0;

}//main

//_____________________________________________________________________________
Bool_t RunTracksV0(StUPCTrack *pair[]) {

  // pair algorighm version 0
  //
  // find pair of tracks already coming from the same vertex

  Int_t npair = 0;

  Int_t ntrk = upcEvt->getNumberOfTracks();
  //tracks loop
  for(Int_t i=0; i<ntrk; i++) {
    StUPCTrack *trk0 = upcEvt->getTrack(i);
    if(!trk0) continue;

    if( !selectTrack(trk0) ) continue;

    //track accepted

    UInt_t vtxId0 = trk0->getVertexId();

    //inner tracks loop
    for(Int_t j=i+1; j<ntrk; j++) {
      StUPCTrack *trk1 = upcEvt->getTrack(j);
      if(!trk1) continue;

      if( !selectTrack(trk1) ) continue;

      //same vertex
      if( trk1->getVertexId() != vtxId0 ) continue;

      //pair accepted

      npair++;
      if( npair > 1 ) break;

      //save pointers to tracks in pair
      pair[0] = trk0;
      pair[1] = trk1;

    }//inner tracks loop

    if(npair > 1) break;

  }//tracks loop

  //one pair
  if( npair != 1 ) return kFALSE;

  hEvtCount->Fill( kPair );
  hEvtCount->Fill( kVtxId );
  return kTRUE;

}//RunTracksV0

//_____________________________________________________________________________
inline Bool_t selectTrack(const StUPCTrack *trk) {

  //hTrkCount->Fill( kTrkAll );

  //max number of primary tracks in vertex associated with the track
  if( trk->getVertex()->getNPrimaryTracks() > maxNPrim ) return kFALSE;

  //TOF match
  Bool_t isTof = trk->getFlag( StUPCTrack::kTof );
  //if(isTof) hTrkCount->Fill( kTof );
  if( matchTof && !isTof ) return kFALSE;

  //min hits in TPC
  if( trk->getNhits() < minNhits ) return kFALSE;

  //max |eta|
  if( TMath::Abs( trk->getEta() ) > maxAbsEta ) return kFALSE;

  return kTRUE;

}//selectTrack

//_____________________________________________________________________________
void FillRecTree(StUPCTrack *pair[], const TLorentzVector &vpair, const TLorentzVector &v0, const TLorentzVector &v1) {

  jRecPt = vpair.Pt();
  jRecY  = vpair.Rapidity();
  jRecM  = vpair.M();

  hMass->Fill(jRecM);

  jBBCSmallEast = (Int_t) upcEvt->getBBCSmallEast();
  jBBCSmallWest = (Int_t) upcEvt->getBBCSmallWest();
  jBBCLargeEast = (Int_t) upcEvt->getBBCLargeEast();
  jBBCLargeWest = (Int_t) upcEvt->getBBCLargeWest();

  jZDCUnAttEast = (Int_t) upcEvt->getZDCUnAttEast();
  jZDCUnAttWest = (Int_t) upcEvt->getZDCUnAttWest();
  jZDCVtxZ = upcEvt->getZdcVertexZ();

  jTOFMult = (Int_t) upcEvt->getTOFMultiplicity();

  jVPDSumEast = (Int_t) upcEvt->getVPDSumEast();
  jVPDSumWest = (Int_t) upcEvt->getVPDSumWest();

  //tracks kinematics
  jT0pT       = pair[0]->getPt();
  jT0eta      = pair[0]->getEta();
  jT0phi      = pair[0]->getPhi();
  jT1pT       = pair[1]->getPt();
  jT1eta      = pair[1]->getEta();
  jT1phi      = pair[1]->getPhi();
  jT0sigEl    = pair[0]->getNSigmasTPCElectron();
  jT1sigEl    = pair[1]->getNSigmasTPCElectron();

  //tracks dE/dx signal and TOF beta
  jT0dEdxSig  = pair[0]->getDEdxSignal();
  jT1dEdxSig  = pair[1]->getDEdxSignal();
  jT0beta     = pair[0]->getTofBeta();
  jT1beta     = pair[1]->getTofBeta();

  //primary vertex
  StUPCVertex *vtx = pair[0]->getVertex();
  jVtxX = vtx->getPosX();
  jVtxY = vtx->getPosY();
  jVtxZ = vtx->getPosZ();
  jNPrimInVtx = vtx->getNPrimaryTracks();
  jNPrimVtxUsed = vtx->getNTracksUsed();

  //DCA to vertex
  jT0dcaXY = pair[0]->getDcaXY();
  jT0dcaZ = pair[0]->getDcaZ();
  jT1dcaXY = pair[1]->getDcaXY();
  jT1dcaZ = pair[1]->getDcaZ();

  //tracks Chi^2
  jT0chi2 = pair[0]->getChi2();
  jT1chi2 = pair[1]->getChi2();

  //TOF match
  jT0matchTof = pair[0]->getFlag( StUPCTrack::kTof );
  jT1matchTof = pair[1]->getFlag( StUPCTrack::kTof );

  //tracks charge
  jT0charge = pair[0]->getCharge();
  jT1charge = pair[1]->getCharge();

  //tracks hits
  jT0nHits    = pair[0]->getNhits();
  jT1nHits    = pair[1]->getNhits();
  jT0nHitsFit = pair[0]->getNhitsFit();
  jT1nHitsFit = pair[1]->getNhitsFit();

  jRecTree->Fill();

}//FillRecTree

//_____________________________________________________________________________
void SortTracks(StUPCTrack *pair[]) {

  //sort tracks in pair according to charge, first track positive,
  //second negative

  if( pair[0]->getCharge() > 0 ) return;

  //swap the tracks to get positive track to the first position
  StUPCTrack *tmp[2] = {pair[0], pair[1]};

  pair[0] = tmp[1];
  pair[1] = tmp[0];


}//SortTracks

//_____________________________________________________________________________
TFile *CreateOutputTree(const string& out) {

  TFile *outfile = TFile::Open(out.c_str(), "recreate");
  if(!outfile) return 0x0;

  //standard reconstructed tree
  jRecTree = new TTree("jRecTree", "jRecTree");

  jRecTree ->Branch("jRecPt", &jRecPt, "jRecPt/D");
  jRecTree ->Branch("jRecY", &jRecY, "jRecY/D");
  jRecTree ->Branch("jRecM", &jRecM, "jRecM/D");

  jRecTree ->Branch("jBBCSmallEast", &jBBCSmallEast, "jBBCSmallEast/I");
  jRecTree ->Branch("jBBCSmallWest", &jBBCSmallWest, "jBBCSmallWest/I");
  jRecTree ->Branch("jBBCLargeEast", &jBBCLargeEast, "jBBCLargeEast/I");
  jRecTree ->Branch("jBBCLargeWest", &jBBCLargeWest, "jBBCLargeWest/I");
  jRecTree ->Branch("jZDCUnAttEast", &jZDCUnAttEast, "jZDCUnAttEast/I");
  jRecTree ->Branch("jZDCUnAttWest", &jZDCUnAttWest, "jZDCUnAttWest/I");
  jRecTree ->Branch("jTOFMult", &jTOFMult, "jTOFMult/I");
  jRecTree ->Branch("jVPDSumEast", &jVPDSumEast, "jVPDSumEast/I");
  jRecTree ->Branch("jVPDSumWest", &jVPDSumWest, "jVPDSumWest/I");
  jRecTree ->Branch("jZDCVtxZ", &jZDCVtxZ, "jZDCVtxZ/D");

  jRecTree ->Branch("jT0pT", &jT0pT, "jT0pT/D");
  jRecTree ->Branch("jT0eta", &jT0eta, "jT0eta/D");
  jRecTree ->Branch("jT0phi", &jT0phi, "jT0phi/D");
  jRecTree ->Branch("jT1pT", &jT1pT, "jT1pT/D");
  jRecTree ->Branch("jT1eta", &jT1eta, "jT1eta/D");
  jRecTree ->Branch("jT1phi", &jT1phi, "jT1phi/D");
  jRecTree ->Branch("jT0sigEl", &jT0sigEl, "jT0sigEl/D");
  jRecTree ->Branch("jT1sigEl", &jT1sigEl, "jT1sigEl/D");
  jRecTree ->Branch("jT0dEdxSig", &jT0dEdxSig, "jT0dEdxSig/D");
  jRecTree ->Branch("jT1dEdxSig", &jT1dEdxSig, "jT1dEdxSig/D");
  jRecTree ->Branch("jT0beta", &jT0beta, "jT0beta/D");
  jRecTree ->Branch("jT1beta", &jT1beta, "jT1beta/D");

  jRecTree ->Branch("jVtxX", &jVtxX, "jVtxX/D");
  jRecTree ->Branch("jVtxY", &jVtxY, "jVtxY/D");
  jRecTree ->Branch("jVtxZ", &jVtxZ, "jVtxZ/D");
  jRecTree ->Branch("jNPrimInVtx", &jNPrimInVtx, "jNPrimInVtx/I");
  jRecTree ->Branch("jNPrimVtxUsed", &jNPrimVtxUsed, "jNPrimVtxUsed/I");

  jRecTree ->Branch("jT0dcaXY", &jT0dcaXY, "jT0dcaXY/D");
  jRecTree ->Branch("jT0dcaZ", &jT0dcaZ, "jT0dcaZ/D");
  jRecTree ->Branch("jT1dcaXY", &jT1dcaXY, "jT1dcaXY/D");
  jRecTree ->Branch("jT1dcaZ", &jT1dcaZ, "jT1dcaZ/D");

  jRecTree ->Branch("jT0chi2", &jT0chi2, "jT0chi2/D");
  jRecTree ->Branch("jT1chi2", &jT1chi2, "jT1chi2/D");

  jRecTree ->Branch("jT0matchTof", &jT0matchTof, "jT0matchTof/O");
  jRecTree ->Branch("jT1matchTof", &jT1matchTof, "jT1matchTof/O");

  jRecTree ->Branch("jT0charge", &jT0charge, "jT0charge/I");
  jRecTree ->Branch("jT1charge", &jT1charge, "jT1charge/I");
  jRecTree ->Branch("jT0nHits", &jT0nHits, "jT0nHits/I");
  jRecTree ->Branch("jT1nHits", &jT1nHits, "jT1nHits/I");
  jRecTree ->Branch("jT0nHitsFit", &jT0nHitsFit, "jT0nHitsFit/I");
  jRecTree ->Branch("jT1nHitsFit", &jT1nHitsFit, "jT1nHitsFit/I");

  //selection criteria in output reconstructed tree
  jRecTree ->Branch("sign", &sign, "sign/I");
  jRecTree ->Branch("minNhits", &minNhits, "minNhits/I");
  jRecTree ->Branch("maxAbsEta", &maxAbsEta, "maxAbsEta/D");
  jRecTree ->Branch("maxNsigPID", &maxNsigPID, "maxNsigPID/D");
  jRecTree ->Branch("matchTof", &matchTof, "matchTof/O");
  jRecTree ->Branch("maxAbsZvtx", &maxAbsZvtx, "maxAbsZvtx/D");
  jRecTree ->Branch("pairSel", &pairSel, "pairSel/I");
  jRecTree ->Branch("maxNPrim", &maxNPrim, "maxNPrim/I");

  return outfile;

}//CreateOutputTree

//_____________________________________________________________________________
void Init() {

  hEvtCount = new TH1I("hEvtCount", "hEvtCount", kMaxCnt-1, 1, kMaxCnt); // selection statistics
  trackMass = TDatabasePDG::Instance()->GetParticle( 11 )->Mass(); // track electron mass from PDG
  RunTracks[kV0] = RunTracksV0;
  hMass = new THB1D("hMass", "hMass", 70, 0.1, 4.);

}//Init

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

  TList *hlist=0x0;
  TH1I *mCounter=0x0;

  //infile present
  if(infile) {
    //take histograms container from input file
    hlist = dynamic_cast<TList*>( infile->Get("HistList") );
    //retrieve the analysis counter:
    mCounter = dynamic_cast<TH1I*>( hlist->FindObject("mCounter") ); // counter from upc trees
  }//infile present

  stringstream st;
  //input and output
  st.width(8); st << left << "Input:" << innam << endl << endl;
  st.width(8); st << left << "Output:" << outnam << endl << endl;
  //analysis counter
  st << "---------------------" << endl;
  if(mCounter) {
    st << Form("Analyzed:   %.0f", mCounter->GetBinContent( kAna )) << endl;
    st << Form("Triggers:   %.0f", mCounter->GetBinContent( kTrg )) << endl;
    st << Form("DatBEMC:    %.0f", mCounter->GetBinContent( kDatBEMC )) << endl;
    st << Form("Written:    %.0f", mCounter->GetBinContent( kWritten )) << endl;
    st << "---------------------" << endl;
  }
  //local counter
  st << Form("Local ana:  %.0f", hEvtCount->GetBinContent( kAnaL )) << endl;
  st << Form("Pair:       %.0f", hEvtCount->GetBinContent( kPair )) << endl;
  st << Form("Same vtx:   %.0f", hEvtCount->GetBinContent( kVtxId )) << endl;
  st << Form("PID el:     %.0f", hEvtCount->GetBinContent( kPID )) << endl;
  st << Form("ZVtx:       %.0f", hEvtCount->GetBinContent( kZvtx )) << endl;
  st << Form("Sign:       %.0f", hEvtCount->GetBinContent( kSign )) << endl;
  st << "---------------------" << endl;
  //mass histogram
  st << hMass;

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
void ShowProggress(Double_t xi, Double_t xall, const string& in, const string& out) {

  if( xall < 0.1 ) return;
  if( xi > xall ) return;

  cout << endl;
  cout.width(10);
  cout << "Input: " << in << endl;
  cout.width(10);
  cout << "Output: " << out << endl;

  struct winsize size;
  ioctl(STDOUT_FILENO, TIOCGWINSZ, &size);
  hMass->SetTotalHeight( size.ws_row-3 ); // full terminal is size.ws_row-1

  //print mass histogram
  cout << hMass;

  //print proggress bar
  Int_t pbar = 35;

  Double_t prog = xi/xall;
  Int_t pos = prog*pbar;

  string pdone = "\u2588"; //full block
  string phead = "\u2591"; //light shade
  string prem = "\u2591"; //light shade
  cout << " [";
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
  //cout << "] " << Form("%.1f", prog*100.)<<" %\r";
  cout << Form("] %.1f", prog*100.)<<" %\r";
  cout.flush();

  // std::cout<<"Event: "<<i<<"\r"; std::cout.flush();

}//ShowProggress




















