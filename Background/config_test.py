# Config file: options for signal fitting

backgroundScriptCfg = {
  
    # Setup
    'inputWSDir':'/eos/user/b/bjoshi/VHAnomalous/2024_03_11_VH_Sys_v4_XS1_BDTv3_DS_fa3_NormalCuts/UL16post/raw/data/hadded_Data/ws/', # location of 'allData.root' file
    'cats':'auto', # auto: automatically inferred from input ws
    'catOffset':0, # add offset to category numbers (useful for categories from different allData.root files)  
    'ext':'16post', # extension to add to output directory
    'year':'combined', # Use combined when merging all years in category (for plots)
    'xvar': 'CMS_hgg_mass', # not yet used, should be passed to the C++ macros
    'plotdir': 'plots',

    # Job submission options
    'batch':'condor', # [condor,SGE,IC,Rome,local]
    'queue':'espresso' # for condor e.g. espresso
  
}
