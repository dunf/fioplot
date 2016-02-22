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
    parser.add_argument("-d", "--directory", help="Directory where JSON files are located...")
 #   parser.add.argument("-t", "--title", help="Title in the chart...", default=None)
    args = parser.parse_args()
    DIR = args.directory
  #  TITLE = args.title


class Plotter(object):
    args = Args()
    #results = {}
    results = []
    test_description = [
        ('fsseqR1-16', 'Seq Read bs=256K, 1 job, IOdepth 16'),
        ('fsseqW1-16', 'Seq Write bs=256K 1 job, IOdepth 16'),
        ('fsrandR1-1', 'Random Read 1 jobs, IOdepth 1'),
        ('fsrandR1-16', 'Random Read 1 jobs, IOdepth 16'),
        ('fsrandR1-32', 'Random Read 1 jobs, IOdepth 32'),
        ('fsrandR1-64', 'Random Read 1 jobs, IOdepth 64'),
        ('fsrandR16-1', 'Random Read 16 jobs, IOdepth 1'),
        ('fsrandR16-16', 'Random Read 16 jobs, IOdepth 16'),
        ('fsrandR16-32', 'Random Read 16 jobs, IOdepth 32'),
        ('fsrandR16-64', 'Random Read 16 jobs, IOdepth 64'),
        ('fsrandW1-1', 'Random Write 1 jobs, IOdepth 1'),
        ('fsrandW1-16', 'Random Write 1 jobs, IOdepth 16'),
        ('fsrandW1-32', 'Random Write 1 jobs, IOdepth 32'),
        ('fsrandW1-64', 'Random Write 1 jobs, IOdepth 64'),
        ('fsrandW16-1', 'Random Write 16 jobs, IOdepth 1'),
        ('fsrandW16-16', 'Random Write 16 jobs, IOdepth 16'),
        ('fsrandW16-32', 'Random Write 16 jobs, IOdepth 32'),
        ('fsrandW16-64', 'Random Write 16 jobs, IOdepth 64'),
        ('fsmixedRW703016-16', 'Mixed RW 70/30 bs=8K, 16 jobs, IOdepth 16')
    ]

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
                        test_type = 'write'                           # means it is a write test
                    else:
                        test_type = 'read'
                except KeyError:
                    try:
                        test_type = j_obj['jobs'][0]['mixed']['io_bytes']
                        test_type = 'mixed'
                    except KeyError:
                        print("Unable to parse file", jobname)
                total_iops = 0
                for job in range(jobs):
                    iops = j_obj['jobs'][job][test_type]['iops']
                    iops_list.append(iops)
                    total_iops += iops
                self.results.append((jobname, total_iops))     # Tuple in array

    def plot(self):
        colors = [
            '#ee0000', '#0000FF', '#FFFF00', '#CCEEFF', '#666666', '#FF00CC', '#6699FF',
            '#663366', '#00CCFF', '#00FFCC', '#003300', '#3399FF', '#CCCCFF', '#003333', '#009999',
            '#660000', '#CC0000', '#CCCC00', '#CCCCCC', '#009933', '#006600', '#003399', '#CCCC99'
        ]
        plt.xlabel('IOPS')
        fig = plt.figure(1)#, figsize=(10, 25))
        fig.subplots_adjust(bottom=0.35, top=0.98, )
        ax = plt.subplot(1,1,1)


        width=1
        index = 0
        self.results.sort()
        tmp = []
        tmp2 = []
        for key, value in self.results:
            plt.barh(index, value, width, color=colors[index], align='center')
            tmp2.append(value)
            for description in self.test_description:
                if description[0] == key:
                    tmp.append(description[1])
            index += 1
        plt.yticks(range(len(self.results)), tmp2 )
        lgd =  ax.legend(tmp, loc=8, bbox_to_anchor=(0.5, -0.40), fontsize='xx-small', ncol=3, fancybox=True).draggable()
        plt.show()

        fig.savefig('./telenor_is_shit.pdf', orientation='portrait', format='pdf')




def main():
    p = Plotter()
    p.read_files()
    p.plot()

if __name__ == "__main__":
    main()

