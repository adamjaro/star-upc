#ifndef StUPCTrack_h
#define StUPCTrack_h

//_____________________________________________________________________________
//    Class for UPC data
//    Author: Jaroslav Adam
//_____________________________________________________________________________

class TLorentzVector;
class TVector3;
class StUPCEvent;
class StUPCBemcCluster;
class StUPCVertex;

#include "TObject.h"

class StUPCTrack: public TObject
{

public:

  StUPCTrack();
  ~StUPCTrack() {}

  //public types
  //flags for mFlags, up to 8 (uchar)
  enum Flag{kBemc=0, kTof, kBemcProj};
  //particles for dE/dx, 4 particle species
  enum Part{kElectron=0, kPion, kKaon, kProton};

  void Clear(Option_t * /*option*/ ="");

  //setters
  void setFlag(Flag flg);

  void setPtEtaPhi(Double_t pt, Double_t eta, Double_t phi) {mPt = pt; mEta = eta; mPhi = phi;}

  void setDcaXY(Float_t dca) { mDcaXY = dca; }
  void setDcaZ(Float_t dca) { mDcaZ = dca; }

  void setCharge(Short_t ch) { mCharge = ch; }

  void setNhits(UShort_t nh) { mNhits = nh; }
  void setNhitsFit(UShort_t nf) { mNhitsFit = nf; }

  void setChi2(Double_t chi2) { mChi2 = chi2; }

  void setDEdxSignal(Double_t de) { mDEdxSignal = de; }
  void setNSigmasTPC(Part pt, Double_t nsig) { mNSigmasTPC[pt] = nsig; }

  void setBemcPtEtaPhi(Double_t pt, Double_t eta, Double_t phi) {mBemcPt = pt; mBemcEta = eta; mBemcPhi = phi;}
  void setBemcClusterId(UInt_t id) { mBemcClsId = id; }
  void setBemcHitE(Float_t he) { mBemcHitE = he; }
  void setBemcNHits(Short_t nh) { mBemcNHits = nh; }

  void setTofBeta(Float_t beta) { mTofBeta = beta; }

  void setVertexId(UInt_t id) { mVtxId = id; }

  void setEvent(StUPCEvent *evt) { mEvt = evt; }

  //getters
  Bool_t getFlag(Flag flg) const;

  void getPtEtaPhi(Double_t &pt, Double_t &eta, Double_t &phi) const {pt = mPt; eta = mEta; phi = mPhi;}
  Double_t getPt() const { return mPt; }
  Double_t getEta() const { return mEta; }
  Double_t getPhi() const { return mPhi; }
  void getLorentzVector(TLorentzVector &lvec, Double_t mass) const;
  void getMomentum(TVector3 &vec) const;

  Float_t getDcaXY() const { return mDcaXY; }
  Float_t getDcaZ() const { return mDcaZ; }

  Short_t getCharge() const { return mCharge; }

  UShort_t getNhits() const { return mNhits; }
  UShort_t getNhitsFit() const { return mNhitsFit; }

  Double_t getChi2() const { return mChi2; }

  Double_t getDEdxSignal() const { return mDEdxSignal; }
  Double_t getNSigmasTPC(Part pt) const { return mNSigmasTPC[pt]; }
  Double_t getNSigmasTPCElectron() const { return mNSigmasTPC[kElectron]; }
  Double_t getNSigmasTPCPion() const { return mNSigmasTPC[kPion]; }
  Double_t getNSigmasTPCKaon() const { return mNSigmasTPC[kKaon]; }
  Double_t getNSigmasTPCProton() const { return mNSigmasTPC[kProton]; }

  void getBemcPtEtaPhi(Double_t &pt, Double_t &eta, Double_t &phi) const {pt = mBemcPt; eta = mBemcEta; phi = mBemcPhi;}
  Double_t getBemcPt() const { return mBemcPt; }
  Double_t getBemcEta() const { return mBemcEta; }
  Double_t getBemcPhi() const { return mBemcPhi; }
  Double_t getBemcPmag() const;
  UInt_t getBemcClusterId() const { return mBemcClsId; }
  Float_t getBemcHitE() const { return mBemcHitE; }
  Short_t getBemcNHits() const { return mBemcNHits; }
  StUPCBemcCluster *getBemcCluster() const;
  void getBemcLorentzVector(TLorentzVector &blvec, Double_t mass) const;

  Float_t getTofBeta() const { return mTofBeta; }

  UInt_t getVertexId() const { return mVtxId; }
  StUPCVertex *getVertex() const;

  StUPCEvent *getEvent() const { return mEvt; }

private:

  StUPCTrack(const StUPCTrack &o); //not implemented
  StUPCTrack &operator=(const StUPCTrack &o); //not implemented

  UChar_t mFlags; // track flags

  Double32_t mPt; // pT at point of dca to primary vertex
  Double32_t mEta; // pseudorapidity at point of dca to primary vertex
  Double32_t mPhi; // phi at point of dca to primary vertex

  Float_t mDcaXY; // perpendicular dca to primary vertex of associated global track
  Float_t mDcaZ; // longitudinal dca to primary vertex of associated global track

  Short_t mCharge; // track electrical charge

  UShort_t mNhits; // total number of hits on track
  UShort_t mNhitsFit; // number of hits used in fit

  Double32_t mChi2; // chi2 of fit

  Double32_t mDEdxSignal; // measured dE/dx value
  static const Int_t mNpart = 4; // number of particle species with dE/dx identification
  Double32_t mNSigmasTPC[mNpart]; // dE/dx n sigmas for particle species

  Double32_t mBemcPt; // pT at BEMC radius
  Double32_t mBemcEta; // pseudorapidity at BEMC radius
  Double32_t mBemcPhi; // phi at BEMC radius
  UInt_t mBemcClsId; // id of BEMC cluster which track is matched to
  Float_t mBemcHitE; // energy of matched BEMC cluster
  Short_t mBemcNHits; // number of BEMC hits matched to the track

  Float_t mTofBeta; // velocity in units of c by TOF

  UInt_t mVtxId; // ID of primary vertex associated with track

  StUPCEvent *mEvt; //! pointer to current event, local use only

  ClassDef(StUPCTrack, 2)

};

#endif


















