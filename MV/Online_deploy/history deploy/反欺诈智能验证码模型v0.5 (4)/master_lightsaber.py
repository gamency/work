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
#import scipy

colon_names = ['dx_tm', 'dx_tra', 'dx_tsk', 'dx_tku', 'dx_fshm', 'dx_fshstd2', 'dx_fshsk', 'dx_fshku', 'dx_fv',
               'dx_fsk', 'dx_fkur', 'tacc_tm', 'tacc_tra', 'tacc_tsk', 'tacc_tku', 'tacc_fshm', 'tacc_fshstd2',
               'tacc_fshsk', 'tacc_fshku', 'tacc_fv', 'tacc_fsk', 'tacc_fkur', 'cur_tm', 'cur_tra', 'cur_tsk',
               'cur_tku', 'cur_fshm', 'cur_fshstd2', 'cur_fshsk', 'cur_fshku', 'cur_fv', 'cur_fsk', 'cur_fkur',
               'curroc_tm', 'curroc_tra', 'curroc_tsk', 'curroc_tku', 'curroc_fshm', 'curroc_fshstd2', 'curroc_fshsk',
               'curroc_fshku', 'curroc_fv', 'curroc_fsk', 'curroc_fkur', 'hbc']
               
message = {"scenario": -1, "terminal": -1, "success": 1}

# FIRST_STAGE_TRACE_NAME = ['Time', 'key_event_type', 'dialog_type', 'mouse_event_type', 'op_x', 'op_y', 'Action']
FIRST_STAGE_TRACE_NAME = ['Time', 'mouse_event_type', 'op_x', 'op_y', 'Action']
# FIRST_STAGE_TRACE_NAME = ['c', 'y', 'p', 'u', 'k', 'o', 'n']
FIRST_STAGE_TRACE_INFORMATION_NAME = ["first_x", "first_y", "second_x", "second_y", "scenario", "terminal", 'Bot']

SECOND_STAGE_TRACE_NAME = ['Time', 'event_type', 'op_x', 'op_y', 'Action']
# SECOND_STAGE_TRACE_NAME = ['c', 'u', 'k', 'o', 'n']
SECOND_STAGE_TRACE_INFORMATION_NAME = ['correct_x', 'correct_y', 'slidebarleft_x', 'slidebarleft_y',
                                       'slidebarright_x', 'slidebarright_y', "scenario", "terminal", 'Bot']

# JEDI = [JEDI1, JEDI2]

def dist_judge(data, verify_info):
    if verify_info['scenario'] == 1:
        bar_center_x = verify_info['slidebarleft_x'] + (verify_info['slidebarright_x'] - verify_info['slidebarleft_x']) / 2
        bar_center_y =  verify_info['slidebarleft_y'] + (verify_info['slidebarright_y'] - verify_info['slidebarleft_y']) / 2
        mouse_up_point = data.loc[data['event_type'] == 2, ['op_x', 'op_y']].values
    else:
        bar_center_x = verify_info['second_x'] + (verify_info['first_x'] - verify_info['second_x']) / 2
        bar_center_y =  verify_info['second_y'] + (verify_info['first_y'] - verify_info['second_y']) / 2
        mouse_up_point = data.loc[data['mouse_event_type'] == 2, ['op_x', 'op_y']].values
        

    #print(data.loc[data['event_type'] == 2, ['op_x', 'op_y']].values)
    #print(mouse_up_point, bar_center_x, bar_center_y)
    if len(mouse_up_point) == 0:
            print("what happen here")
            return 2
    for i in range(0, len(mouse_up_point)):
            #print(i)
        op_x = mouse_up_point[i, 0]
        op_y = mouse_up_point[i, 1]
        
        #print("********", op_x, op_y, bar_center_x, bar_center_y)
        
        if verify_info['scenario'] == 1:
            in_box_check = op_x > verify_info['slidebarleft_x'] and op_x < verify_info['slidebarright_x'] and op_y > verify_info['slidebarleft_y'] and op_y < verify_info['slidebarright_y']
        else:
            in_box_check = op_x > verify_info['second_x'] and op_x < verify_info['first_x'] and op_y > verify_info['second_y'] and op_y < verify_info['first_y']
        
        if op_x == bar_center_x and op_y == bar_center_y:
            #print('hit')
                # try_x['hit_bar_center'] = 1
            #print("********", op_x, op_y, bar_center_x, bar_center_y)
            hit_bar_center = 2
        elif in_box_check:
            #print("click here")
            if verify_info['scenario'] == 1:
                hit_bar_dis_x =  float(mouse_up_point[i,0] - verify_info['slidebarleft_x']) / (verify_info['slidebarright_x'] - verify_info['slidebarleft_x'])
                hit_bar_dis_y =  float(mouse_up_point[i,1] - verify_info['slidebarleft_y']) / (verify_info['slidebarright_y'] - verify_info['slidebarleft_y'])
                hit_bar_center = np.mean([hit_bar_dis_x ,hit_bar_dis_y])
            else:
                hit_bar_dis_x =  float(mouse_up_point[i,0] - verify_info['second_x']) / (verify_info['first_x'] - verify_info['second_x'])
                hit_bar_dis_y =  float(mouse_up_point[i,1] - verify_info['second_y']) / (verify_info['first_y'] - verify_info['second_y'])
                hit_bar_center = np.mean([hit_bar_dis_x ,hit_bar_dis_y])
        else:
            # print("out of bar")
            hit_bar_center = 0
    #print("hit",hit_bar_center)
            
    return hit_bar_center    
    pass


def obi_won(obmessage, jedi_result):
    default_judge_value = 0.89632
    if obmessage == 0:
        return default_judge_value
    elif obmessage == 1:
        return default_judge_value + 1
    elif obmessage == 2:
        return 0.861968
    else:
        return jedi_result


def lightsaber(input_dataframe, model, verify_inf):
    
    #print("before", colon_names)
    #if len(input_dataframe) < 2:
    #    less_point_result = obi_won(0, 0)
    
    #hit_bc = dist_judge(input_dataframe, verify_inf)
    
    #if hit_bc == 2:
    #    return obi_won(2, 0)

    if verify_inf["scenario"] == 0:
        # message_falcon = input_dataframe.loc[0, FIRST_STAGE_TRACE_INFORMARION_NAME]
        track = input_dataframe.loc[0:, FIRST_STAGE_TRACE_NAME]
        #colon_names = ['dx_tm', 'dx_tra', 'dx_tsk', 'dx_tku', 'dx_fshm', 'dx_fshstd2', 'dx_fshsk', 'dx_fshku', 'dx_fv',
        #       'dx_fsk', 'dx_fkur', 'tacc_tm', 'tacc_tra', 'tacc_tsk', 'tacc_tku', 'tacc_fshm', 'tacc_fshstd2',
        #       'tacc_fshsk', 'tacc_fshku', 'tacc_fv', 'tacc_fsk', 'tacc_fkur', 'cur_tm', 'cur_tra', 'cur_tsk',
        #       'cur_tku', 'cur_fshm', 'cur_fshstd2', 'cur_fshsk', 'cur_fshku', 'cur_fv', 'cur_fsk', 'cur_fkur',
        #       'curroc_tm', 'curroc_tra', 'curroc_tsk', 'curroc_tku', 'curroc_fshm', 'curroc_fshstd2', 'curroc_fshsk',
        #       'curroc_fshku', 'curroc_fv', 'curroc_fsk', 'curroc_fkur']
        
        # self.message['success'] = 1
    elif verify_inf["scenario"] == 1:
        # message_falcon = input_dataframe.loc[0, SECOND_STAGE_TRACE_INFORMATION_NAME]
        track = input_dataframe.loc[0:, SECOND_STAGE_TRACE_NAME]
        #colon_names = ['dx_tm', 'dx_tra', 'dx_tsk', 'dx_tku', 'dx_fshm', 'dx_fshstd2', 'dx_fshsk', 'dx_fshku', 'dx_fv',
        #       'dx_fsk', 'dx_fkur', 'tacc_tm', 'tacc_tra', 'tacc_tsk', 'tacc_tku', 'tacc_fshm', 'tacc_fshstd2',
        #       'tacc_fshsk', 'tacc_fshku', 'tacc_fv', 'tacc_fsk', 'tacc_fkur', 'cur_tm', 'cur_tra', 'cur_tsk',
        #       'cur_tku', 'cur_fshm', 'cur_fshstd2', 'cur_fshsk', 'cur_fshku', 'cur_fv', 'cur_fsk', 'cur_fkur',
        #       'curroc_tm', 'curroc_tra', 'curroc_tsk', 'curroc_tku', 'curroc_fshm', 'curroc_fshstd2', 'curroc_fshsk',
        #       'curroc_fshku', 'curroc_fv', 'curroc_fsk', 'curroc_fkur', 'hbc']
        #colon_names.append('hbc')
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
    
    if len(input_dataframe) < 2:
        less_point_result = attack_action.click_distribution()
        if less_point_result == 0.5:
            return obi_won(0, 0)
        else:
            return obi_won(0, 1)
    #message_forceawakens, battelfile, hit_bar_center_flag = attack_action.command_scetor()
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
    #print(colon_military['hbc'])

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
    
    #print(colon_military.head())

    #if  verify_inf["scenario"] == 1:
    #    jedis_result = model.predict_proba(colon_military)[:, -1]
    #else:
    #    dpredict = xgb.DMatrix(colon_military)
    #    jedis_result = model.predict(dpredict)
    #colon_military = colon_military.as_matrix()
    #x_test = scipy.sparse.csc_matrix(colon_military)
    #dpredict = colon_military.as_matrix()
    #dpredict = xgb.DMatrix(colon_military)
    #dpredict = colon_military.as_matrix()
    #jedis_result = model.predict(dpredict)
    jedis_result = model.predict_proba(colon_military)[:,1]
    
    #if hit_bar_center_flag == 0.5:
    if colon_military.loc[0, "hbc"] == 0.5:
        #if len(input_dataframe) <= 2:
        #    return obi_won(0, 0)
            
        jedis_result1 = obi_won(2, 0)
        #print("jedis result is",jedis_result)

        jedis_result = jedis_result * 0.3 + jedis_result1 * 0.7
    
    #if len(input_dataframe) <= 2:
        #return obi_won(0, 0)
    # e = time.time()
    # print("dealing yoda cost", e - s)
    # print("the last jedi perform is: ", jedis_result)
    #
    return jedis_result
    # pass