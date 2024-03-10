tag="Mar24"
ext="2024_03_06"
batch='local'
input_dir="/eos/user/b/bjoshi/VHAnomalous/workspaces/${tag}"

echo $tag
echo $ext
echo $input_dir

# # year-wise WH (Int)
# for year in 2016preVFP 2016postVFP 2017 2018; do
#     procs="wh_ALT_0M,wh_ALT_0PM,wh_ALT_0Mf05"
#     dirext="${tag}_${year}_${ext}_WH_Int"
#     datacard_name="Datacard_${tag}_${year}_${ext}_ANOM_STXS_WH_Int"
#     python RunYields.py --inputWSDirMap $year=$input_dir/$year --cats RECO_WH_LEP_Tag0,RECO_WH_LEP_Tag1,RECO_WH_LEP_Tag2,RECO_WH_LEP_Tag3 --procs $procs --doSystematics  --skipZeroes --batch $batch --ext $dirext
#     python makeDatacard.py --doSystematics --ext $dirext
#     python cleanDatacard.py --datacard Datacard.txt --factor 2 --removeDoubleSided -o $datacard_name.txt
#     done

# # year-wise ZH (Int)
# for year in 2016preVFP 2016postVFP 2017 2018; do
#     procs="zh_ALT_0M,zh_ALT_0PM,zh_ALT_0Mf05"
#     dirext="${tag}_${year}_${ext}_ZH_Int"
#     datacard_name="Datacard_${tag}_${year}_${ext}_ANOM_STXS_ZH_Int"
#     python RunYields.py --inputWSDirMap $year=$input_dir/$year --cats RECO_ZH_LEP_Tag0,RECO_ZH_LEP_Tag1 --procs $procs --doSystematics  --skipZeroes --batch $batch --ext $dirext
#     python makeDatacard.py --doSystematics --ext $dirext
#     python cleanDatacard.py --datacard Datacard.txt --factor 2 --removeDoubleSided -o $datacard_name.txt
#     done

# #combined WH (Int)
# procs="wh_ALT_0M,wh_ALT_0PM,wh_ALT_0Mf05"
# dirext="${tag}_combined_${ext}_WH_Int"
# datacard_name="Datacard_${tag}_combined_${ext}_ANOM_STXS_WH_Int"
# python RunYields.py --inputWSDirMap 2016preVFP=$input_dir/2016preVFP,2016postVFP=$input_dir/2016postVFP,2017=$input_dir/2017,2018=$input_dir/2018 --cats RECO_WH_LEP_Tag0,RECO_WH_LEP_Tag1,RECO_WH_LEP_Tag2,RECO_WH_LEP_Tag3 --procs $procs --doSystematics  --skipZeroes --batch $batch --mergeYears --ext $dirext
# python makeDatacard.py --doSystematics --ext $dirext
# python cleanDatacard.py --datacard Datacard.txt --factor 2 --removeDoubleSided -o $datacard_name.txt

#combined ZH (Int)
procs="zh_ALT_0M,zh_ALT_0PM,zh_ALT_0Mf05"
dirext="${tag}_combined_${ext}_ZH_Int"
datacard_name="Datacard_${tag}_combined_${ext}_ANOM_STXS_ZH_Int"
python RunYields.py --inputWSDirMap 2016preVFP=$input_dir/2016preVFP,2016postVFP=$input_dir/2016postVFP,2017=$input_dir/2017,2018=$input_dir/2018 --cats RECO_ZH_LEP_Tag0,RECO_ZH_LEP_Tag1 --procs $procs --doSystematics  --skipZeroes --batch $batch --mergeYears --ext $dirext
python makeDatacard.py --doSystematics --ext $dirext
python cleanDatacard.py --datacard Datacard.txt --factor 2 --removeDoubleSided -o $datacard_name.txt

# # year-wise ZH (Two Higgs)
# for year in 2016preVFP 2016postVFP 2017 2018; do
#     procs="zh_ALT_0M,zh_ALT_0PM"
#     dirext="${tag}_${year}_${ext}_ZH_twoHiggs"
#     datacard_name="Datacard_${tag}_${year}_{ext}_ANOM_STXS_ZH_twoHiggs"
#     python RunYields.py --inputWSDirMap $year=$input_dir/$year --cats RECO_ZH_LEP_Tag0,RECO_ZH_LEP_Tag1 --procs $procs --doSystematics  --skipZeroes --batch $batch --ext $dirext
#     python makeDatacard.py --doSystematics --ext $dirext
#     python cleanDatacard.py --datacard Datacard.txt --factor 2 --removeDoubleSided -o $datacard_name.txt
#     done

# # year-wise WH (Two Higgs)
# for year in 2016; do
#     procs="wh_ALT_0M,wh_ALT_0PM"
#     dirext="${tag}_${year}_${ext}_WH_twoHiggs"
#     datacard_name="Datacard_${tag}_${year}_${ext}_ANOM_STXS_WH_twoHiggs"
#     python RunYields.py --inputWSDirMap $year=$input_dir/$year --cats RECO_WH_LEP_Tag0,RECO_WH_LEP_Tag1,RECO_WH_LEP_Tag2,RECO_WH_LEP_Tag3 --procs $procs --doSystematics  --skipZeroes --batch $batch --ext $dirext
#     python makeDatacard.py --doSystematics --ext $dirext
#     python cleanDatacard.py --datacard Datacard.txt --factor 2 --removeDoubleSided -o $datacard_name.txt
#     done

# # combined ZH (twoHiggs)
# procs="zh_ALT_0M,zh_ALT_0PM"
# dirext="${tag}_combined_${ext}_ZH_Int"
# datacard_name="Datacard_${tag}_combined_${ext}_ANOM_STXS_ZH_twoHiggs"
# python RunYields.py --inputWSDirMap 2017=$input_dir/2017,2018=$input_dir/2018 --cats RECO_ZH_LEP_Tag0,RECO_ZH_LEP_Tag1 --procs $procs --doSystematics  --skipZeroes --batch $batch --mergeYears --ext $dirext
# python makeDatacard.py --doSystematics --ext $dirext
# python cleanDatacard.py --datacard Datacard.txt --factor 2 --removeDoubleSided -o $datacard_name.txt

# # combined WH (twoHiggs)
# procs="wh_ALT_0M,wh_ALT_0PM"
# dirext="Nov23_combined_2023_11_14_WH_Int"
# datacard_name="Datacard_${tag}_combined_${ext}_ANOM_STXS_WH_twoHiggs"
# python RunYields.py --inputWSDirMap 2016preVFP=$input_dir/2016preVFP,2016postVFP=$input_dir/2016postVFP,2017=$input_dir/2017,2018=$input_dir/2018 --cats RECO_WH_LEP_Tag0,RECO_WH_LEP_Tag1,RECO_WH_LEP_Tag2,RECO_WH_LEP_Tag3 --procs $procs --doSystematics  --skipZeroes --batch $batch --mergeYears --ext $dirext
# python makeDatacard.py --doSystematics --ext $dirext
# python cleanDatacard.py --datacard Datacard.txt --factor 2 --removeDoubleSided -o $datacard_name.txt