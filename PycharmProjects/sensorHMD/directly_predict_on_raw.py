# -*- coding: utf-8 -*-
# This file as well as the whole sensorHMD package are licenced under the FIT licence (see the LICENCE.txt)
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
import matplotlib.pyplot as plt
from Aiengine import Split_Data
import time
import pickle
from optparse import OptionParser
from Fetch_raw_data_file import   generate_data_frame


predict_type = ['twoClass', 'threeClassStaionary', 'sixClass']
#model_type = ['lr', 'rf', 'xg', 'dnn']
model_type = ['lr', 'rf', 'xg']

lr_2class_model = './Model/all_sensor_lr_model_2class.sav'
rf_2class_model = './Model/all_sensor_rf_model_2class.sav'
rf_3class_model = './Model/all_sensor_rf_model_3class_50len.sav'
rf_6class_model = './Model/all_sensor_rf_model_6class.sav'
xg_3class_model = './Model/all_sensor_xg_model_3class_50len.sav'
direct_xg_3class_model = './Model/XG/direct3class.sav'
direct_rf_3class_model = './Model/XG/direct3class.sav'


#model_spot = [rf_2class_model, rf_3class_model, rf_6class_model]
model_spot = [direct_xg_3class_model, direct_rf_3class_model]


sensor_dimension_name = ['Acc_x', 'Acc_y', 'Acc_z', 'Gra_x', 'Gra_y', 'Gra_z', 'Gyr_x', 'Gyr_y', 'Gyr_z',
                         'Light', 'LAcc_x', 'LAcc_y', 'LAcc_z', 'Mag_x', 'Mag_y', 'Mag_z', 'Pres', 'Prox', 'ReHum',
                         'Rov_w', 'Rov_x', 'Rov_y', 'Rov_z', 'SteCou', 'TSD_value', 'id', 'scenario', 'behavior', 'class']


def DatanFeaturelizaiton(harbour_load, raw_data = False, predicting = False):
    if raw_data:
        raw_data_df = generate_data_frame(harbour_load)
    else:
        raw_data_df = harbour_load
    # print(train_raw_data_df.head())
    # VisualizationData(train_raw_data_df)
    # if predicting :
    #     clean_raw_df = raw_data_df
    # else:
    #     clean_raw_df = clean_data(raw_data_df, '', False)
    # print(clean_raw_df.head())
    # VisualizationData(clean_raw_df)

    direct_raw_df = raw_data_df.loc[:, sensor_dimension_name]
    print(direct_raw_df.describe())
    # Rss_clean_raw_df = calc_Rss_statistict(clean_raw_df, '', False)
    # print(Rss_clean_raw_df.head())
    # VisualizationData(Rss_clean_raw_df)

    # Feat_Rss_clean_raw_data_df = calc_time_freq_statistict(Rss_clean_raw_df,
    #                                                        './Data_Table/Feat_Rss_clean_raw_data_sensor_all_50len.csv',
    #                                                        save_file=False)
    # print(Feat_Rss_clean_raw_data_df.head())
    # VisualizationData(Rss_clean_raw_df)

    return direct_raw_df


def predict_type_formalization(dataframe, predictype, withgroundtrue):
    column_name = list(dataframe.columns)
    scenario_column_number = column_name.index('id')

    if predictype == 'twoClass':
        if withgroundtrue:
            test_label_ground_true = dataframe['scenario']
        else:
            test_label_ground_true = ''

        test_data = dataframe.iloc[:, 0: scenario_column_number]

    elif predictype == 'threeClassStaionary':
        df_station = dataframe[dataframe['scenario'] == 0]

        class_index = (df_station['class'] != 0)
        df_station.loc[class_index, 'class'] = 1

        if withgroundtrue:
            test_label_ground_true = df_station['class']
        else:
            test_label_ground_true = ''

        test_data = df_station.iloc[:, 0:scenario_column_number]

    else:
        if withgroundtrue:
            test_label_ground_true = dataframe['class']

        test_data = dataframe.iloc[:, 0:scenario_column_number]

    return test_data, test_label_ground_true


def fire_in_the_hole(test_data, test_label_ground_true, model, with_ground_true = False):
    prediction = model.predict(test_data)
    prediction_probability = model.predict_proba(test_data)

    print("model prediction result is:\n", prediction)
    if with_ground_true:
        print("ground true is:\n", np.array(test_label_ground_true))
        print("score is:\n", model.score(test_data, test_label_ground_true))

    print("probability is:\n", model.predict_proba(test_data))


    return prediction, prediction_probability


# def predict(predict_dataframe, model, predict_type, dataisraw = True):
#     start_time = time.time()
#     if dataisraw:
#         df = DatanFeaturelizaiton(data_dir[0], predicting=True)
#         prediction = fire_in_the_hole(df, model, predict_type, with_ground_true = False)
#     else:
#         prediction = fire_in_the_hole(predict_dataframe, model, predict_type, with_ground_true = False)
#
#
#     pass


def slicing_result(length, predict_result):
    start_index = 0
    result = []
    for i in length:
        end_index = i + start_index
        slice_result = predict_result[start_index : end_index]
        class1_num = sum(slice_result == 1)
        if class1_num / i > 0.5:
            result.append(1)
        else:
            result.append(0)
        start_index = end_index
    return result

def __main__():
    # parser =OptionParser()
    # parser.add_option("-d","--dir", dest="dir",help="data table directory")
    # parser.add_option("-o" , "--output",dest="output", help="predict result file ")
    # (options,args)=parser.parse_args()
    # if options.dir is None or options.output is None:
    #     print("error args")
    #     exit(-1)
    # print("predict starting")

    #data_dir = '/Users/kite/Desktop/human-machine-detect/Data/Data_Table/Feat_Rss_clean_data_all_sensor_all3.csv'
    #data_dir = './Data_Table/Feat_Rss_clean_raw_data_short_behavior_test_data.csv'
    base_dir = '/Users/kite/Desktop/human-machine-detect/Data'
    df = base_dir + '/short_behavior_test_data'

    #data_dir = '/Users/kite/Desktop/human-machine-detect/output.csv'

    #df = pd.read_csv(data_dir)

    Feat_Rss_clean_test_data_df = DatanFeaturelizaiton(df, raw_data=True, predicting = True)
    print(Feat_Rss_clean_test_data_df.head())
    length = Feat_Rss_clean_test_data_df.groupby(Feat_Rss_clean_test_data_df['id']).size()
    print("data group length is:\n", length)

    # for i in list(range(len(predict_type))):
    #     print("****************\n")
    #     #print("predict type is:\n", predict_type[i])
    #     test_data, test_label_ground_true = predict_type_formalization(Feat_Rss_clean_test_data_df, predict_type[i],
    #                                                                    withgroundtrue = True)
    #     model = pickle.load(open(model_spot[i], 'rb'))
    #     predict_result, predict_probability = fire_in_the_hole(test_data, test_label_ground_true, model,  with_ground_true= True)
    #     print("****************\n")

    #only predict stationary scenario , use rf and xg model

    for mo in model_spot:
        test_data, test_label_ground_true = predict_type_formalization(Feat_Rss_clean_test_data_df, predict_type[1],
                                                                       withgroundtrue = True)
        model = pickle.load(open(mo, 'rb'))
        predict_result, predict_probability = fire_in_the_hole(test_data, test_label_ground_true, model,
                                                               with_ground_true=True)
        print("****************\n")

        result = slicing_result(length, predict_result)
        print("slicing result is:\n", result)
        ground_true_result = slicing_result(length, test_label_ground_true)
        print("ground true result is:\n", ground_true_result)
        print("****************\n")



if __name__ == '__main__':
    print("execute raw data fetch")
    __main__()





