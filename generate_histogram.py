import os
import time
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")

def plot_histo(data, tmin, tmax, days, show, outdir):

    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80]
    bins2 = [80, 180]

    f2  = plt.figure()
    ax2 = f2.add_subplot(111)
    title = "Offaxis Histogram %d - %d - (%d days)"%(tmin, tmax, days)
    ax2.set_title(title, fontsize='large')

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

    print("Aggregating data..")
    tmin = _from
    tmax = _from + days*86400

    tstart = time.time()

    aggregated_data = None

    for filename in os.listdir(args.directory):

        if filename.endswith(".npy"):

            file_tmin, file_tmax = extract_times(filename)

            if file_tmin >= tmin and file_tmax <= tmax:

                file = os.path.join(args.directory, filename)
                data = np.load(file)

                if aggregated_data is None:
                    aggregated_data = data
                else:
                    aggregated_data = np.concatenate((aggregated_data, data))

        else:
            print(filename,"skipped.")

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

    print("tmin %d tmax %d number_of_files %d delta %d"%(tmin, tmax, number_of_files, delta))

    tmin, tmax, aggregated_data = aggregate_data(args.directory, args.fromtt, args.days)

    plot_histo(aggregated_data, tmin, tmax, args.days, args.show, args.outdir)
