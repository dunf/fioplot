#!/usr/bin/python3

# This is a fork of Erik HjelmÃ¥s' plotsintex script.
# Usage: ./plotter -t DIRECTORY
# The directories needs to follow this structure:
# DIRECTORY/ConfigName/SomeFolder/fiofiles
# Add additional test configurations to plotter_config.py

# Author: Mihkal Dunfjeld
# Repository: https://bitbucket.org/dunf/fioplot/src/

import os
import argparse
from matplotlib import pyplot as plt
import numpy
import plotter_config
import matplotlib.patches as mpatches
import pwd


class Args(object):
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", help="Source files", nargs=1, required=True)
    parser.add_argument('-d', '--destination', help='Output directory', nargs=1)
    parser.add_argument('-r', '--textfile', help='Generates a textfile with scores', action='store_true')
    args = parser.parse_args()
    DIR = args.source
    DESTINATION = args.destination
    TEXTFILE = args.textfile



class Plotter(object):
    args = Args()
    test_objects = []
    configs = plotter_config.Config.configurations
    test_type = plotter_config.Config.test_type

    def parse_fio_output(self, fio_output):
        try:
            with open(fio_output) as file:
                iops_sum = 0
                for line in file:
                    if 'iops' in line:
                        iops_sum += int(line.split('iops=')[1].split(',')[0])   # IOPS
        except FileNotFoundError:
            print("Error! File ", fio_output, "not found...")
          #  continue
        return iops_sum

    def parse_raw_output(self, raw_file):
        time = []
        values = []
        try:
            with open(raw_file) as file:
                for line in file:
                    line_data = line.split(',') # index 0 is time, index 1 is IOPS
                    time.append(int(line_data[0]))
                    values.append(int(line_data[1]))
                time.append(0)
        except FileNotFoundError:
            print("Error!", raw_file, "not found...")
            #continue
        return time, values

    def calculate_values(self, numjobs, time, values):
        i = 0
        raw_iops_avg = 0
        for job in range(numjobs):  # Test[1] = number of jobs
            job_values = []
            while time[i] <= time[i+1]:
                job_values.append(values[i])
                i += 1
            job_values.append(values[i])
            raw_iops_avg += numpy.mean(job_values)
            i += 1
        deviation = numpy.std(values)
        return raw_iops_avg, deviation

    def read_files(self):
        for conf in self.configs:
            my_path = os.path.join(self.args.DIR[0], conf)
            newest_tmp = sorted(os.listdir(my_path),    # Needed for compatibility with run_fio.sh
                key=lambda last_change: os.path.getctime(os.path.join(my_path, last_change)))
            newest = newest_tmp[-1]
            test_dir = os.path.realpath(self.args.DIR[0])
            for test in self.test_type:
                raw_file = os.path.join(test_dir, conf, newest, test[0] + '-iopslog_iops.log')
                fio_output = os.path.join(test_dir, conf, newest, test[0])
                iops_sum = self.parse_fio_output(fio_output)
                time, values = self.parse_raw_output(raw_file)
                raw_iops_avg, deviation = self.calculate_values(test[1], time, values)
                # Tuple containing test data are added to an array
                self.test_objects.append((conf, test[0], raw_iops_avg, iops_sum, deviation))

    def get_destination(self):
        if self.args.DESTINATION:
            return self.args.DESTINATION[0]
        else:
            return os.getcwd()

    def make_chart(self):
        self.read_files()
        if self.args.TEXTFILE:
            with open(os.path.join(self.get_destination(), 'scores.txt'), 'w') as file:
                pass
        for test in self.test_type:
            raw_means = []
            names = []
            fio_means = []
            std_dev = []
            print("Test: ", test[2])
            if self.args.TEXTFILE:
                with open(os.path.join(self.get_destination(), 'scores.txt'), 'a') as file:
                    file.write('Test: ' + test[2] + "\n")
            for conf in self.test_objects:
                conf_name, test_name, raw_iops, fio_iops, deviation = conf
                if test[0] == test_name:
                    names.append(conf_name)
                    fio_means.append(fio_iops)
                    raw_means.append(raw_iops)
                    std_dev.append(deviation)
                    print(" " * 2, "Configuration: ", conf_name)
                    print(" " * 4, "Raw IOPS: ", raw_iops)
                    print(" " * 4, "Fio IOPS: ", fio_iops)
                    print(" " * 4, "Standard Deviation: ", deviation)
                    if self.args.TEXTFILE:
                        with open(os.path.join(self.get_destination(), 'scores.txt'), 'a') as file:
                            file.write(" " * 2 + 'Configuration: ' + str(conf_name) + "\n")
                            file.write(" " * 4 + 'Raw IOPS: ' + str(raw_iops) + "\n")
                            file.write(" " * 4 + 'Fio IOPS: ' + str(fio_iops) + "\n")
                            file.write(" " * 4 + 'Standard Deviation: ' + str(deviation) + "\n")
            ind = numpy.arange(len(raw_means))
            width = 0.3
            rects1 = plt.bar(ind, raw_means, width, color='gray', align='center', yerr=std_dev,
                error_kw=dict(ecolor='black'))
            rects2 = plt.bar(ind+width, fio_means, width, color='green', align='center')
            plt.ylabel('IOPS')
            plt.title(test[2])
            plt.xticks(ind+width/2, names, rotation=270)
            plt.grid(True, axis='y')
            green = mpatches.Patch(color='green', label='Standard output IOPS ')
            grey = mpatches.Patch(color='grey', label='Raw IOPS')
            plt.legend(handles=[grey, green], bbox_to_anchor=(0.8, 0.1), ncol=2,
                bbox_transform=plt.gcf().transFigure)
            fig = plt.gcf()
            fig.subplots_adjust(top=0.95)
            fig.subplots_adjust(bottom=0.4)
            plt.savefig(os.path.join(self.get_destination(), test[0] + '.pdf'), format='pdf')
            print('-' * 90)
            plt.close()


def main():
    p = Plotter()
    if p.args.DIR:
        p.make_chart()
  #      p.tmp()
    else:
        pass


if __name__ == "__main__":
    main()
