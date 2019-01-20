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


def get_each_group_index(dataframe):
    each_group_start_index = []

    for i in list(range(int(max(dataframe['id'])) + 1)):
        each_group_start_index.append(dataframe[dataframe['id'] == i].index[0])
    # print(each_group_start_index)

    return each_group_start_index


def slicing_data_frame_to_equal_range(dataframe, each_group_start_index):
    length = dataframe.groupby(dataframe['id']).size()
    slice_length = 50

    columns_names = list(dataframe.columns)
    id_colum_index = columns_names.index('id')

    newdf = pd.DataFrame()
    # start_index = 0
    drop = 0
    id_index = 0

    for i in list(range(len(each_group_start_index))):
        # print(i)
        print(length[i], int(length[i] / slice_length))
        if length[i] < slice_length:
            print("   less than 50")
            drop += 1
            # start_index += length[i]
            pass

        # print("start index is", start_index)
        slice_number = int(length[i] / slice_length)

        if length[i] >= slice_length:
            start_index = each_group_start_index[i]
            for sn in list(range(1, slice_number + 1)):
                # print("slice here, start index is", sn)
                end_index = slice_length + start_index

                # print("end_index is", end_index)
                newdf = newdf.append(dataframe.iloc[start_index: end_index, :], ignore_index=True)
                newdf.iloc[slice_length * id_index:slice_length * (id_index + 1), id_colum_index] = id_index
                print("id_ index is ", id_index)
                id_index += 1
                start_index = end_index
                # print(newdf)
                # pass

    return newdf


def plot_sequencial_data(dataframe):
    id_list = set(dataframe['id'])
    for index in id_list:
        trace_tmp = dataframe[dataframe['id'] == index]
        print(index)
        plt.figure(figsize=(8, 6))
        plt.plot(list(range(len(trace_tmp))), trace_tmp['Acc_x'])
        # plt.show()
        plt.plot(list(range(len(trace_tmp))), trace_tmp['Acc_y'])
        # plt.show()
        plt.plot(list(range(len(trace_tmp))), trace_tmp['Acc_z'])
        # scenario_tmp = ''
        # behavie_names_tmp = ''
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


def visualization_data(dataframe):
    group_by_id_count = dataframe.groupby('id').size()
    plt.plot(list(range(len(group_by_id_count))), group_by_id_count)
    plt.show()

    var = group_by_id_count
    fig = plt.figure(figsize=(16, 8))
    ax1 = fig.add_subplot(111)
    ax1.set_xlabel('id')
    ax1.set_ylabel('size')
    ax1.set_title('group by id')
    var.plot(kind='bar', grid=True)
    plt.show()

    group_by_scenario_count = dataframe.groupby('scenario').size()
    print(group_by_scenario_count)

    var = group_by_scenario_count
    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(111)
    ax1.set_xlabel('scenario')
    ax1.set_ylabel('number')
    ax1.set_title('group by scenario')
    var.plot(kind='bar', grid=True)
    plt.show()

    group_by_behavior_count = dataframe.groupby('behavior').size()
    print(group_by_behavior_count)

    var = group_by_behavior_count
    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(111)
    ax1.set_xlabel('behavior')
    ax1.set_ylabel('number')
    ax1.set_title('group by behavior')
    var.plot(kind='bar', grid=True)
    plt.show()

    group_by_class_count = dataframe.groupby('class').size()
    print(group_by_class_count)

    var = group_by_class_count
    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(111)
    ax1.set_xlabel('class')
    ax1.set_ylabel('number')
    ax1.set_title('group by class')
    var.plot(kind='bar', grid=True)
    plt.show()


def clean_data(dataframe, save_data_file, save_file=False):
    group_index = get_each_group_index(dataframe)
    newdf = slicing_data_frame_to_equal_range(dataframe, group_index)

    # group_by_scenbeh_count = newdf.groupby(['scenario', 'behavior']).size()
    # print(group_by_scenbeh_count)

    if save_file:
        newdf.to_csv(save_data_file, index=None)
    return newdf


def __main__():
    # data_dir = './Data_Table/raw_data_short_behavior_test_data.csv'
    data_dir = '/Users/kite/Desktop/human-machine-detect/output.csv'

    df = pd.read_csv(data_dir)

    newdf = clean_data(df, '', False)
    # visualization_data(df)
    plot_sequencial_data(df)

    # group_index = get_each_group_index(df)
    # newdf = slicing_data_frame_to_equal_range(df, group_index)

    group_by_scenbeh_count = newdf.groupby(['scenario', 'behavior']).size()
    print(group_by_scenbeh_count)

    var = group_by_scenbeh_count
    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(111)
    ax1.set_xlabel('class')
    ax1.set_ylabel('number')
    ax1.set_title('group by scenario (0, 1) behavior(0, 1, 2)')
    var.plot(kind='bar', grid=True)
    plt.show()

    # newdf.to_csv('./Data_Table/clean_raw_data_short_behavior_test_data.csv', index = None)


if __name__ == '__main__':
    print("execute raw data fetch")
    __main__()
