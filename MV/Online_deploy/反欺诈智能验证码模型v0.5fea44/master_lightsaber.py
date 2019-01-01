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
    
    if len(input_dataframe) <= 10:
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

    jedis_result = model.predict_proba(colon_military)[:, 1]
    # e = time.time()
    # print("dealing yoda cost", e - s)
    # print("the last jedi perform is: ", jedis_result)
    #
    return jedis_result
    # pass


def main():
    print("come of jedi")
    data = pd.read_csv("/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/selinum_bot_2.csv")
    # data = pd.DataFrame()
    verify_info = {"correct_x": 595, "correct_y": 302.5, "slidebarleft_x": 529, "slidebarleft_y": 457.5,
                   "lidebarright_x": 565, "slidebarright_y": 493.5, "scenario": 1, "terminal": 0}

    start_time = time.time()
    if verify_info["scenario"] == 0:
        # JEDI = JEDI1
        JEDIP1 = "./Model/201802061300_bio_reconstruct2fea44stage1rfpc_addsimple_17.sav"
        JEDI = pickle.load(open(JEDIP1, 'rb'))
    elif verify_info["scenario"] == 1:
        # JEDI = JEDI2
        JEDIP2 = "./Model/201803061752_bio_reconstruct1stage2xgpc_addselinmbot.sav"
        # JEDIP2 = "../Model/201802061300_bio_reconstruct2fea44stage1rfpc_addsimple_17.sav"
        JEDIP2 = "./Model/201802051927_bio_stage2rfpc_fea44_addselinumbot_v1_6.sav"
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
