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

from DeathStar import model_market
# from Xengine import DatanFeaturelizaiton
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# from Aiengine import Split_Data
import time
import pickle

def featurelizationData(df, raw_data, model_scenario):
    # if
    Feat_Rss_clean_test_data_df = DatanFeaturelizaiton(df, raw_data, predicting=True)
    #if data
    model_buy = model_market.model_select(model_scenario)


def __main__():
    raw_data = True
    if raw_data == True:
        base_dir = '/Users/kite/Desktop/human-machine-detect/Data'
        df = base_dir + '/short_behavior_test_data'
    else:
        # data_dir = './Data_Table/Feat_Rss_clean_raw_data_short_behavior_test_data.csv'
        data_dir = '/Users/kite/Desktop/human-machine-detect/output.csv'
        df = pd.read_csv(data_dir)

    Feat_Rss_clean_test_data_df = DatanFeaturelizaiton(df, raw_data, predicting = True)
    print(Feat_Rss_clean_test_data_df.head())

    # for mo in model_spot:
    #     test_data, test_label_ground_true = predict_type_formalization(Feat_Rss_clean_test_data_df, predict_type[1],
    #                                                                    withgroundtrue = True)
    #     model = pickle.load(open(mo, 'rb'))
    #     predict_result, predict_probability = fire_in_the_hole(test_data, test_label_ground_true, model,
    #                                                            with_ground_true=True)
        print("****************\n")


if __name__ == '__main__':
    print("execute raw data fetch")
    __main__()