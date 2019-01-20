# -*- coding: utf-8 -*-
# This file as well as the whole biometricsdetect package are licenced under the FIT licence (see the LICENCE.txt)
# Kite Fu (kitefu@163.com), HangZhou city, 2017
"""
This script can be run with:


.. code-block:: bash

   python run_xx.py path_to_your_csv.csv

xxxxxxxxx

There are a few limitations though

- Currently this only samples to first 50 values.
- Your csv must be space delimited.
- Output is saved as path_to_your_csv.features.csv

"""


import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# from Rohan.Decouple_Captcha import Up_Down_Transf
import sys
from ruamel.yaml import YAML
# from pyspark.sql import SparkSession
import os


class RohanCavlry(object):
    def __init__(self, fetch_data_range, fetch_data_table,  partner_set, bussiness_type):
        self.date_info = fetch_data_range
        self.fdt = fetch_data_table
        self.fps = partner_set
        self.fbt = bussiness_type
        pass

    def parse_captcha(self):
        if self.fbt == 'captcha':
            print("it's captcha bussiness")
            big_data_phase0, big_data_phase1 = Up_Down_Transf(self.pirates_caribben())
            
        pass
        return big_data_phase0, big_data_phase1

    def pirates_caribben(self):
        year = self.date_info[0]
        month_start = self.date_info[1]
        month_end = self.date_info[2]
        start_day = self.date_info[3]
        end_day = self.date_info[4]
        partnercode = self.date_info[8]
        app_name = self.date_info[9]
        test = self.date_info[10]
        spark = SparkSession.builder.appName("test").enableHiveSupport().getOrCreate()
        if test == 1:
            select_df = spark.sql('''select get_json_object(rqst_other_fields, '$.mouseMoving) msg, 
            get_json_object(rqst_other_fields, '$.botProbability) prob, month, day from bigdata.raw_activity_flat 
            where year={} and month >= {} and month <= {} and day <= {} and partnercode='{}' and appName='{}' and event='verification' '''.format(year, month_start, month_end, start_day, end_day, partnercode, app_name))
        else:
            select_df = spark.sql('''select get_json_object(rqst_other_fields, '$.mouseMoving) msg, 
            get_json_object(rqst_other_fields, '$.botProbability) prob, month, day from bigdata.raw_activity_flat 
            where year={} and month >= {} and month <= {} and day <= {} and partnercode='{}' and event='verification' '''.format(year, month_start, month_end, start_day, end_day, partnercode))
        
        df = select_df.toPandas()
        df = df[pd.notnull(df['msg'])]
        return df

    def parse_captcha_local(self):
        # local_file_dir_first_phase = self.date_info[5]
        # local_file_dir_second_phase = self.date_info[6]

        def fetch_file_name(file_dir):
            data_file_names = []
            for root, dirs, files in os.walk(file_dir):
                data_file_names = files.copy()
            if '.DS_Store' in data_file_names:
                data_file_names.remove('.DS_Store')
            return data_file_names

        def colon_soldier(base_location):
            # read in files for colon
            data_file_names = fetch_file_name(base_location)

            # for every colon seed, calling lightsaber
            colon_collection = []
            for item in data_file_names:
                print("_____start____", item)
                colon_location = base_location + str(item)
                colon_seed = open(colon_location, 'r')

                colon_df = pd.read_csv(colon_seed)
                # colon_item = lightsaber(colon_df)
                colon_collection.append(colon_df)

            print(colon_collection)
            print(len(colon_collection))
            # form the lightsaber return to a millitary
            # colon_name = military_name()
            # colon_military = pd.DataFrame(colon_collection, columns=colon_name)
            return colon_collection

        for file_dir in self.date_info[5]:
            if file_dir == 'PC_first_dir':
                phase1_data = colon_soldier(self.date_info[5][file_dir])
            elif file_dir == 'PC_second_dir' and self.date_info[7] == 0:
                phase2_data = colon_soldier(self.date_info[5][file_dir])
            else:
                print("no in pc type")
        if self.date_info[7] == 1:
            phase2_data = colon_soldier(self.date_info[6])
        # return data_file_names
        return phase1_data, phase2_data

    def form(self):
        if self.fbt == 'captcha':
            hdfs_phase1, hdfs_phase2 = self.parse_captcha()
        #if self.date_info[7] == 0:
        local_phase1, local_phase2 = self.parse_captcha_local()
        #     terminal is h5, have first and second phase

        # to fetch data from tweo repository, hdfs & local file system,
        # for capture: hdfs1, hdfs2, local1, local2
        return hdfs_phase1, hdfs_phase2, local_phase1, local_phase2
        pass


def main():
    #file_y = '/Users/kite/Desktop/test.yml'
    file_y = './Rohan/cavalry.yml'
    yaml = YAML()
    cav_info = open(file_y).read()
    cav = yaml.load(cav_info)
    fetch_data_info = [cav['year'], cav['start_month'], cav['end_month'], cav['start_day'], cav['end_day'],
                        cav['PC_data_dir'], cav['Andriod_second_dir'], cav['Terminal']]

    test = RohanCavlry(fetch_data_info, 'bigdata.raw_activity_flat', 'verification', 'captcha')

    test.form()
    result1, result2 = test.parse_captcha()
    # print(result.head())
    pass


if __name__ == '__main__':
    import os
    print(os.path)
    # main()
    filename = "/Users/kite/sdfsadf"
    f = open(filename, 'r')
    for line in f:
        print(line)

    pass
