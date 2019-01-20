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


import os

TwoClass_file_dir = './Model/TwoClass'
ThreeClassStationary_file_dir = './Model/ThreeClassStationary'
SixClass_file_dir = './Model/SixClass'


def model_select(model_scenario):
    market_dir = ''
    model_bill = []
    if model_scenario == 'TwoClass':
        market_dir = TwoClass_file_dir
    elif model_scenario == 'ThreeClassStationary':
        market_dir = ThreeClassStationary_file_dir
    else:
        market_dir = SixClass_file_dir

    for root, dirs, files in os.walk(market_dir):
        model_bill = files.copy()

    return model_bill

# print(model_select('ThreeClassStationary'))
