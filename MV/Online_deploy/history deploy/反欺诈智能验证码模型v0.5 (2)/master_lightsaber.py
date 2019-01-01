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
import xgboost as xgb



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


def obi_won(obmessage, jedi_result):
    default_judge_value = 0.89632
    if obmessage == 0:
        return default_judge_value
    else:
        return jedi_result


def lightsaber(input_dataframe, model, verify_inf):
    if len(input_dataframe) <= 2:
        return obi_won(0, 0)

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

    #jedis_result = model.predict_proba(colon_military)[:, 1]
    dpredict = xgb.DMatrix(colon_military)
    jedis_result = model.predict(dpredict)
    # e = time.time()
    # print("dealing yoda cost", e - s)
    # print("the last jedi perform is: ", jedis_result)
    #
    return jedis_result
    # pass