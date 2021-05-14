#!/usr/bin/python

#ADC conversion from run 14 to run 16

#_____________________________________________________________________________
def main():

    #run14 east ZDC
    a4_1e = 79.145
    a4_2e = 172.321

    #run14 west ZDC
    a4_1w = 94.082
    a4_2w = 204.213

    #run16 east ZDC
    a6_1e = 47.969
    a6_2e = 115.040

    #run16 west ZDC
    a6_1w = 53.393
    a6_2w = 122.475

    print "East:"
    k1, k2 = get_adc(a6_1e, a6_2e, a4_1e, a4_2e)
    adc_run16(1200., k1, k2)

    print
    print "West:"
    k1, k2 = get_adc(a6_1w, a6_2w, a4_1w, a4_2w)
    adc_run16(1200., k1, k2)

#_____________________________________________________________________________
def get_adc(a6_1, a6_2, a4_1, a4_2):

    k1 = (a6_2 - a6_1)/(a4_2 - a4_1)

    k2 = a6_1 - k1*a4_1

    sk1 = "{0:.4f}".format(k1)
    sk2 = "{0:.4f}".format(k2)
    print "k1: "+sk1
    print "k2: "+sk2

    return float(sk1), float(sk2)

#get_adc

#_____________________________________________________________________________
def adc_run16(a4, k1, k2):

    #ADC in run 14 a6 from ADC in run 14 a4

    #a6 = k1 * a4 + k2

    print "a6("+str(a4)+") = "+str(k1*a4 + k2)

#adc_run16

#_____________________________________________________________________________
if __name__ == "__main__":

    main()


















