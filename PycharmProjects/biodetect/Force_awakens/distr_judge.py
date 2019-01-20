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


def dist_judge(data, verify_info):
    if verify_info['scenario'] == 1:
        bar_center_x = verify_info['slidebarleft_x'] + \
                       (verify_info['slidebarright_x'] - verify_info['slidebarleft_x']) / 2
        bar_center_y = verify_info['slidebarleft_y'] + \
                       (verify_info['slidebarright_y'] - verify_info['slidebarleft_y']) / 2

        click_point = data.loc[data['event_type'] == 2, ['op_x', 'op_y']].values
        release_dragndrop_point = data.loc[data['event_type'] == 3, ['op_x', 'op_y']].values
    else:
        bar_center_x = verify_info['second_x'] + \
                       (verify_info['first_x'] - verify_info['second_x']) / 2
        bar_center_y = verify_info['second_y'] + \
                       (verify_info['first_y'] - verify_info['second_y']) / 2

        click_point = data.loc[data['mouse_event_type'] == 2, ['op_x', 'op_y']].values
        release_dragndrop_point = data.loc[data['event_type'] == 3, ['op_x', 'op_y']].values

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
        click_point_action = data.loc[data['Action'] == 12, ['op_x', 'op_y']].values
        if len(click_point_action) == 0:
            print("what happen here")
            click_point_x = 0
            click_point_y = 0
            # return 0.5
            hit_bar_center = 0.5
        click_point = click_point_action

    for i in range(0, len(click_point)):
        op_x = click_point[i, 0]
        op_y = click_point[i, 1]

        if verify_info['scenario'] == 1:
            hit_inbox_check = op_x > verify_info['slidebarleft_x'] \
                              and op_x < verify_info['slidebarright_x'] \
                              and op_y > verify_info['slidebarleft_y'] \
                              and op_y < verify_info['slidebarright_y']
        else:
            hit_inbox_check = op_x > verify_info['second_x'] \
                              and op_x < verify_info['first_x'] \
                              and op_y > verify_info['second_y'] \
                              and op_y < verify_info['first_y']

        if op_x == bar_center_x and op_y == bar_center_y:
            click_point_x = click_point[i, 0]
            click_point_y = click_point[i, 1]
            hit_bar_center = 0.5
        elif hit_inbox_check:
            print("click in box")
            if self.verify_info['scenario'] == 1:
                hit_bar_dis_x = float(click_point[i, 0] - verify_info['slidebarleft_x']) / \
                                (verify_info['slidebarright_x'] - verify_info['slidebarleft_x'])
                hit_bar_dis_y = float(click_point[i, 1] - verify_info['slidebarleft_y']) / \
                                (verify_info['slidebarright_y'] - verify_info['slidebarleft_y'])

                # click_point_x = click_point[i, 0]
                # click_point_y = click_point[i, 1]

            else:
                hit_bar_dis_x = float(click_point[i, 0] - verify_info['second_x']) / \
                                (self.verify_info['first_x'] - verify_info['second_x'])
                hit_bar_dis_y = float(click_point[i, 1] - verify_info['second_y']) / \
                                (self.verify_info['first_y'] - verify_info['second_y'])
            # print(hit_bar_dis_x, hit_bar_dis_y)
            hit_bar_center = np.mean([hit_bar_dis_x, hit_bar_dis_y])
        else:
            print("out of bar click")
            click_point_x = click_point[i, 0]
            click_point_y = click_point[i, 1]
            hit_bar_center = 0.5

    # click_to_release_diff_of_y = np.abs(release_point_y - click_point_y)

    # dist = hit_bar_center, click_to_release_diff_of_y
    return hit_bar_center