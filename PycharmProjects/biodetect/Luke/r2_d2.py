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
# import pandas as pd
# import matplotlib.pyplot as plt
import time


class r2d2(object):
    def __init__(self, message):
        self.message = message
        # result 0 fail, 1 success
        self.result = 0

    # receive chewbacca signal
    def chewbacca_signal(self):
        # self.data
        return self.message

    # receive chewbacca message
    def solo_message(self):
        # self.data
        return self.message

    # receive quantum message
    def quantum_message(self):
        # self.data
        return self.message

    # receive quantum message
    def destroydeathstart_signal(self):
        # self.data
        return self.message