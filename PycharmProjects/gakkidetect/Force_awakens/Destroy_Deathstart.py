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
        self.message = message

    def polar_trench(self):
        time_elapse = (self.data['Time'] - self.data['Time'].shift(1))[1:]
        distance_x = (self.data['op_x'] - self.data['op_x'].shift(1))[1:]
        distance_y = (self.data['op_y'] - self.data['op_y'].shift(1))[1:]

        hor_velocity = distance_x / time_elapse
        ver_velocity = distance_y / time_elapse

        tangential_vel = np.sqrt(np.square(hor_velocity) + np.square(ver_velocity))
        tangential_accel = tangential_vel / time_elapse
        tangential_jerk = tangential_accel / time_elapse

        slop_angle_of_tangen = np.arctan(self.data['op_y'] / self.data['op_x'])
        path_from_original = np.sqrt(np.square(self.data['op_x']) + np.square(self.data['op_y']))
        incresment_of_slop_angle_of_tangen = (slop_angle_of_tangen - slop_angle_of_tangen.shift(1))[1:]
        delta_pop = (path_from_original - path_from_original.shift(1))[1:]

        curvature = incresment_of_slop_angle_of_tangen / delta_pop

        delta_curv = (curvature - curvature.shift(1))[1:]
        curvature_rate_of_change = delta_curv / delta_pop

        curvature[curvature.isnull()] = 0
        curvature_rate_of_change[curvature_rate_of_change.isnull()] = 0

        # original set, comment at fi version 1
        # features = [distance_x, distance_y, hor_velocity, ver_velocity,
        #             tangential_vel, tangential_accel, tangential_jerk,
        #             curvature, curvature_rate_of_change]

        features = [distance_x, distance_y, tangential_vel, tangential_accel, tangential_jerk,
                    curvature, curvature_rate_of_change]

        return features

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
        time_average_deviaton = np.mean(np.sum(sequencial_data - time_mean))
        time_skew = sequencial_data.skew()
        time_kurt = sequencial_data.kurt()
        # comment time_rms at time construct version 1
        # time_rms = np.sqrt(np.mean(np.sum(np.square(sequencial_data))))

        # original full version
        # time_construct = [time_mean, time_std, time_max, time_min, time_range,
        #                   time_average_deviaton, time_skew, time_kurt, time_rms]

        # select version 1
        time_construct = [time_mean, time_std, time_max, time_range,
                          time_average_deviaton, time_skew, time_kurt]

        return time_construct

    # def mid_hemisphere(self, series):
    #     fft_transform = np.abs(np.fft.fft(series))
    #     dc = fft_transform[0]
    #     freq_spectrum = fft_transform[1:int(np.floor(len(series) * 1.0 / 2)) + 1]
    #     freq_sum_ = np.sum(freq_spectrum)
    #
    #     fft_mean = np.mean(freq_spectrum)
    #
    #     fft_var = np.var(freq_spectrum)
    #
    #     fft_std = np.std(freq_spectrum)
    #
    #     pr_freq = freq_spectrum * 1.0 / freq_sum_
    #     fft_entropy = -1 * np.sum([np.log2(p) * p for p in pr_freq])
    #
    #     fft_energy = np.sum(freq_spectrum ** 2) / len(freq_spectrum)
    #
    #     fft_skew = np.mean([0 if fft_std == 0 else np.power((x - fft_mean) / fft_std, 3) for x in self.freq_spectrum])
    #
    #     fft_kurt =  np.mean([0 if fft_std == 0 else np.power((x - fft_mean) / fft_std, 4) - 3
    #                         for x in self.freq_spectrum])
    #
    #     shape_sum = np.sum([x * freq_spectrum[x] for x in range(len(self.freq_spectrum))])
    #     fft_shape_mean = 0 if freq_sum_ == 0 else shape_sum * 1.0 / freq_sum_
    #
    #     def fft_shape_std(fft_shape_mean):
    #         if self._freq_sum_ == 0:
    #             return 0
    #         shape_mean = fft_shape_mean
    #         var = np.sum([0 if freq_sum_ == 0 else np.power((x - shape_mean), 2) * freq_spectrum[x]
    #                       for x in range(len(freq_spectrum))]) / freq_sum_
    #         return np.sqrt(var)
    #
    #     def fft_shape_skew(fft_shape_mean):
    #         if freq_sum_ == 0:
    #             return 0
    #         shape_mean = fft_shape_mean
    #         return np.sum([np.power((x - shape_mean), 3) * freq_spectrum[x]
    #                        for x in range(len(freq_spectrum))]) / freq_sum_
    #
    #     def fft_shape_kurt(fft_shape_mean):
    #         if freq_sum_ == 0:
    #             return 0
    #         shape_mean = fft_shape_mean()
    #         return np.sum([np.power((x - shape_mean), 4) * freq_spectrum[x] - 3 for x in
    #                        range(len(freq_spectrum))]) / freq_sum_
    #
    #     def fft_all(self):
    #         # feature_all = list()
    #         feature_all = []
    #         feature_all.append(self.fft_dc())
    #         feature_all.append(self.fft_shape_mean())
    #         if self.fft_shape_mean == 0:
    #             feature_all.append(0)
    #             feature_all.append(0)
    #             feature_all.append(0)
    #             feature_all.append(0)
    #         else:
    #             feature_all.append(self.fft_shape_std() ** 2)
    #             feature_all.append(self.fft_shape_std())
    #             feature_all.append(self.fft_shape_skew())
    #             feature_all.append(self.fft_shape_kurt())
    #         feature_all.append(self.fft_mean())
    #         feature_all.append(self.fft_var())
    #         feature_all.append(self.fft_std())
    #         feature_all.append(self.fft_skew())
    #         feature_all.append(self.fft_kurt())
    #
    #         return feature_all
        # return

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
            merge_structure = []

            from Force_awakens.Tf_transform import Tsft

            for item in base_structure:
                item_structure = self.super_laser(item)
                merge_structure[0:0] = item_structure

                ts = Tsft(item)
                ts_tmp = ts.fft_all()

                merge_structure[0:0] = ts_tmp

                # merge_structure[0:0] = self.data.loc[0, 'Bot']

            # print(merge_structure)

            destroyer.append("bomb is good")
            # print("attacker begin to invade!")

        return destroyer, merge_structure
