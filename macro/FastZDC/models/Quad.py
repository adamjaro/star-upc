
#quadratic sum of const, E and E^2
#
#sqrt( 100*s0 + s1*E + s2*E^2 )

from ROOT import TMath, TRandom3

#_____________________________________________________________________________
class Quad:
    #_____________________________________________________________________________
    def __init__(self):

        #constant term
        self.s0E = 0.
        self.s0W = 0.

        #linear term in energy
        self.s1E = 0.4
        self.s1W = 0.7

        #quadratic in energy
        self.s2E = 0.2
        self.s2W = 0.23

        #difference in mean for ADC, east and west
        self.deltE = 25.2
        self.deltW = 11.5

        #random generator
        self.rnd = TRandom3()

    #__init__

    #_____________________________________________________________________________
    def __call__(self, en_east, en_west):

        #ADC east and west

        east = self.get_adc(en_east, self.s0E, self.s1E, self.s2E, self.deltE)
        west = self.get_adc(en_west, self.s0W, self.s1W, self.s2W, self.deltW)

        return east, west

    #__call__

    #_____________________________________________________________________________
    def get_adc(self, en, s0, s1, s2, delt):

        #convert energy to ADC

        sigma = TMath.Sqrt( s0**2 + en*s1**2 + (s2*en)**2 )

        adc = -1.

        while adc < 0.:
            adc = en + self.rnd.Gaus(0, sigma)
            adc -= delt

        return adc

    #get_adc










