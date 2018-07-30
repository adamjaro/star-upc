
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

using namespace std;

//output trees
TTree *jRecTree, *jAllTree;
Double_t jRecPt, jRecPt2, jRecY, jRecM;
Double_t jT0Deta, jT0Dphi, jT1Deta, jT1Dphi;
Int_t jBBCSmallEast, jBBCSmallWest, jBBCLargeEast, jBBCLargeWest;
Int_t jBbcSEc, jBbcSWc, jBbcLEc, jBbcLWc;
Int_t jZDCUnAttEast, jZDCUnAttWest, jTOFMult, jBEMCMult;
Double_t jT0pT, jT0eta, jT0phi, jT1pT, jT1eta, jT1phi, jT0eng, jT1eng;
Double_t jT0sigEl, jT1sigEl, jDeltaPhi;
Double_t jT0dEdxSig, jT1dEdxSig, jT0beta, jT1beta;
Double_t jT0phiBemc, jT1phiBemc, jDeltaPhiBemc;
Double_t jVtxX, jVtxY, jVtxZ;
Double_t jT0chi2, jT1chi2;
Double_t jT0bemcE, jT1bemcE, jT0bemcP, jT1bemcP;
Double_t jT0pTBemc, jT1pTBemc, jT0etaBemc, jT1etaBemc;
Bool_t jT0matchBemc, jT1matchBemc, jT0matchTof, jT1matchTof;
Double_t jT0bemcHitE, jT1bemcHitE, jT0EnAtBemc, jT1EnAtBemc;
Int_t jT0charge, jT1charge, jT0nHits, jT1nHits, jT0nHitsFit, jT1nHitsFit;

TTree *jGenTree;
Double_t jGenPt, jGenPt2, jGenM, jGenY;
Double_t jGenP0pT, jGenP0eta, jGenP0phi, jGenP1pT, jGenP1eta, jGenP1phi;

const Double_t kUdf=-9.e9;//default for undefined

//selection criteria
Short_t sign;
UShort_t minNhits;
Double_t maxAbsEta, maxNsigPID;
Bool_t matchBemc, matchTof, projBemc;
Bool_t useBemcEff;
Double_t minDphiBemc;
Float_t maxAbsZvtx;
Double_t maxAbsY;
const Int_t npairSel=2;
enum {kV0=0, kV1};
Int_t pairSel;

//trigger IDs, same as in StUPCFilterMaker.h
enum {kUPCJpsiB_1=0, kUPCJpsiB_2, kUPCmain_1, kUPCmain_2, kZero_bias};

//analysis variables
TFile *infile;
TChain *inchain;
Double_t *parEffBemc;
TRandom3 *rand3;
StUPCEvent *upcEvt;
Bool_t isMC;
Double_t trackMass;
Bool_t (*RunTracks[npairSel])(StUPCTrack *pair[]); // pointers to pair selection functions
TH1I *hEvtCount, *hGenCount, *hTrkCount;
enum{kAnaL=1, kPair, kVtxId, kDphiBemc, kPID, kZvtx, kRap, kSign, kFin, kUPCJpsiB, kMaxCnt};
enum EvtCount{ kAna=1, kTrg, kDatBEMC, kWritten }; // counter from StUPCFilterMaker.h
enum GenCount{ kGenAll=1, kGenSel, kMaxCntGen }; // MC generated counter
enum TrkCount{ kTrkAll=1, kBemc, kTof, kMaxTrkCnt }; // track counter
TH1I *hAnaPerRun, *hSelPerRun;
THB1D *hMass;
Bool_t makeAllTree=0;

//functions
Bool_t RunTracksV0(StUPCTrack *pair[]);
Bool_t RunTracksV1(StUPCTrack *pair[]);
inline Bool_t selectTrack(const StUPCTrack *trk);
Double_t fitFuncErf(Double_t xVal, Double_t *par);
Bool_t RunMC();
void FillRecTree(StUPCTrack *pair[], const TLorentzVector &vpair, const TLorentzVector &v0, const TLorentzVector &v1);
void FillAllTree();
void SortTracks(StUPCTrack *pair[]);
Double_t GetDeltaPhi(Double_t phi0, Double_t phi1);
void Init();
TTree *ConnectInput(const string& in);
TFile *CreateOutputTree(const string& out);
void PrintStat(ostream& out, const string& innam, const string& outnam, Int_t lmg=4);
void ShowProggress(Double_t xi, Double_t xall, const string& in, const string& out);

//_____________________________________________________________________________
int main(void) {

  //string basedir = "/home/jaroslav/analyza/star-upc/"; // local
  string basedir = "/home/tmp/jaroslav/"; // rcf

  //string in = "trees/StUPC.root";
  //string in = "trees/muDst_run0/StUPC_muDst_run0_all.root";
  string in = "StUPC_muDst_dev1_all.root";
  //string in = "trees/test/StUPC_slight14b2_test1.root";
  //string in = "trees/starsim/slight14b/StUPC_slight14b2.root";

  //string out = "build/output.root";
  string out = "output.root";
  //string out = "sel/starsim/sel3/ana_slight14b2_sel3.root";

  //selection criteria
  sign = -1;            // sign of dilepton pair, -1: unlike-sign, +1: like-sign, 0: no sign selection
  pairSel = kV0;        // pair selection version, kV0: already same vertex, kV1: pair and then vertex
  minNhits = 14;        // min number of track hits
  maxAbsEta = 1.;       // max track pseudorapidity, absolute value
  maxNsigPID = 3;       // max number of sigmas for TPC dE/dx PID
  matchBemc = 1;        // track - BEMC matching, 1: required, 0: not required
  matchTof = 0;         // track - TOF matching, 1: required, 0: not required
  projBemc = 1;         // projection to BEMC, 1: required, 0: not required, redundant with matchBemc
  useBemcEff = 0;       // use BEMC matching efficiency from file
  minDphiBemc = 2.618;  // minimal tracks opening angle at BEMC
  maxAbsZvtx = 50.;    // maximal Z position of vertex, absolute value
  maxAbsY = 1.;         // maximal pair rapidity, absolute value

  //overrides to the criteria
  //sign = 1;
  maxNsigPID = 9999.;
  //matchTof = 1;
  //matchBemc = 0;
  //useBemcEff = 1;
  //maxAbsEta = 9.e9;

  //bemc efficiency
  //Double_t epar[] = {0.411, 1.206, 0.241, 0.0009}; // slight14b1_sel2b
  //Double_t epar[] = {0.455, 1.021, 0.328, -0.041}; // conv_sel0, run1, ptot
  Double_t epar[] = {0.423, 1.011, 0.275, -0.015}; // conv/sel0, run3, ptot
  parEffBemc = epar;

  //flag to write all triggers tree
  //makeAllTree = kTRUE;


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

  clock_t cdelta = CLOCKS_PER_SEC*0.5; //clock ticks per 0.5 sec
  clock_t ctim = clock();
  //event loop
  for(Long64_t iev=0; iev<nev; iev++) {
    if( (clock()-ctim) > cdelta ) {
      ShowProggress(iev, nev, in, out);
      ctim = clock();
    }

    //get the event
    upcTree->GetEntry(iev);

    if(isMC) RunMC(); // MC

    //trigger
    if( !isMC && !upcEvt->getTrigger(kUPCJpsiB_1) && !upcEvt->getTrigger(kUPCJpsiB_2) ) continue;
    //if( !isMC && !upcEvt->getTrigger(kZero_bias) ) continue;
    //if( !isMC && !upcEvt->getTrigger(kUPCmain_1) && !upcEvt->getTrigger(kUPCmain_2) ) continue;
    hEvtCount->Fill( kAnaL );
    if( makeAllTree ) FillAllTree();

    //analyzed events per run
    Int_t runnum = upcEvt->getRunNumber();
    hAnaPerRun->Fill( runnum );

    //bbc large tiles
    //if( upcEvt->getBBCLargeEast() > 10 || upcEvt->getBBCLargeWest() > 10 ) continue;

    //tracks
    StUPCTrack *pair[2] = {0,0};
    if( !(*RunTracks[pairSel])(pair) ) continue;

    SortTracks(pair); //put positive track first

    //opening angle at BEMC
    if( GetDeltaPhi(pair[0]->getBemcPhi(), pair[1]->getBemcPhi()) < minDphiBemc ) continue;
    hEvtCount->Fill( kDphiBemc );

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
    if( TMath::Abs( vpair.Rapidity() ) > maxAbsY ) continue;
    hEvtCount->Fill( kRap );

    //sign selection
    Short_t qTrk0 = pair[0]->getCharge();
    Short_t qTrk1 = pair[1]->getCharge();
    if( qTrk0*qTrk1*sign < 0 ) continue;
    hEvtCount->Fill( kSign );

    //event selected

    //selected events per run
    hSelPerRun->Fill( runnum );

    //fill output tree
    FillRecTree(pair, vpair, v0, v1);

    //J/psi mass
    if( vpair.M() > 2.9 && vpair.M() < 3.2 ) {
      hEvtCount->Fill( kFin );
    }

    //for trigger efficiency using UPC-main
    if( upcEvt->getTrigger(kUPCJpsiB_1) || upcEvt->getTrigger(kUPCJpsiB_2) ) {
      hEvtCount->Fill( kUPCJpsiB );
    }

  }//event loop

  hMass->SetTotalHeight( hMass->GetTotalHeight()-1 );
  ShowProggress(nev, nev, in, out);
  cout << endl;
  ofstream out1("out.txt");
  PrintStat(out1, in, out, 6);

  //cout << hMass;

  //write the outputs
  jRecTree->Write();
  jAllTree->Write();
  if( isMC ) jGenTree->Write();
  hEvtCount->Write();
  hGenCount->Write();
  hTrkCount->Write();
  hAnaPerRun->Write();
  hSelPerRun->Write();
  outfile->Close();
  if(infile) infile->Close();
  //infileBemc->Close();

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
Bool_t RunTracksV1(StUPCTrack *pair[]) {

  // pair algorighm version 1
  //
  // find pair of tracks and after that require same vertex for both tracks

  Int_t ncen = 0;
  UInt_t vtxId[2];

  Int_t ntrk = upcEvt->getNumberOfTracks();
  //tracks loop
  for(Int_t i=0; i<ntrk; i++) {
    StUPCTrack *trk = upcEvt->getTrack(i);
    if(!trk) continue;

    if( !selectTrack(trk) ) continue;

    //track accepted

    if(ncen+1 > 2) {ncen++; break;}

    //vertex ID and pointer to track
    vtxId[ncen] = trk->getVertexId();
    pair[ncen] = trk;

    ncen++;
  }//tracks loop

  //one pair
  if( ncen != 2) return kFALSE;
  hEvtCount->Fill( kPair );

  //same vertex
  if( vtxId[0] != vtxId[1] ) return kFALSE;
  hEvtCount->Fill( kVtxId );

  return kTRUE;

}//RunTracksV1

//_____________________________________________________________________________
inline Bool_t selectTrack(const StUPCTrack *trk) {

  hTrkCount->Fill( kTrkAll );

  //BEMC match
  if( matchBemc && !trk->getFlag( StUPCTrack::kBemc ) ) return kFALSE;
  hTrkCount->Fill( kBemc );

  //TOF match
  Bool_t isTof = trk->getFlag( StUPCTrack::kTof );
  if(isTof) hTrkCount->Fill( kTof );
  if( matchTof && !isTof ) return kFALSE;

  //BEMC projection
  if( projBemc && !trk->getFlag( StUPCTrack::kBemcProj ) ) return kFALSE;

  //BEMC eff from parametrization
  if( useBemcEff ) {
    Double_t ranval = rand3->Rndm();
    //Double_t ptval = trk->getBemcPt();
    Double_t pval = trk->getBemcPmag();
    Double_t effval = fitFuncErf(pval, parEffBemc);
    //cout << ptval << " " << effval << " " << (effval < ranval) << endl;
    if( effval < ranval ) return kFALSE;
  }

  //min hits in TPC
  if( trk->getNhits() < minNhits ) return kFALSE;

  //max |eta|
  if( TMath::Abs( trk->getEta() ) > maxAbsEta ) return kFALSE;

  return kTRUE;

}//selectTrack

//_____________________________________________________________________________
Double_t fitFuncErf(Double_t xVal, Double_t *par) {

  return par[3]+par[0]*(1.+TMath::Erf((xVal-par[1])/par[2]/TMath::Sqrt(2.)));
}

//_____________________________________________________________________________
Bool_t RunMC() {

  //MC particles
  hGenCount->Fill( kGenAll );

  //reset tree variables
  jGenP0pT=kUdf; jGenP0eta=kUdf; jGenP0phi=kUdf;
  jGenP1pT=kUdf; jGenP1eta=kUdf; jGenP1phi=kUdf;
  jGenPt=kUdf; jGenPt2=kUdf; jGenM=kUdf; jGenY=kUdf;

  //generated dilepton
  TLorentzVector vgen;

  //if( upcEvt->getNumberOfMCParticles() != 2 ) return kTRUE;

  //cout << "#########" << endl;

  //mc loop
  for(Int_t imc=0; imc<upcEvt->getNumberOfMCParticles(); imc++) {
    TParticle *mcp = upcEvt->getMCParticle(imc);
    if(!mcp) continue;

    //cout << mcp->GetPdgCode() << endl;

    //consider only first two MC particles to prevent GEANT-created
    //electrons
    if( imc > 1 ) break;

    //positive particle first
    if( mcp->GetPDG()->Charge() > 0. ) {
      jGenP0pT = mcp->Pt();
      jGenP0eta = mcp->Eta();
      jGenP0phi = mcp->Phi();
    } else {
      //negative particle
      jGenP1pT = mcp->Pt();
      jGenP1eta = mcp->Eta();
      jGenP1phi = mcp->Phi();
    }

    //generated dilepton
    TLorentzVector vpart;
    vpart.SetXYZM(mcp->Px(),mcp->Py(),mcp->Pz(),mcp->GetMass());

    vgen += vpart;

  }//mc loop

  jGenPt = vgen.Pt();
  jGenPt2 = jGenPt*jGenPt;
  jGenM = vgen.M();
  jGenY = vgen.Rapidity();

  //rapidity selection for MC
  if( TMath::Abs(jGenY) > maxAbsY ) return kFALSE;

  //MC event selected
  jGenTree->Fill();
  hGenCount->Fill( kGenSel );

  return kTRUE;

}//RunMC

//_____________________________________________________________________________
void FillRecTree(StUPCTrack *pair[], const TLorentzVector &vpair, const TLorentzVector &v0, const TLorentzVector &v1) {

  jRecPt = vpair.Pt();
  jRecPt2 = jRecPt*jRecPt;
  jRecY  = vpair.Rapidity();
  jRecM  = vpair.M();

  hMass->Fill(jRecM);

  //tracks and BEMC clusters matching
  StUPCBemcCluster *cls0 = pair[0]->getBemcCluster();
  StUPCBemcCluster *cls1 = pair[1]->getBemcCluster();
  // reset tree vars for case of no clusters
  jT0Deta=kUdf; jT0Dphi=kUdf; jT1Deta=kUdf; jT1Dphi=kUdf;
  if( cls0 && cls1 ) {
    jT0Deta = cls0->getEta() - pair[0]->getBemcEta();
    jT0Dphi = cls0->getPhi() - pair[0]->getBemcPhi();
    jT1Deta = cls1->getEta() - pair[1]->getBemcEta();
    jT1Dphi = cls1->getPhi() - pair[1]->getBemcPhi();
  }

  jBBCSmallEast = (Int_t) upcEvt->getBBCSmallEast();
  jBBCSmallWest = (Int_t) upcEvt->getBBCSmallWest();
  jBBCLargeEast = (Int_t) upcEvt->getBBCLargeEast();
  jBBCLargeWest = (Int_t) upcEvt->getBBCLargeWest();

  jZDCUnAttEast = (Int_t) upcEvt->getZDCUnAttEast();
  jZDCUnAttWest = (Int_t) upcEvt->getZDCUnAttWest();

  jTOFMult = (Int_t) upcEvt->getTOFMultiplicity();
  jBEMCMult = (Int_t) upcEvt->getBEMCMultiplicity();

  //tracks kinematics
  jT0pT       = pair[0]->getPt();
  jT0eta      = pair[0]->getEta();
  jT0phi      = pair[0]->getPhi();
  jT1pT       = pair[1]->getPt();
  jT1eta      = pair[1]->getEta();
  jT1phi      = pair[1]->getPhi();
  jT0sigEl    = pair[0]->getNSigmasTPCElectron();
  jT1sigEl    = pair[1]->getNSigmasTPCElectron();
  //tracks opening angle defined as delta phi < pi, inner angle between the tracks
  jDeltaPhi = GetDeltaPhi(jT0phi, jT1phi);
  //tracks pT, eta and azimuthal angle at BEMC position
  pair[0]->getBemcPtEtaPhi(jT0pTBemc, jT0etaBemc, jT0phiBemc);
  pair[1]->getBemcPtEtaPhi(jT1pTBemc, jT1etaBemc, jT1phiBemc);
  //tracks opening angle at BEMC position
  jDeltaPhiBemc = GetDeltaPhi(jT0phiBemc, jT1phiBemc);
  //tracks energy
  jT0eng = v0.Energy();
  jT1eng = v1.Energy();

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

  //tracks Chi^2
  jT0chi2 = pair[0]->getChi2();
  jT1chi2 = pair[1]->getChi2();

  //tracks BEMC energy and momentum at BEMC
  // reset tree vars for case of no clusters
  jT0bemcE=kUdf; jT1bemcE=kUdf;
  if( cls0 && cls1 ) {
    jT0bemcE = cls0->getEnergy();
    jT1bemcE = cls1->getEnergy();
  }
  TVector3 v0b, v1b;
  v0b.SetPtEtaPhi(pair[0]->getBemcPt(), pair[0]->getBemcEta(), pair[0]->getBemcPhi());
  v1b.SetPtEtaPhi(pair[1]->getBemcPt(), pair[1]->getBemcEta(), pair[1]->getBemcPhi());
  jT0bemcP = v0b.Mag();
  jT1bemcP = v1b.Mag();

  //BEMC match
  jT0matchBemc = pair[0]->getFlag( StUPCTrack::kBemc );
  jT1matchBemc = pair[1]->getFlag( StUPCTrack::kBemc );

  //BEMC energy of matched hit
  jT0bemcHitE = pair[0]->getBemcHitE();
  jT1bemcHitE = pair[1]->getBemcHitE();

  //track energy at BEMC
  jT0EnAtBemc = kUdf;
  jT1EnAtBemc = kUdf;
  if( pair[0]->getFlag( StUPCTrack::kBemcProj ) ) {
    TLorentzVector bv0;
    pair[0]->getBemcLorentzVector(bv0, trackMass);
    jT0EnAtBemc = bv0.E();
  }
  if( pair[1]->getFlag( StUPCTrack::kBemcProj ) ) {
    TLorentzVector bv1;
    pair[1]->getBemcLorentzVector(bv1, trackMass);
    jT1EnAtBemc = bv1.E();
  }

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
void FillAllTree() {

  //fills all trigger tree

  jZDCUnAttEast = (Int_t) upcEvt->getZDCUnAttEast();
  jZDCUnAttWest = (Int_t) upcEvt->getZDCUnAttWest();

  jBBCSmallEast = (Int_t) upcEvt->getBBCSmallEast();
  jBBCSmallWest = (Int_t) upcEvt->getBBCSmallWest();
  jBBCLargeEast = (Int_t) upcEvt->getBBCLargeEast();
  jBBCLargeWest = (Int_t) upcEvt->getBBCLargeWest();

  jTOFMult = (Int_t) upcEvt->getTOFMultiplicity();
  jBEMCMult = (Int_t) upcEvt->getBEMCMultiplicity();

  jAllTree->Fill();

}//FillAllTree

//_____________________________________________________________________________
TFile *CreateOutputTree(const string& out) {

  TFile *outfile = TFile::Open(out.c_str(), "recreate");
  if(!outfile) return 0x0;

  //standard reconstructed tree
  jRecTree = new TTree("jRecTree", "jRecTree");

  jRecTree ->Branch("jRecPt", &jRecPt, "jRecPt/D");
  jRecTree ->Branch("jRecPt2", &jRecPt2, "jRecPt2/D");
  jRecTree ->Branch("jRecY", &jRecY, "jRecY/D");
  jRecTree ->Branch("jRecM", &jRecM, "jRecM/D");
  jRecTree ->Branch("jT0Deta", &jT0Deta, "jT0Deta/D");
  jRecTree ->Branch("jT0Dphi", &jT0Dphi, "jT0Dphi/D");
  jRecTree ->Branch("jT1Deta", &jT1Deta, "jT1Deta/D");
  jRecTree ->Branch("jT1Dphi", &jT1Dphi, "jT1Dphi/D");

  jRecTree ->Branch("jBBCSmallEast", &jBBCSmallEast, "jBBCSmallEast/I");
  jRecTree ->Branch("jBBCSmallWest", &jBBCSmallWest, "jBBCSmallWest/I");
  jRecTree ->Branch("jBBCLargeEast", &jBBCLargeEast, "jBBCLargeEast/I");
  jRecTree ->Branch("jBBCLargeWest", &jBBCLargeWest, "jBBCLargeWest/I");
  jRecTree ->Branch("jBbcSEc", &jBbcSEc, "jBbcSEc/I");
  jRecTree ->Branch("jBbcSWc", &jBbcSWc, "jBbcSWc/I");
  jRecTree ->Branch("jBbcLEc", &jBbcLEc, "jBbcLEc/I");
  jRecTree ->Branch("jBbcLWc", &jBbcLWc, "jBbcLWc/I");
  jRecTree ->Branch("jZDCUnAttEast", &jZDCUnAttEast, "jZDCUnAttEast/I");
  jRecTree ->Branch("jZDCUnAttWest", &jZDCUnAttWest, "jZDCUnAttWest/I");
  jRecTree ->Branch("jTOFMult", &jTOFMult, "jTOFMult/I");
  jRecTree ->Branch("jBEMCMult", &jBEMCMult, "jBEMCMult/I");

  jRecTree ->Branch("jT0pT", &jT0pT, "jT0pT/D");
  jRecTree ->Branch("jT0eta", &jT0eta, "jT0eta/D");
  jRecTree ->Branch("jT0phi", &jT0phi, "jT0phi/D");
  jRecTree ->Branch("jT1pT", &jT1pT, "jT1pT/D");
  jRecTree ->Branch("jT1eta", &jT1eta, "jT1eta/D");
  jRecTree ->Branch("jT1phi", &jT1phi, "jT1phi/D");
  jRecTree ->Branch("jT0eng", &jT0eng, "jT0eng/D");
  jRecTree ->Branch("jT1eng", &jT1eng, "jT1eng/D");
  jRecTree ->Branch("jDeltaPhi", &jDeltaPhi, "jDeltaPhi/D");
  jRecTree ->Branch("jT0phiBemc", &jT0phiBemc, "jT0phiBemc/D");
  jRecTree ->Branch("jT1phiBemc", &jT1phiBemc, "jT1phiBemc/D");
  jRecTree ->Branch("jDeltaPhiBemc", &jDeltaPhiBemc, "jDeltaPhiBemc/D");
  jRecTree ->Branch("jT0sigEl", &jT0sigEl, "jT0sigEl/D");
  jRecTree ->Branch("jT1sigEl", &jT1sigEl, "jT1sigEl/D");
  jRecTree ->Branch("jT0dEdxSig", &jT0dEdxSig, "jT0dEdxSig/D");
  jRecTree ->Branch("jT1dEdxSig", &jT1dEdxSig, "jT1dEdxSig/D");
  jRecTree ->Branch("jT0beta", &jT0beta, "jT0beta/D");
  jRecTree ->Branch("jT1beta", &jT1beta, "jT1beta/D");

  jRecTree ->Branch("jVtxX", &jVtxX, "jVtxX/D");
  jRecTree ->Branch("jVtxY", &jVtxY, "jVtxY/D");
  jRecTree ->Branch("jVtxZ", &jVtxZ, "jVtxZ/D");

  jRecTree ->Branch("jT0chi2", &jT0chi2, "jT0chi2/D");
  jRecTree ->Branch("jT1chi2", &jT1chi2, "jT1chi2/D");
  jRecTree ->Branch("jT0bemcE", &jT0bemcE, "jT0bemcE/D");
  jRecTree ->Branch("jT1bemcE", &jT1bemcE, "jT1bemcE/D");
  jRecTree ->Branch("jT0bemcP", &jT0bemcP, "jT0bemcP/D");
  jRecTree ->Branch("jT1bemcP", &jT1bemcP, "jT1bemcP/D");
  jRecTree ->Branch("jT0pTBemc", &jT0pTBemc, "jT0pTBemc/D");
  jRecTree ->Branch("jT1pTBemc", &jT1pTBemc, "jT1pTBemc/D");
  jRecTree ->Branch("jT0etaBemc", &jT0etaBemc, "jT0etaBemc/D");
  jRecTree ->Branch("jT1etaBemc", &jT1etaBemc, "jT1etaBemc/D");
  jRecTree ->Branch("jT0matchBemc", &jT0matchBemc, "jT0matchBemc/O");
  jRecTree ->Branch("jT1matchBemc", &jT1matchBemc, "jT1matchBemc/O");
  jRecTree ->Branch("jT0bemcHitE", &jT0bemcHitE, "jT0bemcHitE/D");
  jRecTree ->Branch("jT1bemcHitE", &jT1bemcHitE, "jT1bemcHitE/D");
  jRecTree ->Branch("jT0EnAtBemc", &jT0EnAtBemc, "jT0EnAtBemc/D");
  jRecTree ->Branch("jT1EnAtBemc", &jT1EnAtBemc, "jT1EnAtBemc/D");
  jRecTree ->Branch("jT0matchTof", &jT0matchTof, "jT0matchTof/O");
  jRecTree ->Branch("jT1matchTof", &jT1matchTof, "jT1matchTof/O");

  jRecTree ->Branch("jT0charge", &jT0charge, "jT0charge/I");
  jRecTree ->Branch("jT1charge", &jT1charge, "jT1charge/I");
  jRecTree ->Branch("jT0nHits", &jT0nHits, "jT0nHits/I");
  jRecTree ->Branch("jT1nHits", &jT1nHits, "jT1nHits/I");
  jRecTree ->Branch("jT0nHitsFit", &jT0nHitsFit, "jT0nHitsFit/I");
  jRecTree ->Branch("jT1nHitsFit", &jT1nHitsFit, "jT1nHitsFit/I");

  //MC in reconstructed tree
  if( isMC ) {
    jRecTree ->Branch("jGenPt", &jGenPt, "jGenPt/D");
    jRecTree ->Branch("jGenPt2", &jGenPt2, "jGenPt2/D");
    jRecTree ->Branch("jGenM", &jGenM, "jGenM/D");
    jRecTree ->Branch("jGenY", &jGenY, "jGenY/D");
    jRecTree ->Branch("jGenP0pT", &jGenP0pT, "jGenP0pT/D");
    jRecTree ->Branch("jGenP0eta", &jGenP0eta, "jGenP0eta/D");
    jRecTree ->Branch("jGenP0phi", &jGenP0phi, "jGenP0phi/D");
    jRecTree ->Branch("jGenP1pT", &jGenP1pT, "jGenP1pT/D");
    jRecTree ->Branch("jGenP1eta", &jGenP1eta, "jGenP1eta/D");
    jRecTree ->Branch("jGenP1phi", &jGenP1phi, "jGenP1phi/D");
  }

  //selection criteria in output reconstructed tree
  jRecTree ->Branch("sign", &sign, "sign/S");
  jRecTree ->Branch("minNhits", &minNhits, "minNhits/s");
  jRecTree ->Branch("maxAbsEta", &maxAbsEta, "maxAbsEta/D");
  jRecTree ->Branch("maxNsigPID", &maxNsigPID, "maxNsigPID/D");
  jRecTree ->Branch("matchBemc", &matchBemc, "matchBemc/O");
  jRecTree ->Branch("matchTof", &matchTof, "matchTof/O");
  jRecTree ->Branch("projBemc", &projBemc, "projBemc/O");
  jRecTree ->Branch("useBemcEff", &useBemcEff, "useBemcEff/O");
  jRecTree ->Branch("minDphiBemc", &minDphiBemc, "minDphiBemc/D");
  jRecTree ->Branch("maxAbsZvtx", &maxAbsZvtx, "maxAbsZvtx/F");
  jRecTree ->Branch("maxAbsY", &maxAbsY, "maxAbsY/D");
  jRecTree ->Branch("pairSel", &pairSel, "pairSel/I");

  //MC generated tree
  jGenTree = new TTree("jGenTree", "jGenTree");
  if( isMC ) {
    jGenTree ->Branch("jGenPt", &jGenPt, "jGenPt/D");
    jGenTree ->Branch("jGenPt2", &jGenPt2, "jGenPt2/D");
    jGenTree ->Branch("jGenM", &jGenM, "jGenM/D");
    jGenTree ->Branch("jGenY", &jGenY, "jGenY/D");
    jGenTree ->Branch("jGenP0pT", &jGenP0pT, "jGenP0pT/D");
    jGenTree ->Branch("jGenP0eta", &jGenP0eta, "jGenP0eta/D");
    jGenTree ->Branch("jGenP0phi", &jGenP0phi, "jGenP0phi/D");
    jGenTree ->Branch("jGenP1pT", &jGenP1pT, "jGenP1pT/D");
    jGenTree ->Branch("jGenP1eta", &jGenP1eta, "jGenP1eta/D");
    jGenTree ->Branch("jGenP1phi", &jGenP1phi, "jGenP1phi/D");
  }

  //all triggers tree
  jAllTree = new TTree("jAllTree", "jAllTree");
  if( makeAllTree ) {
    jAllTree ->Branch("jZDCUnAttEast", &jZDCUnAttEast, "jZDCUnAttEast/I");
    jAllTree ->Branch("jZDCUnAttWest", &jZDCUnAttWest, "jZDCUnAttWest/I");

    jAllTree ->Branch("jBBCSmallEast", &jBBCSmallEast, "jBBCSmallEast/I");
    jAllTree ->Branch("jBBCSmallWest", &jBBCSmallWest, "jBBCSmallWest/I");
    jAllTree ->Branch("jBBCLargeEast", &jBBCLargeEast, "jBBCLargeEast/I");
    jAllTree ->Branch("jBBCLargeWest", &jBBCLargeWest, "jBBCLargeWest/I");

    jAllTree ->Branch("jTOFMult", &jTOFMult, "jTOFMult/I");
    jAllTree ->Branch("jBEMCMult", &jBEMCMult, "jBEMCMult/I");
  }

  return outfile;

}//CreateOutputTree

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
Double_t GetDeltaPhi(Double_t phi0, Double_t phi1) {

  //tracks opening angle defined as delta phi < pi, inner angle between the tracks

  if( TMath::Abs(phi1-phi0) > TMath::Pi() ) {
    return 2.*TMath::Pi() - TMath::Abs(phi0-phi1);
  } else {
    return TMath::Abs(phi1-phi0);
  }

  return 999.;

}//GetDeltaPhi

//_____________________________________________________________________________
void Init() {

  hEvtCount = new TH1I("hEvtCount", "hEvtCount", kMaxCnt-1, 1, kMaxCnt); // selection statistics
  hGenCount = new TH1I("hGenCount", "hGenCount", kMaxCntGen-1, 1, kMaxCntGen); // MC gen counter
  hTrkCount = new TH1I("hTrkCount", "hTrkCount", kMaxTrkCnt-1, 1, kMaxTrkCnt); //track counter
  trackMass = TDatabasePDG::Instance()->GetParticle( 11 )->Mass(); // track electron mass from PDG
  RunTracks[kV0] = RunTracksV0;
  RunTracks[kV1] = RunTracksV1;
  const Int_t runFirst = 15084000; // run range for counter histograms
  const Int_t runLast = 15167100;
  const Int_t runRange = runLast - runFirst;
  hAnaPerRun = new TH1I("hAnaPerRun", "hAnaPerRun", runRange, runFirst, runLast);
  hSelPerRun = new TH1I("hSelPerRun", "hSelPerRun", runRange, runFirst, runLast);
  hMass = new THB1D("hMass", "hMass", 70, 0.9, 5.);
  rand3 = new TRandom3();
  rand3->SetSeed(5572323);

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
  TH2I *mTriggerCounter=0x0;
  TH1I *mCounter=0x0;

  //infile present
  if(infile) {

  //take histograms container from input file
  hlist = dynamic_cast<TList*>( infile->Get("HistList") );

  //retrieve the trigger counter
  //TH2I *mTriggerCounter = (TH2I*) ((TList*) infile->Get("HistList"))->FindObject("mTriggerCounter"); // counter from upc trees
  mTriggerCounter = dynamic_cast<TH2I*>( hlist->FindObject("mTriggerCounter") ); // counter from upc trees

  Int_t ntrg=0;
  //loop over counter
  for(Int_t ibinX=0; ibinX<mTriggerCounter->GetNbinsX(); ibinX++) {

    Int_t n1 = mTriggerCounter->GetBinContent(ibinX, kUPCJpsiB_1+1);
    Int_t n2 = mTriggerCounter->GetBinContent(ibinX, kUPCJpsiB_2+1);

    if(n1 <=0 && n2 <= 0) continue;

    ntrg += n1 + n2;
  }//loop over counter

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
  st << Form("Dphi BEMC:  %.0f", hEvtCount->GetBinContent( kDphiBemc )) << endl;
  st << Form("PID el:     %.0f", hEvtCount->GetBinContent( kPID )) << endl;
  st << Form("ZVtx:       %.0f", hEvtCount->GetBinContent( kZvtx )) << endl;
  st << Form("Rapidity:   %.0f", hEvtCount->GetBinContent( kRap )) << endl;
  st << Form("Sign:       %.0f", hEvtCount->GetBinContent( kSign )) << endl;
  st << Form("Fin:        %.0f", hEvtCount->GetBinContent( kFin )) << endl;
  st << "---------------------" << endl;
  if( isMC ) {
    st << Form("Gen all:    %.0f", hGenCount->GetBinContent( kGenAll )) << endl;
    st << Form("Gen sel:    %.0f", hGenCount->GetBinContent( kGenSel )) << endl;
    st << "---------------------" << endl;
  }
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
































