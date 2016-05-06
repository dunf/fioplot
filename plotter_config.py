#!/usr/bin/python3

class Config(object):
    configurations = [
#        'Samsung 840 EVO',        # SSD baseline test
#        'BaselineSSD',           # Full run på dozer
#        'Samsung 840 disk1',               # baseSSDapoc
#        'Samsung 840 disk2',              # baseSSDdozer
#        'Samsung 840 disk3',             # baseSSDswitch
#        'Samsung 840 disk4',            # baseSSDtrinity
#	'20RampTime',
#	'noRampTime',
#        'logbsize256',
        'WBT-3R-6O-1K-1.5K',
        'WBT-3R-6O-10K-15K',
        'WBT-3R-6O-100K-200K',
#        'WBT-1R-6O-500-1K',
#        'WBT-1R-6O-500-5K',
#        'WBT-1R-6O-1K-1.5K',
#        'WBT-1R-6O-2K-2.5K',
#        'WBT-1R-6O-3K-5K',
#        'WBT-1R-6O-10K-15K',
#        'WBT-1R-6O-100K-200K',
#        'WBT-1R-6O-jstore100',
#        'WBT-1R-6O-jstore3K',
#        'WBT-3R-3O',   #      replicatest_3
#        'WBT-3R-4O',   #      replicatest_4
#        'WBT-3R-5O',   #      replicatest_5
#        'WBT-3R-6O',   #      replicatest_6
#        'NoWBT-3R-6O', #      Dflt_NoWBT_baseline',
#        'WBT-3R-6O-MS5',      # wb_maxsync5',
#        'WBT-1R-1O-MS1',
#        'WBT-1R-1O-MS30',
#        'WBT-1R-1O-MS40',
#        'WBT-1R-1O-MS60',
#        'WBT-1R-1O-MS90',
#        'WBT-1R-1O-MS120',
#        'WBT-1R-1O-MS240',
#        'WBT-1R-1O-QMO3K',
#        'WBT-1R-1O-QMO0.5K',
#        'WBT-1R-1O-QCMO_3K',
#        'WBT-1R-1O-XFSIO2K0.5K',
#        'WBT-1R-1O-XFSIO2K1K',
#    	'WBT-1R-1O-JW100',
#	    'WBT-1R-1O-JW50',
#    	'WBT-1R-1O-JW200',
#    	'WBT-1R-1O-JW1K',
#        'WBT-1R-1O-DEF',
#        'WBT-1R-1O',
#        'WBT-1R-2O',   #      osdtest_2
#        'WBT-1R-3O',   #      osdtest_3
#        'WBT-1R-4O',   #      osdtest_4
#        'WBT-1R-5O',   #      osdtest_5
#        'WBT-1R-6O',   #      osdtest_6
#        'WBT-1R-6O-JW1000',
#        'WBT-1R-6O-JW500',
#        'WBT-1R-6O-JW300',
#        'WBT-1R-6O-JW200',
#        'WBT-1R-6O-JW100',
#        'WBT-1R-6O-JW50',
#        'WBT-1R-6O-JW20',
#        'wbthrottle',
#        'wbthrottle_run_2',
#        'wbthrottle_run_3',
#        'DebugOff_run_1',
#        'tmp',       
#         '1OSD-HDD-Sync250',     #'OSD_HDD Sync 250',       # onedrive_ssd_max250_run_1
#         'NoWBT-1R-1O-SSD',      # Single OSD_SSD',       # onedrive_ssd_run_2a
#         'NoWBT-1R-1O-HDD',      # Single OSD_HDD
#        'OSD_HDD client cache',   # onedrive_ssd_max250_run_2
#        'JumboFrames_run_1',    # 1 Replica + default settings.
#      	'SAS 15k disk1',  # sasd1Trinity
#      	'SAS 10k disk2',   # sasd2Trinity
#      	'SAS 10k disk3',     # sasd1Apoc
#      	'SAS 10k disk4',     # sasd2Apoc
#        'SAS 10k disk5',    # sasd1Dozer
#      	'SAS 10k disk6',    # sasd2Dozer
#      	'SAS 10k disk7',   # sasd1Switch
#      	'SAS 10k disk8',   # sasd2Switch
#        '0replica',
#        'G6_run_1',
#        'G6_run_2',
#        'run_2_600sec',
#        'run2',
#        'titlap_3',
#        'jobs_qd_testing_run_1',
#        'MaxSync_5_run_1',
#        '1R-Sync-5sec',     #'1 Replica MS 5',       # 1_replica_run_1
#        '1R-Sync-10sec',    #'1 Replica MS 10',      # 1_replica_run_2_maxsync_10
#        '3R-Sync-1sec',     #'1 sec',
#        '3R-Sync-5sec',     #'5 sec',
#        '3R-Sync-10sec',    #10 sec',
#        '3R-Sync-200sec',   # '200 sec',    # MaxSync200
#        'MaxSync_1_run_1',
#        'MaxSync_10_run_1',
#        'MaxSync_10_run_2',
#        'MaxSync_10_run_3',

#        'HDD_ONLY_run_1',
#        'HDD_ONLY_run_2',
#        '9-10 sec',   # Max10Min9

#        'Maxsynctest1',     # Max sync 1
#        'Maxsynctest2',     # Max sync 5
#        'Maxsynctest3',     # Max sync 10
    ]
# Array of tuples that specify the files and number of jobs for each test.
# Format: short testname, number of jobs, test description
    test_type = [
        ('fsseqR1-16', 1, 'Seq Read bs=256K, 1 job, IOdepth 16'),
        ('fsseqW1-16', 1, 'Seq Write bs=256K 1 job, IOdepth 16'),
        ('fsrandR1-1', 1, 'Random Read 1 jobs, IOdepth 1'),
        ('fsrandR1-16', 1, 'Random Read 1 jobs, IOdepth 16'),
        ('fsrandR1-32', 1, 'Random Read 1 jobs, IOdepth 32'),
        ('fsrandR1-64', 1, 'Random Read 1 jobs, IOdepth 64'),
        ('fsrandR16-1', 16, 'Random Read 16 jobs, IOdepth 1'),
        ('fsrandR16-16', 16, 'Random Read 16 jobs, IOdepth 16'),
        ('fsrandR16-32', 16, 'Random Read 16 jobs, IOdepth 32'),
        ('fsrandR16-64', 16, 'Random Read 16 jobs, IOdepth 64'),
        ('fsrandW1-1', 1, 'Random Write 1 jobs, IOdepth 1'),
        ('fsrandW1-16', 1, 'Random Write 1 jobs, IOdepth 16'),
        ('fsrandW1-32', 1, 'Random Write 1 jobs, IOdepth 32'),
        ('fsrandW1-64', 1, 'Random Write 1 jobs, IOdepth 64'),
        ('fsrandW16-1', 16, 'Random Write 16 jobs, IOdepth 1'),
        ('fsrandW16-16', 16, 'Random Write 16 jobs, IOdepth 16'),
        ('fsrandW16-32', 16, 'Random Write 16 jobs, IOdepth 32'),
        ('fsrandW16-64', 16, 'Random Write 16 jobs, IOdepth 64'),
        ('fsmixedRW703016-16', 16, 'Mixed RW 70/30 bs=8K, 16 jobs, IOdepth 16'),

    #    ('fsrandW4-8', 4, 'Random Write 4 jobs, IOdepth 8'),
    #    ('fsrandW4-16', 4, 'Random Write 4 jobs, IOdepth 16'),
    #    ('fsrandW4-32', 4, 'Random Write 4 jobs, IOdepth 32'),
    #    ('fsrandW4-64', 4, 'Random Write 4 jobs, IOdepth 64'),
    #    ('fsrandW8-8', 8, 'Random Write 8 jobs, IOdepth 8'),
    #    ('fsrandW8-16', 8, 'Random Write 8 jobs, IOdepth 16'),
    #    ('fsrandW8-32', 8, 'Random Write 8 jobs, IOdepth 32'),
    #    ('fsrandW8-64', 8, 'Random Write 8 jobs, IOdepth 64'),
    ]
