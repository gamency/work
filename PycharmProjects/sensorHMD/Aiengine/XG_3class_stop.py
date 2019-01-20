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

# import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.model_selection import cross_val_predict, train_test_split, cross_val_score
from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, precision_score, recall_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
# from sklearn import metrics
import pickle
# import xgboost as xgb
from xgboost.sklearn import XGBClassifier
# from sklearn import cross_validation, metrics   #Additional     scklearn functions

from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 12, 4


# n_estimators=40, max_depth=45, min_samples_split=5, max_features=5)

def xg_3class_train(dataframe):
    column_name = list(dataframe.columns)
    scenario_column_number = column_name.index('scenario')
    # print(scenario_column_number)

    # df_stop = dataframe[dataframe['scenario'] == 0]
    dataframe = dataframe[dataframe['scenario'] == 0]

    # class_index = (df_stop['class'] != 0)
    class_index = (dataframe['class'] != 0)
    # df_stop.loc[class_index, 'class'] = 1
    dataframe.loc[class_index, 'class'] = 1

    # labels_true_of_stop = df_stop['class']
    labels_true_of_stop = dataframe['class']
    # train_data_stop = df_stop.iloc[:, 0:scenario_column_number]
    train_data_stop = dataframe.iloc[:, 0:scenario_column_number]

    x_train, x_test, y_train, y_test = train_test_split(train_data_stop, labels_true_of_stop, test_size=0.4)

    pipeline = Pipeline([
        ('clf', XGBClassifier())
    ])

    parameters = {
        'clf__n_estimators': (list(range(10, 500, 100)))
        # 'clf__criterion': ('gini', 'entropy'),
        # 'clf__max_depth': (None, 2, 5, 10, 15, 30, 60),
        # 'clf__min_samples_leaf': (1, 2, 5),
        # 'clf__min_samples_split': (2, 5, 8, 50)
    }

    xg_model = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1, scoring='accuracy', cv=3)

    xg_model.fit(x_train, y_train)
    print('best parameters set is：%0.3f' % xg_model.best_score_)

    print("accuracy at split test set is", xg_model.score(x_test, y_test))
    filename = '../Model/all_sensor_xg_model_3class_50len.sav'
    pickle.dump(xg_model, open(filename, 'wb'))

    return xg_model


def __main__():
    # data_dir = '/Users/kite/Desktop/human-machine-detect/Data/Data_Table/Feat_Rss_clean_data_all_sensor_all3.csv'
    data_dir = '../Data_Table/Feat_Rss_clean_raw_data_sensor_all_50len.csv'

    df = pd.read_csv(data_dir)

    model = xg_3class_train(df)
    return model


if __name__ == '__main__':
    print("execute raw data fetch")
    re = __main__()

    # learning_rate = 0.1,
    # n_estimators = 1000,
    # max_depth = 5,
    # min_child_weight = 1,
    # gamma = 0,
    # subsample = 0.8,
    # colsample_bytree = 0.8,
    # objective = 'binary:logistic',
    # nthread = 4,
    # scale_pos_weight = 1,
    # seed = 27
