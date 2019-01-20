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


# colon_names = ['distance_x_time_mean', 'distance_x_time_std', 'distance_x_time_max', 'distance_x_time_min',
#                'distance_x_time_range', 'distance_x_time_average_deviaton', 'distance_x_time_skew',
#                'distance_x_time_kurt', 'distance_x_time_rms', 'distance_x_freq_dc', 'distance_x_freq_shape_mean',
#                'distance_x_freq_shape_std2', 'distance_x_freq_shape_std', 'distance_x_freq_shape_skew',
#                'distance_x_freq_shape_kurt', 'distance_x_freq_mean', 'distance_x_freq_var', 'distance_x_freq_std',
#                'distance_x_freq_skew', 'distance_x_freq_kurt', 'distance_y_time_mean', 'distance_y_time_std',
#                'distance_y_time_max', 'distance_y_time_min', 'distance_y_time_range',
#                'distance_y_time_average_deviaton', 'distance_y_time_skew', 'distance_y_time_kurt',
#                'distance_y_time_rms', 'distance_y_freq_dc', 'distance_y_freq_shape_mean',
#                'distance_y_freq_shape_std2',
#                'distance_y_freq_shape_std', 'distance_y_freq_shape_skew', 'distance_y_freq_shape_kurt',
#                'distance_y_freq_mean', 'distance_y_freq_var', 'distance_y_freq_std', 'distance_y_freq_skew',
#                'distance_y_freq_kurt', 'hor_velocity_time_mean', 'hor_velocity_time_std', 'hor_velocity_time_max',
#                'hor_velocity_time_min', 'hor_velocity_time_range', 'hor_velocity_time_average_deviaton',
#                'hor_velocity_time_skew', 'hor_velocity_time_kurt', 'hor_velocity_time_rms', 'hor_velocity_freq_dc',
#                'hor_velocity_freq_shape_mean', 'hor_velocity_freq_shape_std2', 'hor_velocity_freq_shape_std',
#                'hor_velocity_freq_shape_skew', 'hor_velocity_freq_shape_kurt', 'hor_velocity_freq_mean',
#                'hor_velocity_freq_var', 'hor_velocity_freq_std', 'hor_velocity_freq_skew', 'hor_velocity_freq_kurt',
#                'ver_velocity_time_mean', 'ver_velocity_time_std', 'ver_velocity_time_max', 'ver_velocity_time_min',
#                'ver_velocity_time_range', 'ver_velocity_time_average_deviaton', 'ver_velocity_time_skew',
#                'ver_velocity_time_kurt', 'ver_velocity_time_rms', 'ver_velocity_freq_dc',
#                'ver_velocity_freq_shape_mean', 'ver_velocity_freq_shape_std2', 'ver_velocity_freq_shape_std',
#                'ver_velocity_freq_shape_skew', 'ver_velocity_freq_shape_kurt', 'ver_velocity_freq_mean',
#                'ver_velocity_freq_var', 'ver_velocity_freq_std', 'ver_velocity_freq_skew', 'ver_velocity_freq_kurt',
#                'tangential_vel_time_mean', 'tangential_vel_time_std', 'tangential_vel_time_max',
#                'tangential_vel_time_min', 'tangential_vel_time_range', 'tangential_vel_time_average_deviaton',
#                'tangential_vel_time_skew', 'tangential_vel_time_kurt', 'tangential_vel_time_rms',
#                'tangential_vel_freq_dc', 'tangential_vel_freq_shape_mean', 'tangential_vel_freq_shape_std2',
#                'tangential_vel_freq_shape_std', 'tangential_vel_freq_shape_skew',
#                'tangential_vel_freq_shape_kurt', 'tangential_vel_freq_mean', 'tangential_vel_freq_var',
#                'tangential_vel_freq_std', 'tangential_vel_freq_skew', 'tangential_vel_freq_kurt',
#                'tangential_accel_time_mean', 'tangential_accel_time_std', 'tangential_accel_time_max',
#                'tangential_accel_time_min', 'tangential_accel_time_range', 'tangential_accel_time_average_deviaton',
#                'tangential_accel_time_skew', 'tangential_accel_time_kurt', 'tangential_accel_time_rms',
#                'tangential_accel_freq_dc', 'tangential_accel_freq_shape_mean', 'tangential_accel_freq_shape_std2',
#                'tangential_accel_freq_shape_std', 'tangential_accel_freq_shape_skew',
#                'tangential_accel_freq_shape_kurt', 'tangential_accel_freq_mean', 'tangential_accel_freq_var',
#                'tangential_accel_freq_std', 'tangential_accel_freq_skew', 'tangential_accel_freq_kurt',
#                'tangential_jerk_time_mean', 'tangential_jerk_time_std', 'tangential_jerk_time_max',
#                'tangential_jerk_time_min', 'tangential_jerk_time_range', 'tangential_jerk_time_average_deviaton',
#                'tangential_jerk_time_skew', 'tangential_jerk_time_kurt', 'tangential_jerk_time_rms',
#                'tangential_jerk_freq_dc', 'tangential_jerk_freq_shape_mean', 'tangential_jerk_freq_shape_std2',
#                'tangential_jerk_freq_shape_std', 'tangential_jerk_freq_shape_skew', 'tangential_jerk_freq_shape_kurt',
#                'tangential_jerk_freq_mean', 'tangential_jerk_freq_var', 'tangential_jerk_freq_std',
#                'tangential_jerk_freq_skew', 'tangential_jerk_freq_kurt', 'curvature_time_mean', 'curvature_time_std',
#                'curvature_time_max', 'curvature_time_min', 'curvature_time_range', 'curvature_time_average_deviaton',
#                'curvature_time_skew', 'curvature_time_kurt', 'curvature_time_rms', 'curvature_freq_dc',
#                'curvature_freq_shape_mean', 'curvature_freq_shape_std2', 'curvature_freq_shape_std',
#                'curvature_freq_shape_skew', 'curvature_freq_shape_kurt', 'curvature_freq_mean', 'curvature_freq_var',
#                'curvature_freq_std', 'curvature_freq_skew', 'curvature_freq_kurt',
#                'curvature_rate_of_change_time_mean',
#                'curvature_rate_of_change_time_std', 'curvature_rate_of_change_time_max',
#                'curvature_rate_of_change_time_min', 'curvature_rate_of_change_time_range',
#                'curvature_rate_of_change_time_average_deviaton', 'curvature_rate_of_change_time_skew',
#                'curvature_rate_of_change_time_kurt', 'curvature_rate_of_change_time_rms',
#                'curvature_rate_of_change_freq_dc', 'curvature_rate_of_change_freq_shape_mean',
#                'curvature_rate_of_change_freq_shape_std2', 'curvature_rate_of_change_freq_shape_std',
#                'curvature_rate_of_change_freq_shape_skew', 'curvature_rate_of_change_freq_shape_kurt',
#                'curvature_rate_of_change_freq_mean', 'curvature_rate_of_change_freq_var',
#                'curvature_rate_of_change_freq_std', 'curvature_rate_of_change_freq_skew',
#                'curvature_rate_of_change_freq_kurt']

# colon_names = ['dx_tm', 'dx_tst', 'dx_tma', 'dx_tmi', 'dx_tra', 'dx_tad', 'dx_tsk', 'dx_tku', 'dx_trms', 'dx_fd',
#                'dx_fshm', 'dx_fshstd2', 'dx_fshst', 'dx_fshsk', 'dx_fshku', 'dx_fm', 'dx_fv', 'dx_fst', 'dx_fsk',
#                'dx_fkur', 'dy_tm', 'dy_tst', 'dy_tma', 'dy_tmi', 'dy_tra', 'dy_tad', 'dy_tsk', 'dy_tku', 'dy_trms',
#                'dy_fd', 'dy_fshm', 'dy_fshstd2', 'dy_fshst', 'dy_fshsk', 'dy_fshku', 'dy_fm', 'dy_fv', 'dy_fst',
#                'dy_fsk', 'dy_fkur', 'hv_tm', 'hv_tst', 'hv_tma', 'hv_tmi', 'hv_tra', 'hv_tad', 'hv_tsk', 'hv_tku',
#                'hv_trms', 'hv_fd', 'hv_fshm', 'hv_fshstd2', 'hv_fshst', 'hv_fshsk', 'hv_fshku', 'hv_fm', 'hv_fv',
#                'hv_fst', 'hv_fsk', 'hv_fkur', 'vv_tm', 'vv_tst', 'vv_tma', 'vv_tmi', 'vv_tra', 'vv_tad', 'vv_tsk',
#                'vv_tku', 'vv_trms', 'vv_fd', 'vv_fshm', 'vv_fshstd2', 'vv_fshst', 'vv_fshsk', 'vv_fshku', 'vv_fm',
#                'vv_fv', 'vv_fst', 'vv_fsk', 'vv_fkur', 'tv_tm', 'tv_tst', 'tv_tma', 'tv_tmi', 'tv_tra', 'tv_tad',
#                'tv_tsk', 'tv_tku', 'tv_trms', 'tv_fd', 'tv_fshm', 'tv_fshstd2', 'tv_fshst', 'tv_fshsk', 'tv_fshku',
#                'tv_fm', 'tv_fv', 'tv_fst', 'tv_fsk', 'tv_fkur', 'tacc_tm', 'tacc_tst', 'tacc_tma', 'tacc_tmi',
#                'tacc_tra', 'tacc_tad', 'tacc_tsk', 'tacc_tku', 'tacc_trms', 'tacc_fd', 'tacc_fshm', 'tacc_fshstd2',
#                'tacc_fshst', 'tacc_fshsk', 'tacc_fshku', 'tacc_fm', 'tacc_fv', 'tacc_fst', 'tacc_fsk', 'tacc_fkur',
#                'tj_tm', 'tj_tst', 'tj_tma', 'tj_tmi', 'tj_tra', 'tj_tad', 'tj_tsk', 'tj_tku', 'tj_trms', 'tj_fd',
#                'tj_fshm', 'tj_fshstd2', 'tj_fshst', 'tj_fshsk', 'tj_fshku', 'tj_fm', 'tj_fv', 'tj_fst', 'tj_fsk',
#                'tj_fkur', 'cur_tm', 'cur_tst', 'cur_tma', 'cur_tmi', 'cur_tra', 'cur_tad', 'cur_tsk', 'cur_tku',
#                'cur_trms', 'cur_fd', 'cur_fshm', 'cur_fshstd2', 'cur_fshst', 'cur_fshsk', 'cur_fshku', 'cur_fm',
#                'cur_fv', 'cur_fst', 'cur_fsk', 'cur_fkur', 'curroc_tm', 'curroc_tst', 'curroc_tma', 'curroc_tmi',
#                'curroc_tra', 'curroc_tad', 'curroc_tsk', 'curroc_tku', 'curroc_trms', 'curroc_fd', 'curroc_fshm',
#                'curroc_fshstd2', 'curroc_fshst', 'curroc_fshsk', 'curroc_fshku', 'curroc_fm', 'curroc_fv',
#                'curroc_fst',
#                'curroc_fsk', 'curroc_fkur']

# colon_names = ['dx_tm', 'dx_tst', 'dx_tma', 'dx_tra', 'dx_tad', 'dx_tsk', 'dx_tku', 'dx_fd', 'dx_fshm', 'dx_fshstd2',
#                'dx_fshsk', 'dx_fshku', 'dx_fm', 'dx_fv', 'dx_fst', 'dx_fsk', 'dx_fkur', 'dy_tm', 'dy_tst', 'dy_tma',
#                'dy_tra', 'dy_tad', 'dy_tsk', 'dy_tku', 'dy_fd', 'dy_fshm', 'dy_fshstd2', 'dy_fshsk', 'dy_fshku',
#                'dy_fm', 'dy_fv', 'dy_fst', 'dy_fsk', 'dy_fkur', 'tv_tm', 'tv_tst', 'tv_tma', 'tv_tra', 'tv_tad',
#                'tv_tsk', 'tv_tku', 'tv_fd', 'tv_fshm', 'tv_fshstd2', 'tv_fshsk', 'tv_fshku', 'tv_fm', 'tv_fv', 'tv_fst',
#                'tv_fsk', 'tv_fkur', 'tacc_tm', 'tacc_tst', 'tacc_tma', 'tacc_tra', 'tacc_tad', 'tacc_tsk', 'tacc_tku',
#                'tacc_fd', 'tacc_fshm', 'tacc_fshstd2', 'tacc_fshsk', 'tacc_fshku', 'tacc_fm', 'tacc_fv', 'tacc_fst',
#                'tacc_fsk', 'tacc_fkur', 'tj_tm', 'tj_tst', 'tj_tma', 'tj_tra', 'tj_tad', 'tj_tsk', 'tj_tku', 'tj_fd',
#                'tj_fshm', 'tj_fshstd2', 'tj_fshsk', 'tj_fshku', 'tj_fm', 'tj_fv', 'tj_fst', 'tj_fsk', 'tj_fkur',
#                'cur_tm', 'cur_tst', 'cur_tma', 'cur_tra', 'cur_tad', 'cur_tsk', 'cur_tku', 'cur_fd', 'cur_fshm',
#                'cur_fshstd2', 'cur_fshsk', 'cur_fshku', 'cur_fm', 'cur_fv', 'cur_fst', 'cur_fsk', 'cur_fkur',
#                'curroc_tm', 'curroc_tst', 'curroc_tma', 'curroc_tra', 'curroc_tad', 'curroc_tsk', 'curroc_tku',
#                'curroc_fd', 'curroc_fshm', 'curroc_fshstd2', 'curroc_fshsk', 'curroc_fshku', 'curroc_fm', 'curroc_fv',
#                'curroc_fst', 'curroc_fsk', 'curroc_fkur']
# fea44 version
colon_names = ['dx_tm', 'dx_tra', 'dx_tsk', 'dx_tku', 'dx_fshm', 'dx_fshstd2', 'dx_fshsk', 'dx_fshku', 'dx_fv',
               'dx_fsk', 'dx_fkur', 'tacc_tm', 'tacc_tra', 'tacc_tsk', 'tacc_tku', 'tacc_fshm', 'tacc_fshstd2',
               'tacc_fshsk', 'tacc_fshku', 'tacc_fv', 'tacc_fsk', 'tacc_fkur', 'cur_tm', 'cur_tra', 'cur_tsk',
               'cur_tku', 'cur_fshm', 'cur_fshstd2', 'cur_fshsk', 'cur_fshku', 'cur_fv', 'cur_fsk', 'cur_fkur',
               'curroc_tm', 'curroc_tra', 'curroc_tsk', 'curroc_tku', 'curroc_fshm', 'curroc_fshstd2', 'curroc_fshsk',
               'curroc_fshku', 'curroc_fv', 'curroc_fsk', 'curroc_fkur']

message = {"scenario": -1, "terminal": -1, "success": 1}

# FIRST_STAGE_TRACE_NAME = ['Time', 'key_event_type', 'dialog_type', 'mouse_event_type', 'op_x', 'op_y', 'Action']
FIRST_STAGE_TRACE_NAME = ['Time', 'mouse_event_type', 'op_x', 'op_y', 'Action']
# FIRST_STAGE_TRACE_NAME = ['c', 'y', 'p', 'u', 'k', 'o', 'n']
FIRST_STAGE_TRACE_INFORMARION_NAME = ["first_x", "first_y", "second_x", "second_y", 'Bot']

SECOND_STAGE_TRACE_NAME = ['Time', 'event_type', 'op_x', 'op_y', 'Action']
# SECOND_STAGE_TRACE_NAME = ['c', 'u', 'k', 'o', 'n']
SECOND_STAGE_TRACE_INFORMATION_NAME = ['correct_x', 'correct_y', 'slidebarleft_x', 'slidebarleft_y',
                                       'slidebarright_x', 'slidebarright_y', 'Bot']

# JEDI = [JEDI1, JEDI2]

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


def obi_won(obmessage, jedi_result):
    default_judge_value = 0.596310
    if obmessage == 0:
        return default_judge_value
    else:
        return jedi_result

@do_cprofile("../profile/ml.prof")
def lightsaber(input_dataframe, model, verify_inf):
    # r2_d2 = []
    # here come of the millennium falcon
    # scenario = verify_inf["scenario"]
    # s = time.time()

    # e = time.time()
    # print("import millennium falcon cost", e-s)

    # s = time.time()

    # mi_falcon = MillenniumFalcon(input_dataframe, phase=1)
    # phase: is training phase or predict phase
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

    if verify_inf["scenario"] == 0:
        # message_falcon = input_dataframe.loc[0, FIRST_STAGE_TRACE_INFORMARION_NAME]
        track = input_dataframe.loc[0:, FIRST_STAGE_TRACE_NAME]
        # self.message['success'] = 1
    elif verify_inf["scenario"] == 1:
        # message_falcon = input_dataframe.loc[0, SECOND_STAGE_TRACE_INFORMATION_NAME]
        track = input_dataframe.loc[0:, SECOND_STAGE_TRACE_NAME]
    else:
        return obi_won(0, 0)
        # self.message['success'] = 1

    # here come of Force awakens

    # s = time.time()
    # from Force_awakens.Destroy_Deathstart import DeathStartSys
    # e = time.time()
    # print("import force awakens cost", e - s)

    # s = time.time()
    # message_falcon = message
    attack_action = DeathStartSys(track, message, verify_inf)
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

    jedis_result = model.predict_proba(colon_military)[:, 1]
    # e = time.time()
    # print("dealing yoda cost", e - s)
    # print("the last jedi perform is: ", jedis_result)
    #
    return jedis_result
    # pass


def main():
    print("come of jedi")

    data = pd.read_csv("../Data/1515396437520_2_1_human.csv")
    # data = pd.read_csv("../Data/1515639877904_2_1_human.csv")
    # data = pd.read_csv("../Data/1515744221084_2_1_bot.csv")
    # data = pd.read_csv("../Data/1515744260670_2_1_bot.csv")
    # data = pd.read_csv("../Data/1515640038092_2_2_human.csv")
    # data = pd.read_csv("../Data/1515396980830_2_2_human.csv")
    # data = pd.read_csv("../Data/1515639305464_1_1_human.csv")
    # data = pd.read_csv("../Data/1515652215717_1_1_human.csv")
    # data = pd.read_csv("../Data/1515652805257_1_1_bot.csv")
    # data = pd.read_csv("../Data/1515998525704_1_1_bot.csv")
    # data = pd.read_csv("../Data/1515652195392_1_1_human.csv")
    # data = pd.read_csv("../Data/1515652205241_1_1_human.csv")
    # data = pd.read_csv("/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/FirstBig/simple_bot44.csv")
    # data = pd.read_csv("/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/SecondBig/selinum_bot_10.csv")
    # data = pd.read_csv("/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/secondtest/selinum_bot_7.csv")
    # data = pd.read_csv("/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/selinum_bot_2.csv")
    # data = pd.read_csv("/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/SecondBig/ff738d19.csv")
    # data = pd.DataFrame()
    verify_info = {"correct_x": 595, "correct_y": 302.5, "slidebarleft_x": 529, "slidebarleft_y": 457.5,
                   "lidebarright_x": 565, "slidebarright_y": 493.5, "scenario": 1, "terminal": 0}

    start_time = time.time()
    if verify_info["scenario"] == 0:
        # JEDI = JEDI1
        JEDIP1 = "../Model/201802061300_bio_reconstruct2fea44stage1rfpc_addsimple_17.sav"
        JEDI = pickle.load(open(JEDIP1, 'rb'))
    elif verify_info["scenario"] == 1:
        # JEDI = JEDI2
        JEDIP2 = "../Model/201803061752_bio_reconstruct1stage2xgpc_addselinmbot.sav"
        # JEDIP2 = "../Model/201802061300_bio_reconstruct2fea44stage1rfpc_addsimple_17.sav"
        JEDIP2 = "../Model/201803061752_bio_reconstruct1stage2xgpc_addselinmbot_pageaddmotion.sav"
        JEDI = pickle.load(open(JEDIP2, 'rb'))
    else:
        return obi_won(0, 0)
    # try:
    #     result = lightsaber(data, JEDI, verify_info)
    #     print("Unexpected error:", sys.exc_info()[0])
    # except:
    #     print("lalalala got an error",obi_won(0, 0))
    #     return obi_won(0, 0)

    result = lightsaber(data, JEDI, verify_info)
    print(type(result))
    result = np.float32(result[0])

    print("duration is: ", time.time() - start_time)
    print("the final result is: ", result)


if __name__ == '__main__':
    main()
