
//_____________________________________________________________________________
//    Class for conversion electrons in UPC studies
//    Author: Jaroslav Adam
//
//    Fills structure of StUPCEvent
//_____________________________________________________________________________

//c++ headers
#include "string.h"
#include <vector>

//root headers
#include "TObjArray.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1I.h"
#include "TH2I.h"
#include "TH1D.h"
#include "TClonesArray.h"
#include "TDatabasePDG.h"
#include "TParticle.h"
#include "TMath.h"

//StRoot headers
#include "StMessMgr.h"
#include "StMuDSTMaker/COMMON/StMuDstMaker.h"
#include "StMuDSTMaker/COMMON/StMuDst.h"
#include "StMuDSTMaker/COMMON/StMuEvent.h"
#include "StMuDSTMaker/COMMON/StMuTrack.h"
#include "StMuDSTMaker/COMMON/StMuMcTrack.h"
#include "StMuDSTMaker/COMMON/StMuPrimaryVertex.h"
#include "StEvent/StTriggerData.h"
#include "KFParticle.h"

//local headers
#include "StUPCEvent.h"
#include "StUPCTrack.h"
#include "StUPCBemcCluster.h"
#include "StUPCVertex.h"

#include "StUPCFilterTrgUtil.h"
#include "StUPCFilterBemcUtil.h"
#include "StUPCConvElMaker.h"

ClassImp(StUPCConvElMaker);

const Double_t StUPCConvElMaker::mMaxDca = 0.9; // maximal DCA to secondary vertex
const Double_t StUPCConvElMaker::mMaxDcaPV = 0.6; // maximal photon candidate DCA to primary vertex
const Double_t StUPCConvElMaker::mMaxSigEl = 4.; // max number of dEdx sigmas for electron, absolute value
const Double_t StUPCConvElMaker::mMaxMass = 0.3; // maximal pair mass
const Double_t StUPCConvElMaker::mMaxDeltaDip = 0.1; // delta-dip angle

//_____________________________________________________________________________
StUPCConvElMaker::StUPCConvElMaker(StMuDstMaker *maker, string outnam) : StMaker("StReadMuDstMaker"),
  mMaker(maker), mMuDst(0x0), mIsMC(0), mOutName(outnam), mOutFile(0x0),
  mHistList(0x0), mCounter(0x0), mErrCounter(0x0), mPairCounter(0x0),
  mHistDca(0x0), mHistDcaPV(0x0), mHistSigEl(0x0), mHistMass(0x0),
  mUPCEvent(0x0), mUPCTree(0x0), mTrgUtil(0x0), mBemcUtil(0x0)
{
  //constructor

  for(UInt_t i=0; i<mMaxTrg; i++) {
    mTrgIDs[i] = 0;
    mTrgRan[i][0] = -999;
    mTrgRan[i][1] = -999;
  }

  LOG_INFO << "StUPCConvElMaker::StUPCConvElMaker() called" << endm;

}//StUPCConvElMaker

//_____________________________________________________________________________
StUPCConvElMaker::~StUPCConvElMaker()
{
  //destructor

  LOG_INFO << "StUPCConvElMaker::~StUPCConvElMaker() destructor called" << endm;

  delete mTrgUtil; mTrgUtil=0;
  delete mBemcUtil; mBemcUtil=0;
  delete mHistList; mHistList=0;
  delete mCounter; mCounter=0;
  delete mErrCounter; mErrCounter=0;
  delete mPairCounter; mPairCounter=0;
  delete mUPCTree; mUPCTree=0;
  delete mUPCEvent; mUPCEvent=0;
  delete mOutFile; mOutFile=0;


  //cout << mCounter << " " << mErrCounter << " " << mHistList << " ";
  //cout << mUPCTree << " " << mUPCEvent << " " << mOutFile << endl;

}//~StUPCConvElMaker

//_____________________________________________________________________________
Int_t StUPCConvElMaker::Init()
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
  mTrgIDs[ kUPCmain_1 ] = 450701; // UPC-main, Run14 AuAu, 1st id
  mTrgRan[ kUPCmain_1 ][0] = 15078073;
  mTrgRan[ kUPCmain_1 ][1] = 15167014;
  //
  mTrgIDs[ kUPCmain_2 ] = 450711; // UPC-main, Run14 AuAu, 2nd id
  mTrgRan[ kUPCmain_2 ][0] = 15153036;
  mTrgRan[ kUPCmain_2 ][1] = 15167007;
  //
  mTrgIDs[ kVPDMB_5_debug ] = 450060; // VPDMB-5-p-nobsmd-hlt, Run14 AuAu, debug purposes
  mTrgRan[ kVPDMB_5_debug ][0] = mTrgRan[ kUPCJpsiB_1 ][0];
  mTrgRan[ kVPDMB_5_debug ][1] = mTrgRan[ kUPCJpsiB_1 ][1];

  //utility for trigger data, BBC and ZDC
  mTrgUtil = new StUPCFilterTrgUtil();

  //initialize BEMC matching utility
  mBemcUtil = new StUPCFilterBemcUtil();

  //create the output file
  mOutFile = new TFile(mOutName.c_str(), "recreate");

  //output UPC event and tree
  mUPCEvent = new StUPCEvent();
  //configure the UPC event
  mUPCEvent->setIsMC( mIsMC );

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

  //counter for pairs
  mPairCounter = new TH1I("mPairCounter", "mPairCounter", kMaxPairCnt-1, 1, kMaxPairCnt);
  mHistList->Add(mPairCounter);

  //counter of analyzed events per run number for each trigger ID
  const Int_t runFirst = 15078000;
  const Int_t runLast = 15167100;
  const Int_t runRange = runLast - runFirst;
  mTriggerCounter = new TH2I("mTriggerCounter", "mTriggerCounter", runRange, runFirst, runLast, mMaxTrg+1, 0, mMaxTrg+1);
  mHistList->Add(mTriggerCounter);

  //dca to sec vtx
  mHistDca = new TH1D("mHistDca", "mHistDca", 1000, 0., 1000.);
  mHistList->Add(mHistDca);

  //dca to PV
  mHistDcaPV = new TH1D("mHistDcaPV", "mHistDcaPV", 1000, 0., 1000.);
  mHistList->Add(mHistDcaPV);

  //number of sigmas for electron
  mHistSigEl = new TH1D("mHistSigEl", "mHistSigEl", 1000, -100., 100.);
  mHistList->Add(mHistSigEl);

  //pair mass
  mHistMass = new TH1D("mHistMass", "mHistMass", 1000, 0., 10.);
  mHistList->Add(mHistMass);

  //delta-dip angle
  mHistDeltaDip = new TH1D("mHistDeltaDip", "mHistDeltaDip", 1000, 0., 1.8);
  mHistList->Add(mHistDeltaDip);

  return kStOk;

}//Init

//_____________________________________________________________________________
Int_t StUPCConvElMaker::Make()
{
  //called for each event

  mUPCEvent->clearEvent(); //clear the output UPC event
  mBemcUtil->clear(); //clear data structures in BEMC util

  //input muDst data
  mMuDst = mMaker->muDst();
  if( !mMuDst ) {
    LOG_INFO << "StUPCConvElMaker::Make() no muDst input" << endm;
    mErrCounter->Fill( kErrNoEvt ); // no muDst input, same err flag as event
    return kStErr;
  }
  //input mu event
  StMuEvent *evt = mMuDst->event();
  if( !evt ) {
    LOG_INFO << "StUPCConvElMaker::Make() no input event" << endm;
    mErrCounter->Fill( kErrNoEvt ); // no input event
    return kStErr;
  }

  mCounter->Fill( kAna ); // analyzed events

  //mc
  if(mIsMC) {
    if( !runMC() ) {
      LOG_INFO << "StUPCConvElMaker::Make() no MC" << endm;
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
  if( mIsMC ) isTrg = kTRUE; //override for MC
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
    LOG_INFO << "StUPCConvElMaker::Make() fill number mismatch" << endm;
    //fill number mismatch
    mErrCounter->Fill( kErrFillMsc );
  }
  mUPCEvent->setFillNumber( fillY );

  //bunch crossing ID
  const StL0Trigger &l0trig = evt->l0Trigger();
  mUPCEvent->setBunchCrossId( l0trig.bunchCrossingId() );
  mUPCEvent->setBunchCrossId7bit( l0trig.bunchCrossingId7bit(runnum) );

  //magnetic field in UPC event and in KF particle
  const Double_t mfield = evt->eventSummary().magneticField();
  mUPCEvent->setMagneticField(mfield);
  KFParticle::SetField(mfield);

  //trigger data for DSM, ZDC, BBC and TOF
  const StTriggerData *trgdat = evt->triggerData();
  if( !trgdat && !mIsMC ) {
    mErrCounter->Fill( kNoTrgDat ); // no trigger data
    LOG_INFO << "StUPCConvElMaker::Make() no trigger data" << endm;
    return kStErr;
  }
  if( trgdat ) {
    mTrgUtil->processEvent(trgdat, mUPCEvent);
    mCounter->Fill( kTrgDat ); // events having trigger data
  }

  //BEMC util
  //magnetic field for track projection to BEMC
  mBemcUtil->setMagField( evt->eventSummary().magneticField()/10. ); //conversion ok, checked by track->pt() and emcPt
  //fill structures with clusters and hits
  if( mBemcUtil->processEvent(mMuDst, mUPCEvent) ) mCounter->Fill( kBemc ); // events having BEMC clusters

  //cout << "Next event" << endl;
  //cout << "Field: " << evt->eventSummary().magneticField() << endl;
  cout << "Next event, vtx: " << mMuDst->numberOfPrimaryVertices() << endl;

  //get array of global tracks
  TObjArray *gtrkArray = mMuDst->globalTracks();
  if( !gtrkArray ) return kStOk;

  //covariance matrices of global tracks
  TClonesArray *gcov = mMuDst->covGlobTrack();
  if( !gcov ) return kStOk;

  //vectors of tracks and KF particles
  vector<StMuTrack*> trkVec;
  vector<KFParticle*> kfVec;

  //global tracks loop
  for(Int_t itrk=0; itrk<gtrkArray->GetEntriesFast(); itrk++) {
    StMuTrack *gtrack = dynamic_cast<StMuTrack*>( gtrkArray->At(itrk) );
    if( !gtrack ) continue;
    mCounter->Fill( kGlobTrkAll );

    //select the track

    //TOF matching
    const StMuBTofPidTraits &tofPid = gtrack->btofPidTraits();
    if( tofPid.matchFlag() == 0 ) continue;

    //BEMC projection
    UInt_t clsId=0;
    Double_t emcPhi=-999., emcEta=-999., emcPt=-999.;
    Bool_t emcProj=kFALSE;
    Float_t hitE=-999.;
    mBemcUtil->matchBEMC(gtrack, emcPhi, emcEta, emcPt, emcProj, clsId, hitE);
    if( !emcProj ) continue;

    //global track selected
    mCounter->Fill( kGlobTrk );

    //store pointer to selected track
    trkVec.push_back(gtrack);
    //KF particle for the track
    Int_t pdg = gtrack->charge() < 0 ? 11 : -11;
    kfVec.push_back( makeKF(gtrack, gcov, pdg) );

  }//global tracks loop

  //build the pairs
  runPairs(trkVec, kfVec);

  //clean-up the KF vector
  for(vector<KFParticle*>::const_iterator it = kfVec.cbegin(); it != kfVec.cend(); it++) {
    delete *it;
  }
  kfVec.clear();

  //write BEMC clusters
  mBemcUtil->writeBEMC(mUPCEvent);

  //event accepted to write to output tree
  mCounter->Fill( kWritten ); // events written to output tree
  mUPCTree->Fill();

  return kStOk;

}//Make

//_____________________________________________________________________________
void StUPCConvElMaker::runPairs(const vector<StMuTrack*>& trkVec, const vector<KFParticle*>& kfVec) {

  //build pairs from selected tracks

  /*
  Procedure to create secondary vertices and photon candidates using KF particles:

    prologue: select global tracks which are matched to TOF and projected to BEMC

    (i) pairs of tracks, KF particle for each track, pair KF particle (photon candidate)

    (ii) secondary vertex by propagating pair KF particle to its decay vertex

    (iii) save tracks in pair and secondary vertex to UPC event as UPCTrack and UPCVertex

    (iv) find primary vertex with closest dca to pair KF particle

    (v) save pair KF particle as UPCTrack (charge = 0), associated primary vertex as UPCVertex,
        set ID of decay secondary vertex in pair KF particle by setBemcClusterId
  */

  if( trkVec.size() != kfVec.size() ) return;

  UInt_t vtxcnt = 0;
  TClonesArray *pvtx = mMuDst->primaryVertices();
  if( !pvtx ) return;
  if( pvtx->GetEntries() == 0 ) return;

  //pairs loop
  for(UInt_t i=0; i<trkVec.size(); i++) {
    if( !kfVec[i] ) continue;

    for(UInt_t j=i+1; j<trkVec.size(); j++) {
      if( !kfVec[j] ) continue;
      mPairCounter->Fill( kPairAll );

      //photon candidate
      KFParticle kfgam(*kfVec[i], *kfVec[j]); // decay vertex is set
      if( !selectPair(kfgam, kfVec[i], kfVec[j], trkVec[i], trkVec[j]) ) continue;
      //pair selected
      mPairCounter->Fill( kPair );

      //find primary vertex with closest dca to pair KF particle kfgam
      StMuPrimaryVertex *pv = findPV(kfgam, pvtx);
      if( !pv ) continue;
      if( !selectPhoton(pv, kfgam) ) continue;
      //photon selected
      mPairCounter->Fill( kGam );

      addPair(pv, kfgam, kfVec[i], kfVec[j], trkVec[i], trkVec[j], vtxcnt);

    }
  }//pairs loop

}//run pairs

//_____________________________________________________________________________
Bool_t StUPCConvElMaker::selectPhoton(StMuPrimaryVertex *pv, KFParticle& kfgam) {

  //photon candidate DCA to primary vertex
  StThreeVectorF pvPos = pv->position();
  Double_t pos[3] = {pvPos.x(), pvPos.y(), pvPos.z()};

  Double_t dca = kfgam.GetDistanceFromVertex(pos);
  mHistDcaPV->Fill( dca );

  if( dca > mMaxDcaPV ) return kFALSE;

  return kTRUE;

}//selectPhoton

//_____________________________________________________________________________
Bool_t StUPCConvElMaker::selectPair(KFParticle& kfgam, KFParticle *k0, KFParticle *k1, StMuTrack *t0, StMuTrack *t1) {

  kfgam.TransportToDecayVertex();

  //dca to secondary vertex
  Double_t dca0 = k0->GetDistanceFromVertex(kfgam);
  Double_t dca1 = k1->GetDistanceFromVertex(kfgam);
  //dca histogram before the selection
  mHistDca->Fill( dca0 );
  mHistDca->Fill( dca1 );
  if( dca0 > mMaxDca || dca1 > mMaxDca ) return kFALSE;

  //number of sigmas for electron
  Double_t nsig0 = t0->nSigmaElectron();
  Double_t nsig1 = t1->nSigmaElectron();
  mHistSigEl->Fill( nsig0 );
  mHistSigEl->Fill( nsig1 );
  if( TMath::Abs(nsig0) > mMaxSigEl || TMath::Abs(nsig1) > mMaxSigEl ) return kFALSE;

  //pair mass
  Double_t mass = kfgam.GetMass();
  mHistMass->Fill( mass );
  if( mass > mMaxMass ) return kFALSE;

  //delta-dip-angle, Eq. 2 in PHYSICAL REVIEW C 79, 064903 (2009)
  k0->TransportToParticle(kfgam);
  k1->TransportToParticle(kfgam);
  TVector3 vec0(k0->GetPx(), k0->GetPy(), k0->GetPz());
  TVector3 vec1(k1->GetPx(), k1->GetPy(), k1->GetPz());

  Double_t deltaDip = TMath::ACos( (vec0.Pt()*vec1.Pt() + vec0.Pz()*vec1.Pz())/(vec0.Mag()*vec1.Mag()) );
  mHistDeltaDip->Fill( deltaDip );
  if( deltaDip > mMaxDeltaDip ) return kFALSE;

  return kTRUE;

}//selectPair

//_____________________________________________________________________________
void StUPCConvElMaker::addPair(StMuPrimaryVertex *pv, KFParticle& kfgam, KFParticle *k0, KFParticle *k1, StMuTrack *t0, StMuTrack *t1, UInt_t& vtxcnt) {

  //secondary vertex
  kfgam.TransportToDecayVertex();
  StUPCVertex *upcVtx = mUPCEvent->addVertex();
  upcVtx->setPosX( kfgam.GetX() );
  upcVtx->setPosY( kfgam.GetY() );
  upcVtx->setPosZ( kfgam.GetZ() );
  upcVtx->setErrX( kfgam.GetErrX() );
  upcVtx->setErrY( kfgam.GetErrY() );
  upcVtx->setErrZ( kfgam.GetErrZ() );
  upcVtx->setId( vtxcnt );

  //tracks
  StUPCTrack *ut0 = mUPCEvent->addTrack();
  StUPCTrack *ut1 = mUPCEvent->addTrack();
  ut0->setVertexId( vtxcnt );
  ut1->setVertexId( vtxcnt );
  //dcaZ for DCA magnitude
  ut0->setDcaZ( k0->GetDistanceFromVertex(kfgam) );
  ut1->setDcaZ( k1->GetDistanceFromVertex(kfgam) );
  //dcaXY for transversal DCA
  ut0->setDcaXY( k0->GetDistanceFromVertexXY(kfgam) );
  ut1->setDcaXY( k1->GetDistanceFromVertexXY(kfgam) );
  //parameters from StMuTrack and KF particle
  k0->TransportToParticle(kfgam);
  k1->TransportToParticle(kfgam);
  setUPCTrack(ut0, t0, k0);
  setUPCTrack(ut1, t1, k1);

  //increment counter for vertex ID
  ++vtxcnt;

  //primary vertex associated with current pair
  StUPCVertex *upcPV = mUPCEvent->addVertex();
  StThreeVectorF pvPos = pv->position();
  StThreeVectorF pvErr = pv->posError();
  Double_t pos[3] = {pvPos.x(), pvPos.y(), pvPos.z()};
  upcPV->setPosX( pos[0] );
  upcPV->setPosY( pos[1] );
  upcPV->setPosZ( pos[2] );
  upcPV->setErrX( pvErr.x() );
  upcPV->setErrY( pvErr.y() );
  upcPV->setErrZ( pvErr.z() );
  upcPV->setId( vtxcnt );

  //photon candidate
  StUPCTrack *gam = mUPCEvent->addTrack();
  gam->setCharge(0);
  gam->setVertexId( vtxcnt );
  //dcaZ for DCA to PV magnitude
  gam->setDcaZ( kfgam.GetDistanceFromVertex(pos) );
  gam->setDcaXY( kfgam.GetDistanceFromVertexXY(pos) );
  //transport photon candidate to production primary vertex
  kfgam.TransportToPoint(pos);
  gam->setPtEtaPhi(kfgam.GetPt(), kfgam.GetEta(), kfgam.GetPhi());
  gam->setChi2( kfgam.GetChi2() );
  //set ID of decay vertex as BemcClusterId
  gam->setBemcClusterId( ut0->getVertexId() );

  //increment counter for vertex ID after adding primary vertex for photon candidate
  ++vtxcnt;

}//addPair

//_____________________________________________________________________________
void StUPCConvElMaker::setUPCTrack(StUPCTrack *ut, StMuTrack *t, KFParticle *kf) {

  //set UPC track parameters from StMuTrack

  ut->setPtEtaPhi(kf->GetPt(), kf->GetEta(), kf->GetPhi());
  ut->setCharge( t->charge() );
  ut->setNhits( t->nHits() );
  ut->setNhitsFit( t->nHitsFit() );
  ut->setChi2( t->chi2() );
  ut->setDEdxSignal( t->dEdx() );
  ut->setNSigmasTPC( StUPCTrack::kElectron, t->nSigmaElectron() );
  ut->setNSigmasTPC( StUPCTrack::kPion, t->nSigmaPion() );
  ut->setNSigmasTPC( StUPCTrack::kKaon, t->nSigmaKaon() );
  ut->setNSigmasTPC( StUPCTrack::kProton, t->nSigmaProton() );

  //matching to BEMC cluster
  UInt_t clsId=0;
  Double_t emcPhi=-999., emcEta=-999., emcPt=-999.;
  Bool_t emcProj=kFALSE;
  Float_t hitE=-999.;
  Short_t nhitsBemc = mBemcUtil->matchBEMC(t, emcPhi, emcEta, emcPt, emcProj, clsId, hitE);
  Bool_t matchBemc = nhitsBemc > 0 ? kTRUE : kFALSE;
  if( emcProj ) {
    ut->setFlag( StUPCTrack::kBemcProj );
    ut->setBemcPtEtaPhi(emcPt, emcEta, emcPhi);
  }
  if( matchBemc ) {
    ut->setFlag( StUPCTrack::kBemc );
    ut->setBemcPtEtaPhi(emcPt, emcEta, emcPhi);
    ut->setBemcClusterId(clsId);
    ut->setBemcHitE(hitE);
  }

  //TOF matching
  const StMuBTofPidTraits &tofPid = t->btofPidTraits();
  Bool_t matchTof = tofPid.matchFlag() != 0 ? kTRUE : kFALSE;
  if( matchTof ) {
    ut->setFlag( StUPCTrack::kTof );
    ut->setTofBeta( tofPid.beta() );
  }

}//setUPCTrack

//_____________________________________________________________________________
StMuPrimaryVertex* StUPCConvElMaker::findPV(const KFParticle& kfgam, TClonesArray *pvtx) {

  //find primary vertex with closest dca to pair KF particle kfgam

  Double_t dcamin = 9.e9;
  StMuPrimaryVertex *pvmin = 0x0;

  //pv loop
  for(Int_t ipv=0; ipv<pvtx->GetEntries(); ipv++) {
    StMuPrimaryVertex *pv = dynamic_cast<StMuPrimaryVertex*>( pvtx->At(ipv) );
    if(!pv) continue;

    const StThreeVectorF vtxPos = pv->position();
    Double_t pos[3];
    pos[0] = vtxPos.x();
    pos[1] = vtxPos.y();
    pos[2] = vtxPos.z();

    Double_t dca = kfgam.GetDistanceFromVertex(pos);

    if( dca < dcamin ) {
      dcamin = dca;
      pvmin = pv;
    }
  }//pv loop

  return pvmin;

}//findPV

//_____________________________________________________________________________
KFParticle* StUPCConvElMaker::makeKF(StMuTrack *gtrack, TClonesArray *gcov, Int_t pid) {

  Int_t idx = gtrack->index2Cov();
  if( idx < 0 ) return 0x0;
  StDcaGeometry *geom = dynamic_cast<StDcaGeometry*>( gcov->At(idx) );
  if( !geom ) return 0x0;

  Double_t xyzp[6];
  Double_t cov[21];
  geom->GetXYZ(xyzp, cov);

  KFParticle *kf = new KFParticle();
  kf->Create(xyzp, cov, gtrack->charge(), pid);

  return kf;

}//makeKF

//_____________________________________________________________________________
Bool_t StUPCConvElMaker::runMC() {

  TClonesArray *muMcTracks = mMuDst->mcArray(1);
  if( !muMcTracks ) return kFALSE;

  TDatabasePDG *pdgdat = TDatabasePDG::Instance();

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

  }//mc tracks loop

  return kTRUE;

}//runMC

//_____________________________________________________________________________
Int_t StUPCConvElMaker::Finish()
{
  //called at the end

  //write the output file
  mOutFile->cd();

  mUPCTree->Write();
  mHistList->Write("HistList", TObject::kSingleKey);

  mOutFile->Close();

  return kStOk;

}//Finish
















































