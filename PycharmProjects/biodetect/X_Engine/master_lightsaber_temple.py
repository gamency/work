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
from Sauron.Eye_of_Sauron import eye

message = {"scenario": -1, "terminal": -1, "success": 1}
# FIRST_STAGE_TRACE_NAME = ['Time', 'key_event_type', 'dialog_type', 'mouse_event_type', 'op_x', 'op_y', 'Action']
FIRST_STAGE_TRACE_NAME = ['Time', 'mouse_event_type', 'op_x', 'op_y', 'Action']
# FIRST_STAGE_TRACE_NAME = ['c', 'y', 'p', 'u', 'k', 'o', 'n']
FIRST_STAGE_TRACE_INFORMARION_NAME = ["first_x", "first_y", "second_x", "second_y", "scenario", "terminal", 'Bot']

SECOND_STAGE_TRACE_NAME = ['Time', 'event_type', 'op_x', 'op_y', 'Action']
# SECOND_STAGE_TRACE_NAME = ['c', 'u', 'k', 'o', 'n']
SECOND_STAGE_TRACE_INFORMATION_NAME = ['correct_x', 'correct_y', 'slidebarleft_x', 'slidebarleft_y',
                                       'slidebarright_x', 'slidebarright_y', "scenario", "terminal", 'Bot']


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
    # series = ['dx', 'dy', 'tv', 'tacc', 'tj', 'cur', 'curroc']
    # construction = ['tm', 'tst', 'tma', 'tra', 'tad', 'tsk', 'tku', 'fd', 'fshm', 'fshstd2', 'fshsk', 'fshku', 'fm',
    #                 'fv', 'fst', 'fsk', 'fkur']

    series = ['dx', 'tacc', 'cur', 'curroc']
    construction = ['tm', 'tra', 'tsk', 'tku', 'fshm', 'fshstd2', 'fshsk', 'fshku', 'fv', 'fsk', 'fkur']
    mn = []
    for i in series:
        for j in construction:
            mn.append(str(i + "_" + j))
    mn.append("hbc")
    mn.append("crd")
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

        # visualize the data
        # eye(colon_df)

        colon_item = lightsaber(colon_df)
        colon_collection.append(colon_item)

    print(colon_collection)
    print(len(colon_collection))
    # form the lightsaber return to a millitary
    colon_name = military_name()
    colon_military = pd.DataFrame(colon_collection, columns=colon_name)
    print(colon_military.head())
    # colon_military.to_csv("../Data_Table/first_stage_train_version3_44fea_addsimplebot_addhbc.csv", index=None)
    colon_military.to_csv("../Data_Table/second_stage_train_version3_44fea_addsimplebot_addselniumbot_pageaddmotion_addhbc_addcrd.csv", index=None)

    # calling jedi temple to train the millitary

    # saving the result

    # return colon_collection
    pass


# def colon_militeray_factory(base_location):
#     colon_seed = colon_soldier(base_location)
#
#     colon_collection = []
#
#     for i in range(0, len(colon_seed)):
#         colon_df = colon_seed[i]
#         colon_item = lightsaber(colon_df)
#         colon_collection.append(colon_item)
#
#     print(colon_collection)
#     print(len(colon_collection))
#     # form the lightsaber return to a millitary
#     colon_name = military_name()
#     colon_military = pd.DataFrame(colon_collection, columns=colon_name)
#     # print(colon_military.head())
#     # colon_military.to_csv("../Data_Table/first_stage_train_version3_44fea_addsimplebot_addhbc.csv", index=None)
#     # colon_military.to_csv("../Data_Table/second_stage_train_version3_44fea_addsimplebot_addselniumbot_pageaddmotion_addhbc.csv", index=None)
#     return colon_military

    pass

def obi_won(message, jedi_result):
    default_judge_value = 0.5
    if message == 0:
        return default_judge_value
    else:
        return jedi_result


def lightsaber(input_dataframe):
    # r2_d2 = []
    # here come of the millennium falcon
    # scenario = 1
    # print(input_dataframe.head())
    # from Millennium_Falcon.falcon_ascend import MillenniumFalcon
    # mi_falcon = MillenniumFalcon(input_dataframe, phase=0)
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

    # here come of Force awakens
    # print(input_dataframe.head())
    # scenario = 1

    if input_dataframe.loc[0, 'scenario']  == 0:
        trace_info = input_dataframe.loc[0, FIRST_STAGE_TRACE_INFORMARION_NAME]
        track = input_dataframe.loc[0:, FIRST_STAGE_TRACE_NAME]
        # self.message['success'] = 1
    elif input_dataframe.loc[0, 'scenario']  == 1:
        trace_info = input_dataframe.loc[0, SECOND_STAGE_TRACE_INFORMATION_NAME]
        track = input_dataframe.loc[0:, SECOND_STAGE_TRACE_NAME]
    else:
        return obi_won(0, 0)

    # trace_info['scenario'] = scenario
    # print(trace_info)
    from Force_awakens.Destroy_Deathstart import DeathStartSys
    attack_action = DeathStartSys(track, message, trace_info)
    message_forceawakens, battelfile = attack_action.command_scetor()

    label = trace_info[-1]

    print("label is", label)
    print("battlefile is", battelfile)

    battelfile.append(label)
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

    # base_dir = "/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/First"

    # base_dir = "/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/FirstBig"
    # scenario = 0
    base_dir = "/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/secondBig"
    # base_dir = "/Users/kite/Desktop/Mobile_verify/Data/trainData/H5/SecondBig"
    # scenario = 1
    colon_soldier(base_dir)

    print("duration is: ", time.time() - start_time)


if __name__ == '__main__':
    main()
