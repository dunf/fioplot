#!/usr/bin/python3

# This is a fork of Erik Hjelmås' plotsintex script.
# Usage: ./plotter -t DIRECTORY
# The directories needs to follow this structure:
# DIRECTORY/SomeConfig/SomeFolder/fiofiles
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
    parser.add_argument("-t", "--testdir", help="Generate barchart for all test configurations")
    parser.add_argument('-d', '--destination', help='Destination dir for output files', nargs=1)
    parser.add_argument('-r', '--histogram', nargs=1, help='Dir in which you want to generate histograms')
    args = parser.parse_args()
    DIR = args.testdir
    DESTINATION = args.destination
    HIST_DIR = args.histogram


class Plotter(object):
    args = Args()
    test_objects = []
    configs = plotter_config.Config.configurations
    test_type = plotter_config.Config.test_type

    def read_files(self):
        for conf in self.configs:
            my_path = os.path.join(self.args.DIR, conf)
            newest_tmp = sorted(os.listdir(my_path),    # Only needed for compatibility with run_fio.sh
                key=lambda last_change: os.path.getctime(os.path.join(my_path, last_change)))
            newest = newest_tmp[-1]
            test_dir = os.path.realpath(self.args.DIR)
            for test in self.test_type:
                raw_file = os.path.join(test_dir, conf, newest, test[0] + '-iopslog_iops.log')
                fio_output = os.path.join(test_dir, conf, newest, test[0])

                try:
                    with open(fio_output) as file:
                        print(fio_output)
                        iops_sum = 0
                        for line in file:
                            if 'iops' in line:
                                iops_sum += int(line.split('iops=')[1].split(',')[0])   # IOPS
                except FileNotFoundError:
                    print("Error! File ", fio_output, "not found...")
                    continue
                time = []
                values = []
                try:
                    with open(raw_file) as file:
                        for line in file:
                            line_data = line.split(',') # [0] is time, [1] is IOPS
                            time.append(int(line_data[0]))
                            values.append(int(line_data[1]))
                        time.append(0)
                except FileNotFoundError:
                    print("Error!", raw_file, "not found...")
                    continue
                i = 0
                raw_iops_avg = 0
                for job in range(test[1]):  # Test[1] = number of jobs
                    job_values = []
                    while time[i] <= time[i+1]:
                        job_values.append(values[i])
                        i += 1
                    job_values.append(values[i])
                    raw_iops_avg += numpy.mean(job_values)
                    i += 1
                # Tuple containing test data are added to an array
                self.test_objects.append((conf, test[0], raw_iops_avg, iops_sum))

    def create_barchart(self):
        fio_means = []
        means = []
        names = []
        for test in self.test_objects:
            print(test)



    def old_create_barchart(self):
        for test in configs.test_type:
            num_jobs = test[1]
            index = 0
            means = []
            std_dev = []
            fio_means = []
            names = []
            t1 = []
            for conf in self.configs:
                print("Test: ", test[2], "---- Configuration: ", conf)
                my_path = os.path.join(self.args.DIR, conf)
                newest_tmp = sorted(os.listdir(my_path),    # Needed for compatibility with run_fio.sh
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
                std_dev.append(numpy.std(values))
                i = 0
                temp = 0
                raw_iops_avg = 0
                for job in range(num_jobs):
                    job_values = []
                    while time[i] <= time[i+1]:
                        job_values.append(values[i])
                        i += 1
                    job_values.append(values[i])
                    raw_iops_avg += numpy.mean(job_values)
                    temp += sum(job_values)/120
                    i += 1
                t1.append(temp)
# ------------------------------ # ERIKS LÃ˜SNING --------------------------------------------------
#                tmp = numpy.zeros(120)
#                i = 0
#                last_element = len(time)-1
#                for j in range(num_jobs):
#                    k = 0
#                    while (time[i] <= time[i+1]) and (i < last_element-1):
#                        tmp[k] += values[i]
#                        k += 1
#                        i += 1
#                    tmp[k] += values[i]
#                    i += 1
#         ##       if i == last_element:
#           #         tmp[k] += values[i]
#            #    print("AVG: ", tmp.mean())
#                erik_means[index] = tmp.mean()
            #    erik_means.append(tmp.mean())
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
                print(" " * 2, "FIO IOPS: ", iops_sum)
                print(" " * 2, "RAW IOPS: ", raw_iops_avg)
                print(" " * 2, "Standard deviation: ", std_dev[index])
                means.append(raw_iops_avg)
                fio_means.append(iops_sum)
                names.append(conf)
                index += 1
            ind = numpy.arange(len(means))
            width = 0.3
            rects1 = plt.bar(ind, means, width, color='gray', align='center', yerr=std_dev,
                error_kw=dict(ecolor='black'))
            rects2 = plt.bar(ind+width, fio_means, width, color='green', align='center')
#            plt.bar(ind+width+0.3, t1, width, color='red')     # Uncomment for Erik score
            plt.ylabel('IOPS')
            plt.title(test[2])
            plt.xticks(ind+width/2, names, rotation=270)
            plt.grid(True, axis='y')

#           How to rotate values?
#            for rect in rects2:
#                height = rect.get_height()
#                plt.text(rect.get_x() + rect.get_width()/2., 1.02*height,
#                        '%d' % int(height),
#                        ha='center', va='bottom' )


            green = mpatches.Patch(color='green', label='Standard output IOPS ')
            grey = mpatches.Patch(color='grey', label='Raw IOPS')
#            red = mpatches.Patch(color='red', label='Raw IOPS/120')
            plt.legend(handles=[grey, green], bbox_to_anchor=(0.8, 0.1), ncol=2,
                bbox_transform=plt.gcf().transFigure)
            fig = plt.gcf()
            fig.subplots_adjust(top=0.95)
            fig.subplots_adjust(bottom=0.4)
#            plt.tight_layout()
#            try:
            plt.savefig('/home/' + pwd.getpwuid(os.getuid()).pw_name + '/Dropbox/Cephios/fioplot/results/' + test[0] + '.pdf')
#            except FileNotFoundError:
#                plt.savefig('/home/birger/Dropbox/Cephios/fioplot/results/' + test[0] + '.pdf')
            if file_exists is True:
                print("File " + test[0] + ".pdf saved...")
            print('-' * 90)
            plt.close()



def main():
    p = Plotter()
    if p.args.DIR:
        p.read_files()
        p.create_barchart()
    elif p.args.HIST_DIR:
        pass
      #  p.create_histogram()
    else:
        pass


if __name__ == "__main__":
    main()
