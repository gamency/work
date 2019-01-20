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

# from Xengine import harbour_delivery
from Xengine import DatanFeaturelizaiton
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
from Aiengine import Split_Data
import time
import pickle
from optparse import OptionParser
import h2o

h2o.init()

load_model = h2o.load_model("/Users/kite/PycharmProjects/sensorHMD/Model/H2OXG/twoclass_h2oxg/GBM_grid_0_AutoML_20171225_164927_model_2")


predict_type = ['twoClass', 'threeClassStaionary', 'sixClass']
# model_type = ['lr', 'rf', 'xg', 'dnn']
model_type = ['lr', 'rf', 'xg']

lr_2class_model = './Model/all_sensor_lr_model_2class.sav'
rf_2class_model = './Model/all_sensor_rf_model_2class.sav'
rf_3class_model = '/sensorHMD/Model/ThreeClassStationary/all_sensor_rf_model_3class_50len.sav'
rf_6class_model = './Model/all_sensor_rf_model_6class.sav'
xg_3class_model = './Model/ThreeClassStationary/all_sensor_xg_model_3class_50len.sav'

# model_spot = [rf_2class_model, rf_3class_model, rf_6class_model]
model_spot = [rf_3class_model]


def predict_type_formalization(dataframe, predictype, withgroundtrue):
    column_name = list(dataframe.columns)
    scenario_column_number = column_name.index('scenario')

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


def fire_in_the_hole(test_data, test_label_ground_true, model, with_ground_true=False):
    prediction = model.predict(test_data)
    prediction_probability = model.predict_proba(test_data)

    # print("model prediction result is:\n", prediction)
    # if with_ground_true:
    #     print("ground true is:\n", np.array(test_label_ground_true))
    # print("score is:\n", model.score(test_data, test_label_ground_true))

    # print("probability is:\n", model.predict_proba(test_data))

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


def fire_all(df):
    # parser =OptionParser()
    # parser.add_option("-d","--dir", dest="dir",help="data table directory")
    # parser.add_option("-o" , "--output",dest="output", help="predict result file ")
    # (options,args)=parser.parse_args()
    # if options.dir is None or options.output is None:
    #     print("error args")
    #     exit(-1)
    # print("predict starting")

    # data_dir = '/Users/kite/Desktop/human-machine-detect/Data/Data_Table/Feat_Rss_clean_data_all_sensor_all3.csv'
    # data_dir = './Data_Table/Feat_Rss_clean_raw_data_short_behavior_test_data.csv'
    # base_dir = '/Users/kite/Desktop/human-machine-detect/Data'
    # df = base_dir + '/short_behavior_test_data'

    # data_dir = '/Users/kite/Desktop/human-machine-detect/output.csv'

    # df = pd.read_csv(data_dir)
    start_time = time.time()

    feat_rss_clean_test_data_df = DatanFeaturelizaiton(df, raw_data=False, predicting=True)
    # print(feat_rss_clean_test_data_df.head())

    # for i in list(range(len(predict_type))):
    #     print("****************\n")
    #     #print("predict type is:\n", predict_type[i])
    #     test_data, test_label_ground_true = predict_type_formalization(feat_rss_clean_test_data_df, predict_type[i],
    #                                                                    withgroundtrue = True)
    #     model = pickle.load(open(model_spot[i], 'rb'))
    #     predict_result, predict_probability = fire_in_the_hole(test_data,
    #                                                            test_label_ground_true, model,  with_ground_true= True)
    #     print("****************\n")

    # only predict stationary scenario , use rf and xg model

    # for mo in model_spot:
    #     test_data, test_label_ground_true = predict_type_formalization(feat_rss_clean_test_data_df, predict_type[1],
    #                                                                    withgroundtrue=True)
    #     model = pickle.load(open(mo, 'rb'))
    #     predict_result, predict_probability = fire_in_the_hole(test_data, test_label_ground_true, model,
    #                                                            with_ground_true=True)
    #
    #     duration = time.time() - start_time
    #     print("****************\n", duration)

    # start_time = time.time()
    test_data, test_label_ground_true = predict_type_formalization(feat_rss_clean_test_data_df, predict_type[1],
                                                                   withgroundtrue=True)
    predict_data = h2o.H2OFrame(test_data)
    predict_probability = load_model.predict(predict_data)

    duration = time.time() - start_time
    print("duration is:\n", duration)
    print("predict_probability is:\n", predict_probability)
    return predict_probability[2].as_data_frame()


def __main__():
    # fire_all()
    pass


if __name__ == '__main__':
    print("execute raw data fetch")
    # __main__()
    pass