
//_____________________________________________________________________________
//    Class for UPC data
//    Author: Jaroslav Adam
//
//    contains parameters of primary vertex relevant for UPC analysis
//_____________________________________________________________________________

//c++ headers

//root headers

//local headers
#include "StUPCVertex.h"

ClassImp(StUPCVertex);

//_____________________________________________________________________________
StUPCVertex::StUPCVertex(): TObject(),
  mPosX(0), mPosY(0), mPosZ(0), mErrX(0), mErrY(0), mErrZ(0),
  mId(0)
{
  //default constructor

}//StUPCVertex



