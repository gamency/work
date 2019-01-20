# -*- coding: utf-8 -*-
# This file as well as the whole sensorHMD package are licenced under the FIT licence (see the LICENCE.txt)
# Kite Fu (kitefu@163.com), HangZhou city, 2017
"""
This script can be run with:


.. code-block::

 it should return a dataframe like this:
Time_Acc	Acc_x	Acc_y	Acc_z	Time_Gra	Gra_x	Gra_y	Gra_z	Time_Gyr	Gyr_x	...	Rov_y	Rov_z
Time_SteCou	SteCou	Time_TSD	TSD_value	id	scenario	behavior	class
0	1.509531e+12	0.181959	6.244078	6.914454	1.509531e+12	0.190685	6.592248	...	1.0	1.0	4
1	1.509531e+12	0.239420	6.445191	7.134721	1.509531e+12	0.190685	6.592248	...	1.0	1.0	4
2	1.509531e+12	0.258574	6.406884	7.144298	1.509531e+12	0.190685	6.592248	...	1.0	1.0	4
3	1.509531e+12	0.153229	6.540959	7.192182	1.509531e+12	0.217926	6.592248	...	1.0	1.0	4
4	1.509531e+12	0.335188	6.464345	7.086837	1.509531e+12	0.217926	6.592248	...	1.0	1.0	4

There are a few limitations though

- Currently this only samples to first 50 values.
- Your csv must be space delimited.
- Output is saved as path_to_your_csv.features.csv

"""

import numpy as np
import pandas as pd
import os
# import sys


def fetch_file_name(file_dir):
    data_file_names = []
    for root, dirs, files in os.walk(file_dir):
        data_file_names = files.copy()
    if '.DS_Store' in data_file_names:
        data_file_names.remove('.DS_Store')
    return data_file_names


def batch_trace_file_name(data_file_names):
    batch_file_name = {}
    file_time = ''
    tmp_list = []
    i = 0
    # batch_file
    for index in list(range(len(data_file_names))):
        tmp_file_time = ''
        file_name_split = data_file_names[index].split("_")
        # print(file_name_split)
        # print(len(data_file_names))
        if len(file_name_split) < 5:
            print("no a data file")
        else:
            # print('file name is ', data_file_names[index])
            tmp_file_time = file_name_split[2] + "_" + file_name_split[3]
            # tmp_file_scenario = file_name_split[0]
            # tmp_file_behavie = file_name_split[1]
            # tmp_file_sensor = file_name_split[4:]
            # print(tmp_file_time)

            if index == 0:
                file_time = tmp_file_time
                # i += 1

            if tmp_file_time == file_time:
                tmp_list.append(data_file_names[index])
                # print("tmp list is\n", tmp_list)
                if len(data_file_names) == 12:
                    batch_file_name[i] = tmp_list
            else:
                file_time = tmp_file_time
                batch_file_name[i] = tmp_list
                tmp_list = []
                tmp_list.append(data_file_names[index])
                i += 1
                # print("i is %d"%i)
    return batch_file_name


def parse_data(data_file):
    all_lines = data_file.readlines()
    data_list = []
    for line in all_lines:
        data_list.append(line.split('|'))

    return list(map(np.float32, data_list))


def format_data_to_same_shape(data_array, d_shape, col_num):
    tmp_array = np.array([])

    if d_shape[0] == 0:
        # print("at first input data is\n", np.array(data_array))
        # print("at dshape 0 is 0 col_num is", col_num, "row is", d_shape[0])
        return np.array(data_array)

    if len(data_array) == 0:
        # print("at len data array is 0 col_num is ",col_num, "row is", d_shape[0])
        return np.zeros((d_shape[0], col_num))
    elif np.array(data_array).shape[0] < d_shape[0]:
        # print("at data array shape != dshape 0 col_num is", col_nfetch_one_trace_fileum, "row is", d_shape[0])
        tmp_array = np.zeros((d_shape[0], np.array(data_array).shape[1]))
        tmp_array[0: np.array(data_array).shape[0], :] = np.array(data_array)
    elif np.array(data_array).shape[0] > d_shape[0]:
        # print("what is going on here? different number is: ", np.array(data_array).shape,
        #       d_shape, (np.array(data_array).shape[0] - d_shape[0]))
        tmp_array = np.array(data_array)[0:d_shape[0], :]
    else:
        # print("at data array is equal col_num is", col_num, "row is", d_shape[0])
        tmp_array = np.array(data_array)
    return tmp_array


def load_datafilenparse(batch_file, base_dir, batch_index):
    # data = []
    scenario_type = batch_file[0].split('_')[0]
    behavie_type = batch_file[0].split('_')[1]

    # print(scenario_type)
    # print(behavie_type)

    if scenario_type == 'stop':
        scenario_value = 0
    else:
        scenario_value = 1

    if behavie_type == 'none':
        behavie_value = 0
    elif behavie_type == 'click':
        behavie_value = 1
    else:
        behavie_value = 2

    total_data_list_for_one_trace = np.array([])

    if len(batch_file) < 12:
        print("no a complete data file")
        return

    three_value_sensor = ['ACCELEROMETER', 'GRAVITY', 'GYROSCOPE', 'LINEAR_ACCELERATION', 'MAGNETIC']
    four_value_sensor = ['ROTATION_VECTOR']
    one_value_sensor = ['LIGHT', 'PRESSURE', 'STEP_COUNTER', 'PROXIMITY', 'RELATIVE_HUMIDITY', 'TYPE_STATIONARY_DETECT']

    for item in batch_file:
        file = base_dir + '/' + str(item)
        data_file = open(file, 'r')

        tmp_data = parse_data(data_file)

        # print("tmp data is ",tmp_data)

        # print("file to calc time freq is", file)
        # print("tmp data is ",tmp_data)
        sensor = item.split('_')[4]
        sensor_name = item[item.index(sensor):]
        # print("sensor_name is", sensor_name)

        if sensor_name in three_value_sensor:
            col_num = 4
        elif sensor_name in four_value_sensor:
            col_num = 5
        elif sensor_name in one_value_sensor:
            col_num = 2
        else:
            print("WARNINIG HERE *******************************************************")
            col_num = 0

        tmp_array = np.array([])

        tmp_array = format_data_to_same_shape(tmp_data, total_data_list_for_one_trace.shape, col_num)

        if total_data_list_for_one_trace.shape[0] == 0:
            total_data_list_for_one_trace = tmp_array
        else:
            total_data_list_for_one_trace = np.hstack((total_data_list_for_one_trace, tmp_array))

    id_array = np.zeros((total_data_list_for_one_trace.shape[0], 1)) + batch_index
    scenario_array = np.zeros((total_data_list_for_one_trace.shape[0], 1)) + scenario_value
    # print("scenario array is", scenario_array)
    behavie_array = np.zeros((total_data_list_for_one_trace.shape[0], 1)) + behavie_value

    total_data_list_for_one_trace = np.hstack((total_data_list_for_one_trace, id_array))
    total_data_list_for_one_trace = np.hstack((total_data_list_for_one_trace, scenario_array))
    total_data_list_for_one_trace = np.hstack((total_data_list_for_one_trace, behavie_array))

    # print(total_data_list_for_one_trace)
    return total_data_list_for_one_trace


def fetch_batch_sensor_file(base_dir):
    # sensor_names = ['ACCELEROMETER', 'GRAVITY', 'GYROSCOPE', 'LIGHT',
    #                 'LINEAR_ACCELERATION', 'MAGNETIC', 'PRESSURE',
    #                 'PROXIMITY', 'RELATIVE_HUMIDITY', 'ROTATION_VECTOR',
    #                 'STEP_COUNTER', 'TYPE_STATIONARY_DETECT']
    # behavie_names = ['none', 'click', 'slide']
    # scenario = ['stop', 'sport']

    file_names = fetch_file_name(base_dir)

    total_data = np.array([])

    batch_file_path = batch_trace_file_name(file_names)
    # print(batch_file_path)

    # print(batch_file_path[1])
    # print("*********begin to fetch data*******")
    # tmp_data = load_datafilenparse(batch_file_path[38], base_dir)
    # print("__________________________________________________")
    # for file in batch_file_path:
    # print(file)
    # print(len(batch_file_path))
    for k, value in enumerate(batch_file_path):
        # print("*******", k, value)

        tmp_data = load_datafilenparse(batch_file_path[value], base_dir, value)
        # print("*********************tmp data is*********", tmp_data)
        if total_data.shape[0] == 0:
            total_data = tmp_data
        else:
            # total_data.vs(tmp_data)
            total_data = np.vstack((total_data, tmp_data))
            # total_data.append(tmp_data)
    # print(total_data)
    # total_data.append(tmp_data)

    return total_data


def add_class(dataframe):
    dataframe['class'] = -1
    index_class0 = (dataframe['scenario'] == 0) & (dataframe['behavior'] == 0)
    dataframe.loc[index_class0, ['class']] = 0

    index_class1 = (dataframe['scenario'] == 0) & (dataframe['behavior'] == 1)
    dataframe.loc[index_class1, ['class']] = 1

    index_class2 = (dataframe['scenario'] == 0) & (dataframe['behavior'] == 2)
    dataframe.loc[index_class2, ['class']] = 2

    index_class3 = (dataframe['scenario'] == 1) & (dataframe['behavior'] == 0)
    dataframe.loc[index_class3, ['class']] = 3

    index_class4 = (dataframe['scenario'] == 1) & (dataframe['behavior'] == 1)
    dataframe.loc[index_class4, ['class']] = 4

    index_class5 = (dataframe['scenario'] == 1) & (dataframe['behavior'] == 2)
    dataframe.loc[index_class5, ['class']] = 5

    return dataframe


def generate_data_frame(base_dir):
    sensor_dimension_name = ['Time_Acc', 'Acc_x', 'Acc_y', 'Acc_z',
                             'Time_Gra', 'Gra_x', 'Gra_y', 'Gra_z',
                             'Time_Gyr', 'Gyr_x', 'Gyr_y', 'Gyr_z',
                             'Time_Light', 'Light',
                             'Time_LAcc', 'LAcc_x', 'LAcc_y', 'LAcc_z',
                             'Time_Mag', 'Mag_x', 'Mag_y', 'Mag_z',
                             'Time_Pres', 'Pres',
                             'Time_Prox', 'Prox',
                             'Time_ReHum', 'ReHum',
                             'Time_Rov', 'Rov_w', 'Rov_x', 'Rov_y', 'Rov_z',
                             'Time_SteCou', 'SteCou',
                             'Time_TSD', 'TSD_value']

    feature_name = sensor_dimension_name

    feature_name.append('id')
    feature_name.append('scenario')
    feature_name.append('behavior')
    # print(feature_name)

    data = fetch_batch_sensor_file(base_dir)

    df = pd.DataFrame(data, columns=feature_name)

    df = add_class(df)

    # print(df.head())
    # print(df.describe())

    return df


def __main__():
    base_dir = '/Users/kite/Desktop/human-machine-detect/Data/All_data'

    # data = fetch_batch_sensor_file(base_dir)
    df = generate_data_frame(base_dir)

    print(df.head())

    df.to_csv('./Data_Table/raw_data_1.csv', index=None)


# if __name__ == '__main__':
    # print("execute raw data fetch")
    # __main__()
