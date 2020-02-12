#!/bin/bash

show=yes
outdir=histograms

# 01/01/2010
python generate_histogram.py --directory ./output/eng_data/offaxis_data --fromtt 189388801 --days 31 --show $show --outdir $outdir

# 2010-02-01 00:00:00
python generate_histogram.py --directory ./output/eng_data/offaxis_data --fromtt 192067200 --days 28 --show $show --outdir $outdir

# 2010-03-01 00:00:00
python generate_histogram.py --directory ./output/eng_data/offaxis_data --fromtt 194486400 --days 31 --show $show --outdir $outdir

# 2010-04-01 00:00:00
python generate_histogram.py --directory ./output/eng_data/offaxis_data --fromtt 197164800 --days 30 --show $show --outdir $outdir

# 2010-05-01 00:00:00
python generate_histogram.py --directory ./output/eng_data/offaxis_data --fromtt 199756800 --days 31 --show $show --outdir $outdir

# 2010-06-01 00:00:00
python generate_histogram.py --directory ./output/eng_data/offaxis_data --fromtt 202435200 --days 30 --show $show --outdir $outdir

# 2010-07-01 00:00:00
python generate_histogram.py --directory ./output/eng_data/offaxis_data --fromtt 205027200 --days 31 --show $show --outdir $outdir

# 2010-08-01 00:00:00
python generate_histogram.py --directory ./output/eng_data/offaxis_data --fromtt 207705600 --days 31 --show $show --outdir $outdir

# 2010-09-01 00:00:00
python generate_histogram.py --directory ./output/eng_data/offaxis_data --fromtt 210384000 --days 30 --show $show --outdir $outdir

# 2010-10-01 00:00:00
python generate_histogram.py --directory ./output/eng_data/offaxis_data --fromtt 212976000 --days 31 --show $show --outdir $outdir

# 2010-11-01 00:00:00
python generate_histogram.py --directory ./output/eng_data/offaxis_data --fromtt 215654400 --days 30 --show $show --outdir $outdir

# 2010-12-01 00:00:00
python generate_histogram.py --directory ./output/eng_data/offaxis_data --fromtt 218246400 --days 31 --show $show --outdir $outdir
