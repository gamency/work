# -*- coding: utf-8 -*-
# This file as well as the whole sensorHMD package are licenced under the FIT licence (see the LICENCE.txt)
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
import matplotlib.pyplot as plt
import time

sensor_short_name = ['Acc', 'Gra', 'Gyr', 'Light', 'LAcc', 'Mag', 'Pres', 'Prox', 'ReHum', 'Rov', 'SteCou', 'TSD']
statistict_name = 'Rss'

Rss_statistic_name = []
# for item in sensor_short_name:
#     Rss_statistic_name.append(item + statistict_name)

Rss_statistic_name = list(map(lambda x: x+'Rss', sensor_short_name))

sensor_dimension_name = {0: ['Acc_x', 'Acc_y', 'Acc_z'], 1: ['Gra_x', 'Gra_y', 'Gra_z'], 2: ['Gyr_x', 'Gyr_y', 'Gyr_z'],
                         3: ['Light'], 4: ['LAcc_x', 'LAcc_y', 'LAcc_z'], 5: ['Mag_x', 'Mag_y', 'Mag_z'],
                         6: ['Pres'], 7: ['Prox'], 8: ['ReHum'],
                         9: ['Rov_w', 'Rov_x', 'Rov_y', 'Rov_z'], 10: ['SteCou'], 11: ['TSD_value']}


def calc_rss_of_sensor(dataframe):
    for i in list(range(len(sensor_short_name))):
        # print("i is", i)
        # print("dimension name len is", len(sensor_dimension_name[i]))
        if len(sensor_dimension_name[i]) < 2:
            # print("sensor value is", np.sum(np.square(dataframe.loc[:, sensor_dimension_name[i]])))
            dataframe[Rss_statistic_name[i]] = np.sum(np.square(dataframe.loc[:, sensor_dimension_name[i]]))
        else:
            # print("sensor dimension name is",sensor_dimension_name[i])
            dataframe[Rss_statistic_name[i]] = np.sum(np.square(dataframe.loc[:, sensor_dimension_name[i]]), axis=1)
    # dataframe['ACCRss'] = np.sum(np.square(dataframe.loc[:, ['Acc_x', 'Acc_y', 'Acc_z']]), axis=1)
    # dataframe['GyrRss'] = np.sum(np.square(dataframe.loc[:, ['Gyr_x', 'Gyr_y', 'Gyr_z']]), axis=1)
    dataframe = dataframe.fillna(0)

    return dataframe


def plot_sequencial_data(dataframe):
    id_list = set(dataframe['id'])
    for index in id_list:
        trace_tmp = dataframe[dataframe['id'] == index]
        # print(index)
        plt.figure(figsize=(8, 6))
        # plt.plot(list(range(len(trace_tmp))), trace_tmp['Acc_x'])
        # plt.show()
        # plt.plot(list(range(len(trace_tmp))), trace_tmp['Acc_y'])
        # plt.show()
        plt.plot(list(range(len(trace_tmp))), trace_tmp['AccRss'])
        scenario_tmp = ''
        behavie_names_tmp = ''
        if sum(trace_tmp['scenario']) == 0:
            scenario_tmp = 'stop'
        else:
            scenario_tmp = 'sport'

        if np.mean(trace_tmp['behavior']) == 0:
            behavie_names_tmp = 'none'
        elif np.mean(trace_tmp['behavior']) == 1:
            behavie_names_tmp = 'click'
        else:
            behavie_names_tmp = 'slide'
        plt.title(str(index) + " scenario: " + scenario_tmp + " behavior: " + behavie_names_tmp + " length: " + str(
            len(trace_tmp)))
        plt.show()


def calc_rss_statistict(dataframe, save_data_file, save_file=False):
    df = calc_rss_of_sensor(dataframe)

    # plot_sequencial_data(df)
    # print(df.head())
    # print(df.describe())

    # df = df.fillna(0)

    if save_file:
        df.to_csv(save_data_file, index=None)
    return df


def __main__():
    # data_dir = '/Users/kite/Desktop/human-machine-detect/Data/Data_Table/clean_data_all_1.csv'

    data_dir = './Data_Table/clean_raw_data_short_behavior_test_data.csv'

    df = pd.read_csv(data_dir)

    # calc_rss_statistict(df,
    #                     '/Users/kite/Desktop/human-machine-detect/Data/Data_Table/Rss_clean_data_all_sensor_all.csv',
    #                     save_file=True)
    start_time = time.time()
    calc_rss_statistict(df, './Data_Table/Rss_clean_raw_data_short_behavior_test_data.csv', save_file=False)
    duration = time.time() - start_time
    print("duration is:\n", duration)


if __name__ == '__main__':
    print("execute raw data fetch")
    __main__()
