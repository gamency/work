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
import time
import pickle
# from Millennium_Falcon.falcon_ascend import MillenniumFalcon
from Force_awakens.Destroy_Deathstart import DeathStartSys
# from Jedi.master_yoda import yoda
import cProfile
import pstats
import os


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


sensor_basket = {'Acc': ['Acc_x', 'Acc_y', 'Acc_z'], 'Gra': ['Gra_x', 'Gra_y', 'Gra_z'],
                     'Gyr': ['Gyr_x', 'Gyr_y', 'Gyr_z'], 'Light': ['Light'], 'LAcc': ['LAcc_x', 'LAcc_y', 'LAcc_z'],
                     'Mag': ['Mag_x', 'Mag_y', 'Mag_z'], 'Pres': ['Pres'], 'Prox': ['Prox'], 'ReHum': ['ReHum'],
                     'Rov': ['Rov_w', 'Rov_x', 'Rov_y', 'Rov_z'], 'SteCou': ['SteCou'], 'TSD': ['TSD_value']}

# select_sensor = ['Acc', 'Gra']
select_sensor = ['Acc', 'Gyr', 'Mag']

Rss_statistic_name = []
Rss_statistic_name = list(map(lambda x: x+'Rss', select_sensor))

select_sensor_basket = []
for i in select_sensor:
    select_sensor_basket[0:0] = sensor_basket[i]
    select_sensor_basket.append('Time_' + i)

fea_colon_names = ['time_mean', 'time_range', 'time_skew', 'time_kurt', 'fft_shape_mean', 'fft_shape_std', 'fft_shape_skew',
               'fft_shape_kurt', 'fft_var', 'fft_skew', 'fft_kurt']

colon_names = ['{}{}'.format(a, b) for b in fea_colon_names for a in select_sensor]


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

    track = input_dataframe.loc[0:, select_sensor_basket]
    # print(track.head())
    # here come of Force awakens

    # s = time.time()
    # # message_falcon = message
    message = {'sensor_basket': sensor_basket, 'select_sensor': select_sensor}
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
    # print("colon military is ", colon_military.head())
    #
    jedis_result = model.predict_proba(colon_military)[:, 1]
    # # e = time.time()
    # # print("dealing yoda cost", e - s)
    # print("the last jedi perform is: ", jedis_result)
    # jedis_result = 0
    #
    return jedis_result
    # pass


def main():
    print("come of jedi")
    data = pd.read_csv("../Data/data.csv")
    data = pd.read_csv("../Data/1522634961204_sensor_android_bot.csv")
    # data = pd.read_csv("../Data/201803291133092_sensor_ios_human.csv", encoding='utf-16', sep='\t')
    # data = pd.read_csv("../Data/201804021409547_sensor_ios_bot.csv", encoding='utf-16', sep='\t')

    # data = pd.DataFrame()

    verify_info = {}
    verify_info["terminal"] = 2
    start_time = time.time()

    if verify_info["terminal"] == 0:
        # JEDIP1 = "../Model/all_sensor_rf_model_3class_50len.sav"
        # JEDI = pickle.load(open(JEDIP1, 'rb'))
        print("terminal is H5")
    elif verify_info["terminal"] == 1:
        JEDIP2 = "../Model/ios_sensor_threesensor.sav"
        JEDI = pickle.load(open(JEDIP2, 'rb'))
        print("terminal is Andriod")
    elif verify_info["terminal"] == 2:
        JEDIP3 = "../Model/ios_sensor_threesensor.sav"
        JEDI = pickle.load(open(JEDIP3, 'rb'))
        print("terminal is Ios")
    else:
        return obi_won(0, 0)
    # try:
    #     result = lightsaber(data, JEDI, verify_info)
    #     print("Unexpected error:", sys.exc_info()[0])
    # except:
    #     print("lalalala got an error",obi_won(0, 0))
    #     return obi_won(0, 0)

    result = lightsaber(data, JEDI, verify_info)
    # print(type(result))
    result = np.float32(result)

    print("duration is: ", time.time() - start_time)
    print("the final result is: ", result)


if __name__ == '__main__':
    main()
