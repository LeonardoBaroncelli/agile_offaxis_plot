import os
import time
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("agg")

def plot_histo(data, tmin, tmax, days, show, outdir, titlesuffix):

    fig_width_pt = 576.79134
    fontsize     = 14

    inches_per_pt = 1.0/72.27               # Convert pt to inch
    golden_mean = (np.sqrt(5)+1.0)/2.0      # Aesthetic ratio
    fig_width = fig_width_pt*inches_per_pt  # width in inches
    fig_height = fig_width/golden_mean      # height in inches

    fig_size =  [fig_width,fig_height]

    params = {  'backend': 'pdf',
                'axes.labelsize': fontsize,
                'font.size': fontsize,
                'legend.fontsize': fontsize,
                'xtick.labelsize': fontsize,
                'ytick.labelsize': fontsize,
                'axes.linewidth': 0.5,
                'lines.linewidth': 0.5,
                #'text.usetex': True,
                'ps.usedistiller': False,
                'figure.figsize': fig_size,
                'font.family': 'DejaVu Sans',
                'font.serif': ['Bitstream Vera Serif']}

    plt.rcParams.update(params)

    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80]
    bins2 = [80, 180]

    f2  = plt.figure()
    ax2 = f2.add_subplot(111)
    if days == 1:
        title = "Offaxis Histogram %d - %d - (%d day) %s"%(tmin, tmax, days, titlesuffix)
    else:
        title = "Offaxis Histogram %d - %d - (%d days) %s"%(tmin, tmax, days, titlesuffix)

    print("Plot title:",title)
    ax2.set_title(title, fontsize='large')
    ttl = ax2.title
    ttl.set_position([.5, 1.05])

    hist, bins = np.histogram(data, bins=bins, density=False)
    hist2, bins2 = np.histogram(data, bins=bins2, density=False)


    width = 1. * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    width2 = 1. * (bins2[1] - bins2[0])
    center2 = (bins2[:-1] + bins2[1:]) / 2

    total_obs = len(data)
    normalized_data =  hist/total_obs*100.
    normalized_data2 = hist2/total_obs*100.

    # print("counts:",hist)
    # print("normalized counts:",normalized_data)
    ax2.bar(center, normalized_data, align='center', color='w', edgecolor='b', width=width)
    ax2.bar(center2, normalized_data2, align='center', color='w', edgecolor='b', width=width2)



    ax2.set_xlim(0., 100.)
    ax2.set_ylim(0., 100.)
    ax2.set_ylabel('\\% of time spent')
    ax2.set_xlabel('off-axis angle $[^\\circ]$')
    labels  = bins
    xlabels = bins
    plt.xticks(xlabels, labels)


    ax2.hist(data, bins, density=True)


    filename = "offaxis_hist_{}_{}.png".format(tmin, tmax)
    outdir = Path(outdir).joinpath(filename)
    f2.savefig(str(outdir))

    if show:
        plt.show()

def extract_times(filename):
    parts = filename.split(".")[0]
    parts = parts.split("_")
    tmin = int(parts[2])
    tmax = int(parts[3])
    return tmin, tmax

def aggregate_data(input_dir, _from, days):

    tmin = _from
    tmax = _from + days*86400

    print("Aggregating data..tmin=%f tmax=%f"%(tmin, tmax))

    tstart = time.time()

    aggregated_data = None

    filenames = [filename for filename in os.listdir(args.directory) if filename.endswith(".npy") ]

    if len(filenames) == 0:
        print(f"No .npy files found in {args.directory}")
        exit(1)

    for filename in filenames:

        file_tmin, file_tmax = extract_times(filename)

        print(f"file_tmin: {file_tmin} file_tmax: {file_tmax} extracted from {filename}")

        if file_tmin >= tmin and file_tmax <= tmax:

            file = os.path.join(args.directory, filename)
            data = np.load(file)

            if aggregated_data is None:
                aggregated_data = data
            else:
                aggregated_data = np.concatenate((aggregated_data, data))


    tstop = time.time()
    print("Took %f seconds"%(tstop-tstart))

    print("Number of values: %d"%(len(aggregated_data)))

    return tmin ,tmax, aggregated_data


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Offaxis Histogram generator')
    parser.add_argument('--directory', type=str, required=True)
    parser.add_argument('--fromtt', type=int, required=True)
    parser.add_argument('--days', type=int, required=True)
    parser.add_argument('--show', type=str2bool, required=True)
    parser.add_argument('--outdir', type=str, required=True)
    parser.add_argument('--titlesuffix', type=str, default="")
    args = parser.parse_args()

    Path(args.outdir).mkdir(parents=True, exist_ok=True)

    metadata_file = Path(args.directory).joinpath("metadata.txt")
    with open(metadata_file, "r") as mtf:
        metadata = mtf.readline()

    tmin, tmax, number_of_files, delta = metadata.split(" ")
    tmin = int(tmin)
    tmax = int(tmax)
    number_of_files = int(number_of_files)
    delta = int(delta)

    print("[dataset info] number_of_files %d tmin %d tmax %d delta %d"%(number_of_files, tmin, tmax, delta))

    tmin, tmax, aggregated_data = aggregate_data(args.directory, args.fromtt, args.days)

    plot_histo(aggregated_data, tmin, tmax, args.days, args.show, args.outdir, args.titlesuffix)
