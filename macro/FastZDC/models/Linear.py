
#linear sum of sigma at 1n and 2n
#
#100*sig + s2(en-100) = 100*sig + s2*en - 100*s2 = 100*(sig-s2) + s2*en

from ROOT import TMath, TRandom3

#_____________________________________________________________________________
class Linear:
    #_____________________________________________________________________________
    def __init__(self):

        #resolution sigma_E/E, east and west
        self.sigE = 0.217
        self.sigW = 0.306

        self.s2E = 0.1
        self.s2W = 0.005

        #difference in mean for ADC, east and west
        self.deltE = 25.2
        self.deltW = 11.5

        #random generator
        self.rnd = TRandom3()

    #__init__

    #_____________________________________________________________________________
    def __call__(self, en_east, en_west):

        #ADC east and west

        east = self.get_adc(en_east, self.sigE, self.s2E, self.deltE)
        west = self.get_adc(en_west, self.sigW, self.s2W, self.deltW)

        return east, west

    #__call__

    #_____________________________________________________________________________
    def get_adc(self, en, sig, s2, delt):

        #convert energy to ADC

        #sigma = en*TMath.Sqrt( ((0.05**2)/en) + 0.2**2 )
        #sigma = en*TMath.Sqrt( ((0.01**2)/en) + sig**2 )
        #sigma = en*TMath.Sqrt( (0.1/en)**2 + sig**2 )
        #sigma = en*sig
        #sigma = 100.*sig
        #sigma = en*TMath.Sqrt( (sig**2) )
        #sigma = 100*sig + 0.1*(en-100) # works for east
        #sigma = 100*sig + 0.005*(en-100) # works for west

        sigma = 100*sig + s2*(en-100)

        adc = -1.

        while adc < 0.:
            #adc = en + rnd.Gaus(0, sig*en)
            #adc = en + rnd.Gaus(0, sig*100.)
            adc = en + self.rnd.Gaus(0, sigma)
            adc -= delt

        #if adc<0.: print adc

        return adc

    #get_adc










