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


colon_names = ['distance_x_time_mean', 'distance_x_time_std', 'distance_x_time_max', 'distance_x_time_min',
               'distance_x_time_range', 'distance_x_time_average_deviaton', 'distance_x_time_skew',
               'distance_x_time_kurt', 'distance_x_time_rms', 'distance_x_freq_dc', 'distance_x_freq_shape_mean',
               'distance_x_freq_shape_std2', 'distance_x_freq_shape_std', 'distance_x_freq_shape_skew',
               'distance_x_freq_shape_kurt', 'distance_x_freq_mean', 'distance_x_freq_var', 'distance_x_freq_std',
               'distance_x_freq_skew', 'distance_x_freq_kurt', 'distance_y_time_mean', 'distance_y_time_std',
               'distance_y_time_max', 'distance_y_time_min', 'distance_y_time_range',
               'distance_y_time_average_deviaton', 'distance_y_time_skew', 'distance_y_time_kurt',
               'distance_y_time_rms', 'distance_y_freq_dc', 'distance_y_freq_shape_mean', 'distance_y_freq_shape_std2',
               'distance_y_freq_shape_std', 'distance_y_freq_shape_skew', 'distance_y_freq_shape_kurt',
               'distance_y_freq_mean', 'distance_y_freq_var', 'distance_y_freq_std', 'distance_y_freq_skew',
               'distance_y_freq_kurt', 'hor_velocity_time_mean', 'hor_velocity_time_std', 'hor_velocity_time_max',
               'hor_velocity_time_min', 'hor_velocity_time_range', 'hor_velocity_time_average_deviaton',
               'hor_velocity_time_skew', 'hor_velocity_time_kurt', 'hor_velocity_time_rms', 'hor_velocity_freq_dc',
               'hor_velocity_freq_shape_mean', 'hor_velocity_freq_shape_std2', 'hor_velocity_freq_shape_std',
               'hor_velocity_freq_shape_skew', 'hor_velocity_freq_shape_kurt', 'hor_velocity_freq_mean',
               'hor_velocity_freq_var', 'hor_velocity_freq_std', 'hor_velocity_freq_skew', 'hor_velocity_freq_kurt',
               'ver_velocity_time_mean', 'ver_velocity_time_std', 'ver_velocity_time_max', 'ver_velocity_time_min',
               'ver_velocity_time_range', 'ver_velocity_time_average_deviaton', 'ver_velocity_time_skew',
               'ver_velocity_time_kurt', 'ver_velocity_time_rms', 'ver_velocity_freq_dc',
               'ver_velocity_freq_shape_mean', 'ver_velocity_freq_shape_std2', 'ver_velocity_freq_shape_std',
               'ver_velocity_freq_shape_skew', 'ver_velocity_freq_shape_kurt', 'ver_velocity_freq_mean',
               'ver_velocity_freq_var', 'ver_velocity_freq_std', 'ver_velocity_freq_skew', 'ver_velocity_freq_kurt',
               'tangential_vel_time_mean', 'tangential_vel_time_std', 'tangential_vel_time_max',
               'tangential_vel_time_min', 'tangential_vel_time_range', 'tangential_vel_time_average_deviaton',
               'tangential_vel_time_skew', 'tangential_vel_time_kurt', 'tangential_vel_time_rms',
               'tangential_vel_freq_dc', 'tangential_vel_freq_shape_mean', 'tangential_vel_freq_shape_std2',
               'tangential_vel_freq_shape_std', 'tangential_vel_freq_shape_skew',
               'tangential_vel_freq_shape_kurt', 'tangential_vel_freq_mean', 'tangential_vel_freq_var',
               'tangential_vel_freq_std', 'tangential_vel_freq_skew', 'tangential_vel_freq_kurt',
               'tangential_accel_time_mean', 'tangential_accel_time_std', 'tangential_accel_time_max',
               'tangential_accel_time_min', 'tangential_accel_time_range', 'tangential_accel_time_average_deviaton',
               'tangential_accel_time_skew', 'tangential_accel_time_kurt', 'tangential_accel_time_rms',
               'tangential_accel_freq_dc', 'tangential_accel_freq_shape_mean', 'tangential_accel_freq_shape_std2',
               'tangential_accel_freq_shape_std', 'tangential_accel_freq_shape_skew',
               'tangential_accel_freq_shape_kurt', 'tangential_accel_freq_mean', 'tangential_accel_freq_var',
               'tangential_accel_freq_std', 'tangential_accel_freq_skew', 'tangential_accel_freq_kurt',
               'tangential_jerk_time_mean', 'tangential_jerk_time_std', 'tangential_jerk_time_max',
               'tangential_jerk_time_min', 'tangential_jerk_time_range', 'tangential_jerk_time_average_deviaton',
               'tangential_jerk_time_skew', 'tangential_jerk_time_kurt', 'tangential_jerk_time_rms',
               'tangential_jerk_freq_dc', 'tangential_jerk_freq_shape_mean', 'tangential_jerk_freq_shape_std2',
               'tangential_jerk_freq_shape_std', 'tangential_jerk_freq_shape_skew', 'tangential_jerk_freq_shape_kurt',
               'tangential_jerk_freq_mean', 'tangential_jerk_freq_var', 'tangential_jerk_freq_std',
               'tangential_jerk_freq_skew', 'tangential_jerk_freq_kurt', 'curvature_time_mean', 'curvature_time_std',
               'curvature_time_max', 'curvature_time_min', 'curvature_time_range', 'curvature_time_average_deviaton',
               'curvature_time_skew', 'curvature_time_kurt', 'curvature_time_rms', 'curvature_freq_dc',
               'curvature_freq_shape_mean', 'curvature_freq_shape_std2', 'curvature_freq_shape_std',
               'curvature_freq_shape_skew', 'curvature_freq_shape_kurt', 'curvature_freq_mean', 'curvature_freq_var',
               'curvature_freq_std', 'curvature_freq_skew', 'curvature_freq_kurt', 'curvature_rate_of_change_time_mean',
               'curvature_rate_of_change_time_std', 'curvature_rate_of_change_time_max',
               'curvature_rate_of_change_time_min', 'curvature_rate_of_change_time_range',
               'curvature_rate_of_change_time_average_deviaton', 'curvature_rate_of_change_time_skew',
               'curvature_rate_of_change_time_kurt', 'curvature_rate_of_change_time_rms',
               'curvature_rate_of_change_freq_dc', 'curvature_rate_of_change_freq_shape_mean',
               'curvature_rate_of_change_freq_shape_std2', 'curvature_rate_of_change_freq_shape_std',
               'curvature_rate_of_change_freq_shape_skew', 'curvature_rate_of_change_freq_shape_kurt',
               'curvature_rate_of_change_freq_mean', 'curvature_rate_of_change_freq_var',
               'curvature_rate_of_change_freq_std', 'curvature_rate_of_change_freq_skew',
               'curvature_rate_of_change_freq_kurt']

# message = {"scenario": -1, "terminal": -1, "success": -1}

FIRST_STAGE_TRACE_NAME = ['Time', 'key_event_type', 'dialog_type', 'mouse_event_type', 'op_x', 'op_y', 'Action']
FIRST_STAGE_TRACE_INFORMARION_NAME = ["first_x", "first_y", "second_x", "second_y", 'Bot']

SECOND_STAGE_TRACE_NAME = ['Time', 'event_type', 'op_x', 'op_y', 'Action']
SECOND_STAGE_TRACE_INFORMATION_NAME = ['correct_x', 'correct_y', 'slidebarleft_x', 'slidebarleft_y',
                                       'slidebarright_x', 'slidebarright_y', 'Bot']


def solo_check(self):
    # solo use self.df to generlize what this data is ,
    # output 3 contents: 1. this data is which stage,  first, second
    #                    2. it's scenario, pc, mobile(only happen at second stage)
    #                    3. check result message
    #                    4. prepare dataframe
    # print("solo start check the Falcon")

    # columns_name = list(self.df.columns)
    # stage = -1
    if self.df.columns[1] == "key_event_type":
        self.message["scenario"] = 0
        self.message["terminal"] = 0
        self.result = 1
    elif self.df.columns[1] == "event_type":
        self.message["scenario"] = 1
        self.message["terminal"] = 0
        self.result = 1
    elif self.df.columns[1] == "mobile_event_type":
        self.message["scenario"] = 1
        self.message["terminal"] = 1
        self.result = 1
    else:
        print("wrong data type")
        self.result = 0

    # print("solo end check of Falcon")
    return self.result


# dealing with missing data
def quantum_prepare(self):
    # self.df
    # print("quantum start prepare the Falcon")

    if self.message['scenario'] == 0:
        trace_information = self.df.loc[0, FIRST_STAGE_TRACE_INFORMARION_NAME]
        self.df = self.df.loc[0:, FIRST_STAGE_TRACE_NAME]
        self.message['success'] = 1
    elif self.message['scenario'] == 1:
        trace_information = self.df.loc[0, SECOND_STAGE_TRACE_INFORMATION_NAME]
        self.df = self.df.loc[0:, SECOND_STAGE_TRACE_NAME]
        self.message['success'] = 1

    # print("quantum end prepare of Falcon")
    return self.df, trace_information


def ascend(self):
    # print("Millennium Falcon start to ascend")
    # if self.chewbacca_check() == 0:
    #     return self.result
    # elif self.solo_check() == 0:
    #     return self.result
    # else:
    #     preprocess_dataframe = self.quantum_prepare()
    #     return self.message, preprocess_dataframe
    preprocess_dataframe, trace_info = self.quantum_prepare()
    return self.message, preprocess_dataframe, trace_info


def obi_won(message, jedi_result):
    default_judge_value = 0.5
    if message == 0:
        return default_judge_value
    else:
        return jedi_result


def lightsaber(input_dataframe):
    # r2_d2 = []
    # here come of the millennium falcon
    from Millennium_Falcon.falcon_ascend import MillenniumFalcon
    mi_falcon = MillenniumFalcon(input_dataframe)
    chewbacca_signal = mi_falcon.chewbacca_check()

    if chewbacca_signal == 0:
        # print("millennium Falcon status is bad ")
        # told obi won to action as befault
        chew_signal = obi_won(chewbacca_signal, 0)
        return chew_signal
    elif mi_falcon.solo_check() == 0:
        # print("all stop")
        # told obi won to action as befault
        return obi_won(0, 0)
    else:
        message_falcon, track, trace_info = mi_falcon.ascend()
        # print("millennium Falcon loads is:\n", track.describe())
        # r2_d2.append(message)
        # print("millennium Falcon message is:\n", message_falcon)

    # here come of Force awakens

    from Force_awakens.Destroy_Deathstart import DeathStartSys
    attack_action = DeathStartSys(track, message_falcon)
    message_forceawakens, battelfile = attack_action.command_scetor()
    # print(battelfile)
    #
    # # here come of Jedi
    #
    colon_collection = []
    colon_collection.append(battelfile)
    colon_military = pd.DataFrame(colon_collection, columns=colon_names)

    from Jedi.master_yoda import yoda
    jedis = yoda(colon_military, message_forceawakens)
    jedis_message, jedis_result = jedis.dagobath()
    print("the last jedi perform is: ", jedis_result)
    #
    return jedis_result
    # pass


def main(params):
    event_info_str = params.get("event_info")
    import json
    event_info = json.dumps(event_info_str)

    list ={"event_info":[{'Time':12,"event_type":12,'op_x':12},{'Time':12,"event_type":12,'op_x':12}]}
    print("come of jedi")
    start_time = time.time()
    data = pd.read_csv("../Data/1515396437520_2_1_human.csv")
    # data = pd.DataFrame()
    result = lightsaber(data)
    print("the final result is: ", result)

    print("duration is: ", time.time() - start_time)


if __name__ == '__main__':
    main()
