
void PrintStat() {

  TFile *in = TFile::Open("/star/u/jaroslav/test/star-upcDst-data/dstreader/ana_v1/merge/output.root");

  TH1I *hEvtCount = dynamic_cast<TH1I*>( in->Get("hEvtCount") );

  enum{kAnaL=1, kPair, kVtxId, kDphiBemc, kPID, kZvtx, kDvtx, kRap, kSign, kFin, kUPCJpsiB, kMaxCnt};
  stringstream st;

  //local counter
  st << "---------------------" << endl;
  st << Form("Local ana:  %.0f", hEvtCount->GetBinContent( kAnaL )) << endl;
  st << Form("Pair:       %.0f", hEvtCount->GetBinContent( kPair )) << endl;
  st << Form("Same vtx:   %.0f", hEvtCount->GetBinContent( kVtxId )) << endl;
  st << Form("Dphi BEMC:  %.0f", hEvtCount->GetBinContent( kDphiBemc )) << endl;
  st << Form("PID el:     %.0f", hEvtCount->GetBinContent( kPID )) << endl;
  st << Form("ZVtx:       %.0f", hEvtCount->GetBinContent( kZvtx )) << endl;
  st << Form("DVtx:       %.0f", hEvtCount->GetBinContent( kDvtx )) << endl;
  st << Form("Rapidity:   %.0f", hEvtCount->GetBinContent( kRap )) << endl;
  st << Form("Sign:       %.0f", hEvtCount->GetBinContent( kSign )) << endl;
  st << Form("Fin:        %.0f", hEvtCount->GetBinContent( kFin )) << endl;
  st << "---------------------" << endl;

  cout << st.str() << endl;

}//PrintStat



