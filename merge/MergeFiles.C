
// jaroslav.adam@cern.ch

void MergeFiles(const string pattern, const string outfile) {

  gSystem->Load("../build/libstar-upc.so");

  //list the output files to a temporary file
  string tmpnam = "files.tmp";
  if( pattern.compare(tmpnam) != 0 ) {
    string command = "ls " + pattern + " > " + tmpnam + " 2>/dev/null";
    gSystem->Exec(command.c_str());
  }

  //load files to the merger
  TFileMerger *merg = new TFileMerger();
  cout << "Loading files for merging" << endl;
  ifstream in1(tmpnam.c_str());
  string line;
  Int_t nFiles = 0;
  while(getline(in1, line)) {
    //cout << line << endl;
    merg->AddFile(line.c_str(), kFALSE);
    nFiles++;
  }
  //files loaded, clean-up the temporary file
  in1.close();
  string rmcmd = "rm -f " + tmpnam + " 2>/dev/null";
  gSystem->Exec(rmcmd.c_str());
  if( nFiles == 0 ) {cout << "No files to merge, exiting." << endl; return;}
  cout << nFiles << " files loaded" << endl;

  //perform the merging
  merg->OutputFile( outfile.c_str() );
  Bool_t stat = merg->Merge();
  if (stat) {
    cout << "Successfully merged " << nFiles << " files" << endl;
  }
  else {
    cout << "Error in merging" << endl;
  }
  delete merg;

}//MergeFiles





















