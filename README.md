# agile_offaxis_plot

## 1)
```bash
conda activate agilepy
python generate_intervals.py --start_tt 189388801 --days 365 --outfile dates_tt.txt
python generate_offaxis_data.py --inputfile dates_tt.txt --outdir ./output --processes 25 --srcx 263.854021 --srcy -32.938507
python generate_histogram.py --directory ./output/eng_data/offaxis_data --fromtt 189388801 --days 10 --outdir histograms  --show false
```

## 2)
Adjust conf.yaml for the next script.
```bash
conda activate agilepy
python generate_timeplot.py --fromtt 289094400 --timeunit hours --timevalue 12 --step 1 --srcx 355.447 --srcy -0.2689 --ref gal
```
