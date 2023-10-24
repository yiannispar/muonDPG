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
vars_title = {
    "response_": "p^{L1}_{T}/p^{Reco}_{T}",
}
trig_TF = {
    'Black': [0.00, 0.83],
    'Red': [0.83, 1.24],
    'Blue': [1.24, 2.40],
    'Yellow': [1.24, 1.6],
    'Pink': [1.6, 2.1],
    'Green': [2.1, 2.40],
    'Gray': [0.00, 2.40]
}

leg = ROOT.TLegend(0.55, 0.13, 0.8, 0.38)
leg.SetFillStyle(0)

colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kYellow, ROOT.kMagenta, ROOT.kGreen, ROOT.kGray]

#for the combined histogram for all regions

# for var in vars_title:
#     for i, (tf, tf_range) in enumerate(trig_TF.items()):
#         region = var + tf + '_'
#         label = tf
#         profile = in_file.Get(region)
#         profile.SetLineColor(colors[i % len(colors)])
#         profile.SetMarkerColor(colors[i % len(colors)])
#         profile.SetTitle(vars_title[var])
#         profile.GetYaxis().SetRangeUser(0.8, 1.6)
#         profile.GetXaxis().SetTitle("pT_{reco}(GeV)")  # Set your X-axis label here
#         profile.GetYaxis().SetTitle("response")  
#         profile.Draw("same")
#         c.Update
#         leg.AddEntry(profile, f"{tf_range[0]:.2f} < |#eta| #leq {tf_range[1]:.2f}", "lep")


        
# latex.DrawLatexNDC(0.78, 0.91, dataset_legend)
# latex.DrawLatexNDC(0.54, 0.55, "Tight L1 quality")
# latex.DrawLatexNDC(0.1, 0.91, "#bf{ #font[22]{CMS} #font[72]{Preliminary} }")
# leg.Draw()
# c.SaveAs(output_dir + var +"testall.png")

#for the separate histograms

for var in vars_title:
    for i, (tf, tf_range) in enumerate(trig_TF.items()):
        region = var + tf + '_'
        label = tf
        profile = in_file.Get(region)
        profile.SetLineColor(colors[i % len(colors)])
        profile.SetMarkerColor(colors[i % len(colors)])
        profile.SetTitle(vars_title[var])
        profile.GetYaxis().SetRangeUser(0.8, 1.6)
        profile.GetXaxis().SetTitle("p_{Treco}(GeV)")  # Set your X-axis label here
        profile.GetYaxis().SetTitle("response")  
        profile.Draw("")
        c.Update
        leg.AddEntry(profile, f"{tf_range[0]:.2f} < |#eta| #leq {tf_range[1]:.2f}", "lep")
        latex.DrawLatexNDC(0.78, 0.91, dataset_legend)
        latex.DrawLatexNDC(0.54, 0.55, "Tight L1 quality")
        latex.DrawLatexNDC(0.1, 0.91, "#bf{ #font[22]{CMS} #font[72]{Preliminary} }")
        leg.Draw()
        c.SaveAs(output_dir + region +"test.png")

