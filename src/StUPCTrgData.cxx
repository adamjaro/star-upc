
//_____________________________________________________________________________
//    Class for UPC data
//    Author: Jaroslav Adam
//
//    Details on BBC and ZDC, optional part of StUPCEvent
//_____________________________________________________________________________

//root headers
#include "Rtypes.h"

//local headers
#include "StUPCTrgData.h"

ClassImp(StUPCTrgData);

//_____________________________________________________________________________
StUPCTrgData::StUPCTrgData():
  mZDCAttEast(0), mZDCAttWest(0), mZDCTdcEast(0),
  mZDCTdcWest(0), mZDCTimeDiff(0)
{
  //default constructor

  for(Int_t i=0; i<mNbbcPMT; i++) {
    mBBCadc[kEast][i] = 0;
    mBBCadc[kWest][i] = 0;
    mBBCtdc[kEast][i] = 0;
    mBBCtdc[kWest][i] = 0;
  }

  for(Int_t i=0; i<mNzdcPMT; i++) {
    mZDCadc[kEast][i] = 0;
    mZDCadc[kWest][i] = 0;
    mZDCPmtTdc[kEast][i] = 0;
    mZDCPmtTdc[kWest][i] = 0;
  }

}//StUPCTrgData

//_____________________________________________________________________________
void StUPCTrgData::setBBCadc(BeamDirection eastwest, UShort_t adc, Int_t ipmt)
{
  //set BBC ADC signal, east and west

  if( ipmt < 1 || ipmt > mNbbcPMT ) return;

  mBBCadc[eastwest][ipmt-1] = adc;

}//setBBCadc

//_____________________________________________________________________________
void StUPCTrgData::setBBCtdc(BeamDirection eastwest, UShort_t tdc, Int_t ipmt)
{
  //set BBC TDC signal, east and west

  if( ipmt < 1 || ipmt > mNbbcPMT ) return;

  mBBCtdc[eastwest][ipmt-1] = tdc;

}//setBBCtdc

//_____________________________________________________________________________
void StUPCTrgData::setZDCadc(BeamDirection eastwest, UShort_t adc, Int_t ipmt)
{
  //set ZDC ADC signals on PMTs

  if( ipmt < 1 || ipmt > mNzdcPMT ) return;

  mZDCadc[eastwest][ipmt-1] = adc;

}//setZDCadc

//_____________________________________________________________________________
void StUPCTrgData::setZDCPmtTdc(BeamDirection eastwest, UShort_t tdc, Int_t ipmt)
{
  //set ZDC TDC signals on PMTs

  if( ipmt < 1 || ipmt > mNzdcPMT ) return;

  mZDCPmtTdc[eastwest][ipmt-1] = tdc;

}//setZDCPmtTdc

//_____________________________________________________________________________
UShort_t StUPCTrgData::getBBCadc(BeamDirection eastwest, Int_t ipmt) const
{
  //get BBC ADC signal, east and west

  if( ipmt < 1 || ipmt > mNbbcPMT ) return 0;

  return mBBCadc[eastwest][ipmt-1];

}//getBBCadc

//_____________________________________________________________________________
UShort_t StUPCTrgData::getBBCtdc(BeamDirection eastwest, Int_t ipmt) const
{
  //get BBC TDC signal, east and west

  if( ipmt < 1 || ipmt > mNbbcPMT ) return 0;

  return mBBCtdc[eastwest][ipmt-1];

}//getBBCtdc

//_____________________________________________________________________________
UInt_t StUPCTrgData::getBBCSum(SmallLarge tiles, BeamDirection eastwest, UShort_t tdcmin, UShort_t tdcmax, UShort_t adcmin) const
{
  //BBC truncated sum over small and large tiles, east and west

  //limits on loop selecting small or large tiles
  Int_t limits[2] = {1,1};
  if( tiles == kSmall ) {
    limits[0] = 1;
    limits[1] = mIPmtLastSmall;
  }
  if( tiles == kLarge ) {
    limits[0] = mIPmtLastSmall+1;
    limits[1] = mNbbcPMT;
  }

  UInt_t sum = 0;
  //small tile loop
  for(Int_t ipmt=limits[0]; ipmt<=limits[1]; ipmt++) {

    //ADC threshold
    if( mBBCadc[eastwest][ipmt-1] < adcmin ) continue;
    //TDC window
    if( mBBCtdc[eastwest][ipmt-1] < tdcmin || mBBCtdc[eastwest][ipmt-1] > tdcmax ) continue;

    sum += mBBCadc[eastwest][ipmt-1];
  }//small tile loop

  return sum;

}//getBBCSmall

//_____________________________________________________________________________
UShort_t StUPCTrgData::getZDCadc(BeamDirection eastwest, Int_t ipmt) const
{
  //get ZDC ADC signals on PMTs

  if( ipmt < 1 || ipmt > mNzdcPMT ) return 0;

  return mZDCadc[eastwest][ipmt-1];

}//setZDCadc

//_____________________________________________________________________________
UShort_t StUPCTrgData::getZDCPmtTdc(BeamDirection eastwest, Int_t ipmt) const
{
  //get ZDC TDC signals on PMTs

  if( ipmt < 1 || ipmt > mNzdcPMT ) return 0;

  return mZDCPmtTdc[eastwest][ipmt-1];

}//setZDCPmtTdc

//_____________________________________________________________________________
UInt_t StUPCTrgData::getZDCadcSum(BeamDirection eastwest) const
{
  //sum over ZDC ADC signals on PMTs
  UInt_t sum = 0;

  for(Int_t i=0; i<mNzdcPMT; i++) {
    sum += mZDCadc[eastwest][i];
  }

  return sum;

}//getZDCadcSum

























































