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
# import matplotlib.pyplot as plt
import time
import os
from Force_awakens.Destroy_Deathstart import DeathStartSys


select_sensor = ['Acc', 'Gyr', 'Mag']
sensor_basket = {'Acc': ['Acc_x', 'Acc_y', 'Acc_z'], 'Gra': ['Gra_x', 'Gra_y', 'Gra_z'],
                     'Gyr': ['Gyr_x', 'Gyr_y', 'Gyr_z'], 'Light': ['Light'], 'LAcc': ['LAcc_x', 'LAcc_y', 'LAcc_z'],
                     'Mag': ['Mag_x', 'Mag_y', 'Mag_z'], 'Pres': ['Pres'], 'Prox': ['Prox'], 'ReHum': ['ReHum'],
                     'Rov': ['Rov_w', 'Rov_x', 'Rov_y', 'Rov_z'], 'SteCou': ['SteCou'], 'TSD': ['TSD_value']}

Rss_statistic_name = []
Rss_statistic_name = list(map(lambda x: x+'Rss', select_sensor))

select_sensor_basket = []
for i in select_sensor:
    select_sensor_basket[0:0] = sensor_basket[i]
    select_sensor_basket.append('Time_' + i)

fea_colon_names = ['time_mean', 'time_range', 'time_skew', 'time_kurt', 'fft_shape_mean', 'fft_shape_std', 'fft_shape_skew',
               'fft_shape_kurt', 'fft_var', 'fft_skew', 'fft_kurt']

colon_name = ['{}{}'.format(a, b) for b in fea_colon_names for a in select_sensor]
colon_name.append('Bot')


def military_name():
    # series = ['distance_x', 'distance_y', 'hor_velocity', 'ver_velocity', 'tangential_vel',
    #           'tangential_accel', 'tangential_jerk', 'curvature', 'curvature_rate_of_change']
    # construction = ['time_mean', 'time_std', 'time_max', 'time_min', 'time_range', 'time_average_deviaton',
    #                 'time_skew', 'time_kurt', 'time_rms', 'freq_dc', 'freq_shape_mean', 'freq_shape_std2',
    #                 'freq_shape_st     d', 'freq_shape_skew', 'freq_shape_kurt', 'freq_mean', 'freq_var', 'freq_std',
    #                 'freq_skew', 'freq_kurt']
    # comment by version 1
    # series = ['dx', 'dy', 'hv', 'vv', 'tv', 'tacc', 'tj', 'cur', 'curroc']
    # construction = ['tm', 'tst', 'tma', 'tmi', 'tra', 'tad', 'tsk', 'tku', 'trms', 'fd', 'fshm', 'fshstd2',
    #                'fshst', 'fshsk', 'fshku', 'fm', 'fv', 'fst', 'fsk', 'fkur']
    # series = ['dx', 'dy', 'tv', 'tacc', 'tj', 'cur', 'curroc']
    # construction = ['tm', 'tst', 'tma', 'tra', 'tad', 'tsk', 'tku', 'fd', 'fshm', 'fshstd2', 'fshsk', 'fshku', 'fm',
    #                 'fv', 'fst', 'fsk', 'fkur']

    series = ['dx', 'tacc', 'cur', 'curroc']
    construction = ['tm', 'tra', 'tsk', 'tku', 'fshm', 'fshstd2', 'fshsk', 'fshku', 'fv', 'fsk', 'fkur']
    mn = []
    for i in series:
        for j in construction:
            mn.append(str(i + "_" + j))
    mn.append("Bot")
    return mn


def fetch_file_name(file_dir):
    data_file_names = []
    for root, dirs, files in os.walk(file_dir):
        data_file_names = files.copy()
    if '.DS_Store' in data_file_names:
        data_file_names.remove('.DS_Store')
    return data_file_names


def colon_soldier(base_location):
    # read in files for colon
    data_file_names = fetch_file_name(base_location)

    # for every colon seed, calling lightsaber
    colon_collection = []
    for item in data_file_names:
        print("_____start____", item)
        colon_location = base_location + '/' + str(item)
        colon_seed = open(colon_location, 'r', encoding='utf-16')
        # , encoding = "utf-16"

        colon_df = pd.read_csv(colon_seed, sep='\t')
        # , sep = '\t'
        colon_item = lightsaber(colon_df)
        colon_collection.append(colon_item)

    print(colon_collection)
    print(len(colon_collection))
    # form the lightsaber return to a millitary
    # colon_name = military_name()
    colon_military = pd.DataFrame(colon_collection, columns=colon_name)
    print(colon_military.head())
    # colon_military.to_csv("../Data_Table/first_stage_train_version3_44fea_addsimplebot.csv", index=None)
    colon_military.to_csv("../Data_Table/ubd_sensor_ios_bot.csv", index=None)

    # calling jedi temple to train the millitary

    # saving the result
    pass
    # return


def obi_won(message, jedi_result):
    default_judge_value = 0.5
    if message == 0:
        return default_judge_value
    else:
        return jedi_result


def lightsaber(input_dataframe):
    # r2_d2 = []
    # here come of the millennium falcon
    # scenario = 0
    # from Millennium_Falcon.falcon_ascend import MillenniumFalcon
    # mi_falcon = MillenniumFalcon(input_dataframe, phase = 0)
    # chewbacca_signal = mi_falcon.chewbacca_check()
    #
    # if chewbacca_signal == 0:
    #     print("millennium Falcon status is bad ")
    #     # told obi won to action as befault
    #     chew_signal = obi_won(chewbacca_signal, 0)
    #     return chew_signal
    # elif mi_falcon.solo_check(scenario) == 0:
    #     print("all stop")
    #     # told obi won to action as befault
    #     return obi_won(0, 0)
    # else:
    #     message_falcon, track, trace_info = mi_falcon.ascend()
    #     # print("millennium Falcon loads is:\n", track.describe())
    #     # r2_d2.append(message)
    #     print("millennium Falcon message is:\n", message_falcon)
    #
    # # here come of Force awakens
    #

    # attack_action = DeathStartSys(track, message_falcon)
    # message_forceawakens, battelfile = attack_action.command_scetor()
    message = {'select_sensor_basket': select_sensor_basket, 'Rss_statistic_name': Rss_statistic_name,
               'sensor_basket': sensor_basket, 'select_sensor': select_sensor}
    track = input_dataframe.loc[0:, select_sensor_basket]

    attack_action = DeathStartSys(track, message)
    message_forceawakens, battelfile = attack_action.command_scetor()

    # colon_military = pd.DataFrame([battelfile], columns=colon_names)
    # colon_military = colon_military.replace([np.inf, -np.inf], np.nan)
    # colon_military = colon_military.fillna(0)

    # label = trace_info[-1]
    label = 1

    # print("label is", label)
    print("battlefile is", battelfile)

    battelfile.append(label)
    # print(battelfile)
    #
    # # here come of Jedi
    #
    # from Jedi.master_yoda import yoda
    # jedis = yoda(battelfile, message_forceawakens)
    # jedis_message, jedis_result = jedis.dagobath()
    # print("the last jedi perform is: ", jedis_result)
    #
    return battelfile
    # pass


def main():
    print("come of jedi")
    start_time = time.time()
    # data = pd.read_csv("../Data/1515396437520_2_1_human.csv")
    # # data = pd.DataFrame()
    # result = lightsaber(data)
    # print("the final result is: ", result)

    # base_dir = "/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/FirstBig"
    # base_dir = "/Users/kite/Desktop/user_behavior_detect_preresearch/Data/trainData/Human/IOS/sensor"
    base_dir = "/Users/kite/Desktop/user_behavior_detect_preresearch/Data/trainData/Bot/IOS/sensor"
    # base_dir = "/Users/kite/Desktop/Mobile_verify/Data/trainData/H5/SecondBig"
    colon_soldier(base_dir)

    print("duration is: ", time.time() - start_time)


if __name__ == '__main__':
    main()
