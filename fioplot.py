#!/usr/bin/python3

# This script reads JSON files outputted by Flexible IO tester (FIO) and plots the results in a
# bar chart using matplotlib.
# Usage: ./plotter.py -d path_to_results_folder [-t title_of_test]


import os
import sys
import json
import argparse
from matplotlib import pyplot as plt


class Args(object):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Directory where JSON files are located...")
    parser.add_argument('-f', '--filename', help='Output filename... Format=pdf', nargs=1)
    args = parser.parse_args()
    DIR = args.directory
    FILENAME = args.filename


class Plotter(object):
    args = Args()
    filename = str(args.FILENAME).split("'")[1]
    results = []
    test_description = [        # Used for description in legend
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
        ('fsmixedRW703016-16', 'Mixed RW 70/30 bs=8K, 16 jobs, IOdepth 16'),
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
        colors = [      # Colors used on bars
            '#FF0000', '#00FFFF', '#0000FF', '#5CB3FF', '#800080', '#FFFF00', '#00FF00', '#FF00FF',
            '#C0C0C0', '#FFA500', '#A52A2A', '#008000', '#808000', '#E66C2C', '#FCDFFF', '#D462FF',
            '#B5EAAA', '#307D7E', '#7FFFD4'
        ]
        plt.title('IOPS jlkdsajf lksajf ølkajf fdflksajflkdsa jf lkdsajflkdsajflkdsafjf')       # Using title as xlabel
        # plt.xlabel('IOPS')
        fig = plt.figure(1)
        fig.subplots_adjust(left=0.5, bottom=0.35, top=0.92)
        ax = plt.subplot(1,1,1)
        width=1
        index = 0
        self.results.sort()
        keys = []
        values = []
        for key, value in self.results:
            plt.barh(index, value, height=1, color=colors[index], align='center', )
            values.append(value)
            for description in self.test_description:
                if description[0] == key:
                    keys.append(description[1])
            index += 1
        plt.yticks(range(len(self.results)), keys)
        ax.legend(keys, loc=8, bbox_to_anchor=(0.5, -0.40), fontsize='xx-small', ncol=3,
                fancybox=True).draggable()
        plt.show()
        fig.savefig('/home/md/Dropbox/Cephios/fioplot/' + self.filename,
                    orientation='portrait', format='pdf')


def main():
    p = Plotter()
    p.read_files()
    p.plot()

if __name__ == "__main__":
    main()

