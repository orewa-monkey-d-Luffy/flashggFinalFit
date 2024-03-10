#tag="Nov23"
#ext="2023_11_14"
year="combined"
tag="Mar24"
ext="2024_03_06"
cats="RECO_WH_LEP_Tag0,RECO_WH_LEP_Tag1,RECO_WH_LEP_Tag2,RECO_WH_LEP_Tag3,RECO_ZH_LEP_Tag0,RECO_ZH_LEP_Tag1"
dirext="${tag}_${year}_${ext}"

python scripts/RunPackager.py --cats $cats --exts "${tag}_2018_${ext},${tag}_2017_${ext},${tag}_2016preVFP_${ext},${tag}_2016postVFP_${ext}" --mergeYears --batch local --massPoints 125
if [[ -d outdir_$dirext/packaged ]]; then
    echo "directory outdir_$ext/packaged already exists!";
else mkdir outdir_$dirext/packaged;
fi
mv outdir_packaged/*.root outdir_$dirext/packaged;

# for year in 2016preVFP 2016postVFP 2017 2018; do
#     dirext="${tag}_${year}_${ext}"
#     for proc in wh_ALT_0M wh_ALT_0PM wh_ALT_0Mf05; do
#         for num in 0 1 2 3; do
#             python scripts/RunPlotter.py --procs $proc --year $year --ext $dirext --cats RECO_WH_LEP_Tag$num
#             echo "done"
#         done
#     done
#     for proc in zh_ALT_0M zh_ALT_0PM zh_ALT_0Mf05; do
#         for num in 0 1; do
#             python scripts/RunPlotter.py --procs $proc --year $year --ext $dirext --cats RECO_ZH_LEP_Tag$num
#             echo "done"
#         done
#     done
# done

# for year in 2016preVFP 2016postVFP 2017 2018; do
#     rm outdir_packaged/*.root;
#     dirext="${tag}_${year}_${ext}"
#     echo $dirext
#     python scripts/RunPackager.py --cats $cats --exts $dirext --batch local --massPoints 125 --year $year
#     if [[ -d outdir_$dirext/packaged ]]; then
#         echo "directory outdir_$ext/packaged already exists!";
#     else mkdir outdir_$dirext/packaged;
#     fi
#     mv outdir_packaged/*.root outdir_$dirext/packaged;
# done

# dirext="${tag}_combined_{ext}"
# rm  outdir_$ext/signalFit/output/*.root
# for proc in wh_ALT_0M wh_ALT_0PM wh_ALT_0Mf05; do
#     for cat in 0 1 2 3 4 5; do
#         python RunPlotter.py --procs $proc --years 2016preVFP,2016postVFP,2017,2018  --ext $ext --cats RECO_WH_LEP_Tag$cat;
#     done
#     for cat in 0 1; do
#         python RunPlotter.py --procs $proc --years 2016preVFP,2016postVFP,2017,2018  --ext $ext --cats RECO_ZH_LEP_Tag$cat;
#     done
# done

# rm  outdir_$ext/signalFit/output/*.root
# for cat in 0 1; do
#     cp outdir_$ext/CMS-HGG_sigfit_packaged_RECO_ZH_LEP_Tag$cat.root outdir_$ext/signalFit/output/CMS-HGG_sigfit_$ext\_RECO_ZH_LEP_Tag$cat.root
# done
# for proc in zh_ALT_0M zh_ALT_0PM zh_ALT_0Mf05; do
#     for cat in 0 1; do
#         python RunPlotter.py --procs $proc --years 2017,2018  --ext $ext --cats RECO_ZH_LEP_Tag$cat;
#     done
# done
