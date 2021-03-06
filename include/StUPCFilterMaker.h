#ifndef StUPCFilterMaker_h
#define StUPCFilterMaker_h

#include "StMaker.h"

class StMuDstMaker;
class StMuDst;
class StUPCEvent;
class StTriggerData;
class StEmcPosition;
class StEmcGeom;
class StMuTrack;
class TH2I;
class StUPCFilterTrgUtil;
class StUPCFilterBemcUtil;

class StUPCFilterMaker: public StMaker {

public:

  StUPCFilterMaker(StMuDstMaker *maker, string outnam="StUPC.root");
  ~StUPCFilterMaker();

  void setIsMC(Int_t mc) { mIsMC = mc; }

  Int_t Init();   //called at the beginning of the analysis
  Int_t Make();   //called for each event
  Int_t Finish(); //called at the end

  //public types
  enum {kUPCJpsiB_1=0, kUPCJpsiB_2, kUPCmain_1, kUPCmain_2, kZero_bias, kMain10_1, kMain10_2, kMain11_1, kMain11_2, kMain11_3, kMon_1, kMon_2};

private:

  StUPCFilterMaker(const StUPCFilterMaker &o); // not implemented
  StUPCFilterMaker &operator=(const StUPCFilterMaker &o); // not implemented

  Bool_t runMC();

  StMuDstMaker *mMaker;  //StMuDstMaker provided to the constructor
  StMuDst *mMuDst; // input muDst data

  Int_t mIsMC; // MC or data

  string mOutName;  // name of the output file
  TFile *mOutFile;  // output file

  TList *mHistList; // list of output histograms

  TH1I *mCounter; // analysis counter
  enum EvtCount{ kAna=1, kTrg, kTrgDat, kBemc, kWritten, kMaxCnt };
  TH1I *mErrCounter; // error counter
  enum ErrCount{ kErrNoEvt=1, kErrFillMsc, kNoTrgDat, kNoMC, kMaxErrCnt };

  StUPCEvent *mUPCEvent; // output UPC event
  TTree *mUPCTree; // output tree

  //table of trigger IDs
  static const UInt_t mMaxTrg = 64; // max num of entries
  Int_t mTrgRan[mMaxTrg][2]; // run range for a given trigger ID
  UInt_t mTrgIDs[mMaxTrg]; // trigger IDs

  TH2I *mTriggerCounter; // analyzed events per run number for each trigger ID

  StUPCFilterTrgUtil *mTrgUtil;
  StUPCFilterBemcUtil *mBemcUtil; //utility class for BEMC matching


  ClassDef(StUPCFilterMaker, 1);

};






#endif

















