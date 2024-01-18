_year = '2018'

signalScriptCfg = {
# Setup
'inputWSDir':'/eos/user/b/bjoshi/VHAnomalous/workspaces/',
'procs':'WHiggs0MToGG,WHiggs0PMToGG,WHiggs0Mf05ph0ToGG',
'cats':'WHLeptonicTag_0,WHLeptonicTag_1,WHLeptonicTag_2,WHLeptonicTag_3',
'ext':'2023_07_13_ANOM_STXS_scaled',
'analysis':'example',
'year':'2018', # Use 'combined' if merging all years: not recommended
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
