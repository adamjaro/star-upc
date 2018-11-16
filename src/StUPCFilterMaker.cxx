
//_____________________________________________________________________________
//    Class for UPC filter
//    Author: Jaroslav Adam
//
//    Fills structure of StUPCEvent
//_____________________________________________________________________________

//c++ headers
#include "string.h"
#include <vector>
#include <map>

//root headers
#include "TObjArray.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1I.h"
#include "TH2I.h"
#include "TClonesArray.h"
#include "TDatabasePDG.h"
#include "TParticle.h"

//StRoot headers
#include "StMessMgr.h"
#include "StMuDSTMaker/COMMON/StMuDstMaker.h"
#include "StMuDSTMaker/COMMON/StMuDst.h"
#include "StMuDSTMaker/COMMON/StMuEvent.h"
#include "StMuDSTMaker/COMMON/StMuPrimaryVertex.h"
#include "StMuDSTMaker/COMMON/StMuTrack.h"
#include "StMuDSTMaker/COMMON/StMuMcTrack.h"
#include "StMuDSTMaker/COMMON/StMuMcVertex.h"
#include "StEvent/StTriggerData.h"

//local headers
#include "StUPCEvent.h"
#include "StUPCTrack.h"
#include "StUPCBemcCluster.h"
#include "StUPCVertex.h"

#include "StUPCFilterTrgUtil.h"
#include "StUPCFilterBemcUtil.h"
#include "StUPCFilterMaker.h"

ClassImp(StUPCFilterMaker);

//_____________________________________________________________________________
StUPCFilterMaker::StUPCFilterMaker(StMuDstMaker *maker, string outnam) : StMaker("StReadMuDstMaker"),
  mMaker(maker), mMuDst(0x0), mIsMC(0), mOutName(outnam), mOutFile(0x0),
  mHistList(0x0), mCounter(0x0), mErrCounter(0x0),
  mUPCEvent(0x0), mUPCTree(0x0), mTrgUtil(0x0), mBemcUtil(0x0)
{
  //constructor

  for(UInt_t i=0; i<mMaxTrg; i++) {
    mTrgIDs[i] = 0;
    mTrgRan[i][0] = -999;
    mTrgRan[i][1] = -999;
  }

  LOG_INFO << "StUPCFilterMaker::StUPCFilterMaker() called" << endm;

}//StUPCFilterMaker

//_____________________________________________________________________________
StUPCFilterMaker::~StUPCFilterMaker()
{
  //destructor

  LOG_INFO << "StUPCFilterMaker::~StUPCFilterMaker() destructor called" << endm;

  delete mTrgUtil; mTrgUtil=0;
  delete mBemcUtil; mBemcUtil=0;
  delete mHistList; mHistList=0;
  delete mCounter; mCounter=0;
  delete mErrCounter; mErrCounter=0;
  delete mUPCTree; mUPCTree=0;
  delete mUPCEvent; mUPCEvent=0;
  delete mOutFile; mOutFile=0;


  //cout << mCounter << " " << mErrCounter << " " << mHistList << " ";
  //cout << mUPCTree << " " << mUPCEvent << " " << mOutFile << endl;

}//~StUPCFilterMaker

//_____________________________________________________________________________
Int_t StUPCFilterMaker::Init()
{
  //called at the beginning

  //build the trigger ID table
  //
  //mTrgIDs[ kUPCJpsiB_1 ] = 450705; // UPCJpsiB, Run14 AuAu, 1st id
  mTrgRan[ kUPCJpsiB_1 ][0] = 15084052;
  mTrgRan[ kUPCJpsiB_1 ][1] = 15167014;
  //
  //mTrgIDs[ kUPCJpsiB_2 ] = 450725; // UPCJpsiB, Run14 AuAu, 2nd id
  mTrgRan[ kUPCJpsiB_2 ][0] = 15153036;
  mTrgRan[ kUPCJpsiB_2 ][1] = 15167007;
  //
  //mTrgIDs[ kUPCmain_1 ] = 450701; // UPC-main, Run14 AuAu, 1st id
  mTrgRan[ kUPCmain_1 ][0] = 15078073;
  mTrgRan[ kUPCmain_1 ][1] = 15167014;
  //
  //mTrgIDs[ kUPCmain_2 ] = 450711; // UPC-main, Run14 AuAu, 2nd id
  mTrgRan[ kUPCmain_2 ][0] = 15153036;
  mTrgRan[ kUPCmain_2 ][1] = 15167007;
  //
  //mTrgIDs[ kZero_bias ] = 9300; // Zero-bias, Run14 AuAu
  mTrgRan[ kZero_bias ][0] = 15045068;
  mTrgRan[ kZero_bias ][1] = 15187006;
  //
  //mTrgIDs[ kMain10_1 ] = 1; // UPC-main, Run10 AuAu, pre-PHYSICS id
  mTrgRan[ kMain10_1 ][0] = 11002120;
  mTrgRan[ kMain10_1 ][1] = 11039045;
  //
  //mTrgIDs[ kMain10_2 ] = 260750; // UPC-main, Run10 AuAu, standard PHYSICS id
  mTrgRan[ kMain10_2 ][0] = 11039046;
  mTrgRan[ kMain10_2 ][1] = 11077018;
  //
  //mTrgIDs[ kMain11_1 ] = 4; // UPC-main, Run11 AuAu, pre-PHYSICS id
  mTrgRan[ kMain11_1 ][0] = 11002120;
  mTrgRan[ kMain11_1 ][1] = 12146002;
  //
  //mTrgIDs[ kMain11_2 ] = 350007; // UPC-main, Run11 AuAu, standard PHYSICS 1st id
  mTrgRan[ kMain11_2 ][0] = 12146003;
  mTrgRan[ kMain11_2 ][1] = 12171017;
  //
  //mTrgIDs[ kMain11_3 ] = 350017; // UPC-main, Run11 AuAu, standard PHYSICS 2nd id
  mTrgRan[ kMain11_3 ][0] = 12146003;
  mTrgRan[ kMain11_3 ][1] = 12171017;
  //
  mTrgIDs[ kMon_1 ] = 450013; // VPD-ZDC-novtx-mon, 1st physics id
  mTrgRan[ kMon_1 ][0] = 15076101;
  mTrgRan[ kMon_1 ][1] = 15167014;
  //
  mTrgIDs[ kMon_2 ] = 450023; // VPD-ZDC-novtx-mon, 2nd physics id
  mTrgRan[ kMon_2 ][0] = 15153036;
  mTrgRan[ kMon_2 ][1] = 15167007;


  //utility for trigger data, BBC and ZDC
  mTrgUtil = new StUPCFilterTrgUtil();

  //initialize BEMC matching utility
  mBemcUtil = new StUPCFilterBemcUtil();

  //create the output file
  mOutFile = new TFile(mOutName.c_str(), "recreate");

  //output UPC event and tree
  mUPCEvent = new StUPCEvent();
  //configure the UPC event
  if( mIsMC > 0 ) mUPCEvent->setIsMC( kTRUE );

  //create the tree
  mUPCTree = new TTree("mUPCTree", "mUPCTree");
  //add branch with event objects
  mUPCTree->Branch("mUPCEvent", &mUPCEvent);

  //output histograms
  mHistList = new TList();
  mHistList->SetOwner();

  //counter of processed events
  mCounter = new TH1I("mCounter", "mCounter", kMaxCnt-1, 1, kMaxCnt);
  mHistList->Add(mCounter);

  //counter for errors encountered during the analysis
  mErrCounter = new TH1I("mErrCounter", "mErrCounter", kMaxErrCnt-1, 1, kMaxErrCnt);
  mHistList->Add(mErrCounter);

  //counter of analyzed events per run number for each trigger ID
  const Int_t runFirst = 15040000; // 15078000  15040000  11000000
  const Int_t runLast  = 15190000; // 15167100
  const Int_t runRange = runLast - runFirst;
  mTriggerCounter = new TH2I("mTriggerCounter", "mTriggerCounter", runRange, runFirst, runLast, mMaxTrg+1, 0, mMaxTrg+1);
  mHistList->Add(mTriggerCounter);

  return kStOk;

}//Init

//_____________________________________________________________________________
Int_t StUPCFilterMaker::Make()
{
  //called for each event

  mUPCEvent->clearEvent(); //clear the output UPC event
  mBemcUtil->clear(); //clear data structures in BEMC util

  //input muDst data
  mMuDst = mMaker->muDst();
  if( !mMuDst ) {
    LOG_INFO << "StUPCFilterMaker::Make() no muDst input" << endm;
    mErrCounter->Fill( kErrNoEvt ); // no muDst input, same err flag as event
    return kStErr;
  }
  //input mu event
  StMuEvent *evt = mMuDst->event();
  if( !evt ) {
    LOG_INFO << "StUPCFilterMaker::Make() no input event" << endm;
    mErrCounter->Fill( kErrNoEvt ); // no input event
    return kStErr;
  }

  mCounter->Fill( kAna ); // analyzed events

  //mc
  if( mIsMC > 0 ) {
    if( !runMC() ) {
      LOG_INFO << "StUPCFilterMaker::Make() no MC" << endm;
      mErrCounter->Fill( kNoMC );
    }
  }

  //trigger
  const StTriggerId trgId = evt->triggerIdCollection().nominal();
  Int_t runnum = evt->runNumber();

  Bool_t isTrg = kFALSE; //determine whether at least one of trigger IDs was fired
  for(UInt_t i=0; i<mMaxTrg; i++) {
    if( mTrgIDs[i] == 0 ) continue; // ID not set
    if( runnum < mTrgRan[i][0] || runnum > mTrgRan[i][1] ) continue; // run range for a given trigger ID

    if( !trgId.isTrigger( mTrgIDs[i] ) ) continue;

    //trigger ID was fired
    mUPCEvent->setTrigger( i );
    isTrg = kTRUE;

    mTriggerCounter->Fill(runnum, i);
  }
  if( mIsMC > 0 ) isTrg = kTRUE; //override for MC
  if( !isTrg ) return kStOk;
  //event passed the trigger

  mCounter->Fill( kTrg ); // events after trigger

  //run number
  mUPCEvent->setRunNumber( runnum );
  //event number
  mUPCEvent->setEventNumber( evt->eventNumber() );

  //beam fill number
  const StRunInfo &runInfo = evt->runInfo();
  Int_t fillY = (Int_t) runInfo.beamFillNumber(yellow);
  Int_t fillB = (Int_t) runInfo.beamFillNumber(blue);
  if( fillY != fillB ) {
    LOG_INFO << "StUPCFilterMaker::Make() fill number mismatch" << endm;
    //fill number mismatch
    mErrCounter->Fill( kErrFillMsc );
  }
  mUPCEvent->setFillNumber( fillY );

  //bunch crossing ID
  const StL0Trigger &l0trig = evt->l0Trigger();
  mUPCEvent->setBunchCrossId( l0trig.bunchCrossingId() );
  mUPCEvent->setBunchCrossId7bit( l0trig.bunchCrossingId7bit(runnum) );

  //magnetic field in UPC event
  mUPCEvent->setMagneticField( evt->eventSummary().magneticField() );

  //trigger data for DSM, ZDC, BBC and TOF
  const StTriggerData *trgdat = evt->triggerData();
  if( !trgdat && mIsMC==0 ) {
    mErrCounter->Fill( kNoTrgDat ); // no trigger data
    LOG_INFO << "StUPCFilterMaker::Make() no trigger data" << endm;
    return kStErr;
  }
  if( trgdat ) {
    mTrgUtil->processEvent(trgdat, mUPCEvent);
    mCounter->Fill( kTrgDat ); // events having trigger data
  }

  //TOF number of hits from StMuDst
  mUPCEvent->setNTofHit( mMuDst->numberOfTofHit() );

/*
  //BEMC high tower and jet patches
  for(Int_t ipatch=0; ipatch<300; ipatch++) {
    cout << "  HT: " << ipatch << " " << (Int_t) trgdat->bemcHighTower(ipatch) << endl;
  }
*/

  //BEMC util
  //magnetic field for track projection to BEMC
  mBemcUtil->setMagField( evt->eventSummary().magneticField()/10. ); //conversion ok, checked by track->pt() and emcPt
  //fill structures with clusters and hits
  if( mBemcUtil->processEvent(mMuDst, mUPCEvent) ) mCounter->Fill( kBemc ); // events having BEMC clusters

  //vertex loop
  for(UInt_t ivtx=0; ivtx<mMuDst->numberOfPrimaryVertices(); ivtx++) {
    //static call to set current primary vertex
    StMuDst::setVertexIndex(ivtx);

    //get array of primary tracks
    TObjArray *trkArray = mMuDst->primaryTracks();
    if( !trkArray ) continue;

    Int_t nSelTracks = 0; //number of tracks selected to write to output UPC event

    //tracks loop
    for(Int_t itrk=0; itrk<trkArray->GetEntriesFast(); itrk++) {
      StMuTrack *track = dynamic_cast<StMuTrack*>( trkArray->At(itrk) );
      if( !track ) continue;

      //matching to BEMC cluster
      UInt_t clsId=0;
      Double_t emcPhi=-999., emcEta=-999., emcPt=-999.;
      Bool_t emcProj=kFALSE;
      Float_t hitE=-999.;
      Short_t nhitsBemc = mBemcUtil->matchBEMC(track, emcPhi, emcEta, emcPt, emcProj, clsId, hitE);
      Bool_t matchBemc = nhitsBemc > 0 ? kTRUE : kFALSE;

      //TOF matching
      const StMuBTofPidTraits &tofPid = track->btofPidTraits();
      Bool_t matchTof = tofPid.matchFlag() != 0 ? kTRUE : kFALSE;

      //require at least one match, only in data or embedding MC
      if( mIsMC!=1 && !matchBemc && !matchTof ) continue;

      //track matched to BEMC or TOF and selected to write to output UPC event
      nSelTracks++;

      //UPC track
      StUPCTrack *upcTrack = mUPCEvent->addTrack();
      upcTrack->setPtEtaPhi(track->pt(), track->eta(), track->phi());
      upcTrack->setDcaXY( track->dcaGlobal().perp() );
      upcTrack->setDcaZ( track->dcaGlobal().z() );
      upcTrack->setCharge( track->charge() );
      upcTrack->setNhits( track->nHits() );
      upcTrack->setNhitsFit( track->nHitsFit() );
      upcTrack->setChi2( track->chi2() );
      upcTrack->setDEdxSignal( track->dEdx() );
      upcTrack->setNSigmasTPC( StUPCTrack::kElectron, track->nSigmaElectron() );
      upcTrack->setNSigmasTPC( StUPCTrack::kPion, track->nSigmaPion() );
      upcTrack->setNSigmasTPC( StUPCTrack::kKaon, track->nSigmaKaon() );
      upcTrack->setNSigmasTPC( StUPCTrack::kProton, track->nSigmaProton() );
      upcTrack->setVertexId( ivtx );
      if( emcProj ) {
        upcTrack->setFlag( StUPCTrack::kBemcProj );
        upcTrack->setBemcPtEtaPhi(emcPt, emcEta, emcPhi);
      }
      if( matchBemc ) {
        upcTrack->setFlag( StUPCTrack::kBemc );
        upcTrack->setBemcPtEtaPhi(emcPt, emcEta, emcPhi);
        upcTrack->setBemcClusterId(clsId);
        upcTrack->setBemcHitE(hitE);
      }
      if( matchTof ) {
        upcTrack->setFlag( StUPCTrack::kTof );
        upcTrack->setTofTime( tofPid.timeOfFlight() );
        upcTrack->setTofPathLength( tofPid.pathLength() );
      }

    }//tracks loop

    if( nSelTracks <= 0 ) continue; //no selected tracks for this vertex

    //position of current primary vertex
    StThreeVectorF vtxPos = evt->primaryVertexPosition();
    StThreeVectorF vtxPosErr = evt->primaryVertexErrors();

    //write vertex to output UPC event
    StUPCVertex *upcVtx = mUPCEvent->addVertex();
    upcVtx->setPosX( vtxPos.x() );
    upcVtx->setPosY( vtxPos.y() );
    upcVtx->setPosZ( vtxPos.z() );
    upcVtx->setErrX( vtxPosErr.x() );
    upcVtx->setErrY( vtxPosErr.y() );
    upcVtx->setErrZ( vtxPosErr.z() );
    upcVtx->setNPrimaryTracks( trkArray->GetEntriesFast() );
    upcVtx->setNTracksUsed( mMuDst->primaryVertex()->nTracksUsed() );
    upcVtx->setId( ivtx );

  }//vertex loop

  //write BEMC clusters
  mBemcUtil->writeBEMC(mUPCEvent);

  //event accepted to write to output tree
  mCounter->Fill( kWritten ); // events written to output tree
  mUPCTree->Fill();

  return kStOk;

}//Make

//_____________________________________________________________________________
Bool_t StUPCFilterMaker::runMC() {

  TClonesArray *muMcVtx = mMuDst->mcArray(0);
  TClonesArray *muMcTracks = mMuDst->mcArray(1);
  if( !muMcTracks ) return kFALSE;
  if( !muMcVtx ) return kFALSE;

  TDatabasePDG *pdgdat = TDatabasePDG::Instance();

  //vertex map from id to position in clones array
  map<Int_t, Int_t> vmap;
  //MC vertex loop
  for(Int_t ivtx=0; ivtx<muMcVtx->GetEntries(); ivtx++) {
    StMuMcVertex *vtx = dynamic_cast<StMuMcVertex*>(muMcVtx->At(ivtx));
    vmap[vtx->Id()] = ivtx;
  }//MC vertex loop

  //mc tracks loop
  for(Int_t i=0; i<muMcTracks->GetEntries(); i++) {
    StMuMcTrack *mcTrk = dynamic_cast<StMuMcTrack*>( muMcTracks->At(i) );
    if(!mcTrk) continue;

    const StThreeVectorF pxyz = mcTrk->Pxyz();
    Float_t px = pxyz.x();
    Float_t py = pxyz.y();
    Float_t pz = pxyz.z();
    Float_t energy = mcTrk->E();

    TParticle *part = mUPCEvent->addMCParticle();
    if(!part) return kFALSE;

    part->SetMomentum(px, py, pz, energy);
    part->SetPdgCode( pdgdat->ConvertGeant3ToPdg( mcTrk->GePid() ) );

    //MC vertex
    StMuMcVertex *vtx = dynamic_cast<StMuMcVertex*>(muMcVtx->At( vmap[mcTrk->IdVx()] ));
    const StThreeVectorF vxyz = vtx->XyzV();

    part->SetProductionVertex(vxyz.x(), vxyz.y(), vxyz.z(), 0.);
    //set original vertex id
    part->SetFirstMother(mcTrk->IdVx());

  }//mc tracks loop

  return kTRUE;

}//runMC

//_____________________________________________________________________________
Int_t StUPCFilterMaker::Finish()
{
  //called at the end

  //write the output file
  mOutFile->cd();

  mUPCTree->Write();
  mHistList->Write("HistList", TObject::kSingleKey);

  mOutFile->Close();

  return kStOk;

}//Finish
















































