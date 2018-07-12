
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
#include "StUPCTrgData.h"
#include "StUPCTrack.h"
#include "StUPCBemcCluster.h"
#include "StUPCVertex.h"
#include "THB1D.h"

using namespace std;

//output trees
TTree *jRecTree;
Int_t jBBCSmallEast, jBBCSmallWest, jBBCLargeEast, jBBCLargeWest;
Int_t jZDCUnAttEast, jZDCUnAttWest, jTOFMult, jBEMCMult;

//trigger IDs, same as in StUPCFilterMaker.h
enum {kUPCJpsiB_1=0, kUPCJpsiB_2, kUPCmain_1, kUPCmain_2, kZero_bias};

//analysis variables
TFile *infile;
TChain *inchain;
StUPCEvent *upcEvt;

//functions
void FillRecTree();
void Init();
TTree *ConnectInput(const string& in);
TFile *CreateOutputTree(const string& out);

//_____________________________________________________________________________
int main(void) {

  string basedir = "/home/jaroslav/analyza/StUPCLib/ver2/"; // local
  //string basedir = "/home/tmp/jaroslav/"; // rcf

  string in = "trees/muDst_run4/StUPC_muDst_run4_all.root";

  string out = "bin/output.root";
  //string out = "output.root";

  //input
  TTree *upcTree = ConnectInput(basedir+in);
  if(!upcTree) {cout << "No input." << endl; return 1;}

  //output
  TFile *outfile = CreateOutputTree(basedir+out);
  if(!outfile) {cout << "Can not open output file." << endl; return -1;}

  //analysis init
  Init();

  Long64_t nev = upcTree->GetEntries();
  cout << "Starting the analysis, events: " << nev << endl;
  cout<<"Input:   "<<in<<endl;
  cout<<"Output:  "<<out<<endl;

  clock_t cdelta = CLOCKS_PER_SEC*2; //clock ticks per given number of seconds
  clock_t ctim = clock();
  //event loop
  for(Long64_t iev=0; iev<nev; iev++) {
    if( (clock()-ctim) > cdelta ) {
      cout << "iev: " << iev << endl;
      ctim = clock();
    }

    //get the event
    upcTree->GetEntry(iev);

    //trigger
    if( !upcEvt->getTrigger(kZero_bias) ) continue;

    FillRecTree();

  }//event loop

  //write the outputs
  jRecTree->Write();
  outfile->Close();
  if(infile) infile->Close();

  return 0;

}//main

//_____________________________________________________________________________
void FillRecTree() {

  jBBCSmallEast = (Int_t) upcEvt->getBBCSmallEast();
  jBBCSmallWest = (Int_t) upcEvt->getBBCSmallWest();
  jBBCLargeEast = (Int_t) upcEvt->getBBCLargeEast();
  jBBCLargeWest = (Int_t) upcEvt->getBBCLargeWest();

  jZDCUnAttEast = (Int_t) upcEvt->getZDCUnAttEast();
  jZDCUnAttWest = (Int_t) upcEvt->getZDCUnAttWest();

  jTOFMult = (Int_t) upcEvt->getTOFMultiplicity();
  jBEMCMult = (Int_t) upcEvt->getBEMCMultiplicity();

  jRecTree->Fill();

}//FillRecTree

//_____________________________________________________________________________
TFile *CreateOutputTree(const string& out) {

  TFile *outfile = TFile::Open(out.c_str(), "recreate");
  if(!outfile) return 0x0;

  //standard reconstructed tree
  jRecTree = new TTree("jRecTree", "jRecTree");

  jRecTree ->Branch("jBBCSmallEast", &jBBCSmallEast, "jBBCSmallEast/I");
  jRecTree ->Branch("jBBCSmallWest", &jBBCSmallWest, "jBBCSmallWest/I");
  jRecTree ->Branch("jBBCLargeEast", &jBBCLargeEast, "jBBCLargeEast/I");
  jRecTree ->Branch("jBBCLargeWest", &jBBCLargeWest, "jBBCLargeWest/I");

  jRecTree ->Branch("jZDCUnAttEast", &jZDCUnAttEast, "jZDCUnAttEast/I");
  jRecTree ->Branch("jZDCUnAttWest", &jZDCUnAttWest, "jZDCUnAttWest/I");
  jRecTree ->Branch("jTOFMult", &jTOFMult, "jTOFMult/I");
  jRecTree ->Branch("jBEMCMult", &jBEMCMult, "jBEMCMult/I");

  return outfile;

}//CreateOutputTree

//_____________________________________________________________________________
void Init() {

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
  //isMC = upcEvt->getIsMC(); // MC or data

  return upcTree;

}//ConnectInput



