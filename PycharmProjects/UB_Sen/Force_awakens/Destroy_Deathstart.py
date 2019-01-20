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
# import pandas as pd
# import matplotlib.pyplot as plt
# import time
# from Force_awakens.Tf_transform import Tsft


class DeathStartSys(object):
    def __init__(self, ion_drive, message):
        self.data = ion_drive
        self.message = {}
        self.message['success'] = 1
        # self.select_sensor_basket = message['select_sensor_basket']
        # self.Rss_statistic = message['Rss_statistic_name']
        self.sensor_basket = message['sensor_basket']
        self.select_sensor = message['select_sensor']

    def polar_trench(self):
        Rss_statistic = []
        for i in self.select_sensor:

            if len(self.sensor_basket[i]) < 2:
                # print("sensor value is", np.sum(np.square(dataframe.loc[:, sensor_dimension_name[i]])))
                # self.data[self.Rss_statistic[sensor_index]] = np.sum(np.square(self.data.loc[:, self.sensor_basket[i]]))
                qa = np.sum(np.square(self.data.loc[:, self.sensor_basket[i]]))
            else:
                # print("sensor dimension name is",sensor_dimension_name[i])
                # self.data[self.Rss_statistic[sensor_index]] = np.sum(np.square(self.data.loc[:, self.sensor_basket[i]]), axis=1)
                qa = np.sum(np.square(self.data.loc[:, self.sensor_basket[i]]), axis=1)
            Rss_statistic.append((qa))

        # self.data = self.data.fillna(0)
        # print(Rss_statistic)

        return Rss_statistic

    def super_laser(self, sequencial_data):
        # time_construct = []
        time_mean = np.mean(sequencial_data)
        # time_var = np.var(sequencial_data)
        time_std = np.std(sequencial_data)
        # time_domain_mode = scipy.stats.mode(sequencial_data)[0]
        time_max = np.max(sequencial_data)

        # time_min comment at time construct version 1
        time_min = np.min(sequencial_data)

        # time_time_over_zero = len(sequencial_data > 0)
        time_range = (time_max - time_min)
        # time_average_deviaton = np.mean(np.sum(sequencial_data - time_mean))
        time_skew = sequencial_data.skew()
        time_kurt = sequencial_data.kurt()
        # comment time_rms at time construct version 1
        # time_rms = np.sqrt(np.mean(np.sum(np.square(sequencial_data))))

        # original full version
        # time_construct = [time_mean, time_std, time_max, time_min, time_range,
        #                   time_average_deviaton, time_skew, time_kurt, time_rms]

        # select version 1
        # time_construct = [time_mean, time_std, time_max, time_range,
        #                   time_average_deviaton, time_skew, time_kurt]

        time_construct = [time_mean, time_range, time_skew, time_kurt]

        return time_construct

    def command_scetor(self):
        # first Locate the death start
        # death_start(message)
        # second start endor action
        # third behavior destroy death start
        # fourth Back of skywalker
        destroyer = []
        # print("message", self.message["success"])

        if self.message["success"] == 1:
            # start analysis death start
            # from Force_awakens.Locate_Location import death_start
            # deathstart_message = death_start(self.message)

            base_structure = self.polar_trench()
            # print("base structure is", base_structure)
            merge_structure = []

            from Force_awakens.Tf_transform import Tsft
            #
            for item in base_structure:
                # print(type(item))
                item_structure = self.super_laser(item)
                merge_structure[0:0] = item_structure

                ts = Tsft(item)
                ts_tmp = ts.fft_all()

                merge_structure[0:0] = ts_tmp

                # merge_structure[0:0] = self.data.loc[0, 'Bot']

            # print("merge structure is", merge_structure)

            destroyer.append("bomb is good")
            # print("attacker begin to invade!")

        return destroyer, merge_structure
