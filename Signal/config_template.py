_year = "<YEAR>"
_tag = "<TAG>"
_ext = "<EXT>"

signalScriptCfg = {
# Setup
'inputWSDir':'/eos/user/b/bjoshi/VHAnomalous/workspaces/%s/%s'%(_tag,_year),
'procs':'wh_ALT_0Mf05,wh_ALT_0M,wh_ALT_0PM,zh_ALT_0Mf05,zh_ALT_0M,zh_ALT_0PM',
'cats':'auto',
'ext': _tag'_'+_ext,
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
