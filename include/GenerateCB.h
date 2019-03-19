
//ROOT headers
#include "TF1.h"
#include "RooRealVar.h"
#include "RooCBShape.h"

//_____________________________________________________________________________
class GenerateCB {

  //Crystal Ball generator

public:

  //_____________________________________________________________________________
  GenerateCB(Double_t xmin, Double_t xmax, Double_t mv, Double_t sv, Double_t av, Double_t nv) {

    //parameters are min, max, mean, sigma, alpha, n

    //build the Crystal Ball PDF
    fX = new RooRealVar("x", "x", xmin, xmax);
    fMean = new RooRealVar("mean", "mean", mv);
    fSigma = new RooRealVar("sigma", "sigma", sv);
    fAlpha = new RooRealVar("alpha", "alpha", av);
    fN = new RooRealVar("n", "n", nv);
    fCBpdf = new RooCBShape("fCBpdf", "fCBpdf", *fX, *fMean, *fSigma, *fAlpha, *fN);

    //generator function
    fG = new TF1("fG", this, &GenerateCB::fg_inp, xmin, xmax, 0);

  }//GenerateCB

  //_____________________________________________________________________________
  ~GenerateCB() {
    delete fG;
    delete fCBpdf;
    delete fX;
    delete fMean;
    delete fSigma;
    delete fAlpha;
    delete fN;
  }//~GenerateCB

  //_____________________________________________________________________________
  Double_t Generate() {

    //generate value according to the Crystal Ball PDF

    return fG->GetRandom();

  }//Generate

private:

  //_____________________________________________________________________________
  Double_t fg_inp(Double_t *xval, Double_t *) {

    //input for generator function

    fX->setVal(xval[0]);
    return fCBpdf->getVal();

  }//fg_inp

  TF1 *fG; // generator function
  RooRealVar *fX, *fMean, *fSigma, *fAlpha, *fN; // CrystalBall parameters
  RooCBShape *fCBpdf; // Crystal Ball PDF

};


