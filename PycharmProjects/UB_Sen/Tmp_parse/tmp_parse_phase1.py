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
    df['Bot'] = 1
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
    dfte = {"buttonClickPoint":{"x":601,"y":408},"buttonLowerRight":{"x":782,"y":431},"buttonTopLeft":{"x":493,"y":389},
            "initialTimeStamp":1521103533802,
            "mouseEvents":[{"action":0,"eventType":1,"point":{"x":596,"y":393},"timestamp":8},
                           {"action":0,"eventType":1,"point":{"x":597,"y":396},"timestamp":13},
                           {"action":0,"eventType":1,"point":{"x":599,"y":405},"timestamp":40},
                           {"action":0,"eventType":1,"point":{"x":601,"y":407},"timestamp":73},
                           {"action":12,"eventType":1,"point":{"x":601,"y":408},"timestamp":89},
                           {"action":0,"eventType":2,"point":{"x":601,"y":408},"timestamp":305},
                           {"action":10,"eventType":3,"point":{"x":601,"y":408},"timestamp":309}],
            "scenario":0,"terminal":0}
    dfparse = parse_data(dfte)
    print(dfparse)
    visualization(dfte)

    # base_dir = "/Users/kite/Desktop/"
    save_base_dir = "/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/"

    save_file = save_base_dir + "wrong_decision_0" + ".csv"
    save_file_to_csv(dfparse, save_file)


if __name__ == '__main__':
    main()
