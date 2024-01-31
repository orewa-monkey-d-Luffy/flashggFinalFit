tag="Nov23"
year="combined"
ext="2023_11_14"

fggff_ws_int_model_opts="-m 125 -P HiggsAnalysis.CombinedLimit.HiggsSingleAnomalousCoupling:FA3_Interference_JHU_ggHSyst_rw_MengsMuV_HeshyXsec_ggHInt_ggHphase --PO CMS_zz4l_fai1,fa3_ggH,muV,muf altSignal=ALT_0M"
#fggff_combine_int_model_opts="--floatOtherPOIs 0 -t -1 --alignEdges 1 --algo=grid -M MultiDimFit --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo Minuit2,0:1. --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 --saveSpecifiedNuis all --saveInactivePOI 1 -m 125 --setParameterRanges muV=0.0,4.0:muf=0.,10.0:fa3_ggH=0,1.:CMS_zz4l_fai1=-0.003,0.003 --points 41"
fggff_combine_int_model_opts="--floatOtherPOIs 0 -t -1 --alignEdges 1 --algo=grid -M MultiDimFit --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo Minuit2,0:1. --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 --saveSpecifiedNuis all --saveInactivePOI 1 --freezeParameters MH,muf,fa3_ggH -m 125 --setParameterRanges CMS_zz4l_fai1=-0.1,0.1 --points 41"
fggff_combine_int_model_opts_float="--floatOtherPOIs 1 -t -1 --alignEdges 1 --algo=grid -M MultiDimFit --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo Minuit2,0:1. --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 --saveSpecifiedNuis all --saveInactivePOI 1 --freezeParameters MH -m 125 --setParameterRanges muV=0.0,4.0:muf=0.,10.0:fa3_ggH=0,1.:CMS_zz4l_fai1=-0.003,0.003 --points 41"

fggff_ws_twoHiggs_model_opts="-m 125.0 -P  HiggsAnalysis.CombinedLimit.HiggsJPC:twoHypothesisHiggs --PO muFloating"
fggff_combine_twoHiggs_model_opts="--algo=grid -M MultiDimFit --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo Minuit2,0:1. --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 --saveSpecifiedNuis all --saveInactivePOI 1 --freezeParameters MH --setParameterRanges r=0.5,4.0 -m 125.00"



dirext="${tag}_VHLEP_combined_${ext}"
output_ws="vh_lep_workspace_${dirext}.root"
datacard="Models/datacards/Datacard_${tag}_combined_${ext}_ANOM_STXS_VH_LEP_Int.txt"
text2workspace.py $datacard -o $output_ws $fggff_ws_int_model_opts
for poi in CMS_zz4l_fai1 muV; do
      prof_name="_profile1D_syst_CMS_${poi}_VHLeptonic_${dirext}"
      combineTool.py -d $output_ws $fggff_combine_int_model_opts -n $prof_name
      plot1DScan.py --POI $poi "higgsCombine$prof_name.MultiDimFit.mH125.root" -o "${poi}_VHLeptonic_${dirext}" --main-label STXS-ANOM_$poi --y-max 30
      #cp "./${poi}_VHLeptonic_${dirext}.pdf" /eos/user/b/bjoshi/www/VHAnomalous/13_11_2023/
done
