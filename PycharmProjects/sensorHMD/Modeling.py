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
# from Xengine import DatanFeaturelizaiton
# from sklearn.model_selection import cross_val_predict, train_test_split, cross_val_score
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# from Aiengine import Split_Data
# import time
# import pickle
# from optparse import OptionParser
from Aiengine import Lr
from Aiengine import RF
from Aiengine import XG
from sklearn import metrics
# from Aiengine import dnn


model_type = ['twoClass', 'threeClassStaionary', 'sixClass']
# model_market = ['Lr', 'RF', 'SVM', 'XG', 'dnn']
model_market = ['Lr', 'RF', 'XG']

lr_model = './Model/all_sensor_lr_model_2class.sav'
rf_model = './Model/all_sensor_rf_model_2class.sav'
# rf_3class_model = './Model/all_sensor_rf_model_3class_50len.sav'
# rf_6class_model = './Model/all_sensor_rf_model_6class.sav'
xg_model = './Model/all_sensor_xg_model_3class_50len2.sav'

# model_spot = [rf_2class_model, rf_3class_model, rf_6class_model]
# model_spot = [rf_3class_model, xg_3class_model]


def model_type_formalization(dataframe, modeltype):
    column_name = list(dataframe.columns)
    scenario_column_number = column_name.index('scenario')

    if modeltype == 'twoClass':
        print('hit two class')
        train_label_ground_true = dataframe['scenario']
        train_data = dataframe.iloc[:, 0: scenario_column_number]

    elif modeltype == 'threeClassStaionary':
        df_station = dataframe[dataframe['scenario'] == 0]

        class_index = (df_station['class'] != 0)
        df_station.loc[class_index, 'class'] = 1

        train_label_ground_true = df_station['class']

        train_data = df_station.iloc[:, 0:scenario_column_number]

    else:
        train_label_ground_true = dataframe['class']

        train_data = dataframe.iloc[:, 0:scenario_column_number]

    return train_data, train_label_ground_true


# def _model_expendation(model, data_name, model_type,):
#
#     pass


def metrics_report(model, validation_data, validation_label):
    print("score is:\n", model.score(validation_data, validation_label))
    print("confusion matrix is:\n", metrics.confusion_matrix(model.predict(validation_data), validation_label))
    target_name = ['none', 'activity']
    print("classification report is:\n", metrics.classification_report(validation_label, model.predict(validation_data),
                                                                       target_names=target_name))
    # print("auc score is:\n", metrics.auc(validation_data, validation_label))
    # print('precision and recall is:\n', metrics.precision_score(validation_label, model.predict(validation_data)))
    # print("F1 score is:\n", metrics.f1_score(validation_label, model.predict(validation_data)))
    print("precision recall with beta = 0.6 \n",
          metrics.precision_recall_fscore_support(validation_label, model.predict(validation_data), beta=0.6))
    # metrics.
    pass


def fire_in_the_hole(train_data, train_label_ground_true, train_al):
    x_train_stop, x_test_stop, y_train_stop, y_test_stop = train_test_split(train_data, train_label_ground_true,
                                                                            test_size=0.4)
    if train_al == 'Lr':
        model = Lr.model_train(x_train_stop, x_test_stop, y_train_stop, y_test_stop)
    elif train_al == 'RF':
        print("start rf")
        model = RF.model_train(x_train_stop, x_test_stop, y_train_stop, y_test_stop)
    else:
        print("start xg")
        model = XG.model_train(x_train_stop, x_test_stop, y_train_stop, y_test_stop)
    # prediction_probability = model.predict_proba(train_data)
    #

    print("model prediction result is:\n", model.predict(x_train_stop))
    print("ground true is:\n", np.array(y_train_stop))

    metrics_report(model, x_test_stop, y_test_stop)
    # print
    #
    # print("probability is:\n", model.predict_proba(train_data))

    return model


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


def __main__():
    # parser =OptionParser()
    # parser.add_option("-d","--dir", dest="dir",help="data table directory")
    # parser.add_option("-o" , "--output",dest="output", help="predict result file ")
    # (options,args)=parser.parse_args()
    # if options.dir is None or options.output is None:
    #     print("error args")
    #     exit(-1)
    # print("modeling starting")

    # if data table have not generate yet:
    # base_dir = '/Users/kite/Desktop/human-machine-detect/Data'
    #
    # train_data_dir = base_dir + '/All_data'

    # if data table have been generate:
    data_dir = './Data_Table/Feat_Rss_clean_raw_data_sensor_all_50len2.csv'

    feat_rss_clean_test_data_df = pd.read_csv(data_dir)
    print(feat_rss_clean_test_data_df.describe())

    # feat_fss_clean_test_data_df = DatanFeaturelizaiton(df, raw_data=False, predicting = False)
    # print(feat_rss_clean_test_data_df.head())

    for mtind in list(range(len(model_type))):
        print("want to model type is", model_type[mtind])
        train_data, train_label_ground_true = model_type_formalization(feat_rss_clean_test_data_df, model_type[mtind])
        for mkind in list(range(len(model_market))):
            print('the select model to train is', model_market[mkind])

            model_result = fire_in_the_hole(train_data, train_label_ground_true, model_market[mkind])

    # for mt in model_spot:
    #     train_data, train_label_ground_true = model_type_formalization(feat_rss_clean_test_data_df, model_type[1],
    #                                                                    withgroundtrue = True)
    #
    #     model_result = fire_in_the_hole(train_data, train_label_ground_true, model_market[2],
    #                                     with_ground_true=True)

            print("****************\n")
            del model_result


if __name__ == '__main__':
    print("execute raw data fetch")
    __main__()
