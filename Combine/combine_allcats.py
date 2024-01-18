import os

pois = {
        'CMS_zz4l_fai1': [-1,1],
        'fa3_ggH': [-1,1],
        'muV': [0,1],
        'muf': [0,1],
}

POI = 'CMS_zz4l_fai1' 
for CAT in ['CAT01', 'CAT02', 'CAT12']:
    cmd = "combine workspace_2023_08_10_ANOM_STXS_{cat}_WHLeptonicTag.root -n .{cat}_{POI} -M MultiDimFit --algo=grid --points=30 --freezeParameters MH --alignEdges true --cminDefaultMinimizerStrategy=0 --setParameterRanges fa3_ggH=-1.0,1.0:CMS_zz4l=-1.0,1.0:muV=0,10:muf=0,10 -t -1 -m 125.00 --setParameters fa3_ggH=1.0,muV=1.0,muf=1.0  --floatOtherPOIs=1 -P {POI}".format(POI=POI, cat=CAT)
    os.system(cmd)
    os.system('plot1DScan.py --POI {POI} higgsCombine.{cat}_{POI}.MultiDimFit.mH125.root -o {POI}_WHLeptonicTag --main-label STXS-ANOM_Int'.format(POI=POI, cat=CAT))
    os.system('cp {POI}_WHLeptonicTag.pdf /eos/user/b/bjoshi/www/VHAnomalous/10_08_2023/{POI}_WHLeptonicTag_{cat}.pdf'.format(cat=CAT,POI=POI))
