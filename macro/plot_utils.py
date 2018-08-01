
import ROOT as rt
from ROOT import TMath, TH1D, TCanvas, TLegend, TLine, TIter, TH1, TH2D, TH2, TF2
from ROOT import RooHist, TLatex
from ROOT import std

#_____________________________________________________________________________
def prepare_TH1D(name, binsiz, xmin, xmax):

  nbins, xmax = get_nbins(binsiz, xmin, xmax)

  return prepare_TH1D_n(name, nbins, xmin, xmax)

#_____________________________________________________________________________
def get_nbins(binsiz, xmin, xmax):

  nbins = int(TMath.Ceil( (xmax-xmin)/binsiz )) #round-up value
  xmax = xmin + float(binsiz*nbins) # move max up to pass the bins

  return nbins, xmax

#_____________________________________________________________________________
def prepare_TH1D_n(name, nbins, xmin, xmax):

  hx = TH1D(name, name, nbins, xmin, xmax)
  set_H1D(hx)
  hx.SetTitle("");

  return hx

#_____________________________________________________________________________
def set_H1D(hx):

  hx.SetOption("E1");
  hx.SetMarkerStyle(rt.kFullCircle);
  hx.SetMarkerColor(rt.kBlack)
  hx.SetLineColor(rt.kBlack);
  hx.SetLineWidth(2);
  hx.SetYTitle("Counts");
  siz = 0.035;
  hx.SetTitleSize(siz)
  hx.SetLabelSize(siz)
  hx.SetTitleSize(siz, "Y")
  hx.SetLabelSize(siz, "Y")

#_____________________________________________________________________________
def prepare_TH2D(name, xbin, xmin, xmax, ybin, ymin, ymax):

  #bins along x and y
  nbinsX, xmax = get_nbins(xbin, xmin, xmax)
  nbinsY, ymax = get_nbins(ybin, ymin, ymax)

  return prepare_TH2D_n(name, nbinsX, xmin, xmax, nbinsY, ymin, ymax)

#_____________________________________________________________________________
def prepare_TH2D_n(name, nbinsX, xmin, xmax, nbinsY, ymin, ymax):

  hx = TH2D(name, name, nbinsX, xmin, xmax, nbinsY, ymin, ymax)
  hx.SetOption("COLZ");
  siz = 0.035
  hx.SetTitleSize(siz)
  hx.SetLabelSize(siz)
  hx.SetTitleSize(siz, "Y")
  hx.SetLabelSize(siz, "Y")
  hx.SetTitleSize(siz, "Z")
  hx.SetLabelSize(siz, "Z")

  hx.SetTitle("")

  return hx

#_____________________________________________________________________________
def norm_to_data(hMC, hDat, col=rt.kBlue):

  #normalize MC hMC to data hDat, suppress errors to draw as line and set color

  hMC.Sumw2()
  hMC.Scale(hDat.Integral("width")/hMC.Integral("width"))
  for ibin in range(hMC.GetNbinsX()+1):
    hMC.SetBinError(ibin, 0)
  hMC.SetLineColor(col)
  hMC.SetMarkerColor(col)



#_____________________________________________________________________________
def box_canvas():

    can = TCanvas("c3", "Analysis", 768, 768)
    rt.gStyle.SetOptStat("")
    rt.gStyle.SetPalette(1)
    rt.gStyle.SetLineWidth(2)
    rt.TGaxis.SetMaxDigits(4)

    can.cd(1)

    return can

#_____________________________________________________________________________
def prepare_leg(xl, yl, dxl, dyl, tsiz=0.045):

  leg = TLegend(xl, yl, xl+dxl, yl+dyl)
  leg.SetFillStyle(0)
  leg.SetBorderSize(0)
  leg.SetTextSize(tsiz)

  return leg

#_____________________________________________________________________________
def col_lin(col, w=4, st=rt.kSolid):

  #create line of a given color
  lin = TLine()
  lin.SetLineColor(col)
  lin.SetLineWidth(w)
  lin.SetLineStyle(st)

  return lin

#_____________________________________________________________________________
def log_fit_result(r1, lmg=6):

  result = ""

  ss = std.stringstream()
  r1.printMultiline(ss, 0, rt.kTRUE)
  stream = ""
  while ss.eof() == False:
    chnum = ss.get()
    if chnum < 0: continue
    stream += chr(chnum)
  #put parameter numbers
  line_stream = stream.split("\n")
  pnum = -1
  for i in range(len(line_stream)):
    if pnum >= 0 and line_stream[i] != "":
      numlin = "  " + str(pnum) + line_stream[i][2+len(str(pnum)):]
      line_stream[i] = numlin
      pnum += 1
    if line_stream[i].find("--------") > -1:
      pnum += 1
    result += line_stream[i] + "\n"

  cor = r1.correlationMatrix()
  result += print_matrix(cor)

  #put left margin
  rline = result.split("\n")
  result = ""
  for line in rline:
    result += " ".ljust(lmg)
    result += line + "\n"

  return result

#_____________________________________________________________________________
def log_fit_parameters(r1, lmg=6):

    #direct access to fit parameters
    result = ""
    arglist = r1.floatParsFinal()
    idx = 0
    arg = arglist.at(idx)
    while arg != None:
        result += " ".ljust(lmg) + arg.GetName() + " = "
        result += "{0:.3f}".format(arg.getVal()) + " +/- "
        result += "{0:.3f}".format(arg.getError())
        result += "\n"
        #move to next
        idx += 1
        arg = arglist.at(idx)

    return result

#_____________________________________________________________________________
def table_fit_parameters(r1):

    #LaTex table with fit parameters
    result = ""
    arglist = r1.floatParsFinal()
    idx = 0
    arg = arglist.at(idx)
    while arg != None:
        result += "$" + arg.GetName() + "$ & "
        result += "{0:.3f}".format(arg.getVal()) + " $\pm$ "
        result += "{0:.3f}".format(arg.getError()) + " \\\\"
        result += "\n"
        #move to next
        idx += 1
        arg = arglist.at(idx)

    return result

#_____________________________________________________________________________
def log_results(out, msg, lmg=6):

    out.write(" ".ljust(lmg) + msg + "\n")

#_____________________________________________________________________________
def print_matrix(mat):

  result = "Correlation matrix:\n"

  line = "".rjust(4) + "| "
  for col in range(mat.GetNcols()):
    line += "{0:5d}  |".format(col)
  result += line + "\n"

  delim = "".ljust(5,"-")
  for col in range(mat.GetNcols()):
    delim += "".ljust(8,"-")
  delim += "-"
  result += delim + "\n"

  for row in range(mat.GetNrows()):
    line = "{0:3d} |".format(row)
    for col in range(mat.GetNcols()):
      line += "{0:8.3f}".format(mat(row,col))
    result += line + "\n"

  result += delim

  return result

#_____________________________________________________________________________
def print_pad(pad):
  
  next = TIter(pad.GetListOfPrimitives())

  print "#####################"
  obj = next()
  while obj != None:
    print obj.GetName(), obj.ClassName()
    obj = next()
  print "#####################"

#_____________________________________________________________________________
def invert_col(pad):

   #set foreground and background color
   #fgcol = rt.kGreen
   fgcol = rt.kOrange-3
   bgcol = rt.kBlack

   pad.SetFillColor(bgcol)
   pad.SetFrameLineColor(fgcol)

   next = TIter(pad.GetListOfPrimitives())
   obj = next()
   while obj != None:
      #H1
      if obj.InheritsFrom(TH1.Class()) == True:
         if obj.GetLineColor() == rt.kBlack:
            obj.SetLineColor(fgcol)
            obj.SetFillColor(bgcol)
         if obj.GetMarkerColor() == rt.kBlack: obj.SetMarkerColor(fgcol)
         obj.SetAxisColor(fgcol, "X")
         obj.SetAxisColor(fgcol, "Y")
         obj.SetLabelColor(fgcol, "X")
         obj.SetLabelColor(fgcol, "Y")
         obj.GetXaxis().SetTitleColor(fgcol)
         obj.GetYaxis().SetTitleColor(fgcol)
      #Legend
      if obj.InheritsFrom(TLegend.Class()) == True:
         obj.SetFillStyle(1000)
         obj.SetFillColor(fgcol)
         obj.SetTextColor(bgcol)
      #RooHist
      if obj.InheritsFrom(RooHist.Class()) == True:
         if obj.GetMarkerColor() == rt.kBlack:
            obj.SetLineColor(fgcol)
            obj.SetMarkerColor(fgcol)
      #H2
      if obj.InheritsFrom(TH2.Class()) == True:
         obj.SetAxisColor(fgcol, "Z")
         obj.SetLabelColor(fgcol, "Z")
         obj.GetZaxis().SetTitleColor(fgcol)
         #obj.SetLineColor(fgcol)
         #obj.SetMarkerColor(fgcol)
      #TLatex
      if obj.InheritsFrom(TLatex.Class()) == True:
         if obj.GetTextColor() == rt.kBlack:
            obj.SetTextColor( fgcol )
      #F2
      if obj.InheritsFrom(TF2.Class()) == True:
        axes = [obj.GetXaxis(), obj.GetYaxis(), obj.GetZaxis()]
        for i in range(len(axes)):
            axes[i].SetAxisColor(fgcol)
            axes[i].SetLabelColor(fgcol)
            axes[i].SetTitleColor(fgcol)
      #move to next item
      obj = next()





















