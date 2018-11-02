
from math import sqrt

from ROOT import TFile

class AnalyzeTree(object):
#_____________________________________________________________________________
    def __init__(self):
        inf = 9.e4
        self.mmin = -inf
        self.mmax = inf
        self.ptmax = inf
        self.ymin = -inf
        self.ymax = inf

#_____________________________________________________________________________
    def SetMass(self, mlo, mhi):
        self.mmin = mlo
        self.mmax = mhi

#_____________________________________________________________________________
    def SetPt(self, pt):
        self.ptmax = pt

#_____________________________________________________________________________
    def SetY(self, ylo, yhi):
        self.ymin = ylo
        self.ymax = yhi

#_____________________________________________________________________________
    def ApplyPrec(self, val, prec):
        return float( ("{0:."+str(prec)+"f}").format(val) )

#_____________________________________________________________________________
    def AnalyzeMC(self, inp, prec=4):
        #analysis input
        infile = TFile.Open(inp, "read")
        #reconstructed tree
        datatree = infile.Get("jRecTree")
        datatree.SetBranchStatus("*", 0)
        datatree.SetBranchStatus("jRecM", 1)
        datatree.SetBranchStatus("jRecY", 1)
        datatree.SetBranchStatus("jRecPt", 1)
        #generated tree
        gentree = infile.Get("jGenTree")
        gentree.SetBranchStatus("*", 0)
        gentree.SetBranchStatus("jGenM", 1)
        gentree.SetBranchStatus("jGenY", 1)
        #formulate selection strings
        #data
        strsel = "jRecM>"+str(self.mmin) + " && jRecM<"+str(self.mmax)
        strsel += " && jRecY>"+str(self.ymin) + " && jRecY<"+str(self.ymax)
        strsel += " && jRecPt<"+str(self.ptmax)
        #MC
        strgen = "jGenM>"+str(self.mmin) + " && jGenM<"+str(self.mmax)
        strgen += " && jGenY>"+str(self.ymin) + " && jGenY<"+str(self.ymax)
        #apply the selections
        nsel = float(datatree.Draw("", strsel))
        ngen = float(gentree.Draw("", strgen))
        if ngen < 0.1: return -1.
        #get efficiency with binomial error
        eff = nsel/ngen
        sigma = eff*sqrt( (ngen-nsel) / (ngen*nsel) )
        #apply the precision
        eff = self.ApplyPrec(eff, prec)
        sigma = self.ApplyPrec(sigma, prec)
        return eff, sigma

#_____________________________________________________________________________
    def AnalyzeStarlight(self, inp, prec=4):
        #Starlight input
        infile = TFile.Open(inp, "read")
        intree = infile.Get("slight_tree")
        intree.SetBranchStatus("*", 0)
        intree.SetBranchStatus("mass", 1)
        intree.SetBranchStatus("rapidity", 1)
        #number of events
        #all events in the file
        nall = float(intree.GetEntries())
        if nall < 0.1: return -1.
        #selected within a given mass and rapidity
        strsel = "mass>"+str(self.mmin) + " && mass<"+str(self.mmax)
        strsel += " && rapidity>"+str(self.ymin) + " && rapidity<"+str(self.ymax)
        nsel = float(intree.Draw("", strsel))
        #use a given precision for the ratio
        return self.ApplyPrec(nsel/nall, prec)

#_____________________________________________________________________________
    def AnalyzeData(self, inp, prec=4):
        #data input
        infile = TFile.Open(inp, "read")
        #data tree
        datatree = infile.Get("jRecTree")
        datatree.SetBranchStatus("*", 0)
        datatree.SetBranchStatus("jRecM", 1)
        datatree.SetBranchStatus("jRecY", 1)
        datatree.SetBranchStatus("jRecPt", 1)
        datatree.SetBranchStatus("jZDCUnAttEast", 1)
        datatree.SetBranchStatus("jZDCUnAttWest", 1)
        #selection formula
        strsel = "jRecM>"+str(self.mmin) + " && jRecM<"+str(self.mmax)
        strsel += " && jRecY>"+str(self.ymin) + " && jRecY<"+str(self.ymax)
        strsel += " && jRecPt<"+str(self.ptmax)
        strsel += " && jZDCUnAttEast < 130"
        strsel += " && jZDCUnAttWest < 160"
        #apply the selection
        ndat = float(datatree.Draw("", strsel))
        return ndat
























