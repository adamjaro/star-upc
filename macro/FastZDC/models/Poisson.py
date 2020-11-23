
# Response with Poisson fluctuations and non-Poissonian contribution
# Grupen, Buvat, p. 509 (530), eq. 4
#
# sigma/E = a1/sqrt(E) (+) a2*[(E/E0)^(l-1) ] = (sum in quadratures) =
# = sqrt( a1^2/E + (a2^2)*[(E/E0)^(2l-2)] )
#
# sigma = sqrt( (a1^2)*E + (a2^2)*(E^2)*[(E/E0)^(2l-2)] )

from ROOT import TMath, TRandom3

#_____________________________________________________________________________
class Poisson:
    #_____________________________________________________________________________
    def __init__(self):

        #scaling Poisson term
        self.a1E = 1.4
        self.a1W = 2.8

        #non-compensation
        self.a2E = 0.67
        self.a2W = 2.5

        #material constant, GeV
        self.E0E = 1.4
        self.E0W = 1.4

        #power law parameter
        self.lE = 0.7
        self.lW = 0.3

        #difference in mean for ADC, east and west
        self.deltE = 100.9-79.1 # J/psi mass
        self.deltW = 101.5-94.1

        #random generator
        self.rnd = TRandom3()

    #__init__

    #_____________________________________________________________________________
    def __call__(self, en_east, en_west):

        #ADC east and west

        east = self.get_adc(en_east, self.a1E, self.a2E, self.E0E, self.lE, self.deltE)
        west = self.get_adc(en_west, self.a1W, self.a2W, self.E0W, self.lW, self.deltW)

        return east, west

    #__call__

    #_____________________________________________________________________________
    def get_adc(self, en, a1, a2, E0, l, delt):

        #convert energy to ADC

        #sigma = sqrt( (a1^2)*E + (a2^2)*(E^2)*[(E/E0)^(2l-2)] )

        sigma = TMath.Sqrt( en*a1**2 + (a2**2)*(en**2)*( (en/E0)**(2*l-2) ) )

        adc = -1.

        while adc < 0.:
            adc = en + self.rnd.Gaus(0, sigma)
            adc -= delt

        return adc

    #get_adc










