
import ROOT as rt
from ROOT import TF1, TF2, gPad, RooArgSet

#import sys
#sys.path.append('../')
#import plot_utils as ut

class PlotPdf(object):
#_____________________________________________________________________________
    def __init__(self, model, adc_east, adc_west):
        self.model = model
        self.adc_east = adc_east
        self.adc_west = adc_west
        self.adc_min = 10
        self.adc_max = 700
        #2D pdf
        self.pdf = TF2("pdf", self.pdf_eval2D, self.adc_min, self.adc_max, self.adc_min, self.adc_max)
        self.pdf.SetNpx(100)
        self.pdf.SetNpy(100)
        #pdf.GetXaxis().SetTitle("x")
        #1D pdf east
        self.pdf_east = TF1("pdf_east", self.pdf_eval_east, self.adc_min, self.adc_max)
        self.pdf_east.SetNpx(1000)

#_____________________________________________________________________________
    def plot(self):

        self.pdf.SetTitle("")

        xtit = ["ZDC East ADC", "ZDC West ADC"]

        self.pdf.GetXaxis().SetTitle(xtit[0])
        self.pdf.GetYaxis().SetTitle(xtit[1])
        self.pdf.GetZaxis().SetTitle("Fit function (arbitraty units)")

        self.pdf.Draw("surf")

#_____________________________________________________________________________
    def plot_east(self):

        self.pdf_east.Draw()

#_____________________________________________________________________________
    def pdf_eval2D(self, x):

        self.model.adc_east.setVal(x[0])
        self.model.adc_west.setVal(x[1])

        #return self.model.model.evaluate()
        return 2e6*self.model.model.getValV(RooArgSet(self.adc_east, self.adc_west))

#_____________________________________________________________________________
    def pdf_eval_east(self, x):

        self.model.adc_east.setVal(x[0])

        return self.model.model_east.model.evaluate()


















