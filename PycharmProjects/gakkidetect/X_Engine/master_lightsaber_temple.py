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


def military_name():
    # series = ['distance_x', 'distance_y', 'hor_velocity', 'ver_velocity', 'tangential_vel',
    #           'tangential_accel', 'tangential_jerk', 'curvature', 'curvature_rate_of_change']
    # construction = ['time_mean', 'time_std', 'time_max', 'time_min', 'time_range', 'time_average_deviaton',
    #                 'time_skew', 'time_kurt', 'time_rms', 'freq_dc', 'freq_shape_mean', 'freq_shape_std2',
    #                 'freq_shape_std', 'freq_shape_skew', 'freq_shape_kurt', 'freq_mean', 'freq_var', 'freq_std',
    #                 'freq_skew', 'freq_kurt']
    # comment by version 1
    # series = ['dx', 'dy', 'hv', 'vv', 'tv', 'tacc', 'tj', 'cur', 'curroc']
    # construction = ['tm', 'tst', 'tma', 'tmi', 'tra', 'tad', 'tsk', 'tku', 'trms', 'fd', 'fshm', 'fshstd2',
    #                'fshst', 'fshsk', 'fshku', 'fm', 'fv', 'fst', 'fsk', 'fkur']
    series = ['dx', 'dy', 'tv', 'tacc', 'tj', 'cur', 'curroc']
    construction = ['tm', 'tst', 'tma', 'tra', 'tad', 'tsk', 'tku', 'fd', 'fshm', 'fshstd2', 'fshsk', 'fshku', 'fm',
                    'fv', 'fst', 'fsk', 'fkur']
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
        colon_seed = open(colon_location, 'r')

        colon_df = pd.read_csv(colon_seed)
        colon_item = lightsaber(colon_df)
        colon_collection.append(colon_item)

    print(colon_collection)
    print(len(colon_collection))
    # form the lightsaber return to a millitary
    colon_name = military_name()
    colon_military = pd.DataFrame(colon_collection, columns=colon_name)
    # colon_military.to_csv("../Data_Table/first_stage_train_version1.csv", index=None)
    colon_military.to_csv("../Data_Table/second_stage_train_version1.csv", index=None)

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
    scenario = 0
    from Millennium_Falcon.falcon_ascend import MillenniumFalcon
    mi_falcon = MillenniumFalcon(input_dataframe, phase = 0)
    chewbacca_signal = mi_falcon.chewbacca_check()

    if chewbacca_signal == 0:
        print("millennium Falcon status is bad ")
        # told obi won to action as befault
        chew_signal = obi_won(chewbacca_signal, 0)
        return chew_signal
    elif mi_falcon.solo_check(scenario) == 0:
        print("all stop")
        # told obi won to action as befault
        return obi_won(0, 0)
    else:
        message_falcon, track, trace_info = mi_falcon.ascend()
        # print("millennium Falcon loads is:\n", track.describe())
        # r2_d2.append(message)
        print("millennium Falcon message is:\n", message_falcon)

    # here come of Force awakens

    from Force_awakens.Destroy_Deathstart import DeathStartSys
    attack_action = DeathStartSys(track, message_falcon)
    message_forceawakens, battelfile = attack_action.command_scetor()

    label = trace_info[-1]

    print("label is", label)
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
    base_dir = "/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/SecondBig"
    colon_soldier(base_dir)

    print("duration is: ", time.time() - start_time)


if __name__ == '__main__':
    main()
