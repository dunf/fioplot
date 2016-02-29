#!/usr/bin/python3

# This is a rewrite of Erik Hjelmås' plotsintex script
# Usage: ./plotter -d DIRECTORY

import os
import argparse
from matplotlib import pyplot as plt
import numpy as np
from numpy import *

test_type_desc = {
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

test_type = [       # Array of tuples where the digit is the number of jobs for each test
    ('fsseqR1-16', 1),
    ('fsseqW1-16', 1),
    ('fsrandR1-1', 1),
    ('fsrandR1-16', 1),
	('fsrandR1-32', 1),
	('fsrandR1-64', 1),
	('fsrandR16-1', 16),
	('fsrandR16-16', 16),
	('fsrandR16-32', 16),
	('fsrandR16-64', 16),
	('fsrandW1-1', 1),
	('fsrandW1-16', 1),
	('fsrandW1-32', 1),
	('fsrandW1-64', 1),
	('fsrandW16-1', 1),
	('fsrandW16-16', 16),
	('fsrandW16-32', 16),
	('fsrandW16-64', 16),
    ('fsmixedRW703016-16', 16),
]

# Description of the test config
test_config = [
   # 'test1',
    #'test3',
    'ssdjournal',
]


class Args(object):
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--testdir", help="Directory where raw data is located...")
    parser.add_argument('-d', '--destination', help='Destination directory for results', nargs=1)
    args = parser.parse_args()
    DIR = args.testdir
    DESTINATION = args.destination


class Plotter(object):
    args = Args()

    def do_stuff(self):
        for test in test_type:
            num_jobs = test[1]
            index = 0
            means = []
            std_dev = []
            names = []
            means = zeros(len(test_config))
            std_dev = zeros(len(test_config))
            fio_means = zeros(len(test_config))
            for conf in test_config:
                my_path = os.path.join(self.args.DIR, conf)
                newest_tmp = sorted(os.listdir(my_path),
                    key=lambda last_change: os.path.getctime(os.path.join(my_path, last_change)))
                newest = newest_tmp[-1]
                dir_with_tests = os.path.realpath(self.args.DIR)
                filename = os.path.join(dir_with_tests, conf, newest, test[0] + '-iopslog_iops.log')
                filenameX = os.path.join(dir_with_tests, conf, newest, test[0])
                time = []
                values = []
               # values = zeros(130)
                present = False
                try:
                    with open(filename) as file:
                        j = 0
                        for line in file:
                            line_data = line.split(',') # [0] is time, [1] is IOPS
                            time.append(int(line_data[0]))
                          #  values[j] = int(line_data[1])
                          #  j += 1
                            values.append(int(line_data[1]))
                    present = True
                except FileNotFoundError:
                    print("Error!", filename, "not found...")
                    continue
                tmp = zeros(130)
             #   dtype=tmp.int
               # tmp = []
                last_element = len(time)-1
                i = 0
                for j in range(num_jobs):
                    k = 0
                    o = 0
                    while (time[i] <= time[i+1]) and (i < last_element-1):
                        tmp[k] += values[i]
                        k += 1
                        i += 1
                    tmp[k] += values[i]
                    i += 1
                if i == last_element:
                    tmp[k+1] += values[i]
                means[index] = tmp.mean()
                std_dev[index] = tmp.std()
                try:
                    with open(filenameX) as file:
                        total = 0
                        for line in file:
                            if 'iops' in line:
                                iops = int(line.split('iops=')[1].split(',')[0])
                                total += iops
                    present = True
                except FileNotFoundError:
                    print("Error! File ", filenameX, "not found...")
                    continue
                fio_means[index] = total
                names.append(conf)
                index += 1
            ind = np.arange(len(means))
            width = 0.3
            rects1 = plt.bar(ind, means, width, color='gray', yerr=std_dev,
                             error_kw=dict(ecolor='black'))
            rects2 = plt.bar(ind+width, fio_means, width, color='black')
            plt.ylabel('IOPS')
            plt.title(test_type_desc.get(test[0]))
            plt.xticks(ind+width/2, names, rotation=270)
            fig = plt.gcf()
            fig.subplots_adjust(bottom=0.4)
            plt.savefig('/home/md/Dropbox/Cephios/fioplot/results_plotter/' + test[0] + '.pdf')
            print("File " + test[0] + ".pdf saved...")
            print('-' * 30)
            plt.close()


def main():
    p = Plotter()
    p.do_stuff()

if __name__ == "__main__":
    main()