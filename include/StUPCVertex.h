#ifndef StUPCVertex_h
#define StUPCVertex_h

//_____________________________________________________________________________
//    Class for UPC data
//    Author: Jaroslav Adam
//_____________________________________________________________________________

#include "TObject.h"

class StUPCVertex: public TObject
{

public:

  StUPCVertex();
  ~StUPCVertex() {}

  //setters
  void setPosX(Float_t x) { mPosX = x; }
  void setPosY(Float_t y) { mPosY = y; }
  void setPosZ(Float_t z) { mPosZ = z; }

  void setErrX(Float_t x) { mErrX = x; }
  void setErrY(Float_t y) { mErrY = y; }
  void setErrZ(Float_t z) { mErrZ = z; }

  void setId(UInt_t id) { mId = id; }

  //getters
  Float_t getPosX() const { return mPosX; }
  Float_t getPosY() const { return mPosY; }
  Float_t getPosZ() const { return mPosZ; }

  Float_t getErrX() const { return mErrX; }
  Float_t getErrY() const { return mErrY; }
  Float_t getErrZ() const { return mErrZ; }

  UInt_t getId() const { return mId; }

private:

  StUPCVertex(const StUPCVertex &o); // not implemented
  StUPCVertex &operator=(const StUPCVertex &o); // not implemented

  Float_t mPosX; // position x
  Float_t mPosY; // position y
  Float_t mPosZ; // position z

  Float_t mErrX; // error in position x
  Float_t mErrY; // error in position y
  Float_t mErrZ; // error in position z

  UInt_t mId; // original vertex ID

  ClassDef(StUPCVertex, 1)

};

#endif

