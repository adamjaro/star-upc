#ifndef StUPCEvent_h
#define StUPCEvent_h

//_____________________________________________________________________________
//    Class for UPC data
//    Author: Jaroslav Adam
//_____________________________________________________________________________

class StUPCTrack;
class TClonesArray;
class StUPCBemcCluster;
class TIterator;
class StUPCVertex;
class TParticle;
class TArrayI;
class TArrayF;

class StUPCEvent
{

public:

  StUPCEvent();
  virtual ~StUPCEvent();

  //public types
  static const UInt_t mMaxTrg = 64; // max num of trigger IDs

  void clearEvent();

  //setters
  void setTrigger(UInt_t idx);
  void setRunNumber(Int_t run) { mRunNum = run; }
  void setEventNumber(Int_t num) { mEvtNum = num; }
  void setFillNumber(Int_t num) { mFillNum = num; }
  void setBunchCrossId(UInt_t id) { mbCrossId = id; }
  void setBunchCrossId7bit(UInt_t id) { mbCrossId7bit = id; }
  void setMagneticField(Double_t mag) { mMagField = mag; }

  void setZDCUnAttEast(UShort_t signal) { mZdcEastUA = signal; }
  void setZDCUnAttWest(UShort_t signal) { mZdcWestUA = signal; }
  void setZdcVertexZ(Float_t vtx) { mZdcVertexZ = vtx; }

  void setBBCSmallEast(UInt_t sum) { mBBCSmallEast = sum; }
  void setBBCSmallWest(UInt_t sum) { mBBCSmallWest = sum; }
  void setBBCLargeEast(UInt_t sum) { mBBCLargeEast = sum; }
  void setBBCLargeWest(UInt_t sum) { mBBCLargeWest = sum; }

  void setVPDSumEast(UShort_t sum) { mVPDSumEast = sum; }
  void setVPDSumWest(UShort_t sum) { mVPDSumWest = sum; }

  void setTOFMultiplicity(UShort_t tof) { mTofMult = tof; }
  void setBEMCMultiplicity(UInt_t be) { mBemcMult = be; }

  StUPCTrack *addTrack();

  StUPCBemcCluster *addCluster();

  StUPCVertex *addVertex();

  void setIsMC(Bool_t mc=kTRUE);
  TParticle *addMCParticle();

  Int_t makeArrayI(Int_t size);
  Int_t makeArrayF(Int_t size);

  //getters
  Bool_t getTrigger(UInt_t idx) const;
  Int_t getRunNumber() const { return mRunNum; }
  Int_t getEventNumber() const { return mEvtNum; }
  Int_t getFillNumber() const { return mFillNum; }
  UInt_t getBunchCrossId() const { return mbCrossId; }
  UInt_t getBunchCrossId7bit() const { return mbCrossId7bit; }
  Double_t getMagneticField() const { return mMagField; }

  UShort_t getZDCUnAttEast() const { return mZdcEastUA; }
  UShort_t getZDCUnAttWest() const { return mZdcWestUA; }
  Float_t getZdcVertexZ() const { return mZdcVertexZ/10.; } // convert from mm to cm

  UInt_t getBBCSmallEast() const { return mBBCSmallEast; }
  UInt_t getBBCSmallWest() const { return mBBCSmallWest; }
  UInt_t getBBCLargeEast() const { return mBBCLargeEast; }
  UInt_t getBBCLargeWest() const { return mBBCLargeWest; }

  UShort_t getVPDSumEast() const { return mVPDSumEast; }
  UShort_t getVPDSumWest() const { return mVPDSumWest; }

  UShort_t getTOFMultiplicity() const { return mTofMult; }
  UInt_t getBEMCMultiplicity() const { return mBemcMult; }

  Int_t getNumberOfTracks() const { return mNtracks; }
  StUPCTrack *getTrack(Int_t iTrack) const;

  Int_t getNumberOfClusters() const { return mNclusters; }
  StUPCBemcCluster *getCluster(Int_t iCls) const;
  StUPCBemcCluster *getClusterId(UInt_t clsId) const;
  TIterator *makeClustersIter() const;

  Int_t getNumberOfVertices() const { return mNvertices; }
  StUPCVertex *getVertex(Int_t iVtx) const;
  StUPCVertex *getVertexId(UInt_t vtxId) const;
  TIterator *makeVerticesIter() const;

  Bool_t getIsMC() const { return mMCParticles != NULL ? kTRUE : kFALSE; }
  Int_t getNumberOfMCParticles() const { return mNmc; }
  TParticle *getMCParticle(Int_t iMC) const;

  TArrayI *getArrayI() const { return mArrayI; }
  TArrayF *getArrayF() const { return mArrayF; }

private:

  StUPCEvent(const StUPCEvent &o); //not implemented
  StUPCEvent &operator=(const StUPCEvent &o); //not implemented

  ULong64_t mTrg; // fired trigger IDs

  Int_t mRunNum; // number of current run
  Int_t mEvtNum; // event number
  Int_t mFillNum; // beam fill number
  UInt_t mbCrossId; // bunch crossing ID
  UInt_t mbCrossId7bit; // bunch crossing ID 7bit
  Double32_t mMagField; // magnetic field

  UShort_t mZdcEastUA; // ZDC unattenuated signal, east
  UShort_t mZdcWestUA; // ZDC unattenuated signal, west
  Float_t mZdcVertexZ; // ZDC vertex z position, mm

  UInt_t mBBCSmallEast; // BBC truncated sum, small tiles, east
  UInt_t mBBCSmallWest; // BBC truncated sum, small tiles, west
  UInt_t mBBCLargeEast; // BBC truncated sum, large tiles, east
  UInt_t mBBCLargeWest; // BBC truncated sum, large tiles, west

  UShort_t mVPDSumEast; // VPD ADC sum east
  UShort_t mVPDSumWest; // VPD ADC sum west

  UShort_t mTofMult; // TOF multiplicity
  UInt_t mBemcMult; // BEMC multiplicity, number of all BEMC clusters in event

  TArrayI *mArrayI; // extension for other integer parameters
  TArrayF *mArrayF; // extension for other floating point parameters

  static TClonesArray *mgUPCTracks; // array of upc tracks
  TClonesArray *mUPCTracks; //-> array of upc tracks
  Int_t mNtracks; // number of upc tracks in event

  static TClonesArray *mgUPCBemcClusters; // array of BEMC clusters
  TClonesArray *mUPCBemcClusters; //-> array of BEMC clusters
  Int_t mNclusters; // number of BEMC clusters written in event

  static TClonesArray *mgUPCVertices; // array of UPC vertices
  TClonesArray *mUPCVertices; //-> array of UPC vertices
  Int_t mNvertices; // number of vertices written in event

  static TClonesArray *mgMCParticles; // array of MC particles
  TClonesArray *mMCParticles; // array of MC particles
  Int_t mNmc; // number of mc particles in event

  ClassDef(StUPCEvent, 1);
};

#endif













