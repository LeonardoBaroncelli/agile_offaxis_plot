import argparse

parser = argparse.ArgumentParser(description='Offaxis time intervals generator')
parser.add_argument('--start_tt', type=int, required=True)
parser.add_argument('--days', type=int, required=True)
parser.add_argument('--outfile', type=str, required=True)

args = parser.parse_args()

start = args.start_tt

dates = [start]
for i in range(args.days):
    lastDate = dates[-1]
    dates.append(lastDate+86400)

with open(args.outfile, "w") as outfile:
    for i,d in enumerate(range(len(dates))):
        if i == len(dates)-1:
            break
        # print(dates[i])
        outfile.write(str(dates[i])+" "+str(dates[i+1])+"\n")

print("Number of intervals:",len(dates))
print("tstart:",dates[0],"tstop",dates[-1])
print("Produced:",args.outfile)
