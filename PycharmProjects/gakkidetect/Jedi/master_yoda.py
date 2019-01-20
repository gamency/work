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

# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import time
# import pickle


class yoda(object):
    def __init__(self, jedis, message, model):
        self.data = jedis
        self.message = message
        self.jedi = ""
        self.model = model

    def jedi_training(self):
        pass
        # return

    def jedi_perform(self):
        # pass
        # if use xgboost dmatirx form uncomment follow
        # preds = self.model.predict_proba(self.data)
        # import xgboost as xgb
        # dtest = xgb.DMatrix(self.data)
        # preds = self.model.predict(dtest)
        # if use xgboost classifier uncomment below
        preds = self.model.predict_proba(self.data)[:, 1]
        # if use rf, uncomment below
        # self.data = self.data.replace([np.inf, -np.inf], np.nan)
        # self.data = self.data.fillna(0)
        # preds = self.model.predict_proba(self.data)[:,1]
        # return preds[0, 1]
        return preds

    def dagobath(self):
        jedi_message = []
        if self.message[0] == "bomb is good":
            # start finding yoda
            # from Jedi.jedi_Temple import jedi_temple
            # self.jedi = jedi_temple(self.message[0])
            jedi_result = self.jedi_perform()
            jedi_message.append("jedi is good")
            # print("jedi success invade!")
            # pass
        return jedi_message, jedi_result
