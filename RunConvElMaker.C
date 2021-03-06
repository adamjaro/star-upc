
//run with stderr to stdout redirection in c shell:
//
//  rm run.log
//  root4star -l -b -q RunConvElMaker.C |& cat > run.log &


//_____________________________________________________________________________
void RunConvElMaker(string filelist="txt/test_low_gpfs.list", Int_t nFiles=1, string outfile="trees/StUPC_conv.root") {

  //maker config
  Bool_t isMC = kFALSE; // data or MC

  Bool_t useClusterParam = kFALSE; // use BEMC cluster conditions below
  Int_t sizeMax = 4;
  Float_t energySeed = 0.4;
  Float_t energyAdd = 0.001;
  Float_t energyThresholdAll = 0.4;


  //load libraries to work with muDst
  gROOT->Macro("loadMuDst.C");

  // Load St_db_Maker and co
  gSystem->Load("StDbLib.so");
  gSystem->Load("StDbBroker.so");
  gSystem->Load("St_db_Maker");

  // Load Emc libraries
  gSystem->Load("StDaqLib");
  gSystem->Load("StEmcRawMaker");
  gSystem->Load("StEmcADCtoEMaker");
  gSystem->Load("StPreEclMaker");
  gSystem->Load("StEpcMaker");

  //load the analysis maker compiled before with cons
  gSystem->Load("StUPCFilterMaker.so");

  //create chain directory-like structure for maker
  //top level
  StChain *chain = new StChain;
  //maker to access muDST data
  StMuDstMaker *maker = new StMuDstMaker(0, 0, "", filelist.c_str(), "", nFiles);

  //St_db_Maker for Emc calibration
  St_db_Maker *db1 = new St_db_Maker("db","$HOME/StarDb","MySQL:StarDb","$STAR/StarDb");
  // Maker to apply calibration
  StEmcADCtoEMaker *adc_to_e = new StEmcADCtoEMaker();
  adc_to_e->setPrint(kFALSE);
  // Makers for clusterfinding
  StPreEclMaker *pre_ecl = new StPreEclMaker();
  pre_ecl->setPrint(kFALSE);
  StEpcMaker *epc = new StEpcMaker();
  epc->setPrint(kFALSE);
  //analysis maker
  StUPCConvElMaker *anaMaker = new StUPCConvElMaker(maker, outfile); //maker for muDst passed to the constructor

  //configure the analysis maker
  if(isMC) anaMaker->setIsMC();

  //no debug printouts
  StMuDebug::setLevel(0);

  Int_t nevt = maker->chain()->GetEntries();
  //nevt=300;
  cout << "Number of events: " << nevt << endl;

  //initialize the makers
  chain->Init();

  //apply BEMC clustering parameters if requested
  if( useClusterParam ) {
    //call need to happen after the StPreEclMaker has been initialized
    pre_ecl->SetClusterConditions("bemc", sizeMax, energySeed, energyAdd, energyThresholdAll, kFALSE);
  }
  cout << "-------------------------------------------" << endl;
  cout << "StEmcOldFinder cluster parameters for BEMC:" << endl;
  StEmcOldFinder *finder = dynamic_cast<StEmcOldFinder*>(pre_ecl->finder());
  //bemc has index 1, according to StRoot/StEmcUtil/others/emcDetectorName.h and StPreEclMaker.cxx
  cout << "  sizeMax: " << finder->sizeMax(1) << endl;
  cout << "  energySeed: " << finder->energySeed(1) << endl;
  cout << "  energyAdd: " << finder->energyAdd(1) << endl;
  cout << "  energyThresholdAll: " << finder->energyThresholdAll(1) << endl;
  cout << "-------------------------------------------" << endl;

  //loop over events
  chain->EventLoop(nevt);
  chain->Finish();

  //release allocated memory
  delete chain;







}//RunFilterMaker

