
//_____________________________________________________________________________
class cb_gen {

  //Crystal Ball generator

public:

  //_____________________________________________________________________________
  cb_gen(Double_t xmin, Double_t xmax, Double_t mv, Double_t sv, Double_t av, Double_t nv) {

    //parameters are min, max, mean, sigma, alpha, n

    //build the Crystal Ball PDF
    x = new RooRealVar("x", "x", xmin, xmax);
    mean = new RooRealVar("mean", "mean", mv);
    sigma = new RooRealVar("sigma", "sigma", sv);
    alpha = new RooRealVar("alpha", "alpha", av);
    n = new RooRealVar("n", "n", nv);
    cbpdf = new RooCBShape("cbpdf", "cbpdf", *x, *mean, *sigma, *alpha, *n);

    //generator function
    fg = new TF1("fg", this, &cb_gen::fg_inp, xmin, xmax, 0);

  }//cb_gen

  //_____________________________________________________________________________
  ~cb_gen() {
    delete fg;
    delete cbpdf;
    delete x;
    delete mean;
    delete sigma;
    delete alpha;
    delete n;
  }//~cb_gen

  //_____________________________________________________________________________
  Double_t generate() {

    //generate value according to the Crystal Ball PDF

    return fg->GetRandom();

  }//generate

private:

  //_____________________________________________________________________________
  Double_t fg_inp(Double_t *xval, Double_t *) {

    //input for generator function

    x->setVal(xval[0]);
    return cbpdf->getVal();

  }//fg_inp

  TF1 *fg; // generator function
  RooRealVar *x, *mean, *sigma, *alpha, *n; // CrystalBall parameters
  RooCBShape *cbpdf; // Crystal Ball PDF

};

//_____________________________________________________________________________
void cb_generate_n(cb_gen &gen, TH1D &hx, Int_t n) {

  //test function to fill a histogram with n events

  for(Int_t i=0; i<n; i++) {
    hx.Fill( gen.generate() );
  }

}//cb_generate_n

//_____________________________________________________________________________
void cb_apply_smear(cb_gen &gen, TTree &mctree, TH1D &hx) {

  //test function to introduce smearing to the original distribution
  Double_t pt0, pt1, gpt0, gpt1;
  mctree.SetBranchAddress("jT0pT", &pt0);
  mctree.SetBranchAddress("jT1pT", &pt1);
  mctree.SetBranchAddress("jGenP0pT", &gpt0);
  mctree.SetBranchAddress("jGenP1pT", &gpt1);

  //tree loop
  for(Int_t i=0; i<mctree.GetEntries(); i++) {

    mctree.GetEntry(i);

    //pt0 -= 0.01;
    //pt1 -= 0.01;

    //pt0 += gen.generate();
    //pt1 += gen.generate();

    pt0 = pt0*(gen.generate() + 1.);
    pt1 = pt1*(gen.generate() + 1.);

    Double_t r0 = (pt0 - gpt0)/gpt0;
    Double_t r1 = (pt1 - gpt1)/gpt1;

    hx.Fill(r0);
    hx.Fill(r1);

  }//tree loop

  mctree.ResetBranchAddresses();

}//cb_apply_smear_n






















