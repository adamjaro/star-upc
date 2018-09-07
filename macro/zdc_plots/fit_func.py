
from ROOT import RooRealVar, RooDataSet, RooArgSet, RooAddPdf, RooArgList
from ROOT import RooGaussian, RooExponential, RooCBShape, RooProdPdf

class Gauss(object):
#_____________________________________________________________________________
    def __init__(self, adc, name):
        #input ADC values
        self.adc = adc
        #1n Gaussian
        mean_nam = "mean_1n_" + name
        self.mean_1n = RooRealVar(mean_nam, mean_nam, 40., 120.)
        sigma_nam = "sigma_1n_" + name
        self.sigma_1n = RooRealVar(sigma_nam, sigma_nam, 0., 100.)
        gauss_nam = "gauss_1n_" + name
        self.gauss_1n = RooGaussian(gauss_nam, gauss_nam, self.adc, self.mean_1n, self.sigma_1n)

class CrystalBall(object):
#_____________________________________________________________________________
    def __init__(self, adc, name):
        #input ADC values
        self.adc = adc
        #2+n reversed Crystal Ball
        #mean
        mean_nam = "mean_2n_" + name
        self.mean_2n = RooRealVar(mean_nam, mean_nam, 150., 200.)
        #sigma
        sigma_nam = "sigma_2n_" + name
        self.sigma_2n = RooRealVar(sigma_nam, sigma_nam, 0., 100.)
        #alpha
        alpha_nam = "alpha_2xn_" + name
        self.alpha_2xn = RooRealVar(alpha_nam, alpha_nam, -10., 0.)
        #n
        n_nam = "n_2xn_" + name
        self.n_2xn = RooRealVar(n_nam, n_nam, 0., 20.)
        #CrystalBall
        cb_name = "cb_2xn_" + name
        self.cb_2xn = RooCBShape(cb_name, cb_name, self.adc, self.mean_2n, self.sigma_2n, self.alpha_2xn, self.n_2xn)

class Model1D(object):
#_____________________________________________________________________________
    def __init__(self, gauss_1n, cb_2xn, name):
        self.gauss_1n = gauss_1n
        self.cb_2xn = cb_2xn
        #number in the model
        n1n_nam = "num_1n_" + name
        self.num_1n = RooRealVar(n1n_nam, n1n_nam, 200, 0, 3000) # 1
        n2n_nam = "num_2n_" + name
        self.num_2n = RooRealVar(n2n_nam, n2n_nam, 100, 0, 3000) # 0.5
        #1D model Gauss + Crystal Ball
        model_nam = "model_" + name
        self.model = RooAddPdf(model_nam, model_nam, RooArgList(self.gauss_1n, self.cb_2xn), RooArgList(self.num_1n, self.num_2n))


class Model2D(object):
#_____________________________________________________________________________
    def __init__(self, adc_east, adc_west):
        #input ADC values
        self.adc_east = adc_east
        self.adc_west = adc_west
        #self.adc_east = RooRealVar("adc_east", "adc_east", 10, 1300)
        #self.adc_west = RooRealVar("adc_west", "adc_west", 10, 1300)
        #east Gaussian
        self.gauss_east = Gauss(self.adc_east, "east")
        self.gauss_east.mean_1n.setVal(72.9)
        self.gauss_east.sigma_1n.setVal(21.4)
        #west Gaussian
        self.gauss_west = Gauss(self.adc_west, "west")
        self.gauss_west.mean_1n.setVal(87.7)
        self.gauss_west.sigma_1n.setVal(26.9)
        #east Crystal Ball
        self.cb_east = CrystalBall(self.adc_east, "east")
        self.cb_east.mean_2n.setVal(166.)
        self.cb_east.sigma_2n.setVal(42.1)
        self.cb_east.alpha_2xn.setVal(-0.7)
        self.cb_east.n_2xn.setVal(0.5)
        #west Crystal Ball
        self.cb_west = CrystalBall(self.adc_west, "west")
        self.cb_west.mean_2n.setVal(174.1)
        self.cb_west.sigma_2n.setVal(29.3)
        self.cb_west.alpha_2xn.setVal(-0.3)
        self.cb_west.n_2xn.setVal(0.8)
        # (g_e + c_e)*(g_w + c_w) = g_e*g_w + c_e*c_w + g_e*c_w + c_e*g_w
        #1n1n 2D Gaussian
        self.pdf_1n1n = RooProdPdf("pdf_1n1n", "pdf_1n1n", RooArgList(self.gauss_east.gauss_1n, self.gauss_west.gauss_1n))
        self.num_1n1n = RooRealVar("num_1n1n", "num_1n1n", 200, 0, 3000) # 1
        #1n2xn Gaussian * Crystal Ball
        self.pdf_1n2xn = RooProdPdf("pdf_1n2xn", "pdf_1n2xn", RooArgList(self.gauss_east.gauss_1n, self.cb_west.cb_2xn))
        self.num_1n2xn = RooRealVar("num_1n2xn", "num_1n2xn", 100, 0, 3000) # 1
        #2xn1n Crystal Ball * Gaussian
        self.pdf_2xn1n = RooProdPdf("pdf_2xn1n", "pdf_2xn1n", RooArgList(self.cb_east.cb_2xn, self.gauss_west.gauss_1n))
        self.num_2xn1n = RooRealVar("num_2xn1n", "num_2xn1n", 100, 0, 3000) # 1
        #2xn2xn 2D Crystal Ball
        self.pdf_2xn2xn = RooProdPdf("pdf_2xn2xn", "pdf_2xn2xn", RooArgList(self.cb_east.cb_2xn, self.cb_west.cb_2xn))
        self.num_2xn2xn = RooRealVar("num_2xn2xn", "num_2xn2xn", 50, 0, 3000) # 1
        #fit model
        self.model = RooAddPdf("model", "model", RooArgList(self.pdf_1n1n, self.pdf_1n2xn, self.pdf_2xn1n, self.pdf_2xn2xn),
        RooArgList(self.num_1n1n, self.num_1n2xn, self.num_2xn1n, self.num_2xn2xn))



        #1D model east
        #self.model_east = Model1D(self.gauss_east.gauss_1n, self.cb_east.cb_2xn, "east")
        #1D model west
        #self.model_west = Model1D(self.gauss_west.gauss_1n, self.cb_west.cb_2xn, "west")
        #2D model east vs. west
        #self.model = RooProdPdf("model", "model", RooArgList(self.model_east.model, self.model_west.model))

        #fit model
        #self.model = RooAddPdf("model", "model", RooArgList(self.gauss2D, self.cb2D), RooArgList(self.num_1n, self.num_2n))


        #self.model = RooProdPdf("model2D", "model2D", RooArgList(self.model_east.gauss_1n, self.model_west.gauss_1n))
        #self.model = RooProdPdf("model2D", "model2D", RooArgList(self.model_east.model, self.model_west.model))
























