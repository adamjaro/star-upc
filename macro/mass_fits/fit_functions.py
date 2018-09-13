
from ROOT import RooRealVar, RooCBShape

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

