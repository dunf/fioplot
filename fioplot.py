#!/usr/bin/python3

# This script reads JSON files outputted by Flexible IO tester (FIO) and plots the results in a
# bar chart using matplotlib.
# Usage: ./plotter.py -d path_to_results_folder



import os
import sys
import json
import argparse
import bs4

from matplotlib import pyplot as plt
import numpy as np



class Args(object):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Directory where JSON files are located...",
        default=None)
    args = parser.parse_args()
    DIR = args.directory


class Plotter(object):
    args = Args()
    #results = {}
    results = []
    test_description = {
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

    def read_files(self):
        for fil in os.listdir(self.args.DIR):
            with open(os.path.realpath(os.path.join(self.args.DIR, fil))) as file:
                j_obj = json.load(file)
                jobname = j_obj['jobs'][0]['jobname']
                iops_list =  []
                jobs = len(j_obj['jobs'])
                try:
                    test_type = j_obj['jobs'][0]['read']['io_bytes']
                    if test_type == 0:                                # Zero bytes read in test
                        test_type = 'write'
                    else:
                        test_type = 'read'
                except KeyError:
                    try:
                        test_type = j_obj['jobs'][0]['mixed']['io_bytes']
                        test_type = 'mixed'
                    except KeyError:
                        continue
                total_iops = 0
                for job in range(jobs):
                    iops = j_obj['jobs'][job][test_type]['iops']
                    iops_list.append(iops)
                    total_iops += iops
                self.results.append((jobname, total_iops))

                #self.results.update({jobname: total_iops})

    def plot(self):
        colors = [
            '#ff0000', '#00FF00', '0000FF', '#FFFF00', '#CCEEFF', '#666666', '#FF00CC', '#6699FF',
            '#663366', '#00CCFF', '#00FFCC', '#003300', '#3399FF', '#CCCCFF', '#003333', '#009999',
            '#660000', '#CC0000', '#CCCC00', '#CCCCCC', '#009933', '#006600', '#003399', '#CCCC99'
        ]
        plt.ylabel('IOPS')
        width=1
        index = 0
        self.results.sort()
        for key, value in self.results, self.results:
            print(key, value)
            plt.bar(index, value, width, color=colors[5], align='center')
            index += 1
        plt.xticks()

        #for key, value, col in sorted(zip(self.results.items(), range(len(self.results)))):
        #    plt.bar(index, value, width, color=colors[col], align='center')
      #  plt.bar(range(len(self.results)), self.results.values(), width, color=colors[10], align='center')
     #   plt.xticks(range(len(self.results)), list(self.results.keys()), rotation=270 )
      #  plt.legend(list(self.results.keys()))
          #  print(key, value)
          #  plt.xticks(, self.results.keys())

        plt.show()


def main():
    p = Plotter()
    p.read_files()
    p.plot()

if __name__ == "__main__":
    main()

#