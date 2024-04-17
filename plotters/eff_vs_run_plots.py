
import ROOT
import argparse
import re
import math
import json

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLegendBorderSize(0)

latex = ROOT.TLatex()
latex.SetTextSize(0.04)
latex.SetTextFont(42)
ROOT.gStyle.SetLegendTextSize(0.04)

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

dataset_legend = args.legend
output_dir = args.o
input_dir = args.i

in_file = ROOT.TFile(input_dir + "merged_total.root","READ")
c = ROOT.TCanvas("c","c",800,800)
c.SetGrid()
c.SetLeftMargin(0.11)

## find run numbers
run_numbers = set()
histos_list = in_file.GetListOfKeys()
for histo in histos_list:
    histo_name = histo.GetName()
    run_number = re.search('22_(.*)_phi', histo_name).group(1)
    run_numbers.add(int(run_number))
run_numbers = sorted(run_numbers)

h_eff_vs_run_BMTF = ROOT.TGraphAsymmErrors(len(run_numbers))
h_eff_vs_run_BMTF.SetMarkerStyle(20)
h_eff_vs_run_BMTF.SetTitle("")
h_eff_vs_run_BMTF.GetXaxis().SetTitle("Run Number")
h_eff_vs_run_BMTF.GetYaxis().SetTitle("Efficiency")

h_eff_vs_run_OMTF = ROOT.TGraphAsymmErrors(len(run_numbers))
h_eff_vs_run_OMTF.SetMarkerStyle(20)
h_eff_vs_run_OMTF.SetTitle("")
h_eff_vs_run_OMTF.GetXaxis().SetTitle("Run Number")
h_eff_vs_run_OMTF.GetYaxis().SetTitle("Efficiency")

h_eff_vs_run_EMTF = ROOT.TGraphAsymmErrors(len(run_numbers))
h_eff_vs_run_EMTF.SetMarkerStyle(20)
h_eff_vs_run_EMTF.SetTitle("")
h_eff_vs_run_EMTF.GetXaxis().SetTitle("Run Number")
h_eff_vs_run_EMTF.GetYaxis().SetTitle("Efficiency")

h_eff_vs_run_uGMT = ROOT.TGraphAsymmErrors(len(run_numbers))
h_eff_vs_run_uGMT.SetMarkerStyle(20)
h_eff_vs_run_uGMT.SetTitle("")
h_eff_vs_run_uGMT.GetXaxis().SetTitle("Run Number")
h_eff_vs_run_uGMT.GetYaxis().SetTitle("Efficiency")

TFs = ["uGMT","BMTF","OMTF","EMTF"]
WPs = ["SingleMu_22"]
vars = ["phi"]

for index, run_number in enumerate(run_numbers,start=1):
        for wp in WPs:
            for var in vars:
                key =  wp + "_" + str(run_number) + "_" + var

                h_passed_BMTF = in_file.Get("BMTF_" + key + "_passed")
                h_total_BMTF =in_file.Get("BMTF_" + key + "_total")
                if h_total_BMTF.Integral() != 0:
                    eff_BMTF = h_passed_BMTF.Integral() / h_total_BMTF.Integral()
                    eff_err_BMTF = (h_passed_BMTF.Integral() / h_total_BMTF.Integral()) * math.sqrt(h_passed_BMTF.Integral()) / h_total_BMTF.Integral()
                    h_eff_vs_run_BMTF.SetPoint(index, run_number, eff_BMTF)
                    h_eff_vs_run_BMTF.SetPointEYlow(index, eff_err_BMTF)
                    if eff_BMTF + eff_err_BMTF > 1:
                        h_eff_vs_run_BMTF.SetPointEYhigh(index, 1-eff_BMTF)
                    else:
                        h_eff_vs_run_BMTF.SetPointEYhigh(index, eff_err_BMTF)
                else:
                    eff_BMTF = 0
                    h_eff_vs_run_BMTF.SetPoint(index, run_number, eff_BMTF)
 
                h_passed_OMTF = in_file.Get("OMTF_" + key + "_passed")
                h_total_OMTF =in_file.Get("OMTF_" + key + "_total")
                if h_total_OMTF.Integral() != 0:
                    eff_OMTF = h_passed_OMTF.Integral() / h_total_OMTF.Integral()
                    eff_err_OMTF = (h_passed_OMTF.Integral() / h_total_OMTF.Integral()) * math.sqrt(h_passed_OMTF.Integral()) / h_total_OMTF.Integral()
                    h_eff_vs_run_OMTF.SetPoint(index, run_number, eff_OMTF)
                    h_eff_vs_run_OMTF.SetPointEYlow(index, eff_err_OMTF)
                    if eff_OMTF + eff_err_OMTF > 1:
                        h_eff_vs_run_OMTF.SetPointEYhigh(index, 1-eff_OMTF)
                    else:
                        h_eff_vs_run_OMTF.SetPointEYhigh(index, eff_err_OMTF)
                else:
                    eff_OMTF = 0
                    h_eff_vs_run_OMTF.SetPoint(index, run_number, eff_OMTF)

                h_passed_EMTF = in_file.Get("EMTF_" + key + "_passed")
                h_total_EMTF =in_file.Get("EMTF_" + key + "_total")
                if h_total_EMTF.Integral() != 0:
                    eff_EMTF = h_passed_EMTF.Integral() / h_total_EMTF.Integral()
                    eff_err_EMTF = (h_passed_EMTF.Integral() / h_total_EMTF.Integral()) * math.sqrt(h_passed_EMTF.Integral()) / h_total_EMTF.Integral()
                    h_eff_vs_run_EMTF.SetPoint(index, run_number, eff_EMTF)
                    h_eff_vs_run_EMTF.SetPointEYlow(index, eff_err_EMTF)
                    if eff_EMTF + eff_err_EMTF > 1:
                        h_eff_vs_run_EMTF.SetPointEYhigh(index, 1-eff_EMTF)
                    else:
                        h_eff_vs_run_EMTF.SetPointEYhigh(index, eff_err_EMTF)             
                else:
                    eff_EMTF = 0
                    h_eff_vs_run_EMTF.SetPoint(index, run_number, eff_EMTF)

                h_passed_uGMT = in_file.Get("uGMT_" + key + "_passed")
                h_total_uGMT =in_file.Get("uGMT_" + key + "_total")
                if h_total_uGMT.Integral() != 0:
                    eff_uGMT = h_passed_uGMT.Integral() / h_total_uGMT.Integral()
                    eff_err_uGMT = (h_passed_uGMT.Integral() / h_total_uGMT.Integral()) * math.sqrt(h_passed_uGMT.Integral()) / h_total_uGMT.Integral()
                    h_eff_vs_run_uGMT.SetPoint(index, run_number, eff_uGMT)
                    h_eff_vs_run_uGMT.SetPointEYlow(index, eff_err_uGMT)
                    if eff_uGMT + eff_err_uGMT > 1:
                        h_eff_vs_run_uGMT.SetPointEYhigh(index, 1-eff_uGMT)
                    else:
                        h_eff_vs_run_uGMT.SetPointEYhigh(index, eff_err_uGMT)          
                else:
                    eff_uGMT = 0
                    h_eff_vs_run_uGMT.SetPoint(index, run_number, eff_uGMT)


                # print(f"run_number: {run_number}, efF_BMTF: {eff_BMTF}, efF_OMTF: {eff_OMTF}, efF_EMTF: {eff_EMTF}, efF_uGMT: {eff_uGMT}")

h_eff_vs_run_BMTF.GetXaxis().SetLimits(min(run_numbers),max(run_numbers))
h_eff_vs_run_BMTF.GetYaxis().SetRangeUser(0.8,1.05)
h_eff_vs_run_BMTF.Draw("AP")
latex.SetTextSize(0.04)
latex.DrawLatexNDC(0.80,0.91,dataset_legend)
latex.DrawLatexNDC(0.76,0.86,"BMTF")
# latex.DrawLatexNDC(0.14, 0.86, "Reco p_{T} #geq 26 GeV")
latex.DrawLatexNDC(0.14, 0.86, "L1 Qual #geq 12")
latex.SetTextSize(0.045)
latex.DrawLatexNDC(0.1, 0.91, "#font[61]{CMS}")
latex.SetTextSize(0.0346)
latex.DrawLatexNDC(0.195, 0.91, "#font[52]{Internal}")
c.SaveAs(output_dir + "eff_vs_run_BMTF.png")

h_eff_vs_run_OMTF.GetXaxis().SetLimits(min(run_numbers),max(run_numbers))
h_eff_vs_run_OMTF.GetYaxis().SetRangeUser(0.8,1.05)
h_eff_vs_run_OMTF.Draw("AP")
latex.SetTextSize(0.04)
latex.DrawLatexNDC(0.80,0.91,dataset_legend)
latex.DrawLatexNDC(0.76,0.86,"OMTF")
# latex.DrawLatexNDC(0.14, 0.86, "Reco p_{T} #geq 26 GeV")
latex.DrawLatexNDC(0.14, 0.86, "L1 Qual #geq 12")
latex.SetTextSize(0.045)
latex.DrawLatexNDC(0.1, 0.91, "#font[61]{CMS}")
latex.SetTextSize(0.0346)
latex.DrawLatexNDC(0.195, 0.91, "#font[52]{Internal}")
c.SaveAs(output_dir + "eff_vs_run_OMTF.png")

h_eff_vs_run_EMTF.GetXaxis().SetLimits(min(run_numbers),max(run_numbers))
h_eff_vs_run_EMTF.GetYaxis().SetRangeUser(0.8,1.05)
h_eff_vs_run_EMTF.Draw("AP")
latex.DrawLatexNDC(0.80,0.91,dataset_legend)
latex.DrawLatexNDC(0.76,0.86,"EMTF")
# latex.DrawLatexNDC(0.14, 0.86, "Reco p_{T} #geq 26 GeV")
latex.DrawLatexNDC(0.14, 0.86, "L1 Qual #geq 12")
latex.SetTextSize(0.045)
latex.DrawLatexNDC(0.1, 0.91, "#font[61]{CMS}")
latex.SetTextSize(0.0346)
latex.DrawLatexNDC(0.195, 0.91, "#font[52]{Internal}")
c.SaveAs(output_dir + "eff_vs_run_EMTF.png")

h_eff_vs_run_uGMT.GetXaxis().SetLimits(min(run_numbers),max(run_numbers))
h_eff_vs_run_uGMT.GetYaxis().SetRangeUser(0.8,1.05)
h_eff_vs_run_uGMT.Draw("AP")
latex.SetTextSize(0.04)
latex.DrawLatexNDC(0.80,0.91,dataset_legend)
latex.DrawLatexNDC(0.76,0.86,"uGMT")
# latex.DrawLatexNDC(0.14, 0.86, "Reco p_{T} #geq 26 GeV")
latex.DrawLatexNDC(0.14, 0.86, "L1 Qual #geq 12")
latex.SetTextSize(0.045)
latex.DrawLatexNDC(0.1, 0.91, "#font[61]{CMS}")
latex.SetTextSize(0.0346)
latex.DrawLatexNDC(0.195, 0.91, "#font[52]{Internal}")
c.SaveAs(output_dir + "eff_vs_run_uGMT.png")