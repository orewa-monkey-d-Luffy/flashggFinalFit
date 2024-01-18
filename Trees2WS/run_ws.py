import os, sys
import logging
import json
import click

import ROOT

from commonTools import dataToProc

YEARS = ['2016preVFP', '2016postVFP', '2017', '2018']

logname = 'run_ws.log'
os.system('rm %s'%logname)
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logging.info("Running Script")
logger = logging.getLogger('urbanGUI')

def make_json(tag):
   ntuples = {}
   for st in ['signal', 'data']:
       ntuples[st] = {}
       for y in YEARS:
           if st=='signal':
               ntuples[st][y] = {
                'ntuples':'', 'samples': {},
               'path_to_workspaces': '/eos/user/b/bjoshi/VHAnomalous/workspaces/{}/{}'.format(tag,y),
               'path_to_hadd':'/eos/user/b/bjoshi/VHAnomalous/ntuples/{}/{}'.format(tag,y)
               }
               ntuples[st][y]['samples']['WHiggs0Mf05ph0ToGG'] = {'production_mode':'wh_ALT_0Mf05'}
               ntuples[st][y]['samples']['WHiggs0PMToGG']      = {'production_mode':'wh_ALT_0PM'}
               ntuples[st][y]['samples']['WHiggs0MToGG']       = {'production_mode':'wh_ALT_0M'}
               ntuples[st][y]['samples']['ZHiggs0Mf05ph0ToGG'] = {'production_mode':'zh_ALT_0Mf05'}
               ntuples[st][y]['samples']['ZHiggs0PMToGG']      = {'production_mode':'zh_ALT_0PM'}
               ntuples[st][y]['samples']['ZHiggs0MToGG']       = {'production_mode':'zh_ALT_0M'}
           else:
               ntuples[st][y] = {'ntuples':'',
               'path_to_hadd':'/eos/user/b/bjoshi/VHAnomalous/ntuples/{}/{}'.format(tag,y),
               'path_to_worksapce':'/eos/user/b/bjoshi/VHAnomalous/workspaces/{}/{}'.format(tag,y)}
   
   with open('ntuples_{}.json'.format(tag),'w') as f_:
       json.dump(ntuples, f_, indent=4)


def hadd_files(tag, print_only=True):
    with open('ntuples_{}.json'.format(tag),'r') as f_:
        ntuples = json.load(f_)    
    
    # check if path exists
    for y in YEARS:
        outDir = ntuples['signal'][y]['path_to_hadd']
        ntp = ntuples['signal'][y]['ntuples']
        
        if os.path.exists(outDir):
            logging.warning('Directory already exists!')
        else:
            logging.info('Creating a new directory {}'.format(outDir))
            cmd = 'mkdir -p {}'.format(outDir)
            if print_only:
                print(cmd)
            else:
                os.system(cmd)
        
        for sig in ntuples['signal'][y]['samples'].keys():
            sig = sig.encode()
            filename = '{}/output_{}_M125_TuneCP5_13TeV-JHUGenV7011-pythia8.root'.format(outDir, sig)
            filelist = [ '%s/%s' % (ntp,f) for f in os.listdir(ntp) if sig in f ]
            cmd = 'hadd -f %s '%filename
            #check if files exist
            for f in filelist:
                _ = ROOT.TFile(f)
                if not _.IsZombie():
                    cmd += f
                    cmd += ' '
                else: logging.warning('%s is corrupted.' % f)
            if print_only: print(cmd)
            else: os.system(cmd)
        
        outDir = ntuples['data'][y]['path_to_hadd']
        ntp = ntuples['data'][y]['ntuples']
        filelist = [ '%s/%s' % (ntp,f) for f in os.listdir(ntp) if '.root' in f ]
        filename = '{}/output_data_{}.root'.format(outDir, y)
        cmd = 'hadd -f {} '.format(filename)
        
        #check if files exist
        for f in filelist:
            _ = ROOT.TFile(f)
            if not _.IsZombie():
                cmd += f
                cmd += ' '
            else: logging.warning('%s is corrupted.' % f)
        cmd += '\n\n'
        if print_only: print(cmd)
        else: os.system(cmd)

def make_workspaces(ntuple_json, config, year, sample_type, print_only=True):
   
    with open(ntuple_json, 'rb') as f_:
       ntuples = json.load(f_)
   
    inDir = ntuples['signal'][year]['path_to_hadd']
    path_to_workspaces = ntuples[sample_type][year]['path_to_workspaces']

    # if the sample_type is "signal" then iterate over all processed
    if sample_type=="signal":
        
        for proc in ntuples[sample_type][year]['samples'].keys():
            proc = proc.encode('utf-8')
            prod_mode_     = ntuples[sample_type][year]['samples'][proc]['production_mode']
            inputTreeFile_ = '{}/output_{}_M125_TuneCP5_13TeV-JHUGenV7011-pythia8.root'.format(inDir, proc)

            if not os.path.exists(inputTreeFile_):
                logging.error('%s file not found!' % inputTreeFile_)
                continue
            
            cmd = 'python trees2ws.py --inputConfig {} '.format(config)
            cmd += '--inputTreeFile {} '.format(inputTreeFile_)
            cmd += '--productionMode {} '.format(prod_mode_)
            cmd += '--year {} '.format(year)
            cmd += ' --doNOTAG --inputMass 125 --doSystematics;\n'
            cmd += 'mv %s/ws_%s/*.root %s;\n'%(inDir,prod_mode_,path_to_workspaces)
            cmd += 'rm -rf %s/ws_%s;\n\n'%(inDir,prod_mode_)
            
            if print_only: print(cmd)
            else: os.system(cmd)
    
    elif sample_type=="data":
        inputTreeFile_ = '{}/output_data_{}.root'.format(inDir, year)

        if not os.path.exists(inputTreeFile_):
            logging.error('%s file not found!' % inputTreeFile_)
            return
        
        cmd = 'python trees2ws_data.py --inputConfig {} '.format(config)
        cmd += '--inputTreeFile {};\n'.format(inputTreeFile_)
        cmd += 'mv %s/ws/*.root %s/allData.root;\n'%(inDir,path_to_workspaces)
        cmd += 'rm -rf %s/ws;\n\n'%(inDir)
        if print_only: print(cmd)
        else: os.system(cmd)
    
    else:
        logging.error('%s is not a sample type' % sample_type)
    
    return
                

def make_all_workspaces(config, tag, print_only):
    ntuple_json = 'ntuples_{}.json'.format(tag)
    if not os.path.exists(ntuple_json):
        logging.error('{} file does not exists!'.format(ntuple_json))
        exit(1)
    
    for st in ['signal','data']:
        for year in YEARS:
            make_workspaces(ntuple_json, config, year, st, print_only)

@click.command()
@click.option('--process'    , default='make_json'     ,      help='Number of greetings.')
@click.option('--tag'        , default='tmp'           ,      help='Number of greetings.')
@click.option('--config'     , default='config_test.py',      help='Config file for making workspaces')
@click.option('--print_only' , is_flag=True            ,      help='Print commands; do not execute!')
def run(process, tag, config, print_only):
    if print_only:
        print("-------------- Commands --------------------")
    if process=="make_json": make_json(tag, print_only)
    elif process=="hadd": hadd_files(tag, print_only)
    elif process=="make_all_ws": make_all_workspaces(config, tag, print_only)
    if print_only:
        print("--------------------------------------------")
     
if __name__=='__main__':
    run()
