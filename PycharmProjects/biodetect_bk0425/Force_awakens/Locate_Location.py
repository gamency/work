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


def death_start(inspectation):
    SCENARIOTYPE = {"keynmouse": 1, "mouse": 2, "touchnclick": 3}
    FEATUREMARKET = {"featuremouse": 0, "featurekey": 1, "featuretouch": 2}

    # base on inspectation get the location of death start
    location_set = []

    print("death start located")

    if inspectation == "quantum_prepare good":
        location_set.append("locate death start location")

    return location_set
