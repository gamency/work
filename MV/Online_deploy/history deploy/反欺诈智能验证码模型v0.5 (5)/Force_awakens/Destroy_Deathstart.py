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
from Tf_transform import Tsft
import pandas as pd
# import matplotlib.pyplot as plt
# import time


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

        tangential_vel = np.sqrt(np.square(ver_velocity) + np.square(ver_velocity))
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

        features = [distance_x, tangential_accel, curvature, curvature_rate_of_change]

        return features

    def super_laser(self, sequencial_data):
        # time_construct = []
        time_mean = np.mean(sequencial_data)
        # time_var = np.var(sequencial_data)
        time_std = np.std(sequencial_data)
        # time_domain_mode = scipy.stats.mode(sequencial_data)[0]
        time_max = np.max(sequencial_data)
        time_min = np.min(sequencial_data)
        # time_time_over_zero = len(sequencial_data > 0)
        time_range = (time_max - time_min)
        time_average_deviaton = np.mean(np.sum(sequencial_data - time_mean))
        time_skew = sequencial_data.skew()
        time_kurt = sequencial_data.kurt()
        time_rms = np.sqrt(np.mean(np.sum(np.square(sequencial_data))))

        time_construct = [time_mean, time_range, time_skew, time_kurt]

        return time_construct
    
    def click_distribution(self):
        if self.verify_info['scenario'] == 1:
            bar_center_x = self.verify_info['slidebarleft_x'] + (self.verify_info['slidebarright_x'] - self.verify_info['slidebarleft_x']) / 2
            bar_center_y =  self.verify_info['slidebarleft_y'] + (self.verify_info['slidebarright_y'] - self.verify_info['slidebarleft_y']) / 2
            mouse_up_point = self.data.loc[self.data['event_type'] == 2, ['op_x', 'op_y']].values
        else:
            bar_center_x = self.verify_info['second_x'] + (self.verify_info['first_x'] - self.verify_info['second_x']) / 2
            bar_center_y =  self.verify_info['second_y'] + (self.verify_info['first_x'] - self.verify_info['second_y']) / 2
            mouse_up_point = self.data.loc[self.data['mouse_event_type'] == 2, ['op_x', 'op_y']].values
        # print(bar_center_x, bar_center_y)
        
        #mouse_up_point = self.data.loc[self.data['event_type'] == 2, ['op_x', 'op_y']].values
        
        # hit_bar_center = 0.0
        # print("what happen here",mouse_up_point)
        if len(mouse_up_point) == 0:
            click_point_action = self.data.loc[pd.to_numeric(self.data['Action']) == 12, ['op_x', 'op_y']].values
            if len(click_point_action) == 0: 
                return 0.5
            else:
                mouse_up_point = click_point_action
                
        for i in range(0, len(mouse_up_point)):
            #print(i)
            op_x = mouse_up_point[i, 0]
            op_y = mouse_up_point[i, 1]
            
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
                print('hit')
                # try_x['hit_bar_center'] = 1
                hit_bar_center = 0.5
            elif hit_inbox_check:
                #print("click here")
                if self.verify_info['scenario'] == 1:
                    hit_bar_dis_x =  float(mouse_up_point[i,0] - self.verify_info['slidebarleft_x']) / (self.verify_info['slidebarright_x'] - self.verify_info['slidebarleft_x'])
                    hit_bar_dis_y =  float(mouse_up_point[i,1] - self.verify_info['slidebarleft_y']) / (self.verify_info['slidebarright_y'] - self.verify_info['slidebarleft_y'])
                else:
                    hit_bar_dis_x = float(mouse_up_point[i, 0] - self.verify_info['second_x']) / \
                                    (self.verify_info['first_x'] - self.verify_info['second_x'])
                    hit_bar_dis_y = float(mouse_up_point[i, 1] - self.verify_info['second_y']) / \
                                    (self.verify_info['first_y'] - self.verify_info['second_y'])
                hit_bar_center = np.mean([hit_bar_dis_x ,hit_bar_dis_y])
            else:
                #print("out of bar click")
                hit_bar_center = 0.0
                
        return hit_bar_center
        #pass

    # def mid_hemisphere(self, series):
    #     fft_transform = np.abs(np.fft.fft(series))
    #     dc = fft_transform[0]
    #     freq_spectrum = fft_transform[1:int(np.floor(len(series) * 1.0 / 2)) + 1]
    #     freq_sum_ = np.sum(freq_spectrum)

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

            # from Force_awakens.Tf_transform import Tsft

            for item in base_structure:
                item_structure = self.super_laser(item)
                merge_structure[0:0] = item_structure

                ts = Tsft(item)
                ts_tmp = ts.fft_all()

                merge_structure[0:0] = ts_tmp

                # merge_structure[0:0] = self.data.loc[0, 'Bot']

            # print(merge_structure)
            # if self.verify_info['scenario'] == 1:
            hit_bar_center_flag = self.click_distribution()
            merge_structure.append(hit_bar_center_flag)

            destroyer.append("bomb is good")
            # print("attacker begin to invade!")

        return destroyer, merge_structure