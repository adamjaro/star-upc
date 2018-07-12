#ifndef StUPCTrgData_h
#define StUPCTrgData_h

//_____________________________________________________________________________
//    Class for UPC data
//    Author: Jaroslav Adam
//_____________________________________________________________________________

class StUPCTrgData
{

public:

  StUPCTrgData();
  virtual ~StUPCTrgData() {}

  //public types
  enum BeamDirection{kEast=0, kWest};
  enum SmallLarge{kSmall=0, kLarge};

  //Setters
  void setBBCadc(BeamDirection eastwest, UShort_t adc, Int_t ipmt);
  void setBBCtdc(BeamDirection eastwest, UShort_t tdc, Int_t ipmt);

  void setZDCadc(BeamDirection eastwest, UShort_t adc, Int_t ipmt);
  void setZDCPmtTdc(BeamDirection eastwest, UShort_t tdc, Int_t ipmt);

  void setZDCAttEast(UShort_t zdc) { mZDCAttEast = zdc; }
  void setZDCAttWest(UShort_t zdc) { mZDCAttWest = zdc; }
  void setZDCTdcEast(UShort_t zdc) { mZDCTdcEast = zdc; }
  void setZDCTdcWest(UShort_t zdc) { mZDCTdcWest = zdc; }
  void setZDCTimeDiff(UShort_t zdc) { mZDCTimeDiff = zdc; }

  //Getters
  UShort_t getBBCadc(BeamDirection eastwest, Int_t ipmt) const;
  UShort_t getBBCtdc(BeamDirection eastwest, Int_t ipmt) const;

  UInt_t getBBCSum(SmallLarge tiles, BeamDirection eastwest, UShort_t tdcmin, UShort_t tdcmax, UShort_t adcmin) const;

  UShort_t getZDCadc(BeamDirection eastwest, Int_t ipmt) const;
  UShort_t getZDCPmtTdc(BeamDirection eastwest, Int_t ipmt) const;

  UInt_t getZDCadcSum(BeamDirection eastwest) const;

  UShort_t getZDCAttEast() const { return mZDCAttEast; }
  UShort_t getZDCAttWest() const { return mZDCAttWest; }
  UShort_t getZDCTdcEast() const { return mZDCTdcEast; }
  UShort_t getZDCTdcWest() const { return mZDCTdcWest; }
  UShort_t getZDCTimeDiff() const { return mZDCTimeDiff; }

private:

  StUPCTrgData(const StUPCTrgData &o); //not implemented
  StUPCTrgData &operator=(const StUPCTrgData &o); //not implemented

  static const Int_t mNbbcPMT = 24; //number of BBC PMTs
  UShort_t mBBCadc[2][mNbbcPMT]; //BBC ADC signals, east and west
  UShort_t mBBCtdc[2][mNbbcPMT]; //BBC TDC signals, east and west

  static const Int_t mIPmtLastSmall = 16; // ipmt for last small BBC tile

  static const Int_t mNzdcPMT = 3; //number of ZDC PMTs
  UShort_t mZDCadc[2][mNzdcPMT]; // ZDC ADC signals, east and west
  UShort_t mZDCPmtTdc[2][mNzdcPMT]; //ZDC TDC signals, east and west
  UShort_t mZDCAttEast; //ZDC attenuated signal, east
  UShort_t mZDCAttWest; //ZDC attenuated signal, west
  UShort_t mZDCTdcEast; //ZDC TDC signal, east
  UShort_t mZDCTdcWest; //ZDC TDC signal, west
  UShort_t mZDCTimeDiff; //ZDC time difference;



  ClassDef(StUPCTrgData, 1)
};

#endif












