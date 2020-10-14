
//_____________________________________________________________________________
void FitResultPrint(stringstream& str, const TFitResult& r1) {

  str << "Minimizer status: " << r1.Status() << "\n";
  str << "Cov matrix status: " << r1.CovMatrixStatus() << "\n";

  r1.FitResult::Print(str, kTRUE);

}//FitResultPrint

//_____________________________________________________________________________
void FitResultShow(TFitResult *res) {

  //test for cast in TFitResult

  cout << "--- FitResultShow ---" << endl;

  //using namespace ROOT::Fit;
  using namespace ROOT;

  stringstream s1, s2;

  //subobject of base class
  res->Fit::FitResult::Print(s1, kTRUE);

  //upcast
  //ROOT::Fit::FitResult *fit_res = dynamic_cast<ROOT::Fit::FitResult*>( res );
  //FitResult *fit_res = dynamic_cast<FitResult*>( res );
  Fit::FitResult *fit_res =
    dynamic_cast<Fit::FitResult*>( res );
  fit_res->Print(s2, kTRUE);


  cout << s1.str() << endl;
  cout << s2.str() << endl;

  cout << "--- FitResultShow ---" << endl;

}//FitResultPrint


