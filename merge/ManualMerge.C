
//_____________________________________________________________________________
void ManualMerge() {

  gSystem->Load("../bin/libStUPCLib.so");

  TFileMerger *merg = new TFileMerger();

  merg->AddFile("/gpfs01/star/pwg/jaroslav/StUPCLib/ver2/trees/muDst_run1/prod/out/StUPC_muDst_run1_prod.root", kFALSE);
  merg->AddFile("/gpfs01/star/pwg/jaroslav/StUPCLib/ver2/trees/muDst_run1/low/out/StUPC_muDst_run1_low.root", kFALSE);
  merg->AddFile("/gpfs01/star/pwg/jaroslav/StUPCLib/ver2/trees/muDst_run1/mid/out/StUPC_muDst_run1_mid.root", kFALSE);
  merg->AddFile("/gpfs01/star/pwg/jaroslav/StUPCLib/ver2/trees/muDst_run1/high/out/StUPC_muDst_run1_high.root", kFALSE);

  merg->OutputFile( "/gpfs01/star/pwg/jaroslav/StUPCLib/ver2/trees/muDst_run1/StUPC_muDst_run1_all.root" );

  Bool_t stat = merg->Merge();
  if (stat) {
    cout<<"Done."<<endl;
  }
  else {
    cout<<"Error in merging"<<endl;
  }

}//ManualMerge

