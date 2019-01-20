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
    dfte = {"answerPosition": {"curTime": 1524626821299, "point": {"x": 141, "y": 10}}, "correctX": 581, "correctY": 824,
     "initialTimeStamp": 1524626309030,
     "mouseEvents": [{"action": 12, "eventType": 1, "point": {"x": 438, "y": 1070}, "timestamp": 500108},
                     {"action": 0, "eventType": 0, "point": {"x": 438, "y": 1070}, "timestamp": 500428},
                     {"action": 0, "eventType": 1, "point": {"x": 379, "y": 1070}, "timestamp": 500791},
                     {"action": 0, "eventType": 1, "point": {"x": 327, "y": 1067}, "timestamp": 500807},
                     {"action": 0, "eventType": 1, "point": {"x": 270, "y": 1050}, "timestamp": 500824},
                     {"action": 0, "eventType": 1, "point": {"x": 217, "y": 1026}, "timestamp": 500840},
                     {"action": 0, "eventType": 1, "point": {"x": 126, "y": 967}, "timestamp": 500857},
                     {"action": 0, "eventType": 1, "point": {"x": 84, "y": 921}, "timestamp": 500873},
                     {"action": 0, "eventType": 1, "point": {"x": 77, "y": 909}, "timestamp": 500890},
                     {"action": 0, "eventType": 1, "point": {"x": 76, "y": 909}, "timestamp": 501024},
                     {"action": 0, "eventType": 1, "point": {"x": 65, "y": 908}, "timestamp": 501042},
                     {"action": 0, "eventType": 1, "point": {"x": 53, "y": 899}, "timestamp": 501057},
                     {"action": 0, "eventType": 1, "point": {"x": 39, "y": 886}, "timestamp": 501074},
                     {"action": 0, "eventType": 1, "point": {"x": 28, "y": 872}, "timestamp": 501090},
                     {"action": 0, "eventType": 1, "point": {"x": 17, "y": 857}, "timestamp": 501107},
                     {"action": 0, "eventType": 1, "point": {"x": 8, "y": 840}, "timestamp": 501125},
                     {"action": 0, "eventType": 1, "point": {"x": 2, "y": 827}, "timestamp": 501141},
                     {"action": 12, "eventType": 1, "point": {"x": 0, "y": 821}, "timestamp": 501158},
                     {"action": 0, "eventType": 0, "point": {"x": 0, "y": 821}, "timestamp": 501428},
                     {"action": 12, "eventType": 1, "point": {"x": 8, "y": 798}, "timestamp": 503809},
                     {"action": 0, "eventType": 0, "point": {"x": 8, "y": 798}, "timestamp": 504029},
                     {"action": 12, "eventType": 1, "point": {"x": 45, "y": 726}, "timestamp": 510044},
                     {"action": 0, "eventType": 0, "point": {"x": 45, "y": 726}, "timestamp": 510429},
                     {"action": 12, "eventType": 1, "point": {"x": 461, "y": 912}, "timestamp": 510858},
                     {"action": 0, "eventType": 2, "point": {"x": 461, "y": 912}, "timestamp": 510866},
                     {"action": 0, "eventType": 1, "point": {"x": 463, "y": 913}, "timestamp": 510876},
                     {"action": 0, "eventType": 1, "point": {"x": 463, "y": 913}, "timestamp": 510877},
                     {"action": 0, "eventType": 1, "point": {"x": 466, "y": 914}, "timestamp": 510892},
                     {"action": 0, "eventType": 1, "point": {"x": 466, "y": 914}, "timestamp": 510892},
                     {"action": 0, "eventType": 1, "point": {"x": 469, "y": 915}, "timestamp": 510909},
                     {"action": 0, "eventType": 1, "point": {"x": 469, "y": 915}, "timestamp": 510910},
                     {"action": 0, "eventType": 1, "point": {"x": 472, "y": 916}, "timestamp": 510925},
                     {"action": 0, "eventType": 1, "point": {"x": 472, "y": 916}, "timestamp": 510926},
                     {"action": 0, "eventType": 1, "point": {"x": 476, "y": 917}, "timestamp": 510943},
                     {"action": 0, "eventType": 1, "point": {"x": 476, "y": 917}, "timestamp": 510944},
                     {"action": 0, "eventType": 1, "point": {"x": 478, "y": 918}, "timestamp": 510959},
                     {"action": 0, "eventType": 1, "point": {"x": 478, "y": 918}, "timestamp": 510959},
                     {"action": 0, "eventType": 1, "point": {"x": 482, "y": 919}, "timestamp": 510976},
                     {"action": 0, "eventType": 1, "point": {"x": 482, "y": 919}, "timestamp": 510977},
                     {"action": 0, "eventType": 1, "point": {"x": 487, "y": 920}, "timestamp": 510993},
                     {"action": 0, "eventType": 1, "point": {"x": 487, "y": 920}, "timestamp": 510994},
                     {"action": 0, "eventType": 1, "point": {"x": 488, "y": 921}, "timestamp": 511008},
                     {"action": 0, "eventType": 1, "point": {"x": 488, "y": 921}, "timestamp": 511010},
                     {"action": 0, "eventType": 1, "point": {"x": 493, "y": 922}, "timestamp": 511026},
                     {"action": 0, "eventType": 1, "point": {"x": 493, "y": 922}, "timestamp": 511027},
                     {"action": 0, "eventType": 1, "point": {"x": 496, "y": 923}, "timestamp": 511043},
                     {"action": 0, "eventType": 1, "point": {"x": 496, "y": 923}, "timestamp": 511044},
                     {"action": 0, "eventType": 1, "point": {"x": 497, "y": 924}, "timestamp": 511061},
                     {"action": 0, "eventType": 1, "point": {"x": 497, "y": 924}, "timestamp": 511064},
                     {"action": 0, "eventType": 1, "point": {"x": 498, "y": 925}, "timestamp": 511126},
                     {"action": 0, "eventType": 1, "point": {"x": 498, "y": 925}, "timestamp": 511126},
                     {"action": 0, "eventType": 1, "point": {"x": 500, "y": 926}, "timestamp": 511142},
                     {"action": 0, "eventType": 1, "point": {"x": 500, "y": 926}, "timestamp": 511142},
                     {"action": 0, "eventType": 1, "point": {"x": 505, "y": 927}, "timestamp": 511160},
                     {"action": 0, "eventType": 1, "point": {"x": 505, "y": 927}, "timestamp": 511162},
                     {"action": 0, "eventType": 1, "point": {"x": 510, "y": 928}, "timestamp": 511296},
                     {"action": 0, "eventType": 1, "point": {"x": 510, "y": 928}, "timestamp": 511296},
                     {"action": 0, "eventType": 1, "point": {"x": 512, "y": 929}, "timestamp": 511410},
                     {"action": 0, "eventType": 1, "point": {"x": 512, "y": 929}, "timestamp": 511411},
                     {"action": 0, "eventType": 1, "point": {"x": 516, "y": 930}, "timestamp": 511425},
                     {"action": 0, "eventType": 1, "point": {"x": 516, "y": 930}, "timestamp": 511425},
                     {"action": 0, "eventType": 1, "point": {"x": 519, "y": 931}, "timestamp": 511457},
                     {"action": 0, "eventType": 1, "point": {"x": 519, "y": 931}, "timestamp": 511467},
                     {"action": 0, "eventType": 1, "point": {"x": 522, "y": 932}, "timestamp": 511494},
                     {"action": 0, "eventType": 1, "point": {"x": 522, "y": 932}, "timestamp": 511495},
                     {"action": 0, "eventType": 1, "point": {"x": 525, "y": 933}, "timestamp": 511542},
                     {"action": 0, "eventType": 1, "point": {"x": 525, "y": 933}, "timestamp": 511543},
                     {"action": 0, "eventType": 1, "point": {"x": 527, "y": 934}, "timestamp": 511558},
                     {"action": 0, "eventType": 1, "point": {"x": 527, "y": 934}, "timestamp": 511559},
                     {"action": 0, "eventType": 1, "point": {"x": 531, "y": 935}, "timestamp": 511577},
                     {"action": 0, "eventType": 1, "point": {"x": 531, "y": 935}, "timestamp": 511578},
                     {"action": 0, "eventType": 1, "point": {"x": 532, "y": 936}, "timestamp": 511592},
                     {"action": 0, "eventType": 1, "point": {"x": 532, "y": 936}, "timestamp": 511592},
                     {"action": 0, "eventType": 1, "point": {"x": 534, "y": 937}, "timestamp": 511608},
                     {"action": 0, "eventType": 1, "point": {"x": 534, "y": 937}, "timestamp": 511609},
                     {"action": 0, "eventType": 1, "point": {"x": 535, "y": 938}, "timestamp": 511625},
                     {"action": 0, "eventType": 1, "point": {"x": 535, "y": 938}, "timestamp": 511625},
                     {"action": 0, "eventType": 1, "point": {"x": 537, "y": 939}, "timestamp": 511642},
                     {"action": 0, "eventType": 1, "point": {"x": 537, "y": 939}, "timestamp": 511643},
                     {"action": 0, "eventType": 1, "point": {"x": 541, "y": 940}, "timestamp": 511658},
                     {"action": 0, "eventType": 1, "point": {"x": 541, "y": 940}, "timestamp": 511659},
                     {"action": 0, "eventType": 1, "point": {"x": 546, "y": 941}, "timestamp": 511675},
                     {"action": 0, "eventType": 1, "point": {"x": 546, "y": 941}, "timestamp": 511676},
                     {"action": 0, "eventType": 1, "point": {"x": 547, "y": 942}, "timestamp": 511692},
                     {"action": 0, "eventType": 1, "point": {"x": 547, "y": 942}, "timestamp": 511693},
                     {"action": 0, "eventType": 1, "point": {"x": 548, "y": 943}, "timestamp": 511708},
                     {"action": 0, "eventType": 1, "point": {"x": 548, "y": 943}, "timestamp": 511709},
                     {"action": 0, "eventType": 1, "point": {"x": 553, "y": 944}, "timestamp": 511726},
                     {"action": 0, "eventType": 1, "point": {"x": 553, "y": 944}, "timestamp": 511727},
                     {"action": 0, "eventType": 1, "point": {"x": 557, "y": 945}, "timestamp": 511742},
                     {"action": 0, "eventType": 1, "point": {"x": 557, "y": 945}, "timestamp": 511743},
                     {"action": 0, "eventType": 1, "point": {"x": 560, "y": 946}, "timestamp": 511758},
                     {"action": 0, "eventType": 1, "point": {"x": 560, "y": 946}, "timestamp": 511759},
                     {"action": 0, "eventType": 1, "point": {"x": 563, "y": 947}, "timestamp": 511776},
                     {"action": 0, "eventType": 1, "point": {"x": 563, "y": 947}, "timestamp": 511776},
                     {"action": 0, "eventType": 1, "point": {"x": 564, "y": 948}, "timestamp": 511792},
                     {"action": 0, "eventType": 1, "point": {"x": 564, "y": 948}, "timestamp": 511794},
                     {"action": 0, "eventType": 1, "point": {"x": 567, "y": 949}, "timestamp": 511809},
                     {"action": 0, "eventType": 1, "point": {"x": 567, "y": 949}, "timestamp": 511809},
                     {"action": 0, "eventType": 1, "point": {"x": 571, "y": 950}, "timestamp": 511825},
                     {"action": 0, "eventType": 1, "point": {"x": 571, "y": 950}, "timestamp": 511827},
                     {"action": 0, "eventType": 1, "point": {"x": 572, "y": 951}, "timestamp": 511843},
                     {"action": 0, "eventType": 1, "point": {"x": 572, "y": 951}, "timestamp": 511844},
                     {"action": 0, "eventType": 1, "point": {"x": 574, "y": 952}, "timestamp": 511859},
                     {"action": 0, "eventType": 1, "point": {"x": 574, "y": 952}, "timestamp": 511859},
                     {"action": 0, "eventType": 1, "point": {"x": 578, "y": 953}, "timestamp": 511876},
                     {"action": 0, "eventType": 1, "point": {"x": 578, "y": 953}, "timestamp": 511876},
                     {"action": 0, "eventType": 1, "point": {"x": 579, "y": 954}, "timestamp": 511892},
                     {"action": 0, "eventType": 1, "point": {"x": 579, "y": 954}, "timestamp": 511893},
                     {"action": 0, "eventType": 1, "point": {"x": 580, "y": 955}, "timestamp": 511910},
                     {"action": 0, "eventType": 1, "point": {"x": 580, "y": 955}, "timestamp": 511911},
                     {"action": 0, "eventType": 1, "point": {"x": 581, "y": 956}, "timestamp": 511926},
                     {"action": 0, "eventType": 1, "point": {"x": 581, "y": 956}, "timestamp": 511927},
                     {"action": 0, "eventType": 1, "point": {"x": 584, "y": 957}, "timestamp": 511943},
                     {"action": 0, "eventType": 1, "point": {"x": 584, "y": 957}, "timestamp": 511944},
                     {"action": 0, "eventType": 1, "point": {"x": 587, "y": 958}, "timestamp": 511960},
                     {"action": 0, "eventType": 1, "point": {"x": 587, "y": 958}, "timestamp": 511961},
                     {"action": 0, "eventType": 1, "point": {"x": 589, "y": 959}, "timestamp": 511975},
                     {"action": 0, "eventType": 1, "point": {"x": 589, "y": 959}, "timestamp": 511977},
                     {"action": 0, "eventType": 1, "point": {"x": 591, "y": 960}, "timestamp": 511992},
                     {"action": 0, "eventType": 1, "point": {"x": 591, "y": 960}, "timestamp": 511993},
                     {"action": 0, "eventType": 1, "point": {"x": 593, "y": 961}, "timestamp": 512009},
                     {"action": 0, "eventType": 1, "point": {"x": 593, "y": 961}, "timestamp": 512009},
                     {"action": 0, "eventType": 1, "point": {"x": 597, "y": 962}, "timestamp": 512025},
                     {"action": 0, "eventType": 1, "point": {"x": 597, "y": 962}, "timestamp": 512025},
                     {"action": 0, "eventType": 1, "point": {"x": 600, "y": 963}, "timestamp": 512043},
                     {"action": 0, "eventType": 1, "point": {"x": 600, "y": 963}, "timestamp": 512043},
                     {"action": 0, "eventType": 1, "point": {"x": 599, "y": 964}, "timestamp": 512059},
                     {"action": 0, "eventType": 1, "point": {"x": 599, "y": 964}, "timestamp": 512060},
                     {"action": 13, "eventType": 3, "point": {"x": 599, "y": 964}, "timestamp": 512067}], "scenario": 1,
     "slideBarLowerRight": {"x": 482, "y": 932}, "slideBarTopLeft": {"x": 440, "y": 892},
     "slideButtonClickPoint": {"x": 461, "y": 912}, "terminal": 0}

    visualization(dfte)

    # base_dir = "/Users/kite/Desktop/"
    # save_base_dir = "/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/"
    #
    # file = open(base_dir + "abcslide.txt")
    # base_dir = "/Users/kite/Desktop/"
    dfparse = parse_data(dfte)
    save_base_dir = "/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/"

    save_file = save_base_dir + "wrong_decision_201804251155" + ".csv"
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
