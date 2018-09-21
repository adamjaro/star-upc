
//_____________________________________________________________________________
void FitResultPrint(stringstream& str, const TFitResult& r1) {

  str << "Minimizer status: " << r1.Status() << "\n";
  str << "Cov matrix status: " << r1.CovMatrixStatus() << "\n";

  r1.FitResult::Print(str, kTRUE);

}//FitResultPrint


