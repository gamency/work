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
    rightbutton_info = data_dic['buttonLowerRight']
    leftbutton_info = data_dic['buttonTopLeft']
    first_x = rightbutton_info['x']
    first_y = rightbutton_info['y']
    second_x = leftbutton_info['x']
    second_y = leftbutton_info['y']
    scenario = data_dic['scenario']
    terminal = data_dic['terminal']

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
    df = df.rename(columns={'action': 'Action', 'timestamp': 'Time', 'eventType': 'mouse_event_type'})
    df['Time'] = df['Time'] + init_time
    df['first_x'] = first_x
    df['first_y'] = first_y
    df['second_x'] = second_x
    df['second_y'] = second_y
    df['scenario'] = scenario
    df['terminal'] = terminal
    df['Bot'] = 0.0825
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
    # plt.plot(pox_x, pox_y)
    plt.scatter(pox_x, pox_y, marker = 'x')
    plt.show()


def save_file_to_csv(dataframe, save_file):
    dataframe.to_csv(save_file, index=None)


def main():
    dfte = {"buttonClickPoint": {"x": 704, "y": 396}, "buttonLowerRight": {"x": 865, "y": 432},
     "buttonTopLeft": {"x": 576, "y": 386}, "initialTimeStamp": 1525965579904,
     "mouseEvents": [{"action": 0, "eventType": 1, "point": {"x": 546, "y": 196}, "timestamp": 923},
                     {"action": 0, "eventType": 1, "point": {"x": 559, "y": 223}, "timestamp": 934},
                     {"action": 0, "eventType": 1, "point": {"x": 561, "y": 229}, "timestamp": 943},
                     {"action": 0, "eventType": 1, "point": {"x": 563, "y": 234}, "timestamp": 954},
                     {"action": 0, "eventType": 1, "point": {"x": 569, "y": 255}, "timestamp": 971},
                     {"action": 0, "eventType": 1, "point": {"x": 568, "y": 258}, "timestamp": 988},
                     {"action": 0, "eventType": 1, "point": {"x": 564, "y": 258}, "timestamp": 1007},
                     {"action": 0, "eventType": 1, "point": {"x": 569, "y": 260}, "timestamp": 1115},
                     {"action": 0, "eventType": 1, "point": {"x": 575, "y": 265}, "timestamp": 1123},
                     {"action": 0, "eventType": 1, "point": {"x": 583, "y": 273}, "timestamp": 1137},
                     {"action": 0, "eventType": 1, "point": {"x": 600, "y": 291}, "timestamp": 1155},
                     {"action": 0, "eventType": 1, "point": {"x": 627, "y": 316}, "timestamp": 1171},
                     {"action": 0, "eventType": 1, "point": {"x": 658, "y": 340}, "timestamp": 1187},
                     {"action": 0, "eventType": 1, "point": {"x": 670, "y": 348}, "timestamp": 1203},
                     {"action": 0, "eventType": 1, "point": {"x": 680, "y": 353}, "timestamp": 1221},
                     {"action": 0, "eventType": 1, "point": {"x": 681, "y": 353}, "timestamp": 1237},
                     {"action": 0, "eventType": 1, "point": {"x": 684, "y": 353}, "timestamp": 1387},
                     {"action": 0, "eventType": 1, "point": {"x": 690, "y": 353}, "timestamp": 1403},
                     {"action": 0, "eventType": 1, "point": {"x": 694, "y": 355}, "timestamp": 1421},
                     {"action": 0, "eventType": 1, "point": {"x": 698, "y": 357}, "timestamp": 1438},
                     {"action": 0, "eventType": 1, "point": {"x": 700, "y": 359}, "timestamp": 1453},
                     {"action": 0, "eventType": 1, "point": {"x": 703, "y": 364}, "timestamp": 1470},
                     {"action": 0, "eventType": 1, "point": {"x": 704, "y": 368}, "timestamp": 1487},
                     {"action": 0, "eventType": 1, "point": {"x": 704, "y": 373}, "timestamp": 1504},
                     {"action": 0, "eventType": 1, "point": {"x": 704, "y": 378}, "timestamp": 1522},
                     {"action": 0, "eventType": 1, "point": {"x": 704, "y": 382}, "timestamp": 1538},
                     {"action": 0, "eventType": 1, "point": {"x": 704, "y": 385}, "timestamp": 1555},
                     {"action": 0, "eventType": 1, "point": {"x": 704, "y": 387}, "timestamp": 1571},
                     {"action": 0, "eventType": 1, "point": {"x": 704, "y": 389}, "timestamp": 1587},
                     {"action": 0, "eventType": 1, "point": {"x": 704, "y": 390}, "timestamp": 1604},
                     {"action": 0, "eventType": 1, "point": {"x": 704, "y": 393}, "timestamp": 1621},
                     {"action": 0, "eventType": 1, "point": {"x": 704, "y": 395}, "timestamp": 1638},
                     {"action": 12, "eventType": 1, "point": {"x": 704, "y": 396}, "timestamp": 1654},
                     {"action": 0, "eventType": 2, "point": {"x": 704, "y": 396}, "timestamp": 1825},
                     {"action": 10, "eventType": 3, "point": {"x": 704, "y": 396}, "timestamp": 1826}], "scenario": 0,
     "terminal": 0}

    dfparse = parse_data(dfte)
    print(dfparse)
    visualization(dfte)

    # base_dir = "/Users/kite/Desktop/"
    save_base_dir = "/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/"

    save_file = save_base_dir + "good_decision_201805110143" + ".csv"
    save_file_to_csv(dfparse, save_file)


if __name__ == '__main__':
    main()
