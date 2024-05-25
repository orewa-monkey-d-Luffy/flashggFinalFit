_year = "2016pre"
_tag = "May2024"
_ext = "_16pre"

signalScriptCfg = {
# Setup
'inputWSDir':'/eos/user/b/bjoshi/VHAnomalous/2024_03_11_VH_Sys_v4_XS1_BDTv3_DS_fa3_NormalCuts/UL16pre/raw/sig/hadded/workspace/',
'procs':'wh_ALT_0PHf05',
'cats':'RECO_WH_LEP_Tag0,RECO_WH_LEP_Tag1,RECO_WH_LEP_Tag2,RECO_WH_LEP_Tag3,RECO_ZH_LEP_Tag0,RECO_ZH_LEP_Tag1',
'ext':_ext,
'analysis':'example',
'year':_year, # Use 'combined' if merging all years: not recommended
'massPoints':'125',#120,130
'xvar': 'CMS_hgg_mass',
#Photon shape systematics  
'scales':'HighR9EB,HighR9EE,LowR9EB,LowR9EE,Gain1EB,Gain6EB', # separate nuisance per year
'scalesCorr':'MaterialCentralBarrel,MaterialOuterBarrel,MaterialForward,FNUFEE,FNUFEB,ShowerShapeHighR9EE,ShowerShapeHighR9EB,ShowerShapeLowR9EE,ShowerShapeLowR9EB', # correlated across years
'scalesGlobal':'NonLinearity,Geant4', # affect all processes equally, correlated across years
'smears':'HighR9EBPhi,HighR9EBRho,HighR9EEPhi,HighR9EERho,LowR9EBPhi,LowR9EBRho,LowR9EEPhi,LowR9EERho', # separate nuisance per year
# Job submission options
'batch':'local',
'queue':'espresso',
}

