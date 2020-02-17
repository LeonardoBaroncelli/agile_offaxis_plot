import argparse
from agilepy.api.AGEng import AGEng

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Offaxis Histogram generator')
    parser.add_argument('--fromtt', type=int, required=True)
    parser.add_argument('--timevalue', type=int, required=True)
    parser.add_argument('--timeunit', type=str, choices=["days", "hours", "minutes", "seconds"], required=True)
    parser.add_argument('--titlesuffix', type=str, default="")
    args = parser.parse_args()

    agEng = AGEng("./conf.yaml")

    src_x=129.7
    src_y=3.7
    ref="gal"
    zmax=60
    step=0.1
    logfilesIndex=None
    computeHistogram=True
    writeFiles=True
    saveImage=True
    formatExt="png"
    tmin = args.fromtt

    if args.timeunit == "days":
        tmax = tmin + args.timevalue*86400
    elif args.timeunit == "hours":
        tmax = tmin + args.timevalue*3600
    elif args.timeunit == "minutes":
        tmax = tmin + args.timevalue*60
    else:
        tmax = tmin + args.timevalue

    title="Visibility plot %f - %f"%(tmin, tmax)

    plot = agEng.visibilityPlot(tmin, tmax, src_x, src_y, ref, zmax, step, computeHistogram, writeFiles, logfilesIndex, saveImage, formatExt, title)
