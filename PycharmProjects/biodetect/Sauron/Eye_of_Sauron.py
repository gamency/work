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


# import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
# import time
# import os
plt.style.use('ggplot')


def local_thunder(data):
    #     find start
    start_x_point = data.loc[0, 'op_x']
    start_y_point = data.loc[0, 'op_y']


    #     find click

    click_point = data.loc[data['event_type'] == 2, ['op_x', 'op_y']].values

    if len(click_point) == 0:
        print("no click signal during operation")
        no_click_signal = 1

        click_point_x = 0
        click_point_y = 0
        # return no_click_signal

    for i in range(0, len(click_point)):
        click_opx = click_point[i, 0]
        click_opy = click_point[i, 1]

        if data.loc[0, 'scenario'] == 1:
            hit_inbox_check = click_opx > data.loc[0, 'slidebarleft_x'] \
                              and click_opx < data.loc[0, 'slidebarright_x'] \
                              and click_opy > data.loc[0, 'slidebarleft_y'] \
                              and click_opy < data.loc[0, 'slidebarright_y']
        else:
            hit_inbox_check = click_opx > data.loc[0, 'second_x'] \
                              and click_opx < data.loc[0, 'first_x'] \
                              and click_opy > data.loc[0, 'second_y'] \
                              and click_opy < data.loc[0, 'first_y']
        if hit_inbox_check:
            click_point_x = click_point[i, 0]
            click_point_y = click_point[i, 1]
            print("click point is", click_point_x, click_point_y)

            #     find end

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

    click_info = {"start_x_point": start_x_point, "start_y_point": start_y_point, "click_point_x": click_point_x,
                  "click_point_y": click_point_y, "release_point_x": release_point_x,
                  "release_point_y": release_point_y}

    return click_info


def plot_click_info(data, click_info):
    #     orbit
    fig = plt.figure(figsize=(18, 8))
    axes = fig.add_subplot(111)

    plt.scatter(data['op_x'], data['op_y'], c='green')

    #     click info
    plt.scatter(click_info["start_x_point"], click_info["start_y_point"], c='yellow')
    plt.scatter(click_info["click_point_x"], click_info["click_point_y"], c='red')
    plt.scatter(click_info["release_point_x"], click_info["release_point_y"], c='pink')

    title_name = "guess"
    if data.loc[0, 'Bot'] == 0:
        title_name = "human"
    elif data.loc[0, 'Bot'] == 1:
        title_name = "bot"
    else:
        title_name = "do not konw"
    # axes.set_title('orbit of data ', title_name)
    plt.title("orbit of data " + str(title_name))

    plt.show()


def eye(data):

    click_info = local_thunder(data)
    plot_click_info(data, click_info)