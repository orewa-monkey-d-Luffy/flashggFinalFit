import os, sys
import click
import json
import logging
from multiprocessing import Pool
from contextlib import closing

#YEARS = ['2016preVFP', '2016postVFP', '2017', '2018']
#YEARS = ['2016preVFP', '2017']
YEARS = ['2016postVFP']
CATEGORIES = ['RECO_WH_LEP_Tag0', 'RECO_ZH_LEP_Tag0', 'RECO_WH_LEP_Tag1', 'RECO_WH_LEP_Tag2', 'RECO_WH_LEP_Tag3', 'RECO_WH_LEP_Tag4', 'RECO_WH_LEP_Tag5', 'RECO_ZH_LEP_Tag1', 'RECO_ZH_LEP_Tag2']
#CATEGORIES = ['RECO_WH_LEP_Tag0', 'RECO_WH_LEP_Tag1', 'RECO_WH_LEP_Tag2', 'RECO_WH_LEP_Tag3', 'RECO_ZH_LEP_Tag0', 'RECO_ZH_LEP_Tag1', 'RECO_ZH_LEP_Tag2']
#CATEGORIES = ['RECO_WH_LEP_Tag4', 'RECO_WH_LEP_Tag5']

logname = 'run_signal_sequence.log'
os.system('rm %s'%logname)
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logging.info("Running Signal Sequence")
logger = logging.getLogger('urbanGUI')

class LocalOptions(object):
    def __init__(self, process):
        
        self.process = process
        
        self.opt = {
            'ext': '',              # Extension
            'cat': '',              # RECO category
            'xvar': 'CMS_hgg_mass', # Observable to fit
            'inputWSDir':'',        # Input flashgg WS directory
            'nBins': 80            # Number of bins for fit
        }

        tmpopt = {}
        if self.process=='fTest':
            tmpopt = {
                'procs':  '',               # Signal processes
                'nProcsToFTest': 5,         # Number of signal processes to fTest (ordered by sum entries), others are set to nRV=1,nWV=1. Set to -1 to run over all
                'mass': 125,                # Mass piont to fit
                'doPlots': False,           # Produce Signal fTest plots
                'threshold': 30,            # Threshold number of events
                'nGaussMax': 5,             # Max number of gaussians to test
                'skipWV': True,            # Skip processing WV case
                'minimizerMethod': 'TNC',   # (Scipy) Minimizer method
                'minimizerTolerance': 1e-8, # (Scipy) Minimizer toleranve
                'xvar': 'CMS_hgg_mass'      # Observable
                }
        elif self.process=='calcPhotonSyst':
            tmpopt = {
                'procs':  '',           # Signal processes
                'scales': 'HighR9EB,HighR9EE,LowR9EB,LowR9EE,Gain1EB,Gain6EB',               # Photon shape systematics: scales
                'scalesCorr': 'MaterialCentralBarrel,MaterialOuterBarrel,MaterialForward,FNUFEE,FNUFEB,ShowerShapeHighR9EE,ShowerShapeHighR9EB,ShowerShapeLowR9EE,ShowerShapeLowR9EB',           # Photon shape systematics: scalesCorr
                'scalesGlobal': 'NonLinearity,Geant',         # Photon shape systematics: scalesGlobal
                'smears': 'HighR9EBPhi,HighR9EBRho,HighR9EEPhi,HighR9EERho,LowR9EBPhi,LowR9EBRho,LowR9EEPhi,LowR9EERho',               # Photon shape systematics: smears
                'thresholdMean': 0.05,       # Reject mean variations if larger than thresholdMean
                'thresholdSigma': 0.5,       # Reject mean variations if larger than thresholdSigma
                'thresholdRate': 0.05,       # Reject mean variations if larger than thresholdRate
            }
        elif self.process=="getEffAcc":
            tmpopt = {
                'procs':  '',           # Signal processes
                'massPoints': '125', # MH
                'skipCOWCorr': False, # Skip centralObjectWeight correction for events in acceptance
                'doSTXSFractions': False # Fractional cross sections in each STXS bin (per stage0 process)
            }
        elif self.process=='getDiagProc':
            tmpopt = {
                'procs':  '',           # Signal processes
                'MH': 125,
                'makeSimpleFTest': False,
                'nRV': 3,
                'nWV': 1,
            }
        elif self.process=='plot':
            tmpopt = {
                'procs': 'all',
                'years': '2016',
                'cats': '',
                'inputWSDir':'',
                'loadCatWeights': '',
                'ext': 'test',
                'xvar': 'CMS_hgg_mass:m_{#gamma#gamma}',
                'mass': '125',
                'MH': '125',
                'nBins': 160,
                'pdf_nBins': 3200,
                'threshold': 0.001,
                'translateCats': None,
                'translateProcs': None,
                'label': 'Simulation',
                'doFWHM': False,
                'outdir': ''
            }
        elif self.process=='package':
            tmpopt = {
                'cats':'auto',
                'inputWSDir':'',
                'exts':'',
                'outputExt':'packaged',
                'massPoints': '120,125,130',
                'mergeYears':False,
                'year':'2016',
                'batch':'condor',
                'queue':'espresso',
                'jobOpts':''
            }
        elif self.process=='signalFit':
            tmpopt = {
                'proc':  '',           # Signal process
                'analysis': 'example',
                'massPoints': '125',
                'outdir': 'tmp',
                'minimizerMethod': 'L-BFGS-B',   # (Scipy) Minimizer method
                'minimizerTolerance': 1e-8,  # (Scipy) Minimizer toleranve
                'scales': 'HighR9EB,HighR9EE,LowR9EB,LowR9EE,Gain1EB,Gain6EB',               # Photon shape systematics: scales
                'scalesCorr': 'MaterialCentralBarrel,MaterialOuterBarrel,MaterialForward,FNUFEE,FNUFEB,ShowerShapeHighR9EE,ShowerShapeHighR9EB,ShowerShapeLowR9EE,ShowerShapeLowR9EB',           # Photon shape systematics: scalesCorr
                'scalesGlobal': 'NonLinearity,Geant',         # Photon shape systematics: scalesGlobal
                'smears': 'HighR9EBPhi,HighR9EBRho,HighR9EEPhi,HighR9EERho,LowR9EBPhi,LowR9EBRho,LowR9EEPhi,LowR9EERho',
                'year': '',
                'doPlots': True,
                'doVoigtian': False,
                'useDCB': False,
                'doEffAccFromJson': True,
                'useDiagonalProcForShape': True,
                'skipVertexScenarioSplit': True,
                'skipZeroes': True,
                'replacementThreshold': 5,
                'beamspotWidthData': 3.4,
                'beamspotWidthMC': 5.14,
                'MHPolyOrder': 1,
                'skipSystematics': False,
                'useDiagonalProcForSyst': True,
                'skipBeamspotReweigh': True
            }
        
        for key in tmpopt.keys():
            self.opt[key] = tmpopt[key]
    
    def print_options(self):
        for key in self.opt:
            print('key: ', key, ', value: ', self.opt[key])
    
    def set_options(self):
        for key in self.opt:
            setattr(self,key,self.opt[key])

def make_configs(tag, ext):
    filename = '../Trees2WS/ntuples_%s.json'%(tag)
    if not os.path.exists(filename):
        print('File %s does not exist!'%filename)
        exit(1)
    
    with open(filename, 'r') as f_:
        ntuples = json.load(f_)
    
    for y in YEARS:
        with open('config_template.py','r') as f_:
            lines = f_.readlines()
        
        for iline, l in enumerate(lines):
            if "<TAG>"  in l: lines[iline] = l.replace("<TAG>",  tag)
            if "<YEAR>" in l: lines[iline] = l.replace("<YEAR>", y)
            if "<EXT>"  in l: lines[iline] = l.replace("<EXT>",  ext)
        
        with open('config_%s_%s.py'%(tag, y), 'w') as f_:
            for l in lines:
                f_.write(l)

def run_step(tag, ext, process, print_only=False):

    # get the workspace directory from ntuple json
    filename = '../Trees2WS/ntuples_%s.json'%(tag)
    if not os.path.exists(filename):
        print('File %s does not exist!'%filename)
        exit(1)
    
    with open(filename, 'r') as f_:
        ntuples = json.load(f_)
    
    opt_args = []
    func = None

    if process=='fTest':
        from scripts.fTest import fTest
        func = fTest
    elif process=='calcPhotonSyst':
        from scripts.calcPhotonSyst import calcPhotonSyst
        func = calcPhotonSyst
    elif process=='getEffAcc':
        from scripts.getEffAcc import getEffAcc
        func = getEffAcc
    elif process=='getDiagProc':
        from scripts.getDiagProc import getDiagProc
        func = getDiagProc
    else: return

    for y in YEARS:
        wsdir = ntuples['signal'][y]['path_to_workspaces']
        processes_ = ntuples['signal'][y]['samples']
        proc_list = []
        for proc in processes_:
            print('Adding process: ', proc)
            proc_list.append(processes_[proc]['production_mode'])
        for cat_ in CATEGORIES:
            opt_args.append(LocalOptions(process))
            opt_args[-1].opt['cat'] = cat_
            opt_args[-1].opt['procs'] = ','.join(proc_list)
            opt_args[-1].opt['ext'] = '_'.join([tag,y,ext])
            opt_args[-1].opt['inputWSDir'] = wsdir
            opt_args[-1].set_options()
    
    if print_only:
        print('-'*30)
        print(' '*10+'print mode')
        print('-'*30)
    for args in opt_args:
        if print_only:
            sys.stdout.write(func.__name__+'.py ')
            for k in args.opt.keys():
                sys.stdout.write('--{} {} '.format(k, args.opt[k]))
        else: func(args)
    # with closing(Pool(8)) as mpl:
    #     mpl.map(func, opt_args)
    #     mpl.terminate()

def run_signalFit(tag, ext, print_only=False):

    from scripts.signalFit import signalFit
    process = 'signalFit'
    
    # get the workspace directory from ntuple json
    filename = '../Trees2WS/ntuples_%s.json'%(tag)
    if not os.path.exists(filename):
        print('File %s does not exist!'%filename)
        exit(1)
    
    with open(filename, 'r') as f_:
        ntuples = json.load(f_)
    
    opt_args = []

    for y in YEARS:
        wsdir = ntuples['signal'][y]['path_to_workspaces']
        processes_ = ntuples['signal'][y]['samples']
        proc_list = []
        for proc in processes_:
            prod_mode_ = processes_[proc]['production_mode']
            
            for cat_ in CATEGORIES:
                    if 'wh' in prod_mode_ and 'ZH' in cat_: continue
                    if 'zh' in prod_mode_ and 'WH' in cat_: continue 
                    opt_args.append(LocalOptions(process))
                    opt_args[-1].opt['cat'] = cat_
                    opt_args[-1].opt['proc'] = prod_mode_
                    opt_args[-1].opt['ext'] = '_'.join([tag,y,ext])
                    opt_args[-1].opt['inputWSDir'] = wsdir
                    opt_args[-1].opt['outdir'] = tag+'_'+ext
                    opt_args[-1].opt['year'] = y
                    opt_args[-1].set_options()
    
    for arg in opt_args: signalFit(arg)
    #for args in opt_args: signalFit(args)
    # with closing(Pool(8)) as mpl:
    #    mpl.map(signalFit, opt_args)
    #    mpl.terminate() 

#hadd -f /eos/user/b/bjoshi/VHAnomalous/workspaces/Nov23/2016postVFP/allSignal.root $(ls -1 /eos/user/b/bjoshi/VHAnomalous/workspaces/Nov23/2016postVFP/output_*pythia8*root)

@click.command()
@click.option('--tag', default='tmp', help='tag')
@click.option('--ext', default='2023_11_10', help='Extension')
@click.option('--process', default='test', help='step in the signal sequence')
@click.option('--print_only', is_flag=True, help='print_only option')
def main(tag, ext, process, print_only):
    make_configs(tag, ext)
    if process=='signalFit': run_signalFit(tag, ext)
    else: run_step(tag, ext, process, print_only)

if __name__=="__main__":
    main()
