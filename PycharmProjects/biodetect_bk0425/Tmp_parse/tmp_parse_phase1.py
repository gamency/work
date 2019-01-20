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
    dfte = {"buttonClickPoint": {"x": 893, "y": 425}, "buttonLowerRight": {"x": 1105, "y": 452},
     "buttonTopLeft": {"x": 816, "y": 406}, "initialTimeStamp": 1524215059404,
     "keyboardEvents": [{"dialogEventType": 0, "eventType": 6, "timestamp": 9486},
                        {"dialogEventType": 0, "eventType": 6, "timestamp": 9678},
                        {"dialogEventType": 0, "eventType": 7, "timestamp": 9762},
                        {"dialogEventType": 0, "eventType": 7, "timestamp": 9874}],
     "mouseEvents": [{"action": 0, "eventType": 1, "point": {"x": 465, "y": 918}, "timestamp": 8},
                     {"action": 0, "eventType": 1, "point": {"x": 450, "y": 927}, "timestamp": 20},
                     {"action": 12, "eventType": 1, "point": {"x": 442, "y": 931}, "timestamp": 108},
                     {"action": 0, "eventType": 0, "point": {"x": 442, "y": 931}, "timestamp": 410},
                     {"action": 0, "eventType": 1, "point": {"x": 403, "y": 850}, "timestamp": 1100},
                     {"action": 0, "eventType": 1, "point": {"x": 414, "y": 842}, "timestamp": 1128},
                     {"action": 0, "eventType": 1, "point": {"x": 439, "y": 826}, "timestamp": 1144},
                     {"action": 0, "eventType": 1, "point": {"x": 594, "y": 728}, "timestamp": 1174},
                     {"action": 0, "eventType": 1, "point": {"x": 649, "y": 698}, "timestamp": 1178},
                     {"action": 0, "eventType": 1, "point": {"x": 768, "y": 639}, "timestamp": 1194},
                     {"action": 0, "eventType": 1, "point": {"x": 881, "y": 592}, "timestamp": 1210},
                     {"action": 0, "eventType": 1, "point": {"x": 962, "y": 557}, "timestamp": 1228},
                     {"action": 0, "eventType": 1, "point": {"x": 1029, "y": 536}, "timestamp": 1244},
                     {"action": 0, "eventType": 1, "point": {"x": 1048, "y": 530}, "timestamp": 1260},
                     {"action": 0, "eventType": 1, "point": {"x": 1052, "y": 527}, "timestamp": 1278},
                     {"action": 0, "eventType": 1, "point": {"x": 1053, "y": 527}, "timestamp": 1294},
                     {"action": 0, "eventType": 1, "point": {"x": 1058, "y": 529}, "timestamp": 1544},
                     {"action": 0, "eventType": 1, "point": {"x": 1071, "y": 539}, "timestamp": 1560},
                     {"action": 0, "eventType": 1, "point": {"x": 1080, "y": 557}, "timestamp": 1578},
                     {"action": 0, "eventType": 1, "point": {"x": 1080, "y": 575}, "timestamp": 1594},
                     {"action": 0, "eventType": 1, "point": {"x": 1070, "y": 602}, "timestamp": 1610},
                     {"action": 0, "eventType": 1, "point": {"x": 1039, "y": 646}, "timestamp": 1628},
                     {"action": 0, "eventType": 1, "point": {"x": 992, "y": 695}, "timestamp": 1644},
                     {"action": 0, "eventType": 1, "point": {"x": 922, "y": 752}, "timestamp": 1660},
                     {"action": 0, "eventType": 1, "point": {"x": 841, "y": 820}, "timestamp": 1678},
                     {"action": 0, "eventType": 1, "point": {"x": 746, "y": 882}, "timestamp": 1694},
                     {"action": 12, "eventType": 1, "point": {"x": 644, "y": 934}, "timestamp": 1710},
                     {"action": 0, "eventType": 0, "point": {"x": 644, "y": 934}, "timestamp": 2032},
                     {"action": 0, "eventType": 1, "point": {"x": 419, "y": 887}, "timestamp": 3636},
                     {"action": 0, "eventType": 1, "point": {"x": 426, "y": 886}, "timestamp": 3652},
                     {"action": 0, "eventType": 1, "point": {"x": 436, "y": 881}, "timestamp": 3660},
                     {"action": 0, "eventType": 1, "point": {"x": 470, "y": 864}, "timestamp": 3676},
                     {"action": 0, "eventType": 1, "point": {"x": 547, "y": 831}, "timestamp": 3694},
                     {"action": 0, "eventType": 1, "point": {"x": 673, "y": 775}, "timestamp": 3738},
                     {"action": 0, "eventType": 1, "point": {"x": 972, "y": 621}, "timestamp": 3744},
                     {"action": 0, "eventType": 1, "point": {"x": 1040, "y": 584}, "timestamp": 3754},
                     {"action": 0, "eventType": 1, "point": {"x": 1260, "y": 470}, "timestamp": 3778},
                     {"action": 0, "eventType": 1, "point": {"x": 1290, "y": 450}, "timestamp": 3794},
                     {"action": 0, "eventType": 1, "point": {"x": 1306, "y": 433}, "timestamp": 3810},
                     {"action": 0, "eventType": 1, "point": {"x": 1324, "y": 408}, "timestamp": 3826},
                     {"action": 0, "eventType": 1, "point": {"x": 1347, "y": 367}, "timestamp": 3844},
                     {"action": 0, "eventType": 1, "point": {"x": 1376, "y": 320}, "timestamp": 3860},
                     {"action": 0, "eventType": 1, "point": {"x": 1409, "y": 261}, "timestamp": 3878},
                     {"action": 0, "eventType": 1, "point": {"x": 1447, "y": 194}, "timestamp": 3894},
                     {"action": 0, "eventType": 1, "point": {"x": 1487, "y": 122}, "timestamp": 3910},
                     {"action": 12, "eventType": 1, "point": {"x": 1546, "y": 25}, "timestamp": 3928},
                     {"action": 0, "eventType": 0, "point": {"x": 1546, "y": 25}, "timestamp": 4144},
                     {"action": 0, "eventType": 1, "point": {"x": 1792, "y": 0}, "timestamp": 4762},
                     {"action": 0, "eventType": 1, "point": {"x": 1731, "y": 123}, "timestamp": 4778},
                     {"action": 0, "eventType": 1, "point": {"x": 1693, "y": 218}, "timestamp": 4794},
                     {"action": 0, "eventType": 1, "point": {"x": 1643, "y": 330}, "timestamp": 4810},
                     {"action": 0, "eventType": 1, "point": {"x": 1596, "y": 445}, "timestamp": 4828},
                     {"action": 12, "eventType": 1, "point": {"x": 1575, "y": 484}, "timestamp": 4840},
                     {"action": 0, "eventType": 0, "point": {"x": 1575, "y": 484}, "timestamp": 5150},
                     {"action": 0, "eventType": 1, "point": {"x": 1101, "y": 480}, "timestamp": 8828},
                     {"action": 0, "eventType": 1, "point": {"x": 1094, "y": 447}, "timestamp": 8844},
                     {"action": 0, "eventType": 1, "point": {"x": 1091, "y": 429}, "timestamp": 8862},
                     {"action": 0, "eventType": 1, "point": {"x": 1089, "y": 419}, "timestamp": 8878},
                     {"action": 0, "eventType": 1, "point": {"x": 1088, "y": 414}, "timestamp": 8894},
                     {"action": 0, "eventType": 1, "point": {"x": 1086, "y": 408}, "timestamp": 8910},
                     {"action": 0, "eventType": 1, "point": {"x": 1083, "y": 404}, "timestamp": 8928},
                     {"action": 0, "eventType": 1, "point": {"x": 1081, "y": 399}, "timestamp": 8944},
                     {"action": 0, "eventType": 1, "point": {"x": 1077, "y": 395}, "timestamp": 8960},
                     {"action": 0, "eventType": 1, "point": {"x": 1066, "y": 386}, "timestamp": 8976},
                     {"action": 0, "eventType": 1, "point": {"x": 1057, "y": 380}, "timestamp": 8994},
                     {"action": 0, "eventType": 1, "point": {"x": 1050, "y": 375}, "timestamp": 9012},
                     {"action": 0, "eventType": 1, "point": {"x": 1042, "y": 371}, "timestamp": 9028},
                     {"action": 0, "eventType": 1, "point": {"x": 1034, "y": 368}, "timestamp": 9044},
                     {"action": 0, "eventType": 1, "point": {"x": 1025, "y": 365}, "timestamp": 9060},
                     {"action": 0, "eventType": 1, "point": {"x": 1016, "y": 362}, "timestamp": 9076},
                     {"action": 0, "eventType": 1, "point": {"x": 1004, "y": 358}, "timestamp": 9094},
                     {"action": 0, "eventType": 1, "point": {"x": 986, "y": 351}, "timestamp": 9110},
                     {"action": 0, "eventType": 1, "point": {"x": 968, "y": 345}, "timestamp": 9126},
                     {"action": 0, "eventType": 1, "point": {"x": 952, "y": 338}, "timestamp": 9144},
                     {"action": 0, "eventType": 1, "point": {"x": 936, "y": 330}, "timestamp": 9160},
                     {"action": 12, "eventType": 1, "point": {"x": 933, "y": 329}, "timestamp": 9176},
                     {"action": 0, "eventType": 2, "point": {"x": 933, "y": 329}, "timestamp": 9360},
                     {"action": 10, "eventType": 3, "point": {"x": 933, "y": 329}, "timestamp": 9488},
                     {"action": 0, "eventType": 1, "point": {"x": 929, "y": 334}, "timestamp": 9694},
                     {"action": 0, "eventType": 1, "point": {"x": 874, "y": 366}, "timestamp": 9788},
                     {"action": 0, "eventType": 1, "point": {"x": 869, "y": 368}, "timestamp": 9806},
                     {"action": 0, "eventType": 1, "point": {"x": 865, "y": 369}, "timestamp": 9838},
                     {"action": 0, "eventType": 1, "point": {"x": 862, "y": 370}, "timestamp": 9844},
                     {"action": 0, "eventType": 1, "point": {"x": 859, "y": 370}, "timestamp": 9860},
                     {"action": 0, "eventType": 1, "point": {"x": 854, "y": 372}, "timestamp": 9876},
                     {"action": 0, "eventType": 1, "point": {"x": 847, "y": 372}, "timestamp": 9894},
                     {"action": 0, "eventType": 1, "point": {"x": 838, "y": 373}, "timestamp": 9912},
                     {"action": 0, "eventType": 1, "point": {"x": 832, "y": 374}, "timestamp": 9928},
                     {"action": 0, "eventType": 1, "point": {"x": 827, "y": 375}, "timestamp": 9944},
                     {"action": 0, "eventType": 1, "point": {"x": 825, "y": 375}, "timestamp": 9960},
                     {"action": 0, "eventType": 1, "point": {"x": 824, "y": 376}, "timestamp": 9978},
                     {"action": 0, "eventType": 1, "point": {"x": 821, "y": 377}, "timestamp": 9994},
                     {"action": 12, "eventType": 1, "point": {"x": 820, "y": 377}, "timestamp": 10012},
                     {"action": 0, "eventType": 2, "point": {"x": 820, "y": 377}, "timestamp": 10206},
                     {"action": 10, "eventType": 3, "point": {"x": 820, "y": 377}, "timestamp": 10306},
                     {"action": 0, "eventType": 1, "point": {"x": 822, "y": 377}, "timestamp": 10356},
                     {"action": 0, "eventType": 1, "point": {"x": 836, "y": 390}, "timestamp": 10360},
                     {"action": 0, "eventType": 1, "point": {"x": 853, "y": 407}, "timestamp": 10388},
                     {"action": 0, "eventType": 1, "point": {"x": 868, "y": 420}, "timestamp": 10394},
                     {"action": 0, "eventType": 1, "point": {"x": 880, "y": 431}, "timestamp": 10412},
                     {"action": 0, "eventType": 1, "point": {"x": 888, "y": 437}, "timestamp": 10428},
                     {"action": 0, "eventType": 1, "point": {"x": 890, "y": 438}, "timestamp": 10444},
                     {"action": 0, "eventType": 1, "point": {"x": 891, "y": 436}, "timestamp": 10476},
                     {"action": 0, "eventType": 1, "point": {"x": 891, "y": 432}, "timestamp": 10494},
                     {"action": 0, "eventType": 1, "point": {"x": 891, "y": 429}, "timestamp": 10510},
                     {"action": 0, "eventType": 1, "point": {"x": 891, "y": 427}, "timestamp": 10526},
                     {"action": 0, "eventType": 1, "point": {"x": 892, "y": 426}, "timestamp": 10560},
                     {"action": 12, "eventType": 1, "point": {"x": 893, "y": 425}, "timestamp": 10576},
                     {"action": 0, "eventType": 2, "point": {"x": 893, "y": 425}, "timestamp": 10642},
                     {"action": 10, "eventType": 3, "point": {"x": 893, "y": 425}, "timestamp": 10724}], "scenario": 0,
     "terminal": 0}
    dfparse = parse_data(dfte)
    print(dfparse)
    visualization(dfte)

    # base_dir = "/Users/kite/Desktop/"
    save_base_dir = "/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/"

    # save_file = save_base_dir + "wrong_decision_0" + ".csv"
    # save_file_to_csv(dfparse, save_file)


if __name__ == '__main__':
    main()
