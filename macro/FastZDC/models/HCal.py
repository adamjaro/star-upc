
#------------------------------------------
# Hadronic calorimeter with resolution as
#
#   sigma/E = a (+) b/sqrt(E) (+) c/E
#
# and with conversion to ADC from energy as
#
#  adc = k1*E + k2
#__________________________________________

from ROOT import TMath, TRandom3

#_____________________________________________________________________________
class HCal:
    #_____________________________________________________________________________
    def __init__(self):

        #east and west ZDC parametrizations
        self.e = self.param()
        self.w = self.param()

        #systematic effects
        self.e.a = 0.18
        self.w.a = 0.09

        #sampling fraction
        self.e.b = 1.6
        self.w.b = 2.8

        #noise
        self.e.c = 0.1
        self.w.c = 0.1

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

        #sigma = sqrt( a^2*E^2 + b^2*E + c^2 )

        sigma = TMath.Sqrt( (par.a**2)*(en**2) + (par.b**2)*en + par.c**2 )

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

            self.a = 0. # systematics
            self.b = 0. # sampling fraction
            self.c = 0. # noise

            self.k1 = 0. # ADC conversion, slope
            self.k2 = 0. # ADC conversion, offset

        #__init__
























