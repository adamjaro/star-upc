
from ROOT import TFile, TClonesArray

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

        #particle loop
        for imc in xrange(self.particles.GetEntriesFast()):
            part = self.particles.At(imc)

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

        return True

    #read















