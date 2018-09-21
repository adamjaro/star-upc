
from ROOT import RooRealVar, RooCBShape, RooArgList, RooGenericPdf

#_____________________________________________________________________________
#mass variable
m = RooRealVar("jRecM", "e^{+}e^{-} mass (GeV)", 0., 10.)
#pT and rapidity
y = RooRealVar("jRecY", "rapidity", -1., 1.)
pT = RooRealVar("jRecPt", "pT", 0., 10.)
pT2 = RooRealVar("jRecPt2", "pT^2", 0., 10.)

#_____________________________________________________________________________
#Crystal Ball function
# J/psi PDF mass for m0 taken as TDatabasePDG::Instance()->GetParticle( 443 )->Mass()
m0 = RooRealVar("m0", "mass", 3.09692, 3., 3.15)
n = RooRealVar("n", "n", 2, 0., 20.)
sig = RooRealVar("sig", "resolution", 0.1, 0.001, 0.2)
alpha = RooRealVar("alpha", "alpha", 0.3, 0.1, 4.1)
cb = RooCBShape("cb", "Crystal Ball PDF", m, m0, sig, alpha, n)

#_____________________________________________________________________________
#Background function
lam = RooRealVar("lambda", "Exponent", -0.6, -10., 0.)
c1 = RooRealVar("c1", "c1", 1.5, 0.5, 2.5)
c2 = RooRealVar("c2", "c2", 0.04, -1., 1.)
bkg_func = "TMath::Abs(jRecM-c1)*TMath::Exp(lambda*(jRecM-c1)*(jRecM-c1)+c2*(jRecM-c1)*(jRecM-c1)*(jRecM-c1))"
#bkg_func = "TMath::Abs(jRecM-c1)*TMath::Exp(lambda*(jRecM-c1)*(jRecM-c1)+c2*jRecM*jRecM*jRecM)"
#abs() is to prevent error messages about negative values below the fit range
bkgd = RooGenericPdf("Background", bkg_func, RooArgList(m, lam, c1, c2))
#version for plotting with fixed parameters
lamF = RooRealVar("lambdaF", "lambdaF", -2.422)
c1f = RooRealVar("c1f", "c1f", 1.227)
c2f = RooRealVar("c2f", "c2f", 0.240)
bkg_func_f = "TMath::Abs(jRecM-c1f)*TMath::Exp(lambdaF*(jRecM-c1f)*(jRecM-c1f)+c2f*(jRecM-c1f)*(jRecM-c1f)*(jRecM-c1f))"
#bkg_func_f = "TMath::Abs(jRecM-c1f)*TMath::Exp(lambdaF*(jRecM-c1f)*(jRecM-c1f)+c2f*jRecM*jRecM*jRecM)"
bkgd_f = RooGenericPdf("Background_f", bkg_func_f, RooArgList(m, lamF, c1f, c2f))


















