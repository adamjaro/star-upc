#ifndef THB1D_H
#define THB1D_H

#include "TH1D.h"

class THB1D: public TH1D {

  Int_t fHeight;
  Int_t fLeftMarg;
  Int_t fTotHeight;
  Double_t fYMax;
  std::vector<std::string> fYLabels;
  std::vector<std::string> fHistLines;
  std::vector<std::string> fDigLines;

public:

  THB1D();
  THB1D(const char *name, const char *title, Int_t nbins, Double_t xmin, Double_t xmax);
  virtual ~THB1D();

  void SetHeight(Int_t h);
  void SetLeftMargin(Int_t m) { fLeftMarg = m; }
  void SetTotalHeight(Int_t th) { fTotHeight = th; };

  Int_t GetTotalHeight() const { return fTotHeight; };

  friend std::ostream& operator<<(std::ostream& os, THB1D& hx);
  friend std::ostream& operator<<(std::ostream& os, THB1D *hx) {
    return operator<<(os, *hx);
  }

private:

};

#endif

