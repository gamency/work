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
# import matplotlib.pyplot as plt
import scipy.stats
import time

sensor_short_name = ['Acc', 'Gra', 'Gyr', 'Light', 'LAcc', 'Mag', 'Pres', 'Prox', 'ReHum', 'Rov', 'SteCou', 'TSD']
statistict_name = 'Rss'

Rss_statistic_name = []
# for item in sensor_short_name:
#     Rss_statistic_name.append(item + statistict_name)

Rss_statistic_name = list(map(lambda x: x+'Rss', sensor_short_name))

time_feature_name = ['time_mean', 'time_std', 'time_max', 'time_min', 'time_range',
                     'time_average_deviaton', 'time_skew', 'time_kurt', 'time_rms']

freq_feature_name = ['freq_dc', 'freq_shape_mean', 'freq_shape_std2', 'freq_shape_std',
                     'freq_shape_skew', 'freq_shape_kurt', 'freq_mean', 'freq_var', 'freq_std',
                     'freq_skew', 'freq_kurt']

label_name = ['scenario', 'behavior', 'class']
afterFeatFeaLen = len(time_feature_name) + len(freq_feature_name)
labelLen = len(label_name)


def calc_time_domain_feature(sequencial_data):
    # time_feature_list = []

    time_mean = np.mean(sequencial_data)
    # time_var = np.var(sequencial_data)
    time_std = np.std(sequencial_data)
    # time_domain_mode = scipy.stats.mode(sequencial_data)[0]
    time_max = np.max(sequencial_data)
    time_min = np.min(sequencial_data)
    # time_time_over_zero = len(sequencial_data > 0)
    time_range = (time_max - time_min)
    time_average_deviaton = np.mean(np.sum(sequencial_data - time_mean))
    time_skew = sequencial_data.skew()
    time_kurt = sequencial_data.kurt()
    time_rms = np.sqrt(np.mean(np.sum(np.square(sequencial_data))))

    # time_feature_list = [time_mean, time_var, time_std, time_domain_mode, time_max,
    #                     time_min, time_time_over_zero, time_time_range,
    #                     time_average_deviaton, time_skew, time_kurt, time_rms]

    time_feature_list = [time_mean, time_std, time_max, time_min, time_range,
                         time_average_deviaton, time_skew, time_kurt, time_rms]
    # col_name = ['time_mean', 'time_var', 'time_std', 'time_max', 'time_min',
    #        'time_time_over_zero', 'time_time_range']

    # col_name = ['time_mean', 'time_std', 'time_max', 'time_min', 'time_range',
    #             'time_average_deviaton', 'time_skew', 'time_kurt', 'time_rms']

    # print(time_feature_list)
    return time_feature_list


class Featurefft(object):
    def __init__(self, sequence_data):
        self.data = sequence_data
        fft_trans = np.abs(np.fft.fft(sequence_data))
        self.dc = fft_trans[0]
        self.freq_spectrum = fft_trans[1:int(np.floor(len(sequence_data) * 1.0 / 2)) + 1]
        self._freq_sum_ = np.sum(self.freq_spectrum)

    def fft_dc(self):
        return self.dc

    def fft_mean(self):
        return np.mean(self.freq_spectrum)

    def fft_var(self):
        return np.var(self.freq_spectrum)

    def fft_std(self):
        return np.std(self.freq_spectrum)

    def fft_entropy(self):
        pr_freq = self.freq_spectrum * 1.0 / self._freq_sum_
        entropy = -1 * np.sum([np.log2(p) * p for p in pr_freq])
        return entropy

    def fft_energy(self):
        return np.sum(self.freq_spectrum ** 2) / len(self.freq_spectrum)

    # def fft_skew(self):
    #     fft_mean, fft_std = self.fft_mean(), self.fft_std()
    #     return np.mean([np.power((x - fft_mean) / fft_std, 3)
    #                     for x in self.freq_spectrum])
    def fft_skew(self):
        fft_mean, fft_std = self.fft_mean(), self.fft_std()

        return np.mean([0 if fft_std == 0 else np.power((x - fft_mean) / fft_std, 3)
                        for x in self.freq_spectrum])

    # def fft_kurt(self):
    #     fft_mean, fft_std = self.fft_mean(), self.fft_std()
    #     return np.mean([np.power((x - fft_mean) / fft_std, 4) - 3
    #                     for x in self.freq_spectrum])
    def fft_kurt(self):
        fft_mean, fft_std = self.fft_mean(), self.fft_std()
        return np.mean([0 if fft_std == 0 else np.power((x - fft_mean) / fft_std, 4) - 3
                        for x in self.freq_spectrum])

    def fft_max(self):
        idx = np.argmax(self.freq_spectrum)
        return idx, self.freq_spectrum[idx]

    def fft_topk_freqs(self, top_k=None):
        idxs = np.argsort(self.freq_spectrum)
        if top_k is None:
            top_k = len(self.freq_spectrum)
        return idxs[:top_k], self.freq_spectrum[idxs[:top_k]]

    # def fft_shape_mean(self):
    #     shape_sum = np.sum([x * self.freq_spectrum[x]
    #                         for x in range(len(self.freq_spectrum))])
    #     return shape_sum * 1.0 / self._freq_sum_
    def fft_shape_mean(self):
        shape_sum = np.sum([x * self.freq_spectrum[x]
                            for x in range(len(self.freq_spectrum))])
        return 0 if self._freq_sum_ == 0 else shape_sum * 1.0 / self._freq_sum_

    # def fft_shape_std(self):
    #     shape_mean = self.fft_shape_mean()
    #     var = np.sum([np.power((x - shape_mean), 2) * self.freq_spectrum[x]
    #                   for x in range(len(self.freq_spectrum))]) / self._freq_sum_
    #     return np.sqrt(var)
    def fft_shape_std(self):
        if self._freq_sum_ == 0:
            return 0
        shape_mean = self.fft_shape_mean()
        var = np.sum([0 if self._freq_sum_ == 0 else np.power((x - shape_mean), 2) * self.freq_spectrum[x]
                      for x in range(len(self.freq_spectrum))]) / self._freq_sum_
        return np.sqrt(var)

    def fft_shape_skew(self):
        if self._freq_sum_ == 0:
            return 0
        shape_mean = self.fft_shape_mean()
        return np.sum([np.power((x - shape_mean), 3) * self.freq_spectrum[x]
                       for x in range(len(self.freq_spectrum))]) / self._freq_sum_

    def fft_shape_kurt(self):
        if self._freq_sum_ == 0:
            return 0
        shape_mean = self.fft_shape_mean()
        return np.sum([np.power((x - shape_mean), 4) * self.freq_spectrum[x] - 3 for x in range(len(self.freq_spectrum))]) / self._freq_sum_

    def fft_all(self):
        # feature_all = list()
        feature_all = []
        feature_all.append(self.fft_dc())
        feature_all.append(self.fft_shape_mean())
        if self.fft_shape_mean == 0:
            feature_all.append(0)
            feature_all.append(0)
            feature_all.append(0)
            feature_all.append(0)
        else:
            feature_all.append(self.fft_shape_std() ** 2)
            feature_all.append(self.fft_shape_std())
            feature_all.append(self.fft_shape_skew())
            feature_all.append(self.fft_shape_kurt())
        feature_all.append(self.fft_mean())
        feature_all.append(self.fft_var())
        feature_all.append(self.fft_std())
        feature_all.append(self.fft_skew())
        feature_all.append(self.fft_kurt())
        return feature_all


def form_time_freq_featurelization_name():
    sensor_short_name = ['Acc', 'Gra', 'Gyr', 'Light', 'LAcc', 'Mag', 'Pres', 'Prox', 'ReHum', 'Rov', 'SteCou', 'TSD']
    # sensor_name = ['ACC', 'Gyr']
    time_feature_name = ['time_mean', 'time_std', 'time_max', 'time_min', 'time_range',
                         'time_average_deviaton', 'time_skew', 'time_kurt', 'time_rms']
    freq_feature_name = ['freq_dc', 'freq_shape_mean', 'freq_shape_std2', 'freq_shape_std',
                         'freq_shape_skew', 'freq_shape_kurt', 'freq_mean', 'freq_var', 'freq_std',
                         'freq_skew', 'freq_kurt']
    class_type = ['scenario', 'behavior', 'class']

    # ACC_sensor_time_name = []
    # Gra_sensor_time_name = []
    # Gyr_sensor_time_name = []
    # Light_sensor_time_name = []
    # LAcc_sensor_time_name = []
    # Mag_sensor_time_name = []
    # Pres_sensor_time_name = []
    # Prox_sensor_time_name = []
    # ReHum_sensor_time_name = []
    # Rov_sensor_time_name = []
    # SteCou_sensor_time_name = []
    # TSD_sensor_time_name = []
    #
    # ACC_sensor_freq_name = []
    # Gra_sensor_freq_name = []
    # Gyr_sensor_freq_name = []
    # Light_sensor_freq_name = []
    # LAcc_sensor_freq_name = []
    # Mag_sensor_freq_name = []
    # Pres_sensor_freq_name = []
    # Prox_sensor_freq_name = []
    # ReHum_sensor_freq_name = []
    # Rov_sensor_freq_name = []
    # SteCou_sensor_freq_name = []
    # TSD_sensor_freq_name = []

    # ACC_sensor_time_name
    column_name = []

    for sensor_item in sensor_short_name:
        # print("sensor item is", sensor_item)
        for item_time in time_feature_name:
            column_name.append(sensor_item + item_time)
        for item_freq in freq_feature_name:
            column_name.append(sensor_item + item_freq)
    # for item_time in time_feature_name:
    #     ACC_sensor_time_name.append('ACC' + item_time)
    # for item_freq in freq_feature_name:
    #     ACC_sensor_freq_name.append('ACC' + item_freq)
    #
    # for item_time in time_feature_name:
    #     Gyr_sensor_time_name.append('Gyr' + item_time)
    # for item_freq in freq_feature_name:
    #     Gyr_sensor_freq_name.append('Gyr' + item_freq)
    #
    # Acc_df_col_name = ACC_sensor_time_name + ACC_sensor_freq_name
    # print(Acc_df_col_name)
    #
    # Gyr_df_col_name = Gyr_sensor_time_name + Gyr_sensor_freq_name + class_type
    # print(Gyr_df_col_name)

    column_name = column_name + class_type
    # print("column name is:", column_name)

    # return Acc_df_col_name, Gyr_df_col_name
    return column_name


# def calc_time_freq_featurelizaiton(dataframe, Acc_df_col_name, Gyr_df_col_name):
def calc_time_freq_featurelizaiton(dataframe, column_name):
    dataframe['id'] = dataframe['id'].astype('int')

    # Rss_time_freq_featurelization = pd.DataFrame()
    for i in list(range(len(Rss_statistic_name))):
        total_data_list_for_one_trace = []
        # print("at i sensor", i)

        for id_index in list(range(0, max(dataframe['id'] + 1))):
            # print("*********id_index is", id_index)
            time_feature_process_data = []
            freq_feature_process_data = []

            time_feature_process_data = calc_time_domain_feature(dataframe[dataframe['id'] == id_index][Rss_statistic_name[i]])
            freq_feature_process_data = Featurefft(dataframe[dataframe['id'] == id_index][Rss_statistic_name[i]]).fft_all()
        # print("***********one round", df[df['id'] == id_index]['Rss'])
            time_feature_process_data.extend(freq_feature_process_data)
        # time_feature_process_data.extend(df[df['id'] == id_index].iloc[0,-5:-2])
            if i == (len(Rss_statistic_name) - 1):
                # print("hit here")
                time_feature_process_data.extend(dataframe[dataframe['id'] == id_index].loc[:, 'scenario': 'class'].iloc[0,:])

            total_data_list_for_one_trace.append(time_feature_process_data)
            # print("for one id round data is\n",total_data_list_for_one_trace)
        if i == 0:
            column_start_index = i
        if i == (len(Rss_statistic_name) - 1):
            column_end_index = column_start_index + afterFeatFeaLen + labelLen
        else:
            column_end_index = column_start_index + afterFeatFeaLen
        tmp_df = pd.DataFrame(total_data_list_for_one_trace, columns = column_name[column_start_index : column_end_index])
        column_start_index = column_end_index
        # print("tmp datashape is", tmp_df.shape)

        if i == 0:
            Rss_time_freq_featurelization = tmp_df
        else:
            Rss_time_freq_featurelization = pd.concat([Rss_time_freq_featurelization, tmp_df], axis=1)
        # print(Rss_time_freq_featurelization.shape)

    # total_data_list_for_one_trace_GyRss = []
    # for id_index in list(range(0, max(dataframe['id']))):
    #     print("*********id_index is", id_index)
    #     time_feature_process_data = calc_time_domain_feature(dataframe[dataframe['id'] == id_index]['GyrRss'])
    #     freq_feature_process_data = Featurefft(dataframe[dataframe['id'] == id_index]['GyrRss']).fft_all()
    #     # print("***********one round", df[df['id'] == id_index]['Rss'])
    #     time_feature_process_data.extend(freq_feature_process_data)
    #     time_feature_process_data.extend(dataframe[dataframe['id'] == id_index].iloc[0, -5:-2])
    #
    #     total_data_list_for_one_trace_GyRss.append(time_feature_process_data)

    # Acc_Rss_time_freq_featurelization = pd.DataFrame(total_data_list_for_one_trace, columns=Acc_df_col_name)
    # Gyr_Rss_time_freq_featurelization = pd.DataFrame(total_data_list_for_one_trace_GyRss, columns=Gyr_df_col_name)

    # Acc_Gyr_Rss_time_freq_featurelization = pd.concat(
    #    [Acc_Rss_time_freq_featurelization, Gyr_Rss_time_freq_featurelization], axis=1)

    # print(Acc_Gyr_Rss_time_freq_featurelization.head())
    # print("finally data shape is", Rss_time_freq_featurelization.shape)

    return Rss_time_freq_featurelization


# def calc_time_freq_featurelizaiton(dataframe, Acc_df_col_name, Gyr_df_col_name):
# def calc_time_freq_featurelizaiton(dataframe, column_name):
#     dataframe['id'] = dataframe['id'].astype('int')
#
#     total_data_list_for_one_trace = []
#     for id_index in list(range(0, max(dataframe['id']))):
#         print("*********id_index is", id_index)
#         time_feature_process_data = calc_time_domain_feature(dataframe[dataframe['id'] == id_index][Rss_statistic_name[i]])
#         freq_feature_process_data = Featurefft(dataframe[dataframe['id'] == id_index]['ACCRss']).fft_all()
#         # print("***********one round", df[df['id'] == id_index]['Rss'])
#         time_feature_process_data.extend(freq_feature_process_data)
#         # time_feature_process_data.extend(df[df['id'] == id_index].iloc[0,-5:-2])
#
#         total_data_list_for_one_trace.append(time_feature_process_data)
#
#     total_data_list_for_one_trace_GyRss = []
#     for id_index in list(range(0, max(dataframe['id']))):
#         print("*********id_index is", id_index)
#         time_feature_process_data = calc_time_domain_feature(dataframe[dataframe['id'] == id_index]['GyrRss'])
#         freq_feature_process_data = Featurefft(dataframe[dataframe['id'] == id_index]['GyrRss']).fft_all()
#         # print("***********one round", df[df['id'] == id_index]['Rss'])
#         time_feature_process_data.extend(freq_feature_process_data)
#         time_feature_process_data.extend(dataframe[dataframe['id'] == id_index].iloc[0, -5:-2])
#
#         total_data_list_for_one_trace_GyRss.append(time_feature_process_data)
#
#     Acc_Rss_time_freq_featurelization = pd.DataFrame(total_data_list_for_one_trace, columns=Acc_df_col_name)
#     Gyr_Rss_time_freq_featurelization = pd.DataFrame(total_data_list_for_one_trace_GyRss, columns=Gyr_df_col_name)
#
#     Acc_Gyr_Rss_time_freq_featurelization = pd.concat(
#         [Acc_Rss_time_freq_featurelization, Gyr_Rss_time_freq_featurelization], axis=1)
#
#     print(Acc_Gyr_Rss_time_freq_featurelization.head())
#
#     return Acc_Gyr_Rss_time_freq_featurelization


def calc_time_freq_statistict(dataframe, save_data_file, save_file=False):
    # Acc_df_col_name, Gyr_df_col_name = form_time_freq_featurelization_name()
    column_name = form_time_freq_featurelization_name()
    # df = calc_time_freq_featurelizaiton(dataframe, Acc_df_col_name, Gyr_df_col_name)
    df = calc_time_freq_featurelizaiton(dataframe, column_name)
    # print(df.head())
    # print(df.describe())
    # print(df.shape)
    # for i in df.columns:
    #     print(i)

    if save_file:
        df.to_csv(save_data_file, index=None)
    return df


def __main__():
    data_dir = './Data_Table/Rss_clean_raw_data_short_behavior_test_data.csv'

    dataframe = pd.read_csv(data_dir)

    start_time = time.time()
    df = calc_time_freq_statistict(dataframe, './Data_Table/Feat_Rss_clean_raw_data_short_behavior_test_data.csv',
                                   save_file=False)
    print("duration is:\n", time.time() - start_time)
    print(df.head())


if __name__ == '__main__':
    print("execute raw data fetch")
    __main__()