#ifndef CUTLINE_H
#define CUTLINE_H

//#include "TLine.h";

class cutLine : public TLine {

public:

  //cut value on x, line length along y, histogram and log scale
  cutLine(Double_t cval, Double_t yl, TH1 *hx, Bool_t logy=kFALSE) {
    Double_t tsel_pos = yl;
    if(!logy) {
      tsel_pos = tsel_pos*(hx->GetMaximum());
    } else {
      if ( hx->GetMinimum() > 0. ) {
        tsel_pos = TMath::Log10(hx->GetMinimum()) + tsel_pos*(TMath::Log10(hx->GetMaximum())-TMath::Log10(hx->GetMinimum()));
      } else {
        tsel_pos = tsel_pos*TMath::Log10(hx->GetMaximum());
      }
      tsel_pos = TMath::Power(10, tsel_pos);
    }
    TLine::SetX1(cval);
    TLine::SetY1(0.);
    TLine::SetX2(cval);
    TLine::SetY2(tsel_pos);

    TLine::SetLineColor(kViolet);
    TLine::SetLineStyle(kDashed);
    TLine::SetLineWidth(4);
  }//cutLine

  ~cutLine() {}







};

#endif












