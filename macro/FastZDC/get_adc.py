#!/usr/bin/python

#ADC conversion from 1n and 2n energies

#_____________________________________________________________________________
def main():

    #East ZDC
    a1_e = 47.969
    a2_e = 115.040

    #West ZDC
    a1_w = 53.393
    a2_w = 122.475

    #1n and 2n energies
    E1 = 102.02
    E2 = 204.287

    print "East:"
    get_adc(a1_e, a2_e, E1, E2)

    print
    print "West:"
    get_adc(a1_w, a2_w, E1, E2)

#main

#_____________________________________________________________________________
def get_adc(a1, a2, E1, E2):

    k1 = (a2 - a1)/(E2 - E1)

    k2 = a1 - k1*E1

    print "k1:", k1
    print "k2:", k2

#get_adc

#_____________________________________________________________________________
if __name__ == "__main__":

    main()

