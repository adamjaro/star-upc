
//_____________________________________________________________________________
void get_bins(vector<Double_t>& bins, list<Double_t>& valAll, list<Double_t>& valSel, Double_t prec, Double_t delt) {

  //sort the lists
  valAll.sort();
  valSel.sort();

  //range for bin edges
  Double_t minval = *(valSel.cbegin());
  Double_t maxval = *(valSel.crbegin());
  cout << "Range for bin edges: " << minval << " " << maxval << endl;

  //move both lists to the start of the range
  list<Double_t>::const_iterator itAll = valAll.cbegin();
  list<Double_t>::const_iterator itSel = valSel.cbegin();
  while( *itAll < minval ) itAll++;
  while( *itSel < minval ) itSel++;

  //starting edge
  bins.push_back(minval);

  //initialize the counters and current maximum
  UInt_t nsel = 0;
  UInt_t nall = 0;
  Double_t cmax = minval + delt;
  //find bin edges
  while(1) {
    //move to the current limit
    while( itSel != valSel.cend() and *itSel < cmax ) {
      nsel++;
      itSel++;
    }
    while( itAll != valAll.cend() and *itAll < cmax ) {
      nall++;
      itAll++;
    }

    //relative Binomial error
    Double_t rel = 1.;
    if( nsel != 0 and nall != 0 and nsel != nall) {
      Double_t xsel = Double_t(nsel);
      Double_t xall = Double_t(nall);
      rel = TMath::Sqrt( (xall-xsel)/(xall*xsel) );
    }

    //test for maximal allowed error
    if( rel < prec ) {
      //bin edge found, max relative error satisfied
      bins.push_back(cmax);
      //reset the counters for next bin
      nall = 0;
      nsel = 0;
      cout << "bin edge: " << cmax << endl;
    }

    //increment the current limit
    cmax += delt;

    //test for end of momenta interval
    if( cmax > maxval ) {
      //set last found edge to the end of values interval and finish
      bins[bins.size()-1] = maxval;
      break;
    }

  }//find bin edges

}//get_bins



























