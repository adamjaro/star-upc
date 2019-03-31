
//_____________________________________________________________________________
void fill_response_matrix(TTree &tree, RooUnfoldResponse &response) {

  Double_t jGenPt2, jRecPt2;
  Bool_t jAccept;

  tree.SetBranchAddress("jGenPt2", &jGenPt2);
  tree.SetBranchAddress("jRecPt2", &jRecPt2);
  tree.SetBranchAddress("jAccept", &jAccept);

  //tree loop
  for(Long64_t i=0; i<tree.GetEntries(); i++) {

    tree.GetEntry(i);

    if( jAccept == kTRUE ) {
      response.Fill(jRecPt2, jGenPt2);
    } else {
      response.Miss(jGenPt2);
    }

    //cout << jGenPt2 << " " << jRecPt2 << " " << jAccept << endl;

  }//tree loop


  tree.ResetBranchAddresses();

}//fill_response_matrix

