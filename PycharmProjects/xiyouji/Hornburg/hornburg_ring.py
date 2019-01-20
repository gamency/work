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
from Rohan import Cavalry
import sys
from ruamel.yaml import YAML
from pyspark.sql import SparkSession
import os


class HornBurg(object):
    def __init__(self, data, fetch_data_table,  partner_set, bussiness_type):
        self.data = data
        pass

    def ring_type(self):
        return 1
        pass

    def river_hole(self):
        return 1
        pass

    def mall(self):
        relief_troops = Cavalry.RohanCavlry(fetch_data_info, 'bigdata.raw_activity_flat', 'verification', 'captcha')

        result1, result2 = relief_troops.form()

        signal_1 = self.ring_type()
        signal_2 = self.river_hole()
        pass


def mian():
    file_y = '/Users/kite/Desktop/test.yml'
    yaml = YAML()
    cav_info = open(file_y).read()
    cav = yaml.load(cav_info)
    fetch_data_info = [cav['year'], cav['start_month'], cav['end_month'], cav['start_day'], cav['end_day'],
                       cav['PC_data_dir'], cav['Andriod_second_dir'], cav['Terminal']]

    test = RohanCavlry(fetch_data_info, 'bigdata.raw_activity_flat', 'verification', 'captcha')

    test.form()
    result1, result2 = test.parse_captcha()
    # print(result.head())
    pass


if __name__ == 'main':
    main()
    pass