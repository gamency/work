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
from Rohan.Decouple_Captcha import up_down_transf
import sys
from ruamel.yaml import YAML
from pyspark.sql import SparkSession
import os


class Gandalf(object):
    def __init__(self):
        pass

    def