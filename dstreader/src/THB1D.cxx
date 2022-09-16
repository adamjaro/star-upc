
//c++ headers
#include <iostream>
#include <sstream>
#include <iomanip>
#include <vector>
#include <string>

//ROOT headers
#include "TMath.h"

//local headers
#include "THB1D.h"

using namespace std;

//_____________________________________________________________________________
THB1D::THB1D() {

  //cout << "THB1D" << endl;

  fHeight = 30;
  SetHeight(fHeight);
  fLeftMarg = 9;
  fTotHeight=0;

  fDigLines.reserve(10);

}//THB1D

//_____________________________________________________________________________
THB1D::THB1D(const char *name, const char *title, Int_t nbins, Double_t xmin, Double_t xmax):
  TH1D(name, title, nbins, xmin, xmax) {

  fHeight = 30;
  SetHeight(fHeight);
  fLeftMarg = 9;
  fTotHeight=0;

  fDigLines.reserve(10);

  fLogy = kFALSE;

}//THB1D

//_____________________________________________________________________________
THB1D::~THB1D() {

  //cout << "~THB1D" << endl;

}//~THB1D

//_____________________________________________________________________________
void THB1D::SetHeight(Int_t h) {

  fHeight = h;

  fYLabels.clear();
  fYLabels.reserve(fHeight);

  fHistLines.clear();
  fHistLines.reserve(fHeight);

}//SetHeight

//_____________________________________________________________________________
ostream& operator<<(std::ostream& os, THB1D& hx) {

  //Y axis labels
  Int_t lyval=0;
  Int_t yunit = 1;
  Int_t ytick = (Int_t) ceil( hx.GetMaximum()/hx.fHeight/yunit );
  ytick *= yunit;

  for(Int_t i=0; i<hx.fHeight; i++) {
    hx.fYLabels.push_back(string(""));
  }
  for(vector<string>::iterator it = hx.fYLabels.begin(); it != hx.fYLabels.end(); it++) {
    lyval += ytick;
    stringstream st;
    st << lyval;
    *it = st.str();
  }

  //fill histogram representation strings
  Int_t yprev=0;
  Int_t nbins = hx.GetNbinsX();
  for(Int_t i=0; i<hx.fHeight; i++) {
    hx.fHistLines.push_back(string(nbins, ' '));
  }
  for(Int_t ibin=1; ibin <= nbins; ibin++) {
    if( ((Int_t) hx.GetBinContent(ibin)) == 0 ) continue;
    Int_t ypos = (Int_t) hx.GetBinContent(ibin)/ytick;
    if( ypos >= hx.fHeight ) {
      ypos = hx.fHeight-1;
    }
    hx.fHistLines[ypos].replace(ibin-1, 1, "-");

    if( ibin == 1 ) {
      yprev = ypos;
      continue;
    }

    if( ypos > yprev ) {
      for(Int_t yc = yprev; yc < ypos; yc++) {
        hx.fHistLines[yc].replace(ibin-1, 1, "I");
      }
    }

    if( yprev > ypos ) {
      for(Int_t yc = ypos; yc < yprev; yc++) {
        hx.fHistLines[yc].replace(ibin-2, 1, "I");
      }
    }

    yprev = ypos;
  }

  //bin content
  Int_t maxdig = (Int_t)( log10(hx.GetMaximum()) + 1 );
  for(Int_t i=0; i<maxdig; i++) {
    hx.fDigLines.push_back(string(nbins, ' '));
  }
  for(Int_t ibin=1; ibin <= nbins; ibin++) {
    Int_t cnt = (Int_t) hx.GetBinContent(ibin);
    stringstream st;
    st.width(maxdig);
    st.fill('_');
    st << right << cnt;
    string scnt( st.str() );
    string sdig;
    for(Int_t idig=0; idig<maxdig; idig++) {
      sdig = scnt[idig];
      if( sdig == "_" ) continue;
      hx.fDigLines[idig].replace(ibin-1, 1, sdig);
    }
  }



  //print the histogram
  Int_t toth = hx.fTotHeight;
  Int_t digmarg = maxdig + 1;
  Int_t ilin = hx.fHeight-1;
  os << endl; toth--;
  for(vector<string>::reverse_iterator it = hx.fYLabels.rbegin(); it != hx.fYLabels.rend(); it++) {
    os.width(hx.fLeftMarg);
    os << right << *it;
    os.width(digmarg);
    os << " ";
    os.width(nbins+2);
    os << hx.fHistLines[ilin--] << endl; toth--;
  }
    os << endl; toth--;

  for(Int_t idig=0; idig<maxdig; idig++) {
    os.width(hx.fLeftMarg);
    if( idig==0 ) {
      os << "CONTENTS";
    } else {
      os << " ";
    }
    os.width(digmarg);
    //os << " ";
    os << pow(10,maxdig-idig-1);
    os.width(nbins+2);
    os << hx.fDigLines[idig] << endl; toth--;
  }
    os << endl; toth--;

  //entries, overflow and underflow
  os.width(hx.fLeftMarg);
  os << "ENTRIES" << " = ";
  os.width(9);
  os << left << hx.GetEntries();
  os << "UNDERFLOW = ";
  os.width(4);
  os << hx.GetBinContent(0);
  os << " OVERFLOW = ";
  os << hx.GetBinContent(nbins+1);
  os << endl; toth--;
  os << endl; toth--;

  while( toth-- > 0 ) {
    os << endl;// toth--;
  }

  //os << "size: " << hx.fHistLines.size() << endl;
  //os << "capacity: " << hx.fHistLines.capacity() << endl;

  //clean-up
  hx.fYLabels.clear();
  hx.fHistLines.clear();
  hx.fDigLines.clear();

  //os << "size: " << hx.fHistLines.size() << endl;
  //os << "capacity: " << hx.fHistLines.capacity() << endl;

  //os << "ftoth: " << hx.fTotHeight << endl;
  //os << "toth: " << toth;
  //os << "ytick: " << ytick;

  return os;
}











































