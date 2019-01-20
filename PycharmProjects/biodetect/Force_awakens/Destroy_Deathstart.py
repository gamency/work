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
    def __init__(self, ion_drive, message, verify_info):
        self.data = ion_drive
        self.message = message
        self.verify_info = verify_info

    def polar_trench(self):
        time_elapse = (self.data['Time'] - self.data['Time'].shift(1))[1:]
        distance_x = (self.data['op_x'] - self.data['op_x'].shift(1))[1:]
        distance_y = (self.data['op_y'] - self.data['op_y'].shift(1))[1:]

        hor_velocity = distance_x / time_elapse
        ver_velocity = distance_y / time_elapse

        tangential_vel = np.sqrt(np.square(hor_velocity) + np.square(ver_velocity))
        tangential_accel = tangential_vel / time_elapse
        # tangential_jerk = tangential_accel / time_elapse

        slop_angle_of_tangen = np.arctan(self.data['op_y'] / self.data['op_x'])
        path_from_original = np.sqrt(np.square(self.data['op_x']) + np.square(self.data['op_y']))
        incresment_of_slop_angle_of_tangen = (slop_angle_of_tangen - slop_angle_of_tangen.shift(1))[1:]
        delta_pop = (path_from_original - path_from_original.shift(1))[1:]

        curvature = incresment_of_slop_angle_of_tangen / delta_pop

        delta_curv = (curvature - curvature.shift(1))[1:]
        curvature_rate_of_change = delta_curv / delta_pop

        curvature[curvature.isnull()] = 0
        curvature_rate_of_change[curvature_rate_of_change.isnull()] = 0

        # hist = self.click_distribution()

        # original set, comment at fi version 1
        # features = [distance_x, distance_y, hor_velocity, ver_velocity,
        #             tangential_vel, tangential_accel, tangential_jerk,
        #             curvature, curvature_rate_of_change]

        # features = [distance_x, distance_y, tangential_vel, tangential_accel, tangential_jerk,
        #             curvature, curvature_rate_of_change]

        features = [distance_x, tangential_accel, curvature, curvature_rate_of_change]

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

    def click_distribution(self):
        if self.verify_info['scenario'] == 1:
            bar_center_x = self.verify_info['slidebarleft_x'] + \
                           (self.verify_info['slidebarright_x'] - self.verify_info['slidebarleft_x'])/2
            bar_center_y = self.verify_info['slidebarleft_y'] + \
                           (self.verify_info['slidebarright_y'] - self.verify_info['slidebarleft_y']) / 2

            click_point = self.data.loc[self.data['event_type'] == 2, ['op_x', 'op_y']].values
            release_dragndrop_point = self.data.loc[self.data['event_type'] == 3, ['op_x', 'op_y']].values
        else:
            bar_center_x = self.verify_info['second_x'] + \
                           (self.verify_info['first_x'] - self.verify_info['second_x']) / 2
            bar_center_y = self.verify_info['second_y'] + \
                           (self.verify_info['first_y'] - self.verify_info['second_y']) / 2

            click_point = self.data.loc[self.data['mouse_event_type'] == 2, ['op_x', 'op_y']].values
            release_dragndrop_point = self.data.loc[self.data['event_type'] == 3, ['op_x', 'op_y']].values

        if len(release_dragndrop_point) == 0:
            print("no click release signal during operation")
            no_click_release_signal = 1
            release_point_x = 0
            release_point_y = 0
            # return no_click_release_signal

        for i in range(0, len(release_dragndrop_point)):
            release_point_x = release_dragndrop_point[i, 0]
            release_point_y = release_dragndrop_point[i, 1]

            #         release_point_x = release_opx[i,0]
            #         release_point_y = release_opy[i,1]
            print("release point is", release_point_x, release_point_y)

        if len(click_point) == 0:
            click_point_action = self.data.loc[self.data['Action'] == 12, ['op_x', 'op_y']].values
            if len(click_point_action) == 0:
                print("what happen here")
                click_point_x = 0
                click_point_y = 0
            # return 0.5
                hit_bar_center = 2
            click_point = click_point_action

        for i in range(0, len(click_point)):
            op_x = click_point[i,0]
            op_y = click_point[i, 1]

            if self.verify_info['scenario'] == 1:
                hit_inbox_check = op_x > self.verify_info['slidebarleft_x'] \
                                  and op_x < self.verify_info['slidebarright_x'] \
                                  and op_y > self.verify_info['slidebarleft_y'] \
                                  and op_y < self.verify_info['slidebarright_y']
            else:
                hit_inbox_check = op_x > self.verify_info['second_x'] \
                                  and op_x < self.verify_info['first_x'] \
                                  and op_y > self.verify_info['second_y'] \
                                  and op_y < self.verify_info['first_y']

            if op_x == bar_center_x and op_y == bar_center_y:
                click_point_x = click_point[i, 0]
                click_point_y = click_point[i, 1]
                hit_bar_center = 2
            elif hit_inbox_check:
                print("click in box")
                if self.verify_info['scenario'] == 1:
                    hit_bar_dis_x = float(click_point[i, 0] - self.verify_info['slidebarleft_x']) / \
                                (self.verify_info['slidebarright_x'] - self.verify_info['slidebarleft_x'])
                    hit_bar_dis_y = float(click_point[i, 1] - self.verify_info['slidebarleft_y']) / \
                                (self.verify_info['slidebarright_y'] - self.verify_info['slidebarleft_y'])

                    click_point_x = click_point[i, 0]
                    click_point_y = click_point[i, 1]

                else:
                    hit_bar_dis_x = float(click_point[i, 0] - self.verify_info['second_x']) / \
                                    (self.verify_info['first_x'] - self.verify_info['second_x'])
                    hit_bar_dis_y = float(click_point[i, 1] - self.verify_info['second_y']) / \
                                    (self.verify_info['first_y'] - self.verify_info['second_y'])
                # print(hit_bar_dis_x, hit_bar_dis_y)
                hit_bar_center = np.mean([hit_bar_dis_x, hit_bar_dis_y])
            else:
                print("out of bar click")
                click_point_x = click_point[i, 0]
                click_point_y = click_point[i, 1]
                hit_bar_center = 0.0

        click_to_release_diff_of_y = np.abs(release_point_y - click_point_y)

        # dist = hit_bar_center, click_to_release_diff_of_y
        return hit_bar_center, click_to_release_diff_of_y
        pass

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
                # print("item is",type(item))
                item_structure = self.super_laser(item)
                merge_structure[0:0] = item_structure

                ts = Tsft(item)
                ts_tmp = ts.fft_all()

                merge_structure[0:0] = ts_tmp

                # merge_structure[0:0] = self.data.loc[0, 'Bot']

            # print("****", len(merge_structure))

            # if self.verify_info['scenario'] == 1:
            hit_bar_center_flag, click_to_release_diff_of_y = self.click_distribution()
            print("********",hit_bar_center_flag)
            # merge_structure.append(hit_bar_center_flag)
            merge_structure.append(hit_bar_center_flag)
            merge_structure.append(click_to_release_diff_of_y)
            print("hit bar center crd are",hit_bar_center_flag, click_to_release_diff_of_y)
            print("after", len(merge_structure),merge_structure)
            destroyer.append("bomb is good")
            # print("attacker begin to invade!")

        return destroyer, merge_structure
