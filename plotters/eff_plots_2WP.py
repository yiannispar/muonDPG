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
# ROOT.gStyle.SetPadTickY(1)


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
elif args.legend == '2024G':
    dataset_legend ='2024G (37.77 fb^{-1})'
    dataset_x1=0.62
    dataset_x2=0.57
elif args.legend == '2024H':
    dataset_legend ='2024H (5.44 fb^{-1})'
    dataset_x1=0.64
    dataset_x2=0.59
elif args.legend == '2024I':
    dataset_legend ='2024I (11.47 fb^{-1})'
    dataset_x1=0.62
    dataset_x2=0.57
elif args.legend == '2024':
    dataset_legend ='109 fb^{-1} (13.6 TeV)'
    dataset_x1=0.60
    dataset_x2=0.55
else:
    dataset_legend = args.legend
    dataset_x1=0.80
    dataset_x2=0.75
output_dir = args.o
input_dir = args.i

## merge root files
# utils.merge_root_files(input_dir)

in_file = ROOT.TFile(input_dir + "merged_total.root","READ")
c = ROOT.TCanvas("c","c",800,800)
# c.SetLeftMargin(0.11)
# c.SetRightMargin(0.15)
c.SetGrid()

WPs = ["SingleMu1_22","SingleMu2_5"]

wp_values = {
    "SingleMu1_22": {"quality": 12, "pt_l1": 22, "pt_reco": 26},
    "SingleMu2_5": {"quality": 8, "pt_l1": 5, "pt_reco": 9}
}

vars_title = {
    "eta": "#eta_{Reco}",
    "phi": "#phi_{Reco}",
    "pt": "p^{#mu,offline}_{T} [GeV]",
    "pt2": "p^{#mu,offline}_{T} [GeV]",
    #"nPV": "Number of Vertices"
}

## eff vs var
for wp in WPs:
    for var in vars_title:
        key = wp + "_" + var
        c.SetLogx(0)
        values = wp_values[wp]
        quality_label = f"L1 quality #geq {values['quality']}"
        pt_l1_label = f"p^{{#mu,L1}}_{{T}} #geq {values['pt_l1']} GeV"
        pt_reco_label = f"p^{{#mu,Reco}}_{{T}} #geq {values['pt_reco']} GeV"

        if var == "eta":

# Retrieve histograms for BMTF, OMTF, EMTF
            h_passed_EMTF = in_file.Get("EMTF_" + key + "_passed")
            h_passed_EMTF = utils.add_overflow(h_passed_EMTF)
            h_total_EMTF = in_file.Get("EMTF_" + key + "_total")
            h_total_EMTF = utils.add_overflow(h_total_EMTF)

            h_passed_BMTF = in_file.Get("BMTF_" + key + "_passed")
            h_passed_BMTF = utils.add_overflow(h_passed_BMTF)
            h_total_BMTF = in_file.Get("BMTF_" + key + "_total")
            h_total_BMTF = utils.add_overflow(h_total_BMTF)

            h_passed_OMTF = in_file.Get("OMTF_" + key + "_passed")
            h_passed_OMTF = utils.add_overflow(h_passed_OMTF)
            h_total_OMTF = in_file.Get("OMTF_" + key + "_total")
            h_total_OMTF = utils.add_overflow(h_total_OMTF)

            # Handle overlap assignment without averaging
            # For |eta| ~ 0.83 (BMTF and OMTF overlap), assign to OMTF
            for i in range(1, h_total_BMTF.GetNbinsX() + 1):
                eta_val = h_total_BMTF.GetXaxis().GetBinCenter(i)
                if 0.8 < abs(eta_val) < 0.86:
                    # Move BMTF points to OMTF
                    passed_bmtf = h_passed_BMTF.GetBinContent(i)
                    total_bmtf = h_total_BMTF.GetBinContent(i)
                    
                    # Add BMTF counts to OMTF
                    h_passed_OMTF.SetBinContent(i, h_passed_OMTF.GetBinContent(i) + passed_bmtf)
                    h_total_OMTF.SetBinContent(i, h_total_OMTF.GetBinContent(i) + total_bmtf)
                    
                    # Optionally zero out the BMTF overlap bin if you don't want to keep it
                    h_passed_BMTF.SetBinContent(i, 0)
                    h_total_BMTF.SetBinContent(i, 0)

            # For |eta| ~ 1.24 (OMTF and EMTF overlap), assign to EMTF
            for i in range(1, h_total_OMTF.GetNbinsX() + 1):
                eta_val = h_total_OMTF.GetXaxis().GetBinCenter(i)
                if 1.23 < abs(eta_val) < 1.26:
                    # Move OMTF points to EMTF
                    passed_omtf = h_passed_OMTF.GetBinContent(i)
                    total_omtf = h_total_OMTF.GetBinContent(i)
                    
                    # Add OMTF counts to EMTF
                    h_passed_EMTF.SetBinContent(i, h_passed_EMTF.GetBinContent(i) + passed_omtf)
                    h_total_EMTF.SetBinContent(i, h_total_EMTF.GetBinContent(i) + total_omtf)

                    # Optionally zero out the OMTF overlap bin
                    h_passed_OMTF.SetBinContent(i, 0)
                    h_total_OMTF.SetBinContent(i, 0)

            # Recreate TEfficiency objects after modification of histograms
            h_eff_EMTF = ROOT.TEfficiency(h_passed_EMTF, h_total_EMTF)
            h_eff_BMTF = ROOT.TEfficiency(h_passed_BMTF, h_total_BMTF)
            h_eff_OMTF = ROOT.TEfficiency(h_passed_OMTF, h_total_OMTF)

            # Draw histograms
            # h_passed_uGMT = in_file.Get("uGMT_" + key + "_passed")
            # h_passed_uGMT = utils.add_overflow(h_passed_uGMT)
            # h_total_uGMT = in_file.Get("uGMT_" + key + "_total")
            # h_total_uGMT = utils.add_overflow(h_total_uGMT)
            # h_eff_uGMT = ROOT.TEfficiency(h_passed_uGMT,h_total_uGMT)
            # # h_eff_uGMT.SetMarkerColor(ROOT.kRed)
            # # h_eff_uGMT.SetLineColor(ROOT.kRed)
            # h_eff_uGMT.SetMarkerColor(color_0)
            # h_eff_uGMT.SetLineColor(color_0)
            # h_eff_uGMT.SetMarkerStyle(20)
            # h_eff_uGMT.Draw()
            

            h_eff_EMTF.SetMarkerColor(color_5)
            h_eff_EMTF.SetLineColor(color_5)
            h_eff_EMTF.SetMarkerStyle(23)
            h_eff_EMTF.Draw()
            h_eff_EMTF.SetTitle(";" + vars_title[var] + ";Efficiency")
            c.Update()
            graph = h_eff_EMTF.GetPaintedGraph() 
            graph.SetMinimum(0)
            graph.SetMaximum(1.1)
            c.Update()
            

            h_eff_BMTF.SetMarkerColor(color_1)
            h_eff_BMTF.SetLineColor(color_1)
            h_eff_BMTF.SetMarkerStyle(21)
            h_eff_BMTF.Draw("same")

            h_eff_OMTF.SetMarkerColor(color_2)
            h_eff_OMTF.SetLineColor(color_2)
            h_eff_OMTF.SetMarkerStyle(22)
            h_eff_OMTF.Draw("same")


            # h_passed_EMTF = in_file.Get("EMTF_" + key + "_passed")
            # h_passed_EMTF = utils.add_overflow(h_passed_EMTF)
            # h_total_EMTF = in_file.Get("EMTF_" + key + "_total")
            # h_total_EMTF = utils.add_overflow(h_total_EMTF)
            # h_eff_EMTF = ROOT.TEfficiency(h_passed_EMTF,h_total_EMTF)
            # # h_eff_EMTF.SetMarkerColor(ROOT.kMagenta)
            # # h_eff_EMTF.SetLineColor(ROOT.kMagenta)
            # h_eff_EMTF.SetMarkerColor(color_5)
            # h_eff_EMTF.SetLineColor(color_5)
            # h_eff_EMTF.SetMarkerStyle(23)
            # h_eff_EMTF.Draw()
            # h_eff_EMTF.SetTitle(";" + vars_title[var] + ";Efficiency")
            # c.Update()
            # graph = h_eff_EMTF.GetPaintedGraph() 
            # graph.SetMinimum(0)
            # graph.SetMaximum(1.1)
            # c.Update()

            # h_passed_BMTF = in_file.Get("BMTF_" + key + "_passed")
            # h_passed_BMTF = utils.add_overflow(h_passed_BMTF)
            # h_total_BMTF = in_file.Get("BMTF_" + key + "_total")
            # h_total_BMTF = utils.add_overflow(h_total_BMTF)
            # h_eff_BMTF = ROOT.TEfficiency(h_passed_BMTF,h_total_BMTF)
            # # h_eff_BMTF.SetMarkerColor(ROOT.kGreen+2)
            # # h_eff_BMTF.SetLineColor(ROOT.kGreen+2)
            # h_eff_BMTF.SetMarkerColor(color_1)
            # h_eff_BMTF.SetLineColor(color_1)
            # h_eff_BMTF.SetMarkerStyle(21)
            # h_eff_BMTF.Draw("same")

            # h_passed_OMTF = in_file.Get("OMTF_" + key + "_passed")
            # h_passed_OMTF = utils.add_overflow(h_passed_OMTF)
            # h_total_OMTF = in_file.Get("OMTF_" + key + "_total")
            # h_total_OMTF = utils.add_overflow(h_total_OMTF)
            # h_eff_OMTF = ROOT.TEfficiency(h_passed_OMTF,h_total_OMTF)
            # # h_eff_OMTF.SetMarkerColor(ROOT.kBlue)
            # # h_eff_OMTF.SetLineColor(ROOT.kBlue)
            # h_eff_OMTF.SetMarkerColor(color_2)
            # h_eff_OMTF.SetLineColor(color_2)
            # h_eff_OMTF.SetMarkerStyle(22)
            # h_eff_OMTF.Draw("same")

            # # Handle overlap assignment without averaging
            # # For |eta| ~ 0.83 (BMTF and OMTF overlap), assign to OMTF
            # for i in range(h_eff_BMTF.GetTotalHistogram().GetNbinsX()):
            #     eta_val = h_eff_BMTF.GetTotalHistogram().GetXaxis().GetBinCenter(i)
            #     if 0.82 < abs(eta_val) < 0.84:
            #         # We can choose to assign these overlap points to OMTF
            #         eff_bmtf = h_eff_BMTF.GetEfficiency(i)
            #         h_eff_OMTF.SetEfficiency(i, eff_bmtf)  # Assign BMTF efficiency to OMTF

            # # For |eta| ~ 1.24 (OMTF and EMTF overlap), assign to EMTF
            # for i in range(h_eff_OMTF.GetTotalHistogram().GetNbinsX()):
            #     eta_val = h_eff_OMTF.GetTotalHistogram().GetXaxis().GetBinCenter(i)
            #     if 1.23 < abs(eta_val) < 1.25:
            #         # Assign to EMTF
            #         eff_omtf = h_eff_OMTF.GetEfficiency(i)
            #         h_eff_EMTF.SetEfficiency(i, eff_omtf)  # Assign OMTF efficiency to EMTF

            # # Draw updated OMTF and EMTF after overlap handling
            # h_eff_OMTF.Draw("same")
            # h_eff_EMTF.Draw("same")

            leg = ROOT.TLegend(0.6,0.13,0.8,0.33)
            leg.SetFillStyle(0)
            leg.AddEntry(h_eff_BMTF,"|#eta| #leq 0.83","lep")
            leg.AddEntry(h_eff_OMTF,"0.83 < |#eta| #leq 1.24","lep")
            leg.AddEntry(h_eff_EMTF,"1.24 < |#eta| #leq 2.4","lep")
            leg.Draw()

            latex.SetTextSize(0.04)
            latex.DrawLatexNDC(dataset_x1,0.91,dataset_legend)
            latex.DrawLatexNDC(0.62,0.48,quality_label)
            latex.DrawLatexNDC(0.62, 0.41, pt_l1_label)
            latex.DrawLatexNDC(0.62, 0.34, pt_reco_label)
            latex.SetTextSize(0.045)
            latex.DrawLatexNDC(0.1, 0.91, "#font[61]{CMS}")
            latex.SetTextSize(0.0346)
            latex.DrawLatexNDC(0.195, 0.91, "#font[52]{Preliminary}")

        else:    

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
            graph.SetMaximum(1.2)
            if var == "pt":
                c.SetLogx(1)
                graph.GetXaxis().SetLimits(1,2000)
                graph.GetXaxis().SetTitleOffset(1.3)
            if var == "pt2":
                if wp == "SingleMu2_5":
                    graph.GetXaxis().SetLimits(0,30)
                else:
                    graph.GetXaxis().SetLimits(0,60)
                graph.GetXaxis().SetTitleOffset(1.2)

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

            leg = ROOT.TLegend(0.61,0.13,0.8,0.38)
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
                latex.DrawLatexNDC(0.64,0.53,quality_label)
                latex.DrawLatexNDC(0.64, 0.46, pt_l1_label)
                latex.DrawLatexNDC(0.64, 0.39, pt_reco_label)
            else:
                latex.DrawLatexNDC(0.64,0.44,quality_label)
                latex.DrawLatexNDC(0.64, 0.39, pt_l1_label)
            latex.SetTextSize(0.045)
            latex.DrawLatexNDC(0.12, 0.85, "#font[61]{CMS}")
            latex.SetTextSize(0.0346)
            latex.DrawLatexNDC(0.12, 0.81, "#font[52]{Preliminary}")



        c.SaveAs(output_dir + "eff_" + key + ".png")
        c.SaveAs(output_dir + "eff_" + key + ".pdf")


ROOT.gStyle.SetPadTickY(1)
c2 = ROOT.TCanvas("c2","c2",800,800)
c2.SetLeftMargin(0.11)
c2.SetRightMargin(0.15)
c2.SetGrid()

## eta vs phi
key = "SingleMu2_5_phi_eta" 
h_passed_uGMT = in_file.Get("uGMT_" + key + "_passed")
h_total_uGMT =in_file.Get("uGMT_" + key + "_total")
h_eff_uGMT = ROOT.TEfficiency(h_passed_uGMT,h_total_uGMT)
h_eff_uGMT.SetTitle(";#eta_{Reco};#phi_{Reco} [rad];Efficiency")
h_eff_uGMT.Draw("colz")

c2.Update()
h_eff_uGMT.GetPaintedHistogram().GetYaxis().SetRangeUser(-3.14, 3.3)
h_eff_uGMT.GetPaintedHistogram().GetXaxis().SetRangeUser(-2.4, 2.4)
c2.Update()

palette = h_eff_uGMT.GetPaintedHistogram().GetListOfFunctions().FindObject("palette")
palette.SetX1NDC(0.865)  # New left x-coordinate of the palette (move right)
palette.SetX2NDC(0.9)  # New right x-coordinate of the palette
palette.SetY1NDC(0.1)  # New bottom y-coordinate of the palette
palette.SetY2NDC(0.9)  # New top y-coordinate of the palette
c2.Update()

latex.SetTextSize(0.04)
latex.DrawLatexNDC(dataset_x2,0.91,dataset_legend)
latex.SetTextSize(0.045)
latex.DrawLatexNDC(0.11, 0.91, "#font[61]{CMS}")
latex.SetTextSize(0.0346)
latex.DrawLatexNDC(0.205, 0.91, "#font[52]{Preliminary}")
line = ROOT.TLine(-1.24, -3.2, -1.24, 3.6)
line.SetLineWidth(2)
line.SetLineColor(ROOT.kBlack)
line.SetLineStyle(9)
line.Draw("same")
line1 = ROOT.TLine(-0.83, -3.2, -0.83, 3.6)
line1.SetLineWidth(2)
line1.SetLineColor(ROOT.kBlack)
line1.SetLineStyle(9)
line1.Draw("same")
line2 = ROOT.TLine(0.83, -3.2, 0.83, 3.6)
line2.SetLineWidth(2)
line2.SetLineColor(ROOT.kBlack)
line2.SetLineStyle(9)
line2.Draw("same")
line3 = ROOT.TLine(1.24, -3.2, 1.24, 3.6)
line3.SetLineWidth(2)
line3.SetLineColor(ROOT.kBlack)
line3.SetLineStyle(9)
line3.Draw("same")

latex.SetTextSize(0.021)
latex.DrawLatexNDC(0.451,0.87,"BMTF")
latex.DrawLatexNDC(0.293,0.87,"OMTF")
latex.DrawLatexNDC(0.185,0.87,"EMTF")
latex.DrawLatexNDC(0.61,0.87,"OMTF")
latex.DrawLatexNDC(0.725,0.87,"EMTF")
c2.SaveAs(output_dir + "eff_" + key + ".png")
c2.SaveAs(output_dir + "eff_" + key + ".pdf")

key = "SingleMu1_22_phi_eta" 
h_passed_uGMT = in_file.Get("uGMT_" + key + "_passed")
h_total_uGMT =in_file.Get("uGMT_" + key + "_total")
h_eff_uGMT = ROOT.TEfficiency(h_passed_uGMT,h_total_uGMT)
h_eff_uGMT.SetTitle(";#eta_{Reco};#phi_{Reco} [rad];Efficiency")
h_eff_uGMT.Draw("colz")

c2.Update()
h_eff_uGMT.GetPaintedHistogram().GetYaxis().SetRangeUser(-3.14, 3.3)
h_eff_uGMT.GetPaintedHistogram().GetXaxis().SetRangeUser(-2.4, 2.4)
c2.Update()

palette = h_eff_uGMT.GetPaintedHistogram().GetListOfFunctions().FindObject("palette")
palette.SetX1NDC(0.865)  # New left x-coordinate of the palette (move right)
palette.SetX2NDC(0.9)  # New right x-coordinate of the palette
palette.SetY1NDC(0.1)  # New bottom y-coordinate of the palette
palette.SetY2NDC(0.9)  # New top y-coordinate of the palette
c2.Update()

latex.SetTextSize(0.04)
latex.DrawLatexNDC(dataset_x2,0.91,dataset_legend)
latex.SetTextSize(0.045)
latex.DrawLatexNDC(0.11, 0.91, "#font[61]{CMS}")
latex.SetTextSize(0.0346)
latex.DrawLatexNDC(0.205, 0.91, "#font[52]{Preliminary}")
line = ROOT.TLine(-1.24, -3.14, -1.24, 3.6)
line.SetLineWidth(2)
line.SetLineColor(ROOT.kBlack)
line.SetLineStyle(9)
line.Draw("same")
line1 = ROOT.TLine(-0.83, -3.14, -0.83, 3.6)
line1.SetLineWidth(2)
line1.SetLineColor(ROOT.kBlack)
line1.SetLineStyle(9)
line1.Draw("same")
line2 = ROOT.TLine(0.83, -3.14, 0.83, 3.6)
line2.SetLineWidth(2)
line2.SetLineColor(ROOT.kBlack)
line2.SetLineStyle(9)
line2.Draw("same")
line3 = ROOT.TLine(1.24, -3.14, 1.24, 3.6)
line3.SetLineWidth(2)
line3.SetLineColor(ROOT.kBlack)
line3.SetLineStyle(9)
line3.Draw("same")

latex.SetTextSize(0.021)
latex.DrawLatexNDC(0.451,0.87,"BMTF")
latex.DrawLatexNDC(0.293,0.87,"OMTF")
latex.DrawLatexNDC(0.185,0.87,"EMTF")
latex.DrawLatexNDC(0.61,0.87,"OMTF")
latex.DrawLatexNDC(0.725,0.87,"EMTF")
c2.SaveAs(output_dir + "eff_" + key + ".png")
c2.SaveAs(output_dir + "eff_" + key + ".pdf")