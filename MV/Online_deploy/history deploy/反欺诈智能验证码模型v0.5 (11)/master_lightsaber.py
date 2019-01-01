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
import pickle
from Millennium_Falcon.falcon_ascend import MillenniumFalcon
from Force_awakens.Destroy_Deathstart import DeathStartSys
from Jedi.master_yoda import yoda

colon_names = ['dx_tm', 'dx_tst', 'dx_tma', 'dx_tmi', 'dx_tra', 'dx_tad', 'dx_tsk', 'dx_tku', 'dx_trms', 'dx_fd',
               'dx_fshm', 'dx_fshstd2', 'dx_fshst', 'dx_fshsk', 'dx_fshku', 'dx_fm', 'dx_fv', 'dx_fst', 'dx_fsk',
               'dx_fkur', 'dy_tm', 'dy_tst', 'dy_tma', 'dy_tmi', 'dy_tra', 'dy_tad', 'dy_tsk', 'dy_tku', 'dy_trms',
               'dy_fd', 'dy_fshm', 'dy_fshstd2', 'dy_fshst', 'dy_fshsk', 'dy_fshku', 'dy_fm', 'dy_fv', 'dy_fst',
               'dy_fsk', 'dy_fkur', 'hv_tm', 'hv_tst', 'hv_tma', 'hv_tmi', 'hv_tra', 'hv_tad', 'hv_tsk', 'hv_tku',
               'hv_trms', 'hv_fd', 'hv_fshm', 'hv_fshstd2', 'hv_fshst', 'hv_fshsk', 'hv_fshku', 'hv_fm', 'hv_fv',
               'hv_fst', 'hv_fsk', 'hv_fkur', 'vv_tm', 'vv_tst', 'vv_tma', 'vv_tmi', 'vv_tra', 'vv_tad', 'vv_tsk',
               'vv_tku', 'vv_trms', 'vv_fd', 'vv_fshm', 'vv_fshstd2', 'vv_fshst', 'vv_fshsk', 'vv_fshku', 'vv_fm',
               'vv_fv', 'vv_fst', 'vv_fsk', 'vv_fkur', 'tv_tm', 'tv_tst', 'tv_tma', 'tv_tmi', 'tv_tra', 'tv_tad',
               'tv_tsk', 'tv_tku', 'tv_trms', 'tv_fd', 'tv_fshm', 'tv_fshstd2', 'tv_fshst', 'tv_fshsk', 'tv_fshku',
               'tv_fm', 'tv_fv', 'tv_fst', 'tv_fsk', 'tv_fkur', 'tacc_tm', 'tacc_tst', 'tacc_tma', 'tacc_tmi',
               'tacc_tra', 'tacc_tad', 'tacc_tsk', 'tacc_tku', 'tacc_trms', 'tacc_fd', 'tacc_fshm', 'tacc_fshstd2',
               'tacc_fshst', 'tacc_fshsk', 'tacc_fshku', 'tacc_fm', 'tacc_fv', 'tacc_fst', 'tacc_fsk', 'tacc_fkur',
               'tj_tm', 'tj_tst', 'tj_tma', 'tj_tmi', 'tj_tra', 'tj_tad', 'tj_tsk', 'tj_tku', 'tj_trms', 'tj_fd',
               'tj_fshm', 'tj_fshstd2', 'tj_fshst', 'tj_fshsk', 'tj_fshku', 'tj_fm', 'tj_fv', 'tj_fst', 'tj_fsk',
               'tj_fkur', 'cur_tm', 'cur_tst', 'cur_tma', 'cur_tmi', 'cur_tra', 'cur_tad', 'cur_tsk', 'cur_tku',
               'cur_trms', 'cur_fd', 'cur_fshm', 'cur_fshstd2', 'cur_fshst', 'cur_fshsk', 'cur_fshku', 'cur_fm',
               'cur_fv', 'cur_fst', 'cur_fsk', 'cur_fkur', 'curroc_tm', 'curroc_tst', 'curroc_tma', 'curroc_tmi',
               'curroc_tra', 'curroc_tad', 'curroc_tsk', 'curroc_tku', 'curroc_trms', 'curroc_fd', 'curroc_fshm',
               'curroc_fshstd2', 'curroc_fshst', 'curroc_fshsk', 'curroc_fshku', 'curroc_fm', 'curroc_fv', 'curroc_fst',
               'curroc_fsk', 'curroc_fkur']

# JEDIP = "./Model/201801171424_bio_stage2xgpc.sav"
# JEDI = pickle.load(open(JEDIP, 'rb'))


def obi_won(message, jedi_result):
    default_judge_value = 0.59631
    if message == 0:
        return default_judge_value
    else:
        return jedi_result


def lightsaber(input_dataframe, model, verify_info):
    # r2_d2 = []
    # here come of the millennium falcon
    scenario = verify_info["scenario"]
    print("in lightsaber scenario is", scenario)
    # s = time.time()
    # e = time.time()
    # print("import millennium falcon cost", e-s)

    # s = time.time()

    mi_falcon = MillenniumFalcon(input_dataframe, scenario)
    chewbacca_signal = mi_falcon.chewbacca_check()
    soloc = mi_falcon.solo_check()
    print("in lightsaber soloc is**************", soloc)

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
        message_falcon, track = mi_falcon.ascend()
        # print("millennium Falcon loads is:\n", track.describe())
        # r2_d2.append(message)
        # print("millennium Falcon message is:\n", message_falcon)
    # e = time.time()
    # print("dealing millennium falcon cost", e - s)

    # here come of Force awakens

    # s = time.time()
    # e = time.time()
    # print("import force awakens cost", e - s)

    # s = time.time()
    attack_action = DeathStartSys(track, message_falcon)
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
    # e = time.time()
   # print("import master_yoda cost", e - s)

   #  s = time.time()
    jedis = yoda(colon_military, message_forceawakens, model)
    jedis_message, jedis_result = jedis.dagobath()
    # e = time.time()
    # print("dealing yoda cost", e - s)
    # print("the last jedi perform is: ", jedis_result)
    #
    return jedis_result