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
from sklearn.model_selection import cross_val_predict, train_test_split, cross_val_score
import matplotlib.pyplot as plt

def TwoClass(dataframe):
    column_name = list(dataframe.columns)
    scenario_column_number = column_name.index('scenario')
    # print(scenario_column_number)

    # treat the class as two class, click, slide behavior here treat as class 1, so use dataframe 'class' as label
    #labels_true = dataframe.loc[ :, 'class']

    # if use scenario label, uncomment below
    labels_true = dataframe['scenario']
    train_data = dataframe.iloc[:, 0: scenario_column_number]

    # if use scenario label, comment below
    #labels_true[labels_true != 0] = 1

    X_train, X_test, y_train, y_test = train_test_split(train_data, labels_true, test_size=0.4)

    return X_train, X_test, y_train, y_test


def ThreeClass(dataframe):
    column_name = list(dataframe.columns)
    scenario_column_number = column_name.index('scenario')
    # print(scenario_column_number)

    df_stop = dataframe[dataframe['scenario'] == 0]

    class_index = (df_stop['class'] != 0)
    df_stop.loc[class_index, 'class'] = 1

    labels_true_of_stop = df_stop['class']
    train_data_stop = df_stop.iloc[:, 0:scenario_column_number]

    # labels_true_of_stop[labels_true_of_stop != 0] = 1


    X_train_stop, X_test_stop, y_train_stop, y_test_stop = train_test_split(train_data_stop, labels_true_of_stop,
                                                                            test_size=0.4)

    return X_train, X_test, y_train, y_test


def SixClass(dataframe):
    column_name = list(dataframe.columns)
    scenario_column_number = column_name.index('scenario')
    #print(scenario_column_number)

    labels_true = dataframe['class']
    train_data = dataframe.iloc[:, 0:scenario_column_number]

    X_train, X_test, y_train, y_test = train_test_split(train_data, labels_true, test_size=0.4)

    return X_train, X_test, y_train, y_test


