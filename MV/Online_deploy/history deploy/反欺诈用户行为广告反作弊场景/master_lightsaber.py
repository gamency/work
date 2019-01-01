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

import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
#import time
#import pickle
# from Millennium_Falcon.falcon_ascend import MillenniumFalcon
from Force_awakens.Destroy_Deathstart import DeathStartSys
# from Jedi.master_yoda import yoda
# import cProfile
# import pstats
# import os
import xgboost as xgb


def do_cprofile(filename):
    """
    Decorator for function profiling.
    """
    def wrapper(func):
        def profiled_func(*args, **kwargs):
            # Flag for do profiling or not.
            DO_PROF = os.getenv("PROFILING")
            DO_PROF = True
            if DO_PROF:
                print("go in here")
                profile = cProfile.Profile()
                profile.enable()
                result = func(*args, **kwargs)
                profile.disable()
                # Sort stat by internal time.
                sortby = "tottime"
                ps = pstats.Stats(profile).sort_stats(sortby)
                ps.dump_stats(filename)
            else:
                result = func(*args, **kwargs)
            return result
        return profiled_func
    return wrapper


def light_tracker(terminal_info):
    sensor_basket = {'Acc': ['Acc_x', 'Acc_y', 'Acc_z'], 'Gra': ['Gra_x', 'Gra_y', 'Gra_z'],
                     'Gyr': ['Gyr_x', 'Gyr_y', 'Gyr_z'], 'Light': ['Light'], 'LAcc': ['LAcc_x', 'LAcc_y', 'LAcc_z'],
                     'Mag': ['Mag_x', 'Mag_y', 'Mag_z'], 'Pres': ['Pres'], 'Prox': ['Prox'], 'ReHum': ['ReHum'],
                     'Rov': ['Rov_w', 'Rov_x', 'Rov_y', 'Rov_z'], 'SteCou': ['SteCou'], 'TSD': ['TSD_value']}

    fea_colon_names = ['time_mean', 'time_range', 'time_skew', 'time_kurt', 'fft_shape_mean', 'fft_shape_std',
                       'fft_shape_skew',
                       'fft_shape_kurt', 'fft_var', 'fft_skew', 'fft_kurt']

    if terminal_info == 0:
        # print("H5")
        behavior_basket = ['Time', 'Xpath_id', 'event_type', 'control_type']
        select_behavior = ['Time', 'event_type']

    elif terminal_info == 1:
        # print("Andriod")
        # select_sensor = ['Acc', 'Gyr', 'Mag']
        select_sensor = ['Acc']
    elif terminal_info == 2:
        # print("IOS")
        # select_sensor = ['Acc', 'Gyr', 'Mag']
        select_sensor = ['Acc']
    else:
        print("unregister terminal occur")

    # Rss_statistic_name = []
    # Rss_statistic_name = list(map(lambda x: x + 'Rss', select_sensor))

    if terminal_info == 1 or terminal_info == 2:
        select_sensor_basket = []
        for i in select_sensor:
            select_sensor_basket[0:0] = sensor_basket[i]
            select_sensor_basket.append('Time_' + i)

        colon_names = ['{}{}'.format(a, b) for b in fea_colon_names for a in select_sensor]

        return sensor_basket, select_sensor, select_sensor_basket, colon_names

    elif terminal_info == 0:
        select_behavior_basket = ['Time', 'Dwell', 'Fly']
        colon_names = ['{}{}'.format(a, b) for b in fea_colon_names for a in select_behavior_basket]
        return behavior_basket, select_behavior, select_behavior_basket, colon_names

    else:
        return -1


def obi_won(obmessage, jedi_result):
    default_judge_value = 0.596310
    if obmessage == 0:
        return default_judge_value
    else:
        return jedi_result


# @do_cprofile("../profile/ml.prof")
def lightsaber(input_dataframe, model, verify_inf):
    # r2_d2 = []
    # here come of the millennium falcon
    # scenario = verify_inf["scenario"]
    # s = time.time()

    # e = time.time()
    # print("import millennium falcon cost", e-s)

    # s = time.time()

    # mi_falcon = MillenniumFalcon(input_dataframe, phase=1)
    # chewbacca_signal = mi_falcon.chewbacca_check()
    #
    # if chewbacca_signal == 0:
    #     # print("millennium Falcon status is bad ")
    #     # told obi won to action as befault
    #     chew_signal = obi_won(chewbacca_signal, 0)
    #     return chew_signal
    # elif mi_falcon.solo_check(scenario) == 0:
    #     # print("all stop")
    #     # told obi won to action as befault
    #     return obi_won(0, 0)
    # else:
    #     message_falcon, track = mi_falcon.ascend()
        # print("millennium Falcon loads is:\n", track.describe())
        # r2_d2.append(message)
        # print("millennium Falcon message is:\n", message_falcon)
    # e = time.time()
    # print("dealing millennium falcon cost", e - s)

    # if verify_inf["scenario"] == 0:
    #     # message_falcon = input_dataframe.loc[0, FIRST_STAGE_TRACE_INFORMARION_NAME]
    #     track = input_dataframe.loc[0:, FIRST_STAGE_TRACE_NAME]
    #     # self.message['success'] = 1
    # elif verify_inf["scenario"] == 1:
    #     # message_falcon = input_dataframe.loc[0, SECOND_STAGE_TRACE_INFORMATION_NAME]
    #     track = input_dataframe.loc[0:, SECOND_STAGE_TRACE_NAME]
    # else:
    #     return obi_won(0, 0)
    #     # self.message['success'] = 1
    if len(input_dataframe) <= 2:
        return obi_won(0, 0)


    if verify_inf['terminal'] == 0:
        behavior_basket, select_behavior, select_behavior_basket, colon_names = light_tracker(verify_inf['terminal'])
        track = input_dataframe
        # print(track.head())
        # here come of Force awakens

        # s = time.time()
        # # message_falcon = message


        # event_type_number = [1, 2, 3, 4, 5]
        # if sum(track['event_type'] == 4) and sum(track['event_type'] == 5)
        #print("track columns is***", track.columns)
        if sum(track['event_type'] == 4) >= 3 and sum(track['event_type'] == 5) >= 3:
            # print("key can be continue")
            h5_event_paire_id_start = 4
            h5_event_paire_id_end = 5
        elif sum(track['event_type'] == 2) >= 3 and sum(track['event_type'] == 3) >= 3:
            # print("pair touch ")
            h5_event_paire_id_start = 2
            h5_event_paire_id_end = 3
        else:
            print("too short to continue")
            return obi_won(0, 0)

        message = {'terminal': verify_inf['terminal'], 'h5_event_paire_id_start': h5_event_paire_id_start,
                   'h5_event_paire_id_end': h5_event_paire_id_end}
        # attack_action = DeathStartSys(track, message)
        # message_forceawakens, battelfile = attack_action.command_scetor()

    elif verify_inf['terminal'] == 1 or verify_inf['terminal'] == 2:
        sensor_basket, select_sensor, select_sensor_basket, colon_names = light_tracker(verify_inf['terminal'])

        track = input_dataframe.loc[0:, select_sensor_basket]
        # print(track.head())
        # here come of Force awakens

        # s = time.time()
        # # message_falcon = message
        message = {'sensor_basket': sensor_basket, 'select_sensor': select_sensor, 'terminal': verify_inf['terminal']}

    else:
        return obi_won(0, 0)

    attack_action = DeathStartSys(track, message)
    message_forceawakens, battelfile = attack_action.command_scetor()
    # e = time.time()
    # print("dealing deathstartsys cost", e - s)
    # print(battelfile)
    #
    # # here come of Jedi
    #
    # s = time.time()
    # colon_collection = list()
    # colon_collection.append(battelfile)
    # e = time.time()
    # print("dealing colon cost", e - s)

    # s = time.time()
    colon_military = pd.DataFrame([battelfile], columns=colon_names)

    # e = time.time()
    # print("dealing colon cost", e - s)

    # s = time.time()
    # from Jedi.master_yoda import yoda
    # e = time.time()
    # print("import master_yoda cost", e - s)

    # s = time.time()
    # jedis = yoda(colon_military, message_forceawakens, model)
    # jedis_message, jedis_result = jedis.dagobath()

    colon_military = colon_military.replace([np.inf, -np.inf], np.nan)
    colon_military = colon_military.fillna(0)
    #print("colon military is ", colon_military.head())
    #
    # jedis_result = model.predict_proba(colon_military)[:, 1]
    # use xgboost matrix
    if verify_inf['terminal'] == 0:
        dpredict = xgb.DMatrix(colon_military)
        jedis_result = model.predict(dpredict)
    else:
        jedis_result = model.predict_proba(colon_military)[:, 1]
    # # e = time.time()
    # # print("dealing yoda cost", e - s)
    # print("the last jedi perform is: ", jedis_result)
    # jedis_result = 0
    #
    return jedis_result
    # pass