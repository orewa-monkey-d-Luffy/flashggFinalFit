# Final Fits (lite)
Welcome to the new Final Fits package. Here lies a a series of scripts which are used to run the final stages of the CMS Hgg analysis: signal modelling, background modelling, datacard creation, final statistical interpretation and final result plots.

Slides from the flashgg tutorial series can be found [here](https://indico.cern.ch/event/963619/contributions/4112177/attachments/2151275/3627204/finalfits_tutorial_201126.pdf)

## Download and setup instructions

```
# Install the GBRLikelihood package which contains the RooDoubleCBFast implementation
cd $CMSSW_BASE/src
git clone git@github.com:jonathon-langford/HiggsAnalysis.git
cd $CMSSW_BASE/src

#Install CombinedLimit
cd $CMSSW_BASE/src
git clone git@github.com:emanueledimarco/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
git checkout from-v8.1.0
source env_standalone.sh 
make -j 8; make
cd $CMSSW_BASE/src


#Install Combine Harvester
cd $CMSSW_BASE/src
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
cd CombineHarvester/
git checkout v2.0.0
scram b -j 9
cd $CMSSW_BASE/src

#install finalFits
git clone git@github.com:bmjoshi/flashggFinalFit.git -b vbfac-dev

cd flashggFinalFit/


cmsenv
source setup.sh
```

In every new shell run the following to add `tools/commonTools` and `tools/commonObjects` to your `${PYTHONPATH}`:
```
cmsenv
source setup.sh
```

## Contents
The Finals Fits package contains several subfolders which are used for the following steps:

* Create the Signal Model (see `Signal` dir)
* Create the Background Model (see `Background` dir)
* Generate a Datacard (see `Datacard` dir)
* Running fits with combine (see `Combine` dir)
* Scripts to produce plots (see `Plots` dir)

The signal modelling, background modelling and datacard creation can be ran in parallel. Of course the final fits (`Combine`) requires the output of these three steps. In addition, the scripts in the `Trees2WS` dir are a series of lightweight scripts for converting standard ROOT trees into a RooWorkspace that can be read by the Final Fits package.

Finally, the objects and tools which are common to all subfolders are defined in the `tools` directory. If your input workspaces differ from the flashgg output workspace structure, then you may need to change the options here.

Each of the relevant folders are documented with specific `README.md` files. Some (temporary) instructions can be found in this [google docs](https://docs.google.com/document/d/1NwUrPvOZ2bByaHNqt_Fr6oYcP7icpbw1mPlw_3lHhEE/edit)


## Instructions for VHLEP

First, you need to create a json file, which will contain the list of processes (WHiggs0Mf05ph0ToGG, WHiggs0Mph0ToGG, WHiggs0PMph0ToGG, ZHiggs0Mf05ph0ToGG, ZHiggs0Mph0ToGG and ZHiggs0PMph0ToGG) and the path to nutples and their respective workspaces. To generate a json file, run the following command

```
cd Tree2WS;
python run_ws.py --process make_json --tag Feb24
```

The workspaces will be stored in a EOS folder, i.e. `/eos/user/{u}/{username}/workspaces/{tag}/{era}`, whereas the hadded ntuples will be stored in `/eos/user/{u}/{username}/ntuples/{tag}/{era}`. You would need to fill in paths to the ntuples produced through flashgg in the blank spaces labeled "ntuples". Once the json is ready, hadd the files using the following command

```
python run_ws.py --process hadd --tag Feb24
```

This takes some time to run. The logs will be stored in `run_ws.log`. Check the logs to make sure that all files for all the eras are hadded properly. If the hadding, fails for certain eras, you can run the script in `print_only` mode. Then you can manually run only the hadd processes that have failed.

```
python run_ws.py --process hadd --tag Feb24 --print_only
```

Once the files are hadded successfully, generate the workspaces. To generate a workspace you will need to get a config form `configs` folder. The latest config used for VHAnomalous is `config_UL18_Oct23.py`.

```
cp configs/config_UL18_Oct23.py .
python run_ws.py --process make_all_ws --tag Feb24 --config config_UL18_Oct23.py
```

Then go to the Signal folder and fit the signal. If there are issues in 2016postVFP, you might have to merge it with 2016preVFP. In that case, use

```
python run_signal_sequence.py --ext {ext} --tag {tag} --process fTest
python run_signal_sequence.py --ext {ext} --tag {tag} --process calcPhotonSyst
python run_signal_sequence.py --ext {ext} --tag {tag} --process getEffAcc
python run_signal_sequence.py --ext {ext} --tag {tag} --process getDiagProc
python run_signal_sequence.py --ext {ext} --tag {tag} --process signalFit
```

```
bash run_packager.sh
```

Next, make the background fits and models. Change the tag, categories and extension in `doBackground.py`.

```
cd ../Background
python doBackground.py
```

Next, make datacards using `doDatacards.sh`. Make sure to change the tag and extension labels.

```
cd ../Datacard/
bash doDatacards.sh
```

If you need to combine the datacards, you manually run `combineCards.py` command.

```
combineCards.py {datacard1} {datacard2} > {combined_datacard}
```

Then create a `Models` directory, copy everything to the Combine directory and run `run_combine.sh`. Before running make sure to change `tag`, `ext` and `eosdir` options.

```
mkdir -p Models/datacards/
mkdir Models/signal/
mkdir Models/background/
bash run_combine.sh
```

Check if the scalings for alternate signals are done properly.

```
Bin/Process RECO_WH_LEP_Tag0_2018/wh_ALT_0M_2018_hgg will get scaled by bsmCoupling_WH
Bin/Process RECO_WH_LEP_Tag0_2018/wh_ALT_0Mf05_2018_hgg will get scaled by intCoupling_WH
Bin/Process RECO_WH_LEP_Tag0_2018/wh_ALT_0PM_2018_hgg will get scaled by smCoupling_WH
```
