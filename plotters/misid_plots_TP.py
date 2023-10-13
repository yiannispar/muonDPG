import ROOT
import argparse
import utils

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetTitleOffset(1.5,"Z")
ROOT.gStyle.SetPalette(ROOT.kBlueGreenYellow)

#parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--legend', type=str, help='dataset legend')
parser.add_argument('-o', type=str, help='output dir')
parser.add_argument('-i', type=str, help='input dir dir')
args = parser.parse_args()

dataset_legend = args.legend
output_dir = args.o
input_dir = args.i

latex = ROOT.TLatex()
latex.SetTextSize(0.04)
ROOT.gStyle.SetLegendTextSize(0.035)

in_file = ROOT.TFile(input_dir + "merged_total.root","READ")
c = ROOT.TCanvas("c","c",800,800)
c.SetLeftMargin(0.11)
c.SetRightMargin(0.15)
c.SetGrid()

WPs = ["SingleMu_22"]

vars_title = {
    #"eta": "#eta_{Reco}",
    #"phi": "#phi_{Reco}",
    "pt": "p^{Reco}_{T} [GeV]",
    "pt2": "p^{Reco}_{T} [GeV]",
    #"nPV": "Number of Vertices"
}

for var in vars_title:
    key = "_" + var

    c.SetLogx(0)
    h_passed_uGMT = in_file.Get("uGMT_" + key +"_passed")
    h_passed_uGMT = utils.add_overflow(h_passed_uGMT)
    h_total_uGMT = in_file.Get("uGMT_" + key + "_total")
    h_total_uGMT = utils.add_overflow(h_total_uGMT)
    h_misid_uGMT = ROOT.TEfficiency(h_passed_uGMT,h_total_uGMT)
    h_misid_uGMT.SetMarkerColor(ROOT.kRed)
    h_misid_uGMT.SetLineColor(ROOT.kRed)
    h_misid_uGMT.SetMarkerStyle(20)
    h_misid_uGMT.Draw()
    h_misid_uGMT.SetTitle(";" + vars_title[var] + ";Charge misidentification")
    c.Update()
    graph = h_misid_uGMT.GetPaintedGraph() 
    graph.SetMinimum(0)
    graph.SetMaximum(1.1)
    if var == "pt":
        c.SetLogx(1)
        graph.GetXaxis().SetLimits(1,1000)
        graph.GetXaxis().SetTitleOffset(1.3)
    if var == "nPV":
        graph.GetXaxis().SetLimits(0,70)
    c.Update()

    h_passed_BMTF = in_file.Get("BMTF_" + key + "_passed")
    h_passed_BMTF = utils.add_overflow(h_passed_BMTF)
    h_total_BMTF = in_file.Get("BMTF_" + key + "_total")
    h_total_BMTF = utils.add_overflow(h_total_BMTF)
    h_misid_BMTF = ROOT.TEfficiency(h_passed_BMTF,h_total_BMTF)
    h_misid_BMTF.SetMarkerColor(ROOT.kGreen+2)
    h_misid_BMTF.SetLineColor(ROOT.kGreen+2)
    h_misid_BMTF.SetMarkerStyle(21)
    h_misid_BMTF.Draw("same")

    h_passed_OMTF = in_file.Get("OMTF_" + key + "_passed")
    h_passed_OMTF = utils.add_overflow(h_passed_OMTF)
    h_total_OMTF = in_file.Get("OMTF_" + key + "_total")
    h_total_OMTF = utils.add_overflow(h_total_OMTF)
    h_misid_OMTF = ROOT.TEfficiency(h_passed_OMTF,h_total_OMTF)
    h_misid_OMTF.SetMarkerColor(ROOT.kBlue)
    h_misid_OMTF.SetLineColor(ROOT.kBlue)
    h_misid_OMTF.SetMarkerStyle(22)
    h_misid_OMTF.Draw("same")

    h_passed_EMTF = in_file.Get("EMTF_" + key + "_passed")
    h_passed_EMTF = utils.add_overflow(h_passed_EMTF)
    h_total_EMTF = in_file.Get("EMTF_" + key + "_total")
    h_total_EMTF = utils.add_overflow(h_total_EMTF)
    h_misid_EMTF = ROOT.TEfficiency(h_passed_EMTF,h_total_EMTF)
    h_misid_EMTF.SetMarkerColor(ROOT.kMagenta)
    h_misid_EMTF.SetLineColor(ROOT.kMagenta)
    h_misid_EMTF.SetMarkerStyle(23)
    h_misid_EMTF.Draw("same")

    leg = ROOT.TLegend(0.55, 0.9, 0.8, 0.65)
    #leg = ROOT.TLegend(0.55,0.13,0.8,0.38)
    leg.SetFillStyle(0)
    leg.AddEntry(h_misid_uGMT,"|#eta| #leq 2.4","lep")
    leg.AddEntry(h_misid_BMTF,"|#eta| #leq 0.83","lep")
    leg.AddEntry(h_misid_OMTF,"0.83 < |#eta| #leq 1.24","lep")
    leg.AddEntry(h_misid_EMTF,"1.24 < |#eta| #leq 2.4","lep")
    leg.Draw()

    latex.DrawLatexNDC(0.78,0.91,dataset_legend)
    latex.DrawLatexNDC(0.54,0.6,"Tight L1 quality")
    #latex.DrawLatexNDC(0.54, 0.48, "p^{#mu,L1}_{T} #geq 22 GeV")
    #if var == "eta" or var == "phi" or var == "nPV":
        # latex.DrawLatexNDC(0.54, 0.41, "p^{#mu,Reco}_{T} #geq 5 GeV")
        #latex.DrawLatexNDC(0.54, 0.41, "5 GeV #leq p^{#mu,Reco}_{T} < 10 GeV")
    latex.DrawLatexNDC(0.1, 0.91, "#bf{ #font[22]{CMS} #font[72]{Preliminary} }")

    c.SaveAs(output_dir + "misid_TP" + key + ".png")

## eta vs phi

key2 = "__phi_eta"

h_misid_uGMT = in_file.Get("h_misid_phi_etauGMT_" )
h_misid_uGMT.SetTitle(";#eta_{Reco};#phi_{Reco} [rad]; Charge misidentification")
h_misid_uGMT.Draw("colz")
latex.DrawLatexNDC(0.70,0.91,dataset_legend)
latex.DrawLatexNDC(0.1, 0.91, "#bf{ #font[22]{CMS} #font[72]{Preliminary} }")
line = ROOT.TLine(-1.24, -4, -1.24, 4)
line.SetLineWidth(2)
line.SetLineColor(ROOT.kRed)
line.SetLineStyle(9)
line.Draw("same")
line1 = ROOT.TLine(-0.83, -4, -0.83, 4)
line1.SetLineWidth(2)
line1.SetLineColor(ROOT.kRed)
line1.SetLineStyle(9)
line1.Draw("same")
line2 = ROOT.TLine(0.83, -4, 0.83, 4)
line2.SetLineWidth(2)
line2.SetLineColor(ROOT.kRed)
line2.SetLineStyle(9)
line2.Draw("same")
line3 = ROOT.TLine(1.24, -4, 1.24, 4)
line3.SetLineWidth(2)
line3.SetLineColor(ROOT.kRed)
line3.SetLineStyle(9)
line3.Draw("same")

latex.SetTextSize(0.021)
latex.DrawLatexNDC(0.46,0.87,"BMTF")
latex.DrawLatexNDC(0.30,0.87,"OMTF")
latex.DrawLatexNDC(0.18,0.87,"EMTF")
latex.DrawLatexNDC(0.605,0.87,"OMTF")
latex.DrawLatexNDC(0.73,0.87,"EMTF")
c.SaveAs(output_dir + "misid_TP" + key2 + ".png")

##l1 eta vs l1 phi

h_l1_misid_uGMT = in_file.Get("h_misid_l1_phi_etauGMT_" )
h_l1_misid_uGMT.SetTitle(";L1#eta;L1#phi [rad]; Charge misidentification")
h_l1_misid_uGMT.Draw("colz")
latex.DrawLatexNDC(0.70,0.91,dataset_legend)
latex.DrawLatexNDC(0.1, 0.91, "#bf{ #font[22]{CMS} #font[72]{Preliminary} }")
line = ROOT.TLine(-1.24, -4, -1.24, 4)
line.SetLineWidth(2)
line.SetLineColor(ROOT.kRed)
line.SetLineStyle(9)
line.Draw("same")
line1 = ROOT.TLine(-0.83, -4, -0.83, 4)
line1.SetLineWidth(2)
line1.SetLineColor(ROOT.kRed)
line1.SetLineStyle(9)
line1.Draw("same")
line2 = ROOT.TLine(0.83, -4, 0.83, 4)
line2.SetLineWidth(2)
line2.SetLineColor(ROOT.kRed)
line2.SetLineStyle(9)
line2.Draw("same")
line3 = ROOT.TLine(1.24, -4, 1.24, 4)
line3.SetLineWidth(2)
line3.SetLineColor(ROOT.kRed)
line3.SetLineStyle(9)
line3.Draw("same")

latex.SetTextSize(0.021)
latex.DrawLatexNDC(0.46,0.87,"BMTF")
latex.DrawLatexNDC(0.30,0.87,"OMTF")
latex.DrawLatexNDC(0.18,0.87,"EMTF")
latex.DrawLatexNDC(0.605,0.87,"OMTF")
latex.DrawLatexNDC(0.73,0.87,"EMTF")
c.SaveAs(output_dir + "misid_TP_l1" + key2 + ".png")

#Difference of eta_phi reco vs eta_phi L1

# Convert TEfficiency histograms to TH2F histograms
h_hist1 = h_misid_uGMT.CreateHistogram()
h_hist2 = h_l1_misid_uGMT.CreateHistogram()

hist_difference = h_hist1.Clone("hist_difference")
hist_difference.Add(h_hist2, -1)
hist_difference.SetTitle(";#eta;#phi [rad]; Charge misidentification")
hist_difference.Draw("colz")
latex.DrawLatexNDC(0.70,0.91,dataset_legend)
latex.DrawLatexNDC(0.1, 0.91, "#bf{ #font[22]{CMS} #font[72]{Preliminary} }")
line = ROOT.TLine(-1.24, -4, -1.24, 4)
line.SetLineWidth(2)
line.SetLineColor(ROOT.kBlack)
line.SetLineStyle(9)
line.Draw("same")
line1 = ROOT.TLine(-0.83, -4, -0.83, 4)
line1.SetLineWidth(2)
line1.SetLineColor(ROOT.kBlack)
line1.SetLineStyle(9)
line1.Draw("same")
line2 = ROOT.TLine(0.83, -4, 0.83, 4)
line2.SetLineWidth(2)
line2.SetLineColor(ROOT.kBlack)
line2.SetLineStyle(9)
line2.Draw("same")
line3 = ROOT.TLine(1.24, -4, 1.24, 4)
line3.SetLineWidth(2)
line3.SetLineColor(ROOT.kBlack)
line3.SetLineStyle(9)
line3.Draw("same")

latex.SetTextSize(0.021)
latex.DrawLatexNDC(0.46,0.87,"BMTF")
latex.DrawLatexNDC(0.30,0.87,"OMTF")
latex.DrawLatexNDC(0.18,0.87,"EMTF")
latex.DrawLatexNDC(0.605,0.87,"OMTF")
latex.DrawLatexNDC(0.73,0.87,"EMTF")
c.SaveAs(output_dir + "misid_TP_difference.png")