import ROOT
import argparse
import utils

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetTitleOffset(1.5,"Z")
# ROOT.gStyle.SetPalette(ROOT.kBlueGreenYellow)

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
# c.SetLeftMargin(0.11)
# c.SetRightMargin(0.15)
c.SetGrid()

WPs = ["SingleMu_22"]

vars_title = {
    "eta": "#eta_{Reco}",
    "phi": "#phi_{Reco}",
    "pt": "p^{Reco}_{T} [GeV]",
    "pt2": "p^{Reco}_{T} [GeV]",
    "nPV": "Number of Vertices"
}

## eff vs var
for wp in WPs:
    for var in vars_title:
        key = wp + "_" + var
        c.SetLogx(0)

        h_passed_uGMT = in_file.Get("uGMT_" + key + "_passed")
        h_passed_uGMT = utils.add_overflow(h_passed_uGMT)
        h_total_uGMT = in_file.Get("uGMT_" + key + "_total")
        h_total_uGMT = utils.add_overflow(h_total_uGMT)
        h_eff_uGMT = ROOT.TEfficiency(h_passed_uGMT,h_total_uGMT)
        h_eff_uGMT.SetMarkerColor(ROOT.kRed)
        h_eff_uGMT.SetLineColor(ROOT.kRed)
        h_eff_uGMT.SetMarkerStyle(20)
        h_eff_uGMT.Draw()
        h_eff_uGMT.SetTitle(";" + vars_title[var] + ";Efficiency")
        c.Update()
        graph = h_eff_uGMT.GetPaintedGraph() 
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
        h_eff_BMTF = ROOT.TEfficiency(h_passed_BMTF,h_total_BMTF)
        h_eff_BMTF.SetMarkerColor(ROOT.kGreen+2)
        h_eff_BMTF.SetLineColor(ROOT.kGreen+2)
        h_eff_BMTF.SetMarkerStyle(21)
        h_eff_BMTF.Draw("same")

        h_passed_OMTF = in_file.Get("OMTF_" + key + "_passed")
        h_passed_OMTF = utils.add_overflow(h_passed_OMTF)
        h_total_OMTF = in_file.Get("OMTF_" + key + "_total")
        h_total_OMTF = utils.add_overflow(h_total_OMTF)
        h_eff_OMTF = ROOT.TEfficiency(h_passed_OMTF,h_total_OMTF)
        h_eff_OMTF.SetMarkerColor(ROOT.kBlue)
        h_eff_OMTF.SetLineColor(ROOT.kBlue)
        h_eff_OMTF.SetMarkerStyle(22)
        h_eff_OMTF.Draw("same")

        h_passed_EMTF = in_file.Get("EMTF_" + key + "_passed")
        h_passed_EMTF = utils.add_overflow(h_passed_EMTF)
        h_total_EMTF = in_file.Get("EMTF_" + key + "_total")
        h_total_EMTF = utils.add_overflow(h_total_EMTF)
        h_eff_EMTF = ROOT.TEfficiency(h_passed_EMTF,h_total_EMTF)
        h_eff_EMTF.SetMarkerColor(ROOT.kMagenta)
        h_eff_EMTF.SetLineColor(ROOT.kMagenta)
        h_eff_EMTF.SetMarkerStyle(23)
        h_eff_EMTF.Draw("same")

        leg = ROOT.TLegend(0.55,0.13,0.8,0.38)
        leg.SetFillStyle(0)
        leg.AddEntry(h_eff_uGMT,"|#eta| #leq 2.4","lep")
        leg.AddEntry(h_eff_BMTF,"|#eta| #leq 0.83","lep")
        leg.AddEntry(h_eff_OMTF,"0.83 < |#eta| #leq 1.24","lep")
        leg.AddEntry(h_eff_EMTF,"1.24 < |#eta| #leq 2.4","lep")
        leg.Draw()

        latex.DrawLatexNDC(0.78,0.91,dataset_legend)
        latex.DrawLatexNDC(0.54,0.55,"Tight L1 quality")
        latex.DrawLatexNDC(0.54, 0.48, "p^{#mu,L1}_{T} #geq 22 GeV")
        if var == "eta" or var == "phi" or var == "nPV":
            # latex.DrawLatexNDC(0.54, 0.41, "p^{#mu,Reco}_{T} #geq 5 GeV")
            latex.DrawLatexNDC(0.54, 0.41, "5 GeV #leq p^{#mu,Reco}_{T} < 10 GeV")
        latex.DrawLatexNDC(0.1, 0.91, "#bf{ #font[22]{CMS} #font[72]{Preliminary} }")

        c.SaveAs(output_dir + "eff_" + key + ".png")

# ## eta vs phi
# key = "SingleMu_5_phi_eta" 
# h_passed_uGMT = in_file.Get("uGMT_" + key + "_passed")
# h_total_uGMT =in_file.Get("uGMT_" + key + "_total")
# h_eff_uGMT = ROOT.TEfficiency(h_passed_uGMT,h_total_uGMT)
# h_eff_uGMT.SetTitle(";#eta;#phi [rad];Efficiency")
# h_eff_uGMT.Draw("colz")
# latex.DrawLatexNDC(0.70,0.91,dataset_legend)
# latex.DrawLatexNDC(0.1, 0.91, "#bf{ #font[22]{CMS} #font[72]{Preliminary} }")
# line = ROOT.TLine(-1.24, -4, -1.24, 4)
# line.SetLineWidth(2)
# line.SetLineColor(ROOT.kBlack)
# line.SetLineStyle(9)
# line.Draw("same")
# line1 = ROOT.TLine(-0.83, -4, -0.83, 4)
# line1.SetLineWidth(2)
# line1.SetLineColor(ROOT.kBlack)
# line1.SetLineStyle(9)
# line1.Draw("same")
# line2 = ROOT.TLine(0.83, -4, 0.83, 4)
# line2.SetLineWidth(2)
# line2.SetLineColor(ROOT.kBlack)
# line2.SetLineStyle(9)
# line2.Draw("same")
# line3 = ROOT.TLine(1.24, -4, 1.24, 4)
# line3.SetLineWidth(2)
# line3.SetLineColor(ROOT.kBlack)
# line3.SetLineStyle(9)
# line3.Draw("same")

# latex.SetTextSize(0.021)
# latex.DrawLatexNDC(0.46,0.87,"BMTF")
# latex.DrawLatexNDC(0.30,0.87,"OMTF")
# latex.DrawLatexNDC(0.18,0.87,"EMTF")
# latex.DrawLatexNDC(0.605,0.87,"OMTF")
# latex.DrawLatexNDC(0.73,0.87,"EMTF")
# c.SaveAs(output_dir + "eff_" + key + ".png")