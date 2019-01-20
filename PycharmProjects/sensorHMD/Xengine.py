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

# from Future_density_Hurricane import Fetch_raw_data_file
# from Future_density_Hurricane import clean_raw_data
# from Future_density_Hurricane import Rss_statistict
# from Future_density_Hurricane import Time_Freq_featurelization

from Fetch_raw_data_file import generate_data_frame
from Clean_raw_data import clean_data
from Rss_statistict import calc_rss_statistict
from Time_Freq_featurelization import calc_time_freq_statistict
# from Aiengine import Split_Data
# from Aiengine import lr_3class_stop
# from Aiengine import Lr
# import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# import pickle
import time


def visualizationdata(dataframe):
    print(dataframe.head())


def DatanFeaturelizaiton(harbour_load, raw_data=False, predicting=False):
    if raw_data:
        raw_data_df = generate_data_frame(harbour_load)
    else:
        raw_data_df = harbour_load
    # print(train_raw_data_df.head())
    # visualizationdata(train_raw_data_df)
    if predicting:
        clean_raw_df = raw_data_df
    else:
        clean_raw_df = clean_data(raw_data_df, '', False)
    # print(clean_raw_df.head())
    # visualizationdata(clean_raw_df)

    Rss_clean_raw_df = calc_rss_statistict(clean_raw_df, '', False)
    # print(Rss_clean_raw_df.head())
    # visualizationdata(Rss_clean_raw_df)

    feat_Rss_clean_raw_data_df = calc_time_freq_statistict(Rss_clean_raw_df,
                                                           './Data_Table/Feat_Rss_clean_raw_data_sensor_all_50len2.csv',
                                                           save_file=False)
    # print(Feat_Rss_clean_raw_data_df.head())
    # visualizationdata(Rss_clean_raw_df)

    return feat_Rss_clean_raw_data_df


# def ModelingnTunning(dataframe):
#     #print(dataframe.head())
#     X_train, X_test, y_train, y_test = Split_Data.TwoClass(dataframe)
#     lr_3class_model = Lr.lr_train(X_train, X_test, y_train, y_test)
#
#     # X_train, X_test, y_train, y_test = Split_Data.ThreeClass(dataframe)
#
#     # X_train, X_test, y_train, y_test = Split_Data.SixClass(dataframe)
#
#     # form data , select model, result
#
#
#     #train_model = lr_3class_stop.lr_3Class_train(dataframe)


# def Predicting(dataframe, model):
#     print(dataframe.head())
#
#     column_name = list(dataframe.columns)
#     scenario_column_number = column_name.index('scenario')
#     # print(scenario_column_number)
#
#     df_stop = dataframe[dataframe['scenario'] == 0]
#
#     class_index = (df_stop['class'] != 0)
#     df_stop.loc[class_index, 'class'] = 1
#
#     Y_test = df_stop['class']
#     X_test = df_stop.iloc[:, 0:scenario_column_number]
#
#     # column_name = list(dataframe.columns)
#     # scenario_column_number = column_name.index('scenario')
#     # # print(scenario_column_number)
#     #
#     # # treat the class as two class, click, slide behavior here treat as class 1, so use dataframe 'class' as label
#     # Y_test = dataframe['class']
#     #
#     # # if use scenario label, uncomment below
#     # # labels_true = dataframe['scenario']
#     # X_test = dataframe.iloc[:, 0: scenario_column_number]
#     #
#     # # if use scenario label, comment below
#     # Y_test[Y_test != 0] = 1
#
#
#     model_name = './Model/all_sensor_rf_model_3class.sav'
#     #model_name = './Model/all_sensor_lr_model_2class.sav'
#     #model_name = './Model/all_sensor_xg_model_3class.sav'
#
#     xg_model = pickle.load(open(model_name, 'rb'))
#
#     result = xg_model.score(X_test, Y_test)
#     print(result)
#
#     prediction = xg_model.predict(X_test)
#     print('prediction is', prediction)
#     print('ground true is', np.array(Y_test))
#     print('original true is ', np.array(dataframe['class']))
#     print('predict probably is', xg_model.predict_proba(X_test))


def harbour_delivery(harbour, predicting=False):
    # ticket = {}
    ticket = pd.DataFrame()
    print(harbour)
    print(len(harbour))
    # for loadindex in list(range(len(harbour))):
    #     print("parth is ", harbour[loadindex])
    #     ticket[loadindex] = DatanFeaturelizaiton(harbour[loadindex], predicting)
    #     ticket = DatanFeaturelizaiton(harbour, predicting)
    ticket = DatanFeaturelizaiton(harbour, raw_data=True, predicting=False)
    # ticket = DatanFeaturelizaiton(loads)

    return ticket


# def fire_on():
#     pass


def __main__():
    # Feat_Rss_clean_raw_data_Test = DatanFeaturelizaiton(data_dir[0])
    base_dir = '/Users/kite/Desktop/human-machine-detect/Data'

    train_data_dir = base_dir + '/All_data'
    test_data_dir = base_dir + '/short_behavior_test_data'

    data_dir = [train_data_dir, test_data_dir]
    start_time = time.time()
    res = harbour_delivery(data_dir[0], predicting=False)

    # train_model = ModelingnTunning(res[0])

    # start_time = time.time()

    # print("**************************************res is")
    # print(res.head)
    # Predicting(res, '')
    duration = time.time() - start_time
    # print("predict duration is: ",duration)

    return res


if __name__ == '__main__':
    print("execute raw data fetch")
    # __main__()
