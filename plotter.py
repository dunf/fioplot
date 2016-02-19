#!/usr/bin/python3

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
    results = {}
    test_type = { 'read': 'read', 'write': 'write', 'mixed': 'mixed' }

    def read_files(self):
        for fil in os.listdir(self.args.DIR):
            with open(os.path.realpath(os.path.join(self.args.DIR, fil))) as file:
                j_obj = json.load(file)
                jobname = j_obj['jobs'][0]['jobname']
                iops_list =  []
                jobs = len(j_obj['jobs'])
                read_or_write = j_obj['jobs'][0]['read']['io_bytes']

                if read_or_write == 0:
                    read_or_write = 'write'
                else:
                    read_or_write = 'read'
                total_iops = 0
                for job in range(jobs):
                    iops = j_obj['jobs'][job][read_or_write]['iops']
                    iops_list.append(iops)
                    total_iops += iops
                self.results.update({jobname: total_iops})
       # print(self.results)

    def plot(self):
        #plt.title('tittei')
        plt.xlabel('GROUP')
        plt.ylabel('IOPS')
        index = 0
        for key, value in sorted(self.results.items()):
            plt.bar(index, value, color='y')
            print(key, value)
            index += 1


        plt.show()

def usage():
    if len(sys.argv) == 0:
        print("Usage: ", sys.argv[0], " -d", " path to directory where JSON files are located...")

def main():
    usage()
    p = Plotter()
    p.read_files()
    p.plot()

if __name__ == "__main__":
    main()

