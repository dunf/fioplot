#!/usr/bin/python3

# This is a rewrite of Erik Hjelmås' plotsintex script
# Usage: ./plotter -d DIRECTORY

import os
import sys
import json
import argparse
from matplotlib import pyplot as plt
import numpy as np
from numpy import *
import re

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

# Array contains testing configurations
test_config = [
    'test1',
    'test2',
]
#442.420463039

class Args(object):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Directory where JSON files are located...")
 #   parser.add_argument('-f', '--filename', help='Output filename... Format=pdf', nargs=1, default=None)
    args = parser.parse_args()
    DIR = args.directory
 #   FILENAME = args.filename


class Plotter(object):
    args = Args()

    def do_stuff(self):
        for test in test_type:
            jobs = test[1]


            for conf in test_config:
                mypath = os.path.join(self.args.DIR, conf)
                print(mypath)
                newest_tmp = sorted(os.listdir(mypath),
                    key=lambda last_change: os.path.getctime(os.path.join(mypath, last_change)))
                print(newest_tmp)
                newest = newest_tmp[-1]
                print(newest)
                filename = os.path.join(self.args.DIR, conf, newest, test, '-iopslog_iops.log')
                print(filename)
                filenameX = os.path.join(self.args.DIR, conf, newest, test, test)
                print(filenameX)
                time = []
                values = []
                with open(filename) as file:
                    for line in file:
                        linedata = line.split(',') # [0] is time, [1] is IOPS




def main():
    p = Plotter()
    p.do_stuff()

if __name__ == "__main__":
    main()