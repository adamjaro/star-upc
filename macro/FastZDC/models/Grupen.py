
#-----------------------------------------------------------------------
# Grupen, Buvat, Handbook on detectors, p. 509 (530), eq. 4:
#
#   sigma/E = a1/sqrt(E) (+) a2*[(E/E0)^(l-1) ] = (sum in quadratures) =
#   = sqrt( a1^2/E + (a2^2)*[(E/E0)^(2l-2)] )
#
#   sigma = sqrt( (a1^2)*E + (a2^2)*(E^2)*[(E/E0)^(2l-2)] )
#
# Conversion to ADC from energy as
#
#  adc = k1*E + k2
#_______________________________________________________________________

from ROOT import TMath, TRandom3

#_____________________________________________________________________________
class Grupen:
    #_____________________________________________________________________________
    def __init__(self):

        #east and west ZDC parametrizations
        self.e = self.param()
        self.w = self.param()

        #scaling Poisson term
        self.e.a1 = 1.5
        self.w.a1 = 2.8

        #non-compensation
        self.e.a2 = 0.67
        self.w.a2 = 2.5

        #material constant, GeV
        self.e.E0 = 1.4
        self.w.E0 = 1.4

        #power law parameter
        self.e.l = 0.7
        self.w.l = 0.3

        #ADC conversion
        self.e.k1 = 0.66
        self.e.k2 = -18.94
        self.w.k1 = 0.68
        self.w.k2 = -15.52

        #random generator
        self.rnd = TRandom3()

    #__init__

    #_____________________________________________________________________________
    def __call__(self, en_east, en_west):

        #ADC east and west

        east = self.get_adc(en_east, self.e)
        west = self.get_adc(en_west, self.w)

        return east, west

    #__call__

    #_____________________________________________________________________________
    def get_adc(self, en, par):

        #convert energy to ADC for a given ZDC parametrization

        #sigma = sqrt( (a1^2)*E + (a2^2)*(E^2)*[(E/E0)^(2l-2)] )

        sigma = TMath.Sqrt( en*(par.a1**2) + (par.a2**2)*(en**2)*( (en/par.E0)**(2*par.l-2) ) )

        adc = -1.

        while adc < 0.:
            #energy response
            en_resp = en + self.rnd.Gaus(0, sigma)

            #ADC from energy
            adc = par.k1*en_resp + par.k2

        return adc

    #get_adc

    #_____________________________________________________________________________
    class param:
        #east and west parametrization
        #_____________________________________________________________________________
        def __init__(self):

            self.a1 = 0. # scaling Poisson term
            self.a2 = 0. # non-compensation
            self.E0 = 0. # material constant, GeV
            self.l = 0. # power law parameter

            self.k1 = 0. # ADC conversion, slope
            self.k2 = 0. # ADC conversion, offset

        #__init__


















