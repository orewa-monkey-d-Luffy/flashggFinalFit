import os
import json
from commonTools import lumiMap

#tag="Nov23"
#ext="2023_11_14"

tag="Feb24"
ext="2024_02_26"

#YEARS = ['2016preVFP', '2016postVFP', '2017', '2018']
YEARS = ['2016','2017','2018']
CATEGORIES = ['RECO_WH_LEP_Tag0', 'RECO_WH_LEP_Tag1', 'RECO_WH_LEP_Tag2', 'RECO_WH_LEP_Tag3','RECO_WH_LEP_Tag4', 'RECO_WH_LEP_Tag5',  'RECO_ZH_LEP_Tag0', 'RECO_ZH_LEP_Tag1', 'RECO_ZH_LEP_Tag2']
#CATEGORIES = CATEGORIES = ['RECO_WH_LEP_Tag0', 'RECO_WH_LEP_Tag1', 'RECO_WH_LEP_Tag2', 'RECO_WH_LEP_Tag3', 'RECO_ZH_LEP_Tag0', 'RECO_ZH_LEP_Tag1']

filename = '../Trees2WS/ntuples_%s.json'%(tag)
if not os.path.exists(filename):
    print('File %s does not exist!'%filename)
    exit(1)

with open(filename, 'r') as f_:
    ntuples = json.load(f_)

for y in YEARS:

    if not os.path.exists('outdir_{}_{}_{}'.format(tag, y, ext)):
        os.system('mkdir outdir_{}_{}_{}'.format(tag, y, ext))

    wsdir = ntuples['signal'][y]['path_to_workspaces']
    processes_ = ntuples['signal'][y]['samples']
    proc_list = []

    lumi_ = lumiMap[y]

    for cat_ in CATEGORIES:
        cmd = 'bash runBackgroundScripts.sh -i {wsdir}/allData.root -p none -f {cat} --ext {tag}_{year}_{ext} --catOffset 1 --intLumi {lumi} --year {year} --batch local --queue cmsan --sigFile none --isData --fTest'.format(year=y, tag=tag, ext=ext, wsdir=wsdir, cat=cat_, lumi=lumi_)
        #print(cmd)
        os.system(cmd)
        rename_cmd = 'rename CMS-HGG_multipdf_{cat}.root CMS-HGG_multipdf_{cat}_{year}.root outdir_{tag}_{year}_{ext}/*.root'.format(tag=tag, year=y, ext=ext, cat=cat_)
        #print(rename_cmd)
        os.system(rename_cmd)