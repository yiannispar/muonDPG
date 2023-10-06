import math

def add_overflow(h):
    nbins = h.GetNbinsX()+1
    e1 = h.GetBinError(nbins-1)
    e2 = h.GetBinError(nbins)
    h.AddBinContent(nbins-1, h.GetBinContent(nbins))
    h.SetBinError(nbins-1, math.sqrt(e1*e1 + e2*e2))
    h.SetBinContent(nbins, 0)
    h.SetBinError(nbins, 0)
    return h