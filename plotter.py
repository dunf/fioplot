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
    #'jobs_test',
    #'qd_test',
  #  'qd_test_onBlockDev'
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
            fio_means = []
            names = []
            means = zeros(len(test_config))            # No bueno
            #std_dev = zeros(len(test_config))          # No bueno
            #fio_means = zeros(len(test_config))        # No bueno

            for conf in test_config:
                print("Processing test:", conf, "---- File: ", test[0])
                my_path = os.path.join(self.args.DIR, conf)
                newest_tmp = sorted(os.listdir(my_path),
                    key=lambda last_change: os.path.getctime(os.path.join(my_path, last_change)))
                newest = newest_tmp[-1]
                dir_with_tests = os.path.realpath(self.args.DIR)
                filename = os.path.join(dir_with_tests, conf, newest, test[0] + '-iopslog_iops.log')
                filenameX = os.path.join(dir_with_tests, conf, newest, test[0])
                time = []
                values = []
                present = False
                try:
                    with open(filename) as file:
                        j = 0
                        for line in file:
                            line_data = line.split(',') # [0] is time, [1] is IOPS
                            time.append(int(line_data[0]))
                            values.append(int(line_data[1]))
                    present = True
                except FileNotFoundError:
                    print("Error!", filename, "not found...")
                    continue
#
#-------------------- NEW -------------------------------------
                all_jobs = []
                last_element = len(time)-1
                i = 0
                avg_sum = 0
                for job in range(num_jobs):
                    per_job = []
                    while (time[i] <= time[i+1]) and (i < last_element-1):
                        per_job.append(values[i])
                        i += 1
                    avg_sum += np.mean(per_job)

                    #all_jobs.append(np.mean(per_job))
                    i += 1
                print("Sum avg IOPS: ", avg_sum)

# ------------------------------ # ERIKS LØSNING ----------------------------------------
#                i = 0
#                tmp = zeros(130)
#                last_element = len(time)-1
#                for j in range(num_jobs):
#                    k = 0
#                    while (time[i] <= time[i+1]) and (i < last_element-1):
#                        tmp[k] += values[i]
#                        k += 1
#                        i += 1
#                    tmp[k] += values[i]
#                    i += 1
#                if i == last_element:
#                    tmp[k+1] += values[i]

# -----------------------------------------------------------------------
              #  print(tmp)
        #        means.append(np.mean(all_jobs))

               # print("AVG: ", tmp.mean())
#                print("StdDev: ", tmp.std())
#                print("AVG: ", np.mean(tmp))
            #    std_dev[index] = np.std(tmp)
                means[index] = avg_sum         #tmp.mean()
              #  print("StdDev: ", np.std(tmp))
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
                print("FIO IOPS: ", total)
        #        fio_means[index] = total
                fio_means.append(total)
                names.append(conf)
                index += 1
            ind = np.arange(len(means))
            width = 0.3
            rects1 = plt.bar(ind, means, width, color='gray', #yerr=std_dev,
                             error_kw=dict(ecolor='black'))
            rects2 = plt.bar(ind+width, fio_means, width, color='brown')
            plt.ylabel('IOPS')
            plt.title(test_type_desc.get(test[0]))
            plt.xticks(ind+width/2, names, rotation=270)
           # plt.text(ind+0.45, fio_means+50, fio_means, ha='center')
            fig = plt.gcf()
            fig.subplots_adjust(bottom=0.4)
            plt.savefig('/home/md/Dropbox/Cephios/fioplot/results_plotter/' + test[0] + '.pdf')
            if present == True:
                print("File " + test[0] + ".pdf saved...")
            print('-' * 30)
            plt.close()


def main():
    p = Plotter()
    p.do_stuff()

if __name__ == "__main__":
    main()