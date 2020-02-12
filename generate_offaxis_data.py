import matplotlib as plt
import numpy as np
from agilepy.api.AGEng import AGEng
from multiprocessing import Process
import argparse
from pathlib import Path
from time import time

def chunkIt(lst, num):
    avg = len(lst) / float(num)
    out = []
    last = 0.0

    while last < len(lst):
        out.append(lst[int(last):int(last + avg)])
        last += avg

    return out


def task(thread_id, inputs, filename, tmin, tmax, ref, src_x, src_y, writeFiles, zmax, step):
    print("Thread %d running.."%(thread_id), end=" ")
    tot= len(inputs)
    for idx,tt in enumerate(inputs):
        print("Thread ",thread_id,"processing ",tmin,tmax,idx+1,"/",tot)
        tmin = tt[0]
        tmax = tt[1]
        plot = agEng._computePointingDistancesFromSource(tmin, tmax, src_x, src_y, ref, zmax=zmax, step=step, writeFiles=writeFiles, logfilesIndex="/ASDC_PROC3/DATA_ASDCSTDk/INDEX/LOG.log.index")




if __name__=="__main__":

    agEng = AGEng("./conf.yaml")

    parser = argparse.ArgumentParser(description='Offaxis data generator')
    parser.add_argument('--inputfile', type=str, required=True)
    parser.add_argument('--outdir', type=str, required=True)
    parser.add_argument('--processes', type=int, required=True)
    args = parser.parse_args()


    agEng.config.setOptions(outdir=args.outdir)
    number_of_processes = args.processes
    filename = args.inputfile

    ref="gal"
    src_x=129.7
    src_y=3.7
    writeFiles=True
    zmax=60
    step=100

    with open(filename) as fn:
        lines = fn.readlines()

    input_tmin_tmax = []
    for idx,line in enumerate(lines):
        st = line.split(" ")
        tmin = int(st[0])
        tmax = int(st[1])
        input_tmin_tmax.append((tmin,tmax))


    process_inputs = chunkIt(input_tmin_tmax, number_of_processes)


    processes = []
    for idx, p_inputs in enumerate(process_inputs):
        print("generating process...(%d). Chunk size for process: %d"%(idx, len(p_inputs)))
        p = Process(target=task, args=(idx, p_inputs, filename, tmin, tmax, ref, src_x, src_y, writeFiles, zmax, step))
        processes.append(p)

    time_s = time()

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    took = time()-time_s
    print("Took %f seconds with %d processes"%(took, args.processes))

    metadafilename = "metadata.txt"
    metadataoutpath = Path(args.outdir).joinpath("eng_data/offaxis_data")
    metadataoutpath.mkdir(parents=True, exist_ok=True)
    metadataoutfilepath = metadataoutpath.joinpath(metadafilename)

    with open(metadataoutfilepath, "w") as mto:
        tmin = input_tmin_tmax[0][0]
        tmax = input_tmin_tmax[-1][1]
        number_of_files = len(input_tmin_tmax)
        delta = input_tmin_tmax[0][1]-input_tmin_tmax[0][0]
        mto.write("%d %d %d %d"%(tmin, tmax, number_of_files, delta))
