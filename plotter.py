#!/usr/bin/python3

# This is a fork of Erik HjelmÃ¥s' plotsintex script.
# Usage: ./plotter -t DIRECTORY
# The directories needs to follow this structure:
# DIRECTORY/SomeConfiguration/RandomGeneratedFolder/fiofiles
# Add additional test configurations to test_config.py

# Author: Mihkal Dunfjeld

import os
import argparse
from matplotlib import pyplot as plt
import numpy as np
import test_config


test_type_desc = {      # Dict used for titles in diagrams
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

# Array of tuples that specify the files and number of jobs for each test.
# Naming convention: fs + rand/seq/mixed + (R)ead/(W)rite + number of jobs + - + IO depth
test_type = [
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
	('fsrandW16-1', 16),
	('fsrandW16-16', 16),
	('fsrandW16-32', 16),
	('fsrandW16-64', 16),
    ('fsmixedRW703016-16', 16),
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
    configs = test_config.Config.configurations
    def create_barchart(self):
        for test in test_type:
            num_jobs = test[1]
            index = 0
            means = []
            std_dev = []
            fio_means = []
            names = []

          #  means = zeros(len(test_config))            # No bueno
          #  std_dev = zeros(len(test_config))          # No bueno
          #  fio_means = zeros(len(test_config))        # No bueno

            for conf in self.configs:
                print("Processing test:", conf, "---- File: ", test[0])
                my_path = os.path.join(self.args.DIR, conf)
                newest_tmp = sorted(os.listdir(my_path),
                    key=lambda last_change: os.path.getctime(os.path.join(my_path, last_change)))
                newest = newest_tmp[-1]
                dir_with_tests = os.path.realpath(self.args.DIR)
                raw_file = os.path.join(dir_with_tests, conf, newest, test[0] + '-iopslog_iops.log')
                fio_output = os.path.join(dir_with_tests, conf, newest, test[0])
                time = []
                values = []
                file_exists = False
                try:
                    with open(raw_file) as file:
                        for line in file:
                            line_data = line.split(',') # [0] is time, [1] is IOPS
                            time.append(int(line_data[0]))
                            values.append(int(line_data[1]))
                    file_exists = True
                    time.append(0)
                except FileNotFoundError:
                    print("Error!", raw_file, "not found...")
                    continue
                std_dev.append(np.std(values))
                i = 0
                raw_iops_sum = 0
                for job in range(num_jobs):
                    job_values = []
                    while (time[i] <= time[i+1]): #and (i < last_element-1):
                        job_values.append(values[i])
                        i += 1
                    job_values.append(values[i])
                    raw_iops_sum += np.mean(job_values)
                    i += 1

# ------------------------------ # ERIKS LÃ˜SNING --------------------------------------------------
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
                # print("AVG: ", tmp.mean())
# -------------------------------------------------------------------------------------------------
                try:
                    with open(fio_output) as file:
                        iops_sum = 0
                        for line in file:
                            if 'iops' in line:
                                iops = int(line.split('iops=')[1].split(',')[0])
                                iops_sum += iops
                    file_exists = True
                except FileNotFoundError:
                    print("Error! File ", fio_output, "not found...")
                    continue
                print(" " * 2, "RAW IOPS: ", raw_iops_sum)
                print(" " * 2, "FIO IOPS: ", iops_sum)
                print(" " * 2, "Standard deviation: ", std_dev[index])
                means.append(raw_iops_sum)
                fio_means.append(iops_sum)
                names.append(conf)
                index += 1
            ind = np.arange(len(means))
            width = 0.3
            plt.bar(ind, means, width, color='gray', yerr=std_dev, error_kw=dict(ecolor='black'))
            plt.bar(ind+width, fio_means, width, color='green')
            plt.ylabel('IOPS')
            plt.title(test_type_desc.get(test[0]))
            plt.xticks(ind+width/2, names, rotation=270)
            fig = plt.gcf()
            fig.subplots_adjust(bottom=0.4)
            plt.savefig('/home/md/Dropbox/Cephios/fioplot/results_plotter/' + test[0] + '.pdf')
            if file_exists is True:
                print("File " + test[0] + ".pdf saved...")
            print('-' * 80)
            plt.close()


def main():
    p = Plotter()
    if p.args.DIR:
        p.create_barchart()


if __name__ == "__main__":
    main()
