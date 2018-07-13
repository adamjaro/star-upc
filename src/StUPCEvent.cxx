
//_____________________________________________________________________________
//    Class for UPC data
//    Author: Jaroslav Adam
//
//    UPC event containing trigger, ... and
//    arbitrary data in TArrayI and TArrayD containters
//_____________________________________________________________________________

//c++ headers

//root headers
#include "TClonesArray.h"
#include "TIterator.h"
#include "TParticle.h"
#include "TArrayI.h"
#include "TArrayF.h"

//local headers
#include "StUPCTrack.h"
#include "StUPCBemcCluster.h"
#include "StUPCVertex.h"

#include "StUPCEvent.h"

ClassImp(StUPCEvent);

TClonesArray *StUPCEvent::mgUPCTracks = 0;
TClonesArray *StUPCEvent::mgUPCBemcClusters = 0;
TClonesArray *StUPCEvent::mgUPCVertices = 0;
TClonesArray *StUPCEvent::mgMCParticles = 0;

//_____________________________________________________________________________
StUPCEvent::StUPCEvent():
  mTrg(0), mRunNum(0), mEvtNum(0), mFillNum(0), mbCrossId(0), mbCrossId7bit(0),
  mMagField(0), mZdcEastUA(0), mZdcWestUA(0), mBBCSmallEast(0), mBBCSmallWest(0),
  mBBCLargeEast(0), mBBCLargeWest(0), mTofMult(0), mBemcMult(0),
  mArrayI(0x0), mArrayF(0x0),
  mUPCTracks(0x0), mNtracks(0),
  mUPCBemcClusters(0x0), mNclusters(0),
  mUPCVertices(0x0), mNvertices(0),
  mMCParticles(0x0), mNmc(0)
{
  //default constructor

  for(UInt_t i=0; i<mMaxDsm; i++) mLastDSM[i] = 0;

  if(!mgUPCTracks) {
    mgUPCTracks = new TClonesArray("StUPCTrack");
    mUPCTracks = mgUPCTracks;
    mUPCTracks->SetOwner(kTRUE);
  }

  if(!mgUPCBemcClusters) {
    mgUPCBemcClusters = new TClonesArray("StUPCBemcCluster");
    mUPCBemcClusters = mgUPCBemcClusters;
    mUPCBemcClusters->SetOwner(kTRUE);
  }

  if(!mgUPCVertices) {
    mgUPCVertices = new TClonesArray("StUPCVertex");
    mUPCVertices = mgUPCVertices;
    mgUPCVertices->SetOwner(kTRUE);
  }

}//StUPCEvent

//_____________________________________________________________________________
StUPCEvent::~StUPCEvent()
{
  //destructor

  if(mArrayI) {delete mArrayI; mArrayI = 0x0;}
  if(mArrayF) {delete mArrayF; mArrayF = 0x0;}
  if(mUPCTracks) {delete mUPCTracks; mUPCTracks = 0x0;}
  if(mUPCBemcClusters) {delete mUPCBemcClusters; mUPCBemcClusters = 0x0;}
  if(mUPCVertices) {delete mUPCVertices; mUPCVertices = 0x0;}
  if(mMCParticles) {delete mMCParticles; mMCParticles = 0x0;}

}//~StUPCEvent

//_____________________________________________________________________________
void StUPCEvent::clearEvent()
{
  // clear event variables

  mTrg = 0;

  mBemcMult = 0;

  mUPCTracks->Clear("C");
  mNtracks = 0;

  mUPCBemcClusters->Clear("C");
  mNclusters = 0;

  mUPCVertices->Clear("C");
  mNvertices = 0;

  if(mMCParticles) {
    mMCParticles->Clear("C");
    mNmc = 0;
  }

  if(mArrayI) mArrayI->Reset();
  if(mArrayF) mArrayF->Reset();

}//clearEvent

//_____________________________________________________________________________
void StUPCEvent::setTrigger(UInt_t idx)
{
  //set fired trigger ID at position idx
  if( idx >= mMaxTrg ) return;

  mTrg |= (1 << idx);

}//setTrigger

//_____________________________________________________________________________
void StUPCEvent::setLastDSM(UShort_t dsm, UInt_t channel)
{
  //set last DSM word
  if( channel >= mMaxDsm ) return;

  mLastDSM[channel] = dsm;
}//setLastDSM

//_____________________________________________________________________________
StUPCTrack *StUPCEvent::addTrack()
{
  // construct new upc track

  return dynamic_cast<StUPCTrack*>( mUPCTracks->ConstructedAt(mNtracks++) );

}//addTrack

//_____________________________________________________________________________
StUPCBemcCluster *StUPCEvent::addCluster()
{
  // construct new BEMC cluster

  return dynamic_cast<StUPCBemcCluster*>( mUPCBemcClusters->ConstructedAt(mNclusters++) );

}//addCluster

//_____________________________________________________________________________
StUPCVertex *StUPCEvent::addVertex()
{
  //construct new UPC vertex

  return dynamic_cast<StUPCVertex*>( mUPCVertices->ConstructedAt(mNvertices++) );

}//addVertex

//_____________________________________________________________________________
void StUPCEvent::setIsMC(Bool_t mc) {

  // set the event as MC, initialize mc array

  if(!mc) return;

  if(!mgMCParticles) {
    mgMCParticles = new TClonesArray("TParticle");
    mMCParticles = mgMCParticles;
    mMCParticles->SetOwner(kTRUE);
  }

}//setIsMC

//_____________________________________________________________________________
TParticle *StUPCEvent::addMCParticle()
{
  // construct new mc TParticle

  if(!mMCParticles) return 0x0;

  return dynamic_cast<TParticle*>( mMCParticles->ConstructedAt(mNmc++) );

}//addMCParticle

//_____________________________________________________________________________
Int_t StUPCEvent::makeArrayI(Int_t size) {

  //create the object of TArrayI, skip if it has been already created
  //the array allows the event to be extended for other integer variables

  if( mArrayI ) return -999; // already initialized

  mArrayI = new TArrayI(size);

  return mArrayI->GetSize();

}//MakeArrayI

//_____________________________________________________________________________
Int_t StUPCEvent::makeArrayF(Int_t size) {

  //create the object of TArrayF, skip if it has been already created
  //the array allows the event to be extended for other floating point variables

  if( mArrayF ) return -999; // already initialized

  mArrayF = new TArrayF(size);

  return mArrayF->GetSize();

}//MakeArrayF

//_____________________________________________________________________________
Bool_t StUPCEvent::getTrigger(UInt_t idx) const
{
  //get fired trigger ID at position idx
  if( idx >= mMaxTrg ) return kFALSE;

  if( mTrg & (1 << idx) ) return kTRUE;
  return kFALSE;

}//setTrigger

//_____________________________________________________________________________
UShort_t StUPCEvent::getLastDSM(UInt_t channel) const
{
  //get last DSM word
  if( channel >= mMaxDsm ) return 0;

  return mLastDSM[channel];
}//getLastDSM

//_____________________________________________________________________________
StUPCTrack *StUPCEvent::getTrack(Int_t iTrack) const
{
  // get upc track

  StUPCTrack *track = dynamic_cast<StUPCTrack*>( mUPCTracks->At(iTrack) );
  if(track) track->setEvent( const_cast<StUPCEvent*>(this) );

  return track;

}//getTrack

//_____________________________________________________________________________
StUPCBemcCluster *StUPCEvent::getCluster(Int_t iCls) const
{
  // get BEMC cluster

  return dynamic_cast<StUPCBemcCluster*>( mUPCBemcClusters->At(iCls) );

}//getCluster

//_____________________________________________________________________________
StUPCBemcCluster *StUPCEvent::getClusterId(UInt_t clsId) const
{
  // get BEMC cluster according to origial ID

  //clusters loop
  StUPCBemcCluster *cls=0x0;
  TIterator *clsIter = makeClustersIter();
  while( (cls = dynamic_cast<StUPCBemcCluster*>( clsIter->Next() )) != NULL ) {

    //get cluster with a given ID
    if( cls->getId() == clsId ) {delete clsIter; return cls;}
  }//clusters loop

  delete clsIter;
  return 0x0;

}//getCluster

//_____________________________________________________________________________
TIterator *StUPCEvent::makeClustersIter() const
{
  // create iterator for BEMC clusters clones array

  return mUPCBemcClusters->MakeIterator();

}//getClustersIter

//_____________________________________________________________________________
StUPCVertex *StUPCEvent::getVertex(Int_t iVtx) const
{
  //get UPC vertex from clones array

  return dynamic_cast<StUPCVertex*>( mUPCVertices->At(iVtx) );

}//getVertex

//_____________________________________________________________________________
StUPCVertex *StUPCEvent::getVertexId(UInt_t vtxId) const
{
  // get vertex according to original ID

  //vertex loop
  StUPCVertex *vtx = 0x0;
  TIterator *vtxIter = makeVerticesIter();
  while( (vtx = dynamic_cast<StUPCVertex*>( vtxIter->Next() )) != NULL ) {

    //get vertex with a given ID
    if( vtx->getId() == vtxId ) {delete vtxIter; return vtx;}
  }//vertex loop

  delete vtxIter;
  return 0x0;

}//getVertexId

//_____________________________________________________________________________
TIterator *StUPCEvent::makeVerticesIter() const
{
  // create iterator for vertices clones array

  return mUPCVertices->MakeIterator();

}//makeVerticesIter

//_____________________________________________________________________________
TParticle *StUPCEvent::getMCParticle(Int_t iMC) const
{
  // get mc TParticle

  if(!mMCParticles) return 0x0;

  return dynamic_cast<TParticle*>( mMCParticles->At(iMC) );

}//getMCParticle

















