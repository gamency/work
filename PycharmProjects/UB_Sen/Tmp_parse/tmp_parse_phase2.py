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
import pandas as pd
import matplotlib.pyplot as plt


def parse_data(data_dic):
    #     data = data_dic['mouseEvents']
    init_time = data_dic["initialTimeStamp"]
    rightbutton_info = data_dic['slideBarLowerRight']
    leftbutton_info = data_dic['slideBarTopLeft']
    first_x = rightbutton_info['x']
    first_y = rightbutton_info['y']
    second_x = leftbutton_info['x']
    second_y = leftbutton_info['y']
    scenario = data_dic['scenario']
    terminal = data_dic['terminal']

    correct_x = data_dic['correctX']
    correct_y = data_dic['correctY']

    df = pd.DataFrame(data_dic['mouseEvents'])
    pox = list(df['point'])
    #     print(df.head())
    pox_x = []
    pox_y = []
    for item in pox:
        #         print(item['x'])
        pox_x.append(item['x'])
        pox_y.append(item['y'])
    df['op_x'] = pox_x
    df['op_y'] = pox_y
    df = df.drop('point', 1)
    df = df.rename(columns={'action': 'Action', 'timestamp': 'Time', 'eventType': 'event_type'})
    df['Time'] = df['Time'] + init_time
    df['correct_x'] = correct_x
    df['correct_y'] = correct_y
    df['slidebarright_x'] = first_x
    df['slidebarright_y'] = first_y
    df['slidebarleft_x'] = second_x
    df['slidebarleft_y'] = second_y
    df['scenario'] = scenario
    df['terminal'] = terminal
    df['Bot'] = 0
    return df


def visualization(data_dic):
    df = pd.DataFrame(data_dic['mouseEvents'])
    pox = list(df['point'])
    pox_x = []
    pox_y = []
    for item in pox:
#         print(item['x'])
        pox_x.append(item['x'])
        pox_y.append(item['y'])
    # p1 = plt.scatter(x[idx_1, 1], x[idx_1, 0], marker='x', color='m', label='1', s=30)
    plt.plot(pox_x, pox_y)
    # plt.scatter(pox_x, pox_y, marker = 'x')
    plt.show()


def save_file_to_csv(dataframe, save_file):
    dataframe.to_csv(save_file, index=None)


def main():
    dfte = {"answerPosition": {"curTime": 1522721801176, "point": {"x": 155, "y": 10}}, "correctX": 704, "correctY": 351,
     "initialTimeStamp": 1522721793729,
     "mouseEvents": [{"action": 0, "eventType": 1, "point": {"x": 693, "y": 422}, "timestamp": 2918},
                     {"action": 0, "eventType": 1, "point": {"x": 713, "y": 418}, "timestamp": 3001},
                     {"action": 0, "eventType": 1, "point": {"x": 713, "y": 418}, "timestamp": 3067},
                     {"action": 0, "eventType": 1, "point": {"x": 704, "y": 428}, "timestamp": 3135},
                     {"action": 0, "eventType": 1, "point": {"x": 703, "y": 430}, "timestamp": 3200},
                     {"action": 0, "eventType": 1, "point": {"x": 705, "y": 434}, "timestamp": 3384},
                     {"action": 0, "eventType": 1, "point": {"x": 701, "y": 444}, "timestamp": 3449},
                     {"action": 0, "eventType": 1, "point": {"x": 612, "y": 443}, "timestamp": 3512},
                     {"action": 0, "eventType": 1, "point": {"x": 578, "y": 431}, "timestamp": 3574},
                     {"action": 0, "eventType": 1, "point": {"x": 576, "y": 430}, "timestamp": 3634},
                     {"action": 0, "eventType": 1, "point": {"x": 577, "y": 430}, "timestamp": 3693},
                     {"action": 0, "eventType": 1, "point": {"x": 578, "y": 431}, "timestamp": 3754},
                     {"action": 0, "eventType": 1, "point": {"x": 578, "y": 435}, "timestamp": 3815},
                     {"action": 0, "eventType": 1, "point": {"x": 576, "y": 443}, "timestamp": 3878},
                     {"action": 12, "eventType": 1, "point": {"x": 576, "y": 442}, "timestamp": 3936},
                     {"action": 0, "eventType": 0, "point": {"x": 576, "y": 442}, "timestamp": 4221},
                     {"action": 0, "eventType": 2, "point": {"x": 576, "y": 442}, "timestamp": 4289},
                     {"action": 0, "eventType": 1, "point": {"x": 607, "y": 434}, "timestamp": 4546},
                     {"action": 0, "eventType": 1, "point": {"x": 607, "y": 434}, "timestamp": 4547},
                     {"action": 0, "eventType": 1, "point": {"x": 681, "y": 427}, "timestamp": 4613},
                     {"action": 0, "eventType": 1, "point": {"x": 681, "y": 427}, "timestamp": 4613},
                     {"action": 0, "eventType": 1, "point": {"x": 708, "y": 422}, "timestamp": 4681},
                     {"action": 0, "eventType": 1, "point": {"x": 708, "y": 422}, "timestamp": 4682},
                     {"action": 0, "eventType": 1, "point": {"x": 737, "y": 428}, "timestamp": 4979},
                     {"action": 0, "eventType": 1, "point": {"x": 737, "y": 428}, "timestamp": 4980},
                     {"action": 0, "eventType": 1, "point": {"x": 752, "y": 431}, "timestamp": 5041},
                     {"action": 0, "eventType": 1, "point": {"x": 752, "y": 431}, "timestamp": 5042},
                     {"action": 0, "eventType": 1, "point": {"x": 757, "y": 431}, "timestamp": 5102},
                     {"action": 0, "eventType": 1, "point": {"x": 757, "y": 431}, "timestamp": 5102},
                     {"action": 0, "eventType": 1, "point": {"x": 757, "y": 432}, "timestamp": 5222},
                     {"action": 0, "eventType": 1, "point": {"x": 757, "y": 432}, "timestamp": 5223},
                     {"action": 0, "eventType": 1, "point": {"x": 754, "y": 432}, "timestamp": 5285},
                     {"action": 0, "eventType": 1, "point": {"x": 754, "y": 432}, "timestamp": 5286},
                     {"action": 0, "eventType": 1, "point": {"x": 753, "y": 432}, "timestamp": 5348},
                     {"action": 0, "eventType": 1, "point": {"x": 753, "y": 432}, "timestamp": 5348},
                     {"action": 0, "eventType": 1, "point": {"x": 752, "y": 432}, "timestamp": 5411},
                     {"action": 0, "eventType": 1, "point": {"x": 752, "y": 432}, "timestamp": 5411},
                     {"action": 0, "eventType": 1, "point": {"x": 747, "y": 432}, "timestamp": 5477},
                     {"action": 0, "eventType": 1, "point": {"x": 747, "y": 432}, "timestamp": 5479},
                     {"action": 0, "eventType": 1, "point": {"x": 746, "y": 432}, "timestamp": 5536},
                     {"action": 0, "eventType": 1, "point": {"x": 746, "y": 432}, "timestamp": 5537},
                     {"action": 0, "eventType": 1, "point": {"x": 744, "y": 432}, "timestamp": 5599},
                     {"action": 0, "eventType": 1, "point": {"x": 744, "y": 432}, "timestamp": 5600},
                     {"action": 0, "eventType": 1, "point": {"x": 743, "y": 432}, "timestamp": 5720},
                     {"action": 0, "eventType": 1, "point": {"x": 743, "y": 432}, "timestamp": 5720},
                     {"action": 0, "eventType": 1, "point": {"x": 738, "y": 432}, "timestamp": 5782},
                     {"action": 0, "eventType": 1, "point": {"x": 738, "y": 432}, "timestamp": 5782},
                     {"action": 0, "eventType": 1, "point": {"x": 733, "y": 431}, "timestamp": 5844},
                     {"action": 0, "eventType": 1, "point": {"x": 733, "y": 431}, "timestamp": 5845},
                     {"action": 0, "eventType": 1, "point": {"x": 732, "y": 430}, "timestamp": 5904},
                     {"action": 0, "eventType": 1, "point": {"x": 732, "y": 430}, "timestamp": 5905},
                     {"action": 0, "eventType": 1, "point": {"x": 729, "y": 430}, "timestamp": 6202},
                     {"action": 0, "eventType": 1, "point": {"x": 729, "y": 430}, "timestamp": 6203},
                     {"action": 0, "eventType": 1, "point": {"x": 728, "y": 430}, "timestamp": 6262},
                     {"action": 0, "eventType": 1, "point": {"x": 728, "y": 430}, "timestamp": 6263},
                     {"action": 0, "eventType": 1, "point": {"x": 726, "y": 430}, "timestamp": 6387},
                     {"action": 0, "eventType": 1, "point": {"x": 726, "y": 430}, "timestamp": 6388},
                     {"action": 0, "eventType": 1, "point": {"x": 724, "y": 430}, "timestamp": 6448},
                     {"action": 0, "eventType": 1, "point": {"x": 724, "y": 430}, "timestamp": 6448},
                     {"action": 0, "eventType": 1, "point": {"x": 723, "y": 430}, "timestamp": 6507},
                     {"action": 0, "eventType": 1, "point": {"x": 723, "y": 430}, "timestamp": 6508},
                     {"action": 0, "eventType": 1, "point": {"x": 722, "y": 430}, "timestamp": 6568},
                     {"action": 0, "eventType": 1, "point": {"x": 722, "y": 430}, "timestamp": 6568},
                     {"action": 13, "eventType": 3, "point": {"x": 722, "y": 430}, "timestamp": 7219},
                     {"action": 0, "eventType": 0, "point": {"x": 722, "y": 430}, "timestamp": 7447}], "scenario": 1,
     "slideBarLowerRight": {"x": 591, "y": 462}, "slideBarTopLeft": {"x": 549, "y": 422},
     "slideButtonClickPoint": {"x": 576, "y": 442}, "terminal": 0}

    visualization(dfte)

    # base_dir = "/Users/kite/Desktop/"
    save_base_dir = "/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/SecondBig/"

    dfparse = parse_data(dfte)
    save_file = save_base_dir + "ff738d" + "23" + ".csv"
    save_file_to_csv(dfparse, save_file)
    # file = open(base_dir + "abcslide.txt")
    # index = 0
    # for line in file:
    #     print(index)
    #     line = eval(line)
    #     dfparse = parse_data(line)
    #     print(dfparse)
    #
    #
    #     save_file = save_base_dir + "selinum_bot_" + str(index) + ".csv"
    #     save_file_to_csv(dfparse, save_file)
    #     index += 1


if __name__ == '__main__':
    main()
