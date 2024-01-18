import os
import json
import click
from commonTools import dataToProc

@click.command()
@click.option('--ntuple-json', default='ntuples_Oct23.json'  , help='JSON containing path to hadded files.')
@click.option('--config'     , default='config_UL18_Oct23.py', help='Config file for workspaces.')
@click.option('--year'       , default='2018'                , help="Year")
@click.option('--sample-type', default='signal'              , help="Choose sample from (signal/data)")
def make_workspaces(ntuple_json, config, year, sample_type):
   
   with open(ntuple_json, 'rb') as f_:
       ntuples = json.load(f_)
   
   path_to_workspace = ntuples[sample_type][year]['path_to_workspace']
   
   for proc in ntuples[sample_type][year]['samples'].keys():
      proc = proc.encode('utf-8')
      inputTreeFile_ = ntuples[sample_type][year]['samples'][proc]['path']
      if not os.path.exists(inputTreeFile_):
          print('File for process {} does not exist!!!'.format(proc))
          continue
      prod_mode_     = dataToProc(ntuples[sample_type][year]['samples'][proc]['production_mode'])
      
      cmd = 'python trees2ws.py --inputConfig {} '.format(config)
      cmd += '--inputTreeFile {} '.format(inputTreeFile_)
      cmd += '--productionMode {} '.format(prod_mode_)
      cmd += '--year {} '.format(year)
      cmd += ' --doNOTAG --inputMass 125 --doSystematics'
      
      print(cmd)
      os.system(cmd)
      cmd = 'mv %s/ws_%s %s'%('/'.join(inputTreeFile_.split('/')[:-1]),prod_mode_,path_to_workspace)
      print(cmd)
      os.system(cmd)

if __name__=='__main__':
    make_workspaces()
