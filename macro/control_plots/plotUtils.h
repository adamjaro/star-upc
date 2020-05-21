#ifndef plotutils_h
#define plotutils_h

//_____________________________________________________________________________
void AdjustCanvas(TCanvas *can, Int_t nCol, Int_t nRow, Float_t bmg=-1., Float_t lmg=-1., Float_t tmg=-1.)
{

  can->Clear();
  can->SetFillColor(0);
  can->Divide(nCol,nRow);
/*
  for(Int_t i=1; i<=nCol*nRow; i++) {
    if(bmg >= 0.) can->cd(i)->SetBottomMargin(  bmg );
    if(lmg >= 0.) can->cd(i)->SetLeftMargin(    lmg );
    if(tmg >= 0.) can->cd(i)->SetTopMargin(     tmg );
  }
*/
}//AdjustCanvas

//_____________________________________________________________________________
TLegend *PrepareLeg(Double_t xl, Double_t yl, Double_t dxl, Double_t dyl, Float_t tsiz=0.045) {

  TLegend* leg = new TLegend(xl, yl, xl+dxl, yl+dyl);
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetTextSize(tsiz);

  return leg;

}//PrepareLeg

//_____________________________________________________________________________
TLegend *UoLegLin(TH1 *hx, Double_t xl, Double_t yl, Double_t dxl, Double_t dyl, Float_t tsiz=0.045) {

  //legend for underflow and overflow

  TLegend *leg = PrepareLeg(xl, yl, dxl, dyl, tsiz);

  string ovfstr = Form("Underflow: %.0f, overflow: %.0f", hx->GetBinContent(0), hx->GetBinContent(hx->GetNbinsX()+1));
  leg->AddEntry((TObject*)0, ovfstr.c_str(), "");

  return leg;

}//UoLegLin

//_____________________________________________________________________________
TLine *colLin(Color_t col, Width_t w=4, Style_t st=kSolid) {

  //create line of a given color
  TLine *lin = new TLine();
  lin->SetLineColor(col);
  lin->SetLineWidth(w);
  lin->SetLineStyle(st);

  return lin;

}//colLine

//_____________________________________________________________________________
Int_t getNBins(Double_t xbin, Double_t xmin, Double_t& xmax) {

  //get number of bins given bin size and range, adjust max to pass the bins

  Int_t nbins = (Int_t) TMath::Ceil( (xmax-xmin)/xbin ); // round-up value
  xmax = xmin + (Double_t) xbin*nbins; // move max up to pass the bins

  return nbins;

}//getNBins

//_____________________________________________________________________________
TCanvas *boxCanvas() {

  //make rectangular canvas
  TCanvas *can = new TCanvas("c3", "Analysis", 768., 768.);
  //TCanvas *can = new TCanvas("c3", "Analysis", 900., 900.); // for high-res png
  gStyle->SetOptStat("");//nemruo
  gStyle->SetPalette(1);
  gStyle->SetLineWidth(2);      //axis line
  gStyle->SetFrameLineWidth(2); //frame line
  TGaxis::SetMaxDigits(3);
  Double_t lmg = 0.3;
  Double_t bmg = 0.3;
  AdjustCanvas(can, 1, 1, bmg, lmg);

  //can->SetGrid();

  return can;

}//boxCanvas

//_____________________________________________________________________________
void SetLineMarkerColor(TH1 *hx, Int_t col) {

  hx->SetLineColor(col);
  hx->SetMarkerColor(col);

}//SetLineMarkerColor

//_____________________________________________________________________________
void setH1Col(TH1 *hx, Int_t col) {

  SetLineMarkerColor(hx, col);

}//setH1Col

//_____________________________________________________________________________
void SetH1D(TH1D *hx) {

  //set common histos properties
  hx->SetOption("E1");
  //hx->SetOption("E2");
  hx->SetMarkerStyle(kFullCircle);
  hx->SetMarkerColor(kBlack); hx->SetLineColor(kBlack);
  //hx->SetMarkerColor(kBlue+1); hx->SetLineColor(kBlue+1);
  //hx->SetMarkerSize(0.7);
  hx->SetLineWidth(2);
  hx->SetYTitle("Counts");
  Float_t siz = 0.035; // 0.05
  hx->SetTitleSize(siz);       hx->SetLabelSize(siz);
  hx->SetTitleSize(siz, "Y");  hx->SetLabelSize(siz, "Y");

}//SetH1D

//_____________________________________________________________________________
TH1D *PrepareTH1D(const char *name, Int_t nbins, Double_t xmin, Double_t xmax)
{

  TH1D *hx = new TH1D(name, name, nbins, xmin, xmax);
  SetH1D(hx);
  hx->SetTitle("");

  return hx;

}//PrepareTH1D

//_____________________________________________________________________________
TH1D *PrepareTH1D(const char *name, Double_t binsiz, Double_t xmin, Double_t xmax)
{

  Int_t nbins = (Int_t) TMath::Ceil( (xmax-xmin)/binsiz ); // round-up value
  xmax = xmin + (Double_t) binsiz*nbins; // move max up to pass the bins

  return PrepareTH1D(name, nbins, xmin, xmax);

}//PrepareTH1D

//_____________________________________________________________________________
TH2D *PrepareTH2D(const char *name, Int_t nbinsX, Double_t xmin, Double_t xmax, Int_t nbinsY, Double_t ymin, Double_t ymax)
{

  TH2D *hx = new TH2D(name, name, nbinsX, xmin, xmax, nbinsY, ymin, ymax);
  hx->SetOption("COLZ");
  Float_t siz = 0.035;
  hx->SetTitleSize(siz);       hx->SetLabelSize(siz);
  hx->SetTitleSize(siz, "Y");  hx->SetLabelSize(siz, "Y");
  hx->SetTitleSize(siz, "Z");  hx->SetLabelSize(siz, "Z");
  hx->SetTitle("");
  return hx;

}//PrepareTH2D

//_____________________________________________________________________________
TH2D *PrepareTH2D(const char *name, Double_t xbin, Double_t xmin, Double_t xmax, Double_t ybin, Double_t ymin, Double_t ymax)
{
  //bins along x
  Int_t nbinsX = (Int_t) TMath::Ceil( (xmax-xmin)/xbin ); // round-up value
  xmax = xmin + (Double_t) xbin*nbinsX; // move max up to pass the bins

  //bins along y
  Int_t nbinsY = (Int_t) TMath::Ceil( (ymax-ymin)/ybin ); // round-up value
  ymax = ymin + (Double_t) ybin*nbinsY; // move max up to pass the bins

  return PrepareTH2D(name, nbinsX, xmin, xmax, nbinsY, ymin, ymax);

}//PrepareTH2D

//_____________________________________________________________________________
TH2I *PrepareTH2I(const char *name, Int_t nbinsX, Double_t xmin, Double_t xmax, Int_t nbinsY, Double_t ymin, Double_t ymax)
{

  TH2I *hx = new TH2I(name, name, nbinsX, xmin, xmax, nbinsY, ymin, ymax);
  hx->SetOption("COLZ");
  Float_t siz = 0.05;
  hx->SetTitleSize(siz);       hx->SetLabelSize(siz);
  hx->SetTitleSize(siz, "Y");  hx->SetLabelSize(siz, "Y");
  hx->SetTitleSize(siz, "Z");  hx->SetLabelSize(siz, "Z");
  hx->SetTitle("");
  return hx;

}//PrepareTH2I

//_____________________________________________________________________________
TH3I *PrepareTH3I(const char *nm, Int_t nx, Double_t xl, Double_t xh, Int_t ny, Double_t yl, Double_t yh, Int_t nz, Double_t zl, Double_t zh) {

  TH3I *hx = new TH3I(nm, nm, nx, xl, xh, ny, yl, yh, nz, zl, zh);
  Float_t siz = 0.05;
  hx->SetTitleSize(siz);       hx->SetLabelSize(siz);
  hx->SetTitleSize(siz, "Y");  hx->SetLabelSize(siz, "Y");
  hx->SetTitleSize(siz, "Z");  hx->SetLabelSize(siz, "Z");
  hx->SetTitle("");
  return hx;

}//PrepareTH3I

//_____________________________________________________________________________
TH3F *PrepareTH3F(const char *nm, Int_t nx, Double_t xl, Double_t xh, Int_t ny, Double_t yl, Double_t yh, Int_t nz, Double_t zl, Double_t zh) {

  TH3F *hx = new TH3F(nm, nm, nx, xl, xh, ny, yl, yh, nz, zl, zh);
  Float_t siz = 0.05;
  hx->SetTitleSize(siz);       hx->SetLabelSize(siz);
  hx->SetTitleSize(siz, "Y");  hx->SetLabelSize(siz, "Y");
  hx->SetTitleSize(siz, "Z");  hx->SetLabelSize(siz, "Z");
  hx->SetTitle("");
  return hx;

}//PrepareTH3I

//_____________________________________________________________________________
void normToData(TH1 *hMC, TH1 *hDat, Color_t col=kBlue) {

  //normalize MC hMC to data hDat, suppress errors to draw as line and set color

  hMC->Sumw2();
  hMC->Scale(hDat->Integral("width")/hMC->Integral("width"));
  for(Int_t ibin=0; ibin<hMC->GetNbinsX()+1; ibin++) hMC->SetBinError(ibin, 0);

  SetLineMarkerColor(hMC, col);

}//normToData

//_____________________________________________________________________________
void printPad(TList *list) {

  //print content of the list

  cout << "#####################" << endl;
  TIter next(list);
  while( TObject *obj = next() ) {
    cout << obj->GetName() << " " << obj->ClassName() << endl;
  }
  cout << "#####################" << endl;

}//printPad

//_____________________________________________________________________________
void printPad(TVirtualPad *pad) {

  //print pad content

  printPad(pad->GetListOfPrimitives());

}//printPad

//_____________________________________________________________________________
void invertCol(TVirtualPad *pad) {

  //set foreground and background color
  //Color_t fgcol = kGreen;
  Color_t fgcol = kOrange-3;
  Color_t bgcol = kBlack;

  pad->GetCanvas()->SetFillColor(bgcol);
  pad->SetFillColor(bgcol);
  pad->SetFrameLineColor(fgcol);

  TIter next(gPad->GetListOfPrimitives());
  while( TObject *obj = next() ) {
    //H1
    if( obj->InheritsFrom(TH1::Class()) ) {
      TH1 *hx = (TH1*)obj;
      if(hx->GetLineColor() == kBlack) {
        hx->SetLineColor(fgcol);
        hx->SetFillColor(bgcol);
      }
      if(hx->GetMarkerColor() == kBlack) hx->SetMarkerColor(fgcol);
      hx->SetAxisColor(fgcol, "X");
      hx->SetAxisColor(fgcol, "Y");
      hx->SetLabelColor(fgcol, "X");
      hx->SetLabelColor(fgcol, "Y");
      hx->GetXaxis()->SetTitleColor(fgcol);
      hx->GetYaxis()->SetTitleColor(fgcol);
    }
    //H2
    if( obj->InheritsFrom(TH2::Class()) ) {
      TH2 *hx = (TH2*)obj;
      hx->SetAxisColor(fgcol, "Z");
      hx->SetLabelColor(fgcol, "Z");
      hx->GetZaxis()->SetTitleColor(fgcol);
    }
    //Legend
    if( obj->InheritsFrom(TLegend::Class()) ) {
      TLegend *leg = (TLegend*)obj;
      leg->SetTextColor(fgcol);
      TIter ln(leg->GetListOfPrimitives());
      while( TObject *lo = ln() ) {
        TLegendEntry *ent = dynamic_cast<TLegendEntry*>(lo);
        if(!ent) continue;
        TH1 *hx = dynamic_cast<TH1*>(ent->GetObject());
        if(hx) {
          hx->SetFillColor(bgcol);
          if( hx->GetMarkerColor() == kBlack ) {
            hx->SetMarkerColor(fgcol);
            hx->SetLineColor(fgcol);
          }
        }
      }
    }
    //Latex
    if( obj->InheritsFrom(TLatex::Class()) ) {
      TLatex *lat = (TLatex*) obj;
      if( lat->GetTextColor() == kBlack ) lat->SetTextColor( fgcol );
    }
    //RooHist
    if( obj->InheritsFrom(RooHist::Class()) ) {
      RooHist *rh = (RooHist*) obj;
      if( rh->GetMarkerColor() == kBlack ) {
        rh->SetMarkerColor( fgcol );
        rh->SetLineColor( fgcol );
      }
    }
    //TGraph
    if( obj->InheritsFrom(TGraph::Class()) ) {
      TGraph *gr = (TGraph*)obj;
      gr->SetFillColor(bgcol);
      if(gr->GetLineColor() == kBlack) {
        gr->SetLineColor(fgcol);
        gr->SetMarkerColor(fgcol);
      }
    }
    //TFrame
    if( obj->InheritsFrom(TFrame::Class()) ) {
      TFrame *fr = (TFrame*) obj;
      fr->SetFillColor(bgcol);
      fr->SetLineColor(fgcol);
    }
    //TCrown
    if( obj->InheritsFrom(TCrown::Class()) ) {
      TCrown *cw = (TCrown*) obj;
      if(cw->GetLineColor() == kBlack) {
        cw->SetLineColor(fgcol);//kWhite
      }
    }
  }

}//invertCol

//_____________________________________________________________________________
void logFitResult(ofstream& out, RooFitResult *r1, Int_t lmg=6) {

  stringstream str;

  r1->defaultPrintStream(&str);
  r1->Print("v");
  r1->defaultPrintStream(&cout);

  //printf redirection for correlation matrix
  // https://stackoverflow.com/questions/10150468/how-to-redirect-cin-and-cout-to-files
  // https://stackoverflow.com/questions/11110300/how-to-capture-output-of-printf
  // https://stackoverflow.com/questions/1162068/redirect-both-cout-and-stdout-to-a-string-in-c-for-unit-testing
  // http://en.cppreference.com/w/c/io/setvbuf
  str << "Correlation matrix:\n";
  const Int_t nbuf = 1e5;
  Char_t matrix_buf[nbuf];
  fflush(stdout);
  setvbuf(stdout,matrix_buf,_IOFBF,nbuf);

  r1->correlationMatrix().Print();

  setbuf(stdout,NULL);
  str << matrix_buf;

  //put left margin and parameter numbers
  string line;
  Int_t pnum = -4;
  while( getline(str, line) ) {
    //put parameter numbers
    if( ((Int_t)line.find("InitialValue")) > -1 ) pnum++;
    if( line.empty() ) pnum = -4;
    if( pnum >-4 ) {
      pnum++;
      if (pnum >= 0) {
        string pstr = to_string(pnum);
        line.replace(2, pstr.length(), pstr);
      }
    }
    //put left margin
    if(!line.empty()) {
      out.width(lmg);
      out << "";
    }

    out << line << endl;
  }

}//logFitResult

//_____________________________________________________________________________
void logFitResult(ofstream& out, TFitResult *r1, Int_t lmg=6) {

  stringstream str;

  str << "Minimizer status: " << r1->Status() << "\n";
  str << "Cov matrix status: " << r1->CovMatrixStatus() << "\n";

  r1->FitResult::Print(str, kTRUE);

  //put left margin
  string line;
  while( getline(str, line) ) {
    if(!line.empty()) {
      out.width(lmg);
      out << "";
    }

    out << line << endl;
  }

}//logFitResult

//_____________________________________________________________________________
void setBinomialErr(TH1 *hTarget, TH1 *hAll, TH1 *hSel)
{

  Double_t xGen, xRec;

  //loop over bins
  for(Int_t ibin=-1; ibin<hTarget->GetNbinsX()+1; ibin++) {
    if( hTarget->GetBinContent(ibin) <= 0. ) {
      hTarget->SetBinError(ibin, 0.);
      continue;
    }

    xGen = hAll->GetBinContent(ibin);
    xRec = hSel->GetBinContent(ibin);
    if(xGen < 0.1) xGen=99999999.; if(xRec < 0.1) xRec=99999999.;

    hTarget->SetBinError(ibin, ( xRec/xGen*TMath::Sqrt( (xGen-xRec) / (xGen*xRec) ) ) );

  }//loop over bins

}//setBinomialErr

//_____________________________________________________________________________
TH1* divHist(TH1* h0, TH1 *h1)
{

  TH1 *hx;
  hx = (TH1*)h0->Clone();
  hx->Divide(h1);

  setBinomialErr(hx, h1, h0);

  return hx;

}//divHist

//_____________________________________________________________________________
void SetGraphStyle(TGraph* g, Color_t mcolor, Style_t mstyle, Size_t msize, Color_t lcolor, Style_t lstyle, Width_t lwidth) {

  g->SetMarkerColor(mcolor);
  g->SetMarkerSize(msize);
  g->SetMarkerStyle(mstyle);
  g->SetLineColor(lcolor);
  g->SetLineStyle(lstyle);
  g->SetLineWidth(lwidth);

}//SetGraphStyle










#endif

























