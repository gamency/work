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
plt.style.use('ggplot')


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
    dfte = {"answerPosition": {"curTime": 1532508439006, "point": {"x": 182, "y": 10}}, "correctX": 197, "correctY": 168,
     "initialTimeStamp": 1532508222735,
     "mouseEvents": [{"action": 0, "eventType": 2, "point": {"x": 39, "y": 259}, "timestamp": 212942},
                     {"action": 0, "eventType": 1, "point": {"x": 54, "y": 260}, "timestamp": 213135},
                     {"action": 0, "eventType": 1, "point": {"x": 64, "y": 261}, "timestamp": 213209},
                     {"action": 0, "eventType": 1, "point": {"x": 64, "y": 261}, "timestamp": 213219},
                     {"action": 0, "eventType": 1, "point": {"x": 69, "y": 262}, "timestamp": 213243},
                     {"action": 0, "eventType": 1, "point": {"x": 73, "y": 263}, "timestamp": 213285},
                     {"action": 0, "eventType": 1, "point": {"x": 81, "y": 263}, "timestamp": 213350},
                     {"action": 0, "eventType": 1, "point": {"x": 87, "y": 263}, "timestamp": 213402},
                     {"action": 0, "eventType": 1, "point": {"x": 89, "y": 264}, "timestamp": 213430},
                     {"action": 0, "eventType": 1, "point": {"x": 91, "y": 264}, "timestamp": 213456},
                     {"action": 0, "eventType": 1, "point": {"x": 99, "y": 264}, "timestamp": 213500},
                     {"action": 0, "eventType": 1, "point": {"x": 110, "y": 265}, "timestamp": 213548},
                     {"action": 0, "eventType": 1, "point": {"x": 117, "y": 265}, "timestamp": 213586},
                     {"action": 0, "eventType": 1, "point": {"x": 121, "y": 265}, "timestamp": 213620},
                     {"action": 0, "eventType": 1, "point": {"x": 131, "y": 266}, "timestamp": 213655},
                     {"action": 0, "eventType": 1, "point": {"x": 140, "y": 266}, "timestamp": 213703},
                     {"action": 0, "eventType": 1, "point": {"x": 143, "y": 266}, "timestamp": 213740},
                     {"action": 0, "eventType": 1, "point": {"x": 147, "y": 266}, "timestamp": 213794},
                     {"action": 0, "eventType": 1, "point": {"x": 151, "y": 266}, "timestamp": 213817},
                     {"action": 0, "eventType": 1, "point": {"x": 154, "y": 267}, "timestamp": 213865},
                     {"action": 0, "eventType": 1, "point": {"x": 161, "y": 267}, "timestamp": 213920},
                     {"action": 0, "eventType": 1, "point": {"x": 163, "y": 267}, "timestamp": 213953},
                     {"action": 0, "eventType": 1, "point": {"x": 164, "y": 267}, "timestamp": 213971},
                     {"action": 0, "eventType": 1, "point": {"x": 170, "y": 267}, "timestamp": 214015},
                     {"action": 0, "eventType": 1, "point": {"x": 173, "y": 267}, "timestamp": 214067},
                     {"action": 0, "eventType": 1, "point": {"x": 177, "y": 267}, "timestamp": 214113},
                     {"action": 0, "eventType": 1, "point": {"x": 179, "y": 267}, "timestamp": 214133},
                     {"action": 0, "eventType": 1, "point": {"x": 182, "y": 267}, "timestamp": 214195},
                     {"action": 0, "eventType": 1, "point": {"x": 183, "y": 267}, "timestamp": 214218},
                     {"action": 0, "eventType": 1, "point": {"x": 187, "y": 267}, "timestamp": 214271},
                     {"action": 0, "eventType": 1, "point": {"x": 188, "y": 267}, "timestamp": 214323},
                     {"action": 0, "eventType": 1, "point": {"x": 190, "y": 267}, "timestamp": 214362},
                     {"action": 0, "eventType": 1, "point": {"x": 192, "y": 267}, "timestamp": 214402},
                     {"action": 0, "eventType": 1, "point": {"x": 192, "y": 267}, "timestamp": 214442},
                     {"action": 0, "eventType": 1, "point": {"x": 193, "y": 267}, "timestamp": 214484},
                     {"action": 0, "eventType": 1, "point": {"x": 194, "y": 267}, "timestamp": 214518},
                     {"action": 0, "eventType": 1, "point": {"x": 195, "y": 267}, "timestamp": 214567},
                     {"action": 0, "eventType": 1, "point": {"x": 197, "y": 267}, "timestamp": 214660},
                     {"action": 0, "eventType": 1, "point": {"x": 197, "y": 267}, "timestamp": 214688},
                     {"action": 0, "eventType": 1, "point": {"x": 198, "y": 267}, "timestamp": 214714},
                     {"action": 0, "eventType": 1, "point": {"x": 199, "y": 267}, "timestamp": 214777},
                     {"action": 0, "eventType": 1, "point": {"x": 200, "y": 267}, "timestamp": 214819},
                     {"action": 0, "eventType": 1, "point": {"x": 201, "y": 267}, "timestamp": 214840},
                     {"action": 0, "eventType": 1, "point": {"x": 203, "y": 267}, "timestamp": 214901},
                     {"action": 0, "eventType": 1, "point": {"x": 203, "y": 267}, "timestamp": 214925},
                     {"action": 0, "eventType": 1, "point": {"x": 205, "y": 267}, "timestamp": 214979},
                     {"action": 0, "eventType": 1, "point": {"x": 205, "y": 267}, "timestamp": 215023},
                     {"action": 0, "eventType": 1, "point": {"x": 207, "y": 266}, "timestamp": 215063},
                     {"action": 0, "eventType": 1, "point": {"x": 208, "y": 266}, "timestamp": 215127},
                     {"action": 0, "eventType": 1, "point": {"x": 209, "y": 266}, "timestamp": 215168},
                     {"action": 0, "eventType": 1, "point": {"x": 209, "y": 266}, "timestamp": 215198},
                     {"action": 0, "eventType": 1, "point": {"x": 210, "y": 266}, "timestamp": 215219},
                     {"action": 0, "eventType": 1, "point": {"x": 211, "y": 266}, "timestamp": 215296},
                     {"action": 0, "eventType": 1, "point": {"x": 212, "y": 266}, "timestamp": 215333},
                     {"action": 0, "eventType": 1, "point": {"x": 213, "y": 266}, "timestamp": 215386},
                     {"action": 0, "eventType": 1, "point": {"x": 213, "y": 266}, "timestamp": 215418},
                     {"action": 0, "eventType": 1, "point": {"x": 214, "y": 266}, "timestamp": 215452},
                     {"action": 0, "eventType": 1, "point": {"x": 215, "y": 265}, "timestamp": 215520},
                     {"action": 0, "eventType": 1, "point": {"x": 216, "y": 265}, "timestamp": 215555},
                     {"action": 0, "eventType": 1, "point": {"x": 217, "y": 265}, "timestamp": 215614},
                     {"action": 0, "eventType": 1, "point": {"x": 218, "y": 265}, "timestamp": 215713},
                     {"action": 0, "eventType": 1, "point": {"x": 218, "y": 265}, "timestamp": 216010},
                     {"action": 13, "eventType": 3, "point": {"x": 218, "y": 265}, "timestamp": 216013}], "scenario": 1,
     "sensorInfos": [{"pressureTime": 920, "pressureValue": 0.43921572},
                     {"pressureTime": 976, "pressureValue": 0.43921572},
                     {"pressureTime": 994, "pressureValue": 0.43921572},
                     {"pressureTime": 1017, "pressureValue": 0.43921572},
                     {"pressureTime": 1072, "pressureValue": 0.43921572},
                     {"pressureTime": 1119, "pressureValue": 0.43921572},
                     {"pressureTime": 1165, "pressureValue": 0.43921572},
                     {"pressureTime": 1188, "pressureValue": 0.43921572},
                     {"pressureTime": 1248, "pressureValue": 0.43921572},
                     {"pressureTime": 1259, "pressureValue": 0.43921572},
                     {"pressureTime": 1327, "pressureValue": 0.43921572},
                     {"pressureTime": 1375, "pressureValue": 0.43921572},
                     {"pressureTime": 1416, "pressureValue": 0.43921572},
                     {"pressureTime": 1461, "pressureValue": 0.43921572},
                     {"pressureTime": 1495, "pressureValue": 0.43921572},
                     {"pressureTime": 1538, "pressureValue": 0.43921572},
                     {"pressureTime": 1575, "pressureValue": 0.43921572},
                     {"pressureTime": 1624, "pressureValue": 0.43921572},
                     {"pressureTime": 1717, "pressureValue": 0.43921572},
                     {"pressureTime": 1737, "pressureValue": 0.43921572},
                     {"pressureTime": 1769, "pressureValue": 0.43921572},
                     {"pressureTime": 1833, "pressureValue": 0.43921572},
                     {"pressureTime": 1873, "pressureValue": 0.43921572},
                     {"pressureTime": 1895, "pressureValue": 0.43921572},
                     {"pressureTime": 1957, "pressureValue": 0.43921572},
                     {"pressureTime": 1979, "pressureValue": 0.43921572},
                     {"pressureTime": 2036, "pressureValue": 0.43921572},
                     {"pressureTime": 2074, "pressureValue": 0.43921572},
                     {"pressureTime": 2117, "pressureValue": 0.43921572},
                     {"pressureTime": 2184, "pressureValue": 0.43921572},
                     {"pressureTime": 2218, "pressureValue": 0.43921572},
                     {"pressureTime": 2243, "pressureValue": 0.43921572},
                     {"pressureTime": 2275, "pressureValue": 0.43921572},
                     {"pressureTime": 2348, "pressureValue": 0.43921572},
                     {"pressureTime": 2384, "pressureValue": 0.43921572},
                     {"pressureTime": 2443, "pressureValue": 0.43921572},
                     {"pressureTime": 2472, "pressureValue": 0.43921572}], "slideBarLowerRight": {"x": 57, "y": 279},
     "slideBarTopLeft": {"x": 15, "y": 239}, "slideButtonClickPoint": {"x": 39, "y": 259}, "terminal": 1}

    visualization(dfte)

    # base_dir = "/Users/kite/Desktop/"
    # save_base_dir = "/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/"
    #
    # file = open(base_dir + "abcslide.txt")
    # base_dir = "/Users/kite/Desktop/"
    dfparse = parse_data(dfte)
    save_base_dir = "/Users/kite/Desktop/Mobile_verify/Data/trainData/H5/"

    save_file = save_base_dir + "andriod_wrong_decision_201806281046" + ".csv"
    save_file_to_csv(dfparse, save_file)
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
