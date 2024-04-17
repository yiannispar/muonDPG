import ROOT
import argparse
import utils

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetTitleOffset(1.5, "Z")
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

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--legend', type=str, help='Dataset legend')
parser.add_argument('-o', type=str, help='Output directory')
parser.add_argument('-i', type=str, help='Input directory')
args = parser.parse_args()

dataset_legend = args.legend
output_dir = args.o
input_dir = args.i

utils.merge_root_files(input_dir)

in_file = ROOT.TFile(input_dir + "merged_total.root", "READ")
c = ROOT.TCanvas("c", "c", 800, 800)
c.SetGrid()

WPs = ["SingleMu1_10", "SingleMu2_10", "SingleMu3_10", "SingleMu4_10"]

vars_title = {
    "eta": "#eta_{Reco}",
    "phi": "#phi_{Reco}",
    "pt2": "p^{Reco}_{T} [GeV]",
    "pt": "p^{Reco}_{T} [GeV]"
}

# Define marker colors for each WP
# marker_colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kCyan]
marker_colors = [color_0, color_1, color_2, color_5]

# Loop over each variable
for var in vars_title:

    # Clear histograms list for each variable
    eff_histograms = []

    leg = ROOT.TLegend(0.65, 0.15, 0.95, 0.48)
    leg.SetFillStyle(0)

    for i, wp in enumerate(WPs):
        key = wp + "_" + var

        h_passed_BMTF = in_file.Get("BMTF_" + key + "_passed")
        h_passed_BMTF = utils.add_overflow(h_passed_BMTF)
        h_total_BMTF = in_file.Get("BMTF_" + key + "_total")
        h_total_BMTF = utils.add_overflow(h_total_BMTF)
        h_eff_BMTF = ROOT.TEfficiency(h_passed_BMTF, h_total_BMTF)
        marker_color = marker_colors[i % len(marker_colors)]  # Cycle through colors
        h_eff_BMTF.SetMarkerColor(marker_color)
        h_eff_BMTF.SetLineColor(marker_color)
        h_eff_BMTF.SetMarkerStyle(20 + i)  # Vary marker style

        eff_histograms.append(h_eff_BMTF)

        # Generate legend entry label
        quality_threshold = 12 + i
        legend_entry_label = "Quality #geq {}".format(quality_threshold)

        # Add entry to legend
        leg.AddEntry(h_eff_BMTF, legend_entry_label, "lep")

    # Draw histograms for current variable
    c.cd()
    eff_histograms[0].Draw()
    for hist in eff_histograms[1:]:
        hist.Draw("same")

    # Draw legend and additional text
    leg.Draw()
    latex.SetTextSize(0.04)
    latex.DrawLatexNDC(0.80,0.91,dataset_legend)
    # latex.DrawLatexNDC(0.54, 0.48, "p^{#mu,L1}_{T} #geq 22 GeV")
    # if var == "eta" or var == "phi" or var == "nPV":
    #     latex.DrawLatexNDC(0.54, 0.41, "p^{#mu,Reco}_{T} #geq 26 GeV")
    latex.SetTextSize(0.045)
    latex.DrawLatexNDC(0.1, 0.91, "#font[61]{CMS}")
    latex.SetTextSize(0.0346)
    latex.DrawLatexNDC(0.195, 0.91, "#font[52]{Internal}")
    latex.DrawLatexNDC(0.69, 0.48, "#bf{p^{#mu,L1}_{T} #geq 10 GeV}")
    
    c.Update() 
    if var == "pt":# Ensure canvas is updated before modifying histogram settings
        eff_histograms[0].GetPaintedGraph().GetXaxis().SetRangeUser(10, 160)
    eff_histograms[0].GetPaintedGraph().GetYaxis().SetRangeUser(0, 1.1)

    # Save canvas as image
    c.SaveAs(output_dir + "eff_qual_" + var + ".png")

# Close input file
in_file.Close()

