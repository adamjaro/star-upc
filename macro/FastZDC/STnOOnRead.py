
from ROOT import TFile, TClonesArray, TMath, TLorentzVector

#_____________________________________________________________________________
class STnOOnRead:
    #_____________________________________________________________________________
    def __init__(self, infile):

        #energy in event at positive and negative rapidity
        self.epos = 0.
        self.eneg = 0.

        #number of neutrons at positive and negative rapidity
        self.npos = 0
        self.nneg = 0

        #flag for XnXn event
        self.is_XnXn = False

        #flag for central event
        self.is_Cen = False

        #J/psi kinematics
        self.pT = 0.
        self.y = 0.
        self.m = 0.

        #absolute eta for electron and positron
        self.aeta_max = 1.

        #minimal electron and positron for central trigger
        #self.p_min = 1.014

        #open the input
        self.inp = TFile.Open(infile)
        self.tree = self.inp.Get("slight_tree")

        #connect the input tree
        self.particles = TClonesArray("TParticle", 200)
        self.tree.SetBranchAddress("particles", self.particles)

        #number of events in input tree
        self.nev = self.tree.GetEntriesFast()

    #__init__

    #_____________________________________________________________________________
    def read(self, iev):

        #read a given event

        if iev >= self.nev: return False

        self.tree.GetEntry(iev)

        #initialize event variables
        self.epos = 0.
        self.eneg = 0.

        self.npos = 0
        self.nneg = 0

        self.is_XnXn = False
        self.is_Cen = True

        vec = TLorentzVector()

        #particle loop
        for imc in xrange(self.particles.GetEntriesFast()):
            part = self.particles.At(imc)

            #central electron and positron
            if TMath.Abs( part.GetPdgCode() ) == 11:
                if TMath.Abs(part.Eta()) > self.aeta_max: self.is_Cen = False
                #if part.P() < self.p_min: self.is_Cen = False
                pv = TLorentzVector()
                part.Momentum(pv)
                vec += pv

            #select the neutrons
            if part.GetPdgCode() != 2112: continue

            #energy at positive and negative rapidity
            if part.Eta() > 0:
                self.epos += part.Energy()
                self.npos += 1
            else:
                self.eneg += part.Energy()
                self.nneg += 1

        #particle loop

        #flag for XnXn event
        if self.npos > 0 and self.nneg > 0: self.is_XnXn = True

        #J/psi kinematics
        self.pT = vec.Pt()
        self.y = vec.Rapidity()
        self.m = vec.M()

        return True

    #read















