import ROOT
import argparse
import utils
import os

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetTitleOffset(1.5,"Z")
ROOT.gStyle.SetPalette(ROOT.kBlueGreenYellow)
latex = ROOT.TLatex()
latex.SetTextSize(0.04)
latex.SetTextFont(42)
ROOT.gStyle.SetLegendTextSize(0.035)

# Colors
color_0 = ROOT.TColor.GetColor(87,144,252) #blue
color_1 = ROOT.TColor.GetColor(248,156,32) #orange
color_2 = ROOT.TColor.GetColor(228,37,54) #red
color_3 = ROOT.TColor.GetColor(150,74,139) #purple
color_4 = ROOT.TColor.GetColor(156,156,161) #gray
color_5 = ROOT.TColor.GetColor(122,33,221) #purple

#parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--legend', type=str, help='dataset legend')
parser.add_argument('-o', type=str, help='output dir')
parser.add_argument('-i', type=str, help='input dir dir')
args = parser.parse_args()

if args.legend == '2024B':
    dataset_legend ='2024B (0.13 fb^{-1})'
    dataset_x1=0.64
    dataset_x2=0.59
elif args.legend == '2024C':
    dataset_legend ='2024C (7.24 fb^{-1})'
    dataset_x1=0.64
    dataset_x2=0.59
elif args.legend == '2024D':
    dataset_legend ='2024D (7.96 fb^{-1})'
    dataset_x1=0.64
    dataset_x2=0.59
elif args.legend == '2024E':
    dataset_legend ='2024E (11.32 fb^{-1})'
    dataset_x1=0.62
    dataset_x2=0.57
elif args.legend == '2024F':
    dataset_legend ='2024F (27.76 fb^{-1})'
    dataset_x1=0.62
    dataset_x2=0.57
elif args.legend == '2024':
    dataset_legend ='97 fb^{-1} (13.6 TeV)'
    dataset_x1=0.64
    dataset_x2=0.59
else:
    dataset_legend = args.legend
    dataset_x1=0.80
    dataset_x2=0.75
output_dir = args.o
input_dir = args.i

## merge root files
utils.merge_root_files(input_dir)

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
    #"nPV": "Number of Vertices"
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
        # h_eff_uGMT.SetMarkerColor(ROOT.kRed)
        # h_eff_uGMT.SetLineColor(ROOT.kRed)
        h_eff_uGMT.SetMarkerColor(color_0)
        h_eff_uGMT.SetLineColor(color_0)
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
        # h_eff_BMTF.SetMarkerColor(ROOT.kGreen+2)
        # h_eff_BMTF.SetLineColor(ROOT.kGreen+2)
        h_eff_BMTF.SetMarkerColor(color_1)
        h_eff_BMTF.SetLineColor(color_1)
        h_eff_BMTF.SetMarkerStyle(21)
        h_eff_BMTF.Draw("same")

        h_passed_OMTF = in_file.Get("OMTF_" + key + "_passed")
        h_passed_OMTF = utils.add_overflow(h_passed_OMTF)
        h_total_OMTF = in_file.Get("OMTF_" + key + "_total")
        h_total_OMTF = utils.add_overflow(h_total_OMTF)
        h_eff_OMTF = ROOT.TEfficiency(h_passed_OMTF,h_total_OMTF)
        # h_eff_OMTF.SetMarkerColor(ROOT.kBlue)
        # h_eff_OMTF.SetLineColor(ROOT.kBlue)
        h_eff_OMTF.SetMarkerColor(color_2)
        h_eff_OMTF.SetLineColor(color_2)
        h_eff_OMTF.SetMarkerStyle(22)
        h_eff_OMTF.Draw("same")

        h_passed_EMTF = in_file.Get("EMTF_" + key + "_passed")
        h_passed_EMTF = utils.add_overflow(h_passed_EMTF)
        h_total_EMTF = in_file.Get("EMTF_" + key + "_total")
        h_total_EMTF = utils.add_overflow(h_total_EMTF)
        h_eff_EMTF = ROOT.TEfficiency(h_passed_EMTF,h_total_EMTF)
        # h_eff_EMTF.SetMarkerColor(ROOT.kMagenta)
        # h_eff_EMTF.SetLineColor(ROOT.kMagenta)
        h_eff_EMTF.SetMarkerColor(color_5)
        h_eff_EMTF.SetLineColor(color_5)
        h_eff_EMTF.SetMarkerStyle(23)
        h_eff_EMTF.Draw("same")

        leg = ROOT.TLegend(0.62,0.13,0.8,0.38)
        leg.SetFillStyle(0)
        leg.AddEntry(h_eff_uGMT,"|#eta| #leq 2.4","lep")
        leg.AddEntry(h_eff_BMTF,"|#eta| #leq 0.83","lep")
        leg.AddEntry(h_eff_OMTF,"0.83 < |#eta| #leq 1.24","lep")
        leg.AddEntry(h_eff_EMTF,"1.24 < |#eta| #leq 2.4","lep")
        leg.Draw()

        latex.SetTextSize(0.04)
        latex.DrawLatexNDC(dataset_x1,0.91,dataset_legend)
        if var == "eta" or var == "phi" or var == "nPV":
            # latex.DrawLatexNDC(0.54, 0.41, "p^{#mu,Reco}_{T} #geq 5 GeV")
            latex.DrawLatexNDC(0.62,0.55,"#bf{Tight L1 quality}")
            latex.DrawLatexNDC(0.64, 0.48, "#bf{p^{#mu,L1}_{T} #geq 22 GeV}")
            latex.DrawLatexNDC(0.62, 0.41, " #bf{p^{#mu,Reco}_{T} #geq 26 GeV}")
        else:
            latex.DrawLatexNDC(0.62,0.48,"#bf{Tight L1 quality}")
            latex.DrawLatexNDC(0.64, 0.41, "#bf{p^{#mu,L1}_{T} #geq 22 GeV}")
        latex.SetTextSize(0.045)
        latex.DrawLatexNDC(0.1, 0.91, "#font[61]{CMS}")
        latex.SetTextSize(0.0346)
        latex.DrawLatexNDC(0.195, 0.91, "#font[52]{Internal}")



        c.SaveAs(output_dir + "eff_" + key + ".png")

c2 = ROOT.TCanvas("c2","c2",800,800)
c2.SetLeftMargin(0.11)
c2.SetRightMargin(0.15)
c2.SetGrid()

## eta vs phi
key = "SingleMu_22_phi_eta" 
h_passed_uGMT = in_file.Get("uGMT_" + key + "_passed")
h_total_uGMT =in_file.Get("uGMT_" + key + "_total")
h_eff_uGMT = ROOT.TEfficiency(h_passed_uGMT,h_total_uGMT)
h_eff_uGMT.SetTitle(";#eta_{Reco};#phi_{Reco} [rad];Efficiency")
h_eff_uGMT.Draw("colz")
latex.SetTextSize(0.04)
latex.DrawLatexNDC(dataset_x2,0.91,dataset_legend)
latex.SetTextSize(0.045)
latex.DrawLatexNDC(0.11, 0.91, "#font[61]{CMS}")
latex.SetTextSize(0.0346)
latex.DrawLatexNDC(0.205, 0.91, "#font[52]{Internal}")
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
latex.DrawLatexNDC(0.453,0.87,"BMTF")
latex.DrawLatexNDC(0.30,0.87,"OMTF")
latex.DrawLatexNDC(0.18,0.87,"EMTF")
latex.DrawLatexNDC(0.605,0.87,"OMTF")
latex.DrawLatexNDC(0.73,0.87,"EMTF")
c2.SaveAs(output_dir + "eff_" + key + ".png")