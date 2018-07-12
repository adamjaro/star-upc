#ifndef StUPCConvElMaker_h
#define StUPCConvElMaker_h

#include "StMaker.h"

class StMuDstMaker;
class StMuDst;
class StUPCEvent;
class StUPCTrack;
class StTriggerData;
class StEmcPosition;
class StEmcGeom;
class StMuTrack;
class StMuPrimaryVertex;
class KFParticle;
class TH2I;
class StUPCFilterTrgUtil;
class StUPCFilterBemcUtil;

class StUPCConvElMaker: public StMaker {

public:

  StUPCConvElMaker(StMuDstMaker *maker, string outnam="StUPC.root");
  ~StUPCConvElMaker();

  void setIsMC(Bool_t mc=kTRUE) { mIsMC = mc; }
  void setWriteTrgData(Bool_t write = kTRUE) { mWriteTrgData = write; }

  Int_t Init();   //called at the beginning of the analysis
  Int_t Make();   //called for each event
  Int_t Finish(); //called at the end

  //public types
  enum {kUPCJpsiB_1=0, kUPCJpsiB_2, kUPCmain_1, kUPCmain_2, kVPDMB_5_debug};

private:

  StUPCConvElMaker(const StUPCConvElMaker &o); // not implemented
  StUPCConvElMaker &operator=(const StUPCConvElMaker &o); // not implemented

  void runPairs(const vector<StMuTrack*>& trkVec, const vector<KFParticle*>& kfVec);
  Bool_t selectPhoton(StMuPrimaryVertex *pv, KFParticle& kfgam);
  Bool_t selectPair(KFParticle& kfgam, KFParticle *k0, KFParticle *k1, StMuTrack *t0, StMuTrack *t1);
  void addPair(StMuPrimaryVertex *pv, KFParticle& kfgam, KFParticle *k0, KFParticle *k1, StMuTrack *t0, StMuTrack *t1, UInt_t& vtxcnt);
  void setUPCTrack(StUPCTrack *ut, StMuTrack *t, KFParticle *kf);
  KFParticle* makeKF(StMuTrack *gtrack, TClonesArray *gcov, Int_t pid);
  StMuPrimaryVertex* findPV(const KFParticle& kfgam, TClonesArray *pvtx);
  Bool_t runMC();

  StMuDstMaker *mMaker;  //StMuDstMaker provided to the constructor
  StMuDst *mMuDst; // input muDst data

  Bool_t mIsMC; // MC or data

  string mOutName;  // name of the output file
  TFile *mOutFile;  // output file

  TList *mHistList; // list of output histograms

  TH1I *mCounter; // analysis counter
  enum EvtCount{ kAna=1, kTrg, kTrgDat, kBemc, kGlobTrkAll, kGlobTrk, kWritten, kMaxCnt };
  TH1I *mErrCounter; // error counter
  enum ErrCount{ kErrNoEvt=1, kErrFillMsc, kNoTrgDat, kNoMC, kMaxErrCnt };
  TH1I *mPairCounter;
  enum PairCount{ kPairAll=1, kPair, kGam, kMaxPairCnt };

  //selection criteria in the maker
  static const Double_t mMaxDca; // maximal DCA to secondary vertex
  static const Double_t mMaxDcaPV; // maximal photon candidate DCA to primary vertex
  static const Double_t mMaxSigEl; // max number of dEdx sigmas for electron
  static const Double_t mMaxMass; // maximal pair mass
  static const Double_t mMaxDeltaDip; // delta-dip angle

  //histograms corresponding to selection criteria
  TH1D *mHistDca; // dca to sec vtx
  TH1D *mHistDcaPV; // dca to PV
  TH1D *mHistSigEl; // n sigmas for electron
  TH1D *mHistMass; // pair invarian mass
  TH1D *mHistDeltaDip; // delta-dip angle

  StUPCEvent *mUPCEvent; // output UPC event
  TTree *mUPCTree; // output tree

  //table of trigger IDs
  static const UInt_t mMaxTrg = 64; // max num of entries
  Int_t mTrgRan[mMaxTrg][2]; // run range for a given trigger ID
  UInt_t mTrgIDs[mMaxTrg]; // trigger IDs

  TH2I *mTriggerCounter; // analyzed events per run number for each trigger ID

  Bool_t mWriteTrgData; // flag to write trigger data to output UPC event

  StUPCFilterTrgUtil *mTrgUtil;
  StUPCFilterBemcUtil *mBemcUtil; //utility class for BEMC matching


  ClassDef(StUPCConvElMaker, 1);

};






#endif

















