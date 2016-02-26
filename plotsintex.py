#!/usr/bin/python3


# takes a dir as command line argument: G5 or G6

import numpy as np
from numpy import * 
import sys
import matplotlib.pyplot as plt
import csv
import os
import re

# assossiative array just to use for titles in the plots
testtype = {
    'fsseqR1-16': 'Seq Read bs=256K, 1 job, IOdepth 16',
    'fsseqW1-16': 'Seq Write bs=256K 1 job, IOdepth 16',
	'fsrandR1-1': 'Random Read 1 jobs, IOdepth 1',
	'fsrandR1-16': 'Random Read 1 jobs, IOdepth 16',
	'fsrandR1-32': 'Random Read 1 jobs, IOdepth 32',
	'fsrandR1-64': 'Random Read 1 jobs, IOdepth 64',
	'fsrandR16-1': 'Random Read 16 jobs, IOdepth 1',
	'fsrandR16-16': 'Random Read 16 jobs, IOdepth 16',
	'fsrandR16-32': 'Random Read 16 jobs, IOdepth 32',
	'fsrandR16-64': 'Random Read 16 jobs, IOdepth 64',
	'fsrandW1-1': 'Random Write 1 jobs, IOdepth 1',
	'fsrandW1-16': 'Random Write 1 jobs, IOdepth 16',
	'fsrandW1-32': 'Random Write 1 jobs, IOdepth 32',
	'fsrandW1-64': 'Random Write 1 jobs, IOdepth 64',
	'fsrandW16-1': 'Random Write 16 jobs, IOdepth 1',
	'fsrandW16-16': 'Random Write 16 jobs, IOdepth 16',
	'fsrandW16-32': 'Random Write 16 jobs, IOdepth 32',
	'fsrandW16-64': 'Random Write 16 jobs, IOdepth 64',
    'fsmixedRW703016-16': 'Mixed RW 70/30 bs=8K, 16 jobs, IOdepth 16',
}
# these are the tests to actually include in the plots, possibly a subset of the above
numtesttype = [
    'fsseqR1-16',
    'fsseqW1-16',
	'fsrandR1-1',
	'fsrandR1-16',
	'fsrandR1-32',
	'fsrandR1-64',
	'fsrandR16-1',
	'fsrandR16-16',
	'fsrandR16-32',
	'fsrandR16-64',
	'fsrandW1-1',
	'fsrandW1-16',
	'fsrandW1-32',
	'fsrandW1-64',
	'fsrandW16-1',
	'fsrandW16-16',
	'fsrandW16-32',
	'fsrandW16-64',
    'fsmixedRW703016-16',
]
# these are the architectures to include
numtestarch = [
    'S3500',
#    'S3500-dwc',
##    'S3500-ext4-nojournal',
##    'S3500-ext4',
#    'S3500-xfs',
#    'S3700',
##    'S3700-dwc',
 #   'S3700-ext4-nojournal',
    'S3700-ext4',
    'S3700-xfs',
    'WDRed',
    'WDRed-dwc',
    'WDRed-ext4-nojournal',
    'WDRed-ext4',
    'WDRed-xfs',
    'RAID5',
    'RAID5-dwc',
    'RAID5-ctrlcache',
#    'bcache-RAID10-xfs-noatime',
    'bcache-RAID10',
    'bcache-RAID10-dwc',
    'bcache-RAID10-ctrlcache',
    'bcache-RAID10-dwc-ctrlcache',
    'RAID10',
    'RAID10-dwc',
    'RAID10-ctrlcache',
#    'bcache-RAID10-ext4-nojournal',
#    'bcache-RAID10-ext4',
#    'bcache-RAID10-xfs',
#    'bcache-RAID10-xfs-nobarrier',
#    'bcache-RAID10-xfs-nobarrier-noatime',
#    'bcache-RAID5-ext4-nojournal',
#    'bcache-RAID5-ext4',
#    'bcache-RAID5-xfs',
#    'bcache-RAID5-xfs-nobarrier',
#    'bcache-RAID5-xfs-noatime',
#    'bcache-RAID5-xfs-nobarrier-noatime',
    'bcache-RAID5',
    'bcache-RAID5-dwc',
##    'bcache-RAID5-ctrlcache',
    'bcache-RAID5-dwc-ctrlcache',
    'native-fusemount',
    'vm-fusemount-ext4',
    'vm-gfapi-dev',
    'vm-gfapi-ext4',
]

#f = open('/home/erikh/Desktop/PERF-CAP/results/tex/out.tex','w')
#f.write('\\input{/home/erikh/office/maler/preamble.tex}\n')
#f.write('\\begin{document}\n')
for tk in numtesttype:  # SKIP ALL SEQ/MIXED FOR NOW SINCE BW NOT IOPS THERE
    re_dig = re.compile('\d+')
    if re.search(r"rand", tk):
        jobs = int(re_dig.search(tk).group(0))
    elif tk == 'fsmixedRW703016-16':
        #jobs = 16
        continue
    else:
        #jobs = 1
        continue
    print(jobs)
    means = zeros (len(numtestarch))
    stds = zeros (len(numtestarch))
    fiomeans = zeros (len(numtestarch))
    idx = 0
#    dirty = []
    names = []
    print(sys.argv)
    for ak in numtestarch:
        print(ak)
        #mypath = sys.argv[1]
        mypath = os.path.join(sys.argv[1], ak)
        newest_tmp = sorted(os.listdir(mypath),
            key=lambda p: os.path.getctime(os.path.join(mypath, p)))
        newest = newest_tmp[-1] # choose most recently changed dataset
# store amount of dirty_data in list dirty:
#        if 'randW' in tk:
#            filename = sys.argv[1] + ak + '/' + newest + '/' + tk + '-dirty_data'
# hmmm, should use try except
#            with open(filename, "r") as file_to_read:
#                for line in file_to_read: 
#                    dirty.append(float(line))
        # read iops numbers and compute mean and std dev:
        filename = sys.argv[1] + ak + '/' + newest + '/' + tk + '-iopslog_iops.log'
        filenameX = sys.argv[1] + ak + '/' + newest + '/' + tk # fio's own number also 
        time = np.loadtxt(filename,delimiter=', ',usecols=(0,))
        value = np.loadtxt(filename,delimiter=', ',usecols=(1,))
        tmp = zeros(120)
        lastelement = len(time)-1
        print(filename)
        print(lastelement)
        i = 0
        for j in range(jobs):
            k = 0
            while (time[i] <= time[i+1]) and (i < lastelement-1):
                tmp[k] += value[i]
                k += 1
                i += 1
            tmp[k] += value[i]
            i += 1
        if i == lastelement:
            tmp[k+1] += value[i]
        print(i)
        print(tmp.mean(), tmp.std())
        means[idx] = tmp.mean()
        stds[idx] = tmp.std()
        names.append(ak)
        # get fios own iops value
        temp = []
        with open(filenameX, "r") as file_to_read: # get the IOPS-values from all lines
            for line in file_to_read:              # containing the word 'iops'
                if 'iops' in line:                 # put these values in temp
                    m = re.search('iops=(\d+)', line)
                    temp.append(m.group(1))
        fiomeans[idx] = sum([float(a) for a in temp]) # sum these iops values
        idx += 1                                   # increase index for means, std, fiomeans
    # IOPS plot:
    ind = np.arange(len(means))
    width = 0.3 
    rects1 = plt.bar(ind,means,width,color='gray',yerr=stds,error_kw=dict(ecolor='black'))
    rects2 = plt.bar(ind+width,fiomeans,width,color='black')
    plt.ylabel('IOPS')
    plt.title(testtype[tk])
    plt.xticks(ind+width/2, names, rotation=270)
    fig = plt.gcf()
    fig.subplots_adjust(bottom=0.4)
    plt.savefig('/home/md/Dropbox/Cephios/fioplot/results/' + tk + '.pdf')
    plt.close()
#    f.write('\\includegraphics[width=0.9\\textwidth]{/home/erikh/Desktop/PERF-CAP/results/figs/' + tk + '.pdf} \\\\ \n')
    # dirty_data plot if available:
#    if len(dirty) > 1:
#        ind = np.arange(len(dirty))
#        width = 0.3 
#        rects1 = plt.bar(ind+width,dirty,width,color='black')
#        plt.ylabel('GiB')
#        plt.title(testtype[tk])
#        plt.xticks(ind+width/2, names, rotation=270)
#        fig = plt.gcf()
#        fig.subplots_adjust(bottom=0.4)
#        plt.savefig('/home/erikh/Desktop/PERF-CAP/results/figs/' + tk + '.pdf')
#        plt.close()
#        f.write('\\includegraphics[width=0.9\\textwidth]{/home/erikh/Desktop/PERF-CAP/results/figs/' + tk + '.pdf} \\\\ \n')
    #
#f.write('\\end{document}\n')
#f.close()
