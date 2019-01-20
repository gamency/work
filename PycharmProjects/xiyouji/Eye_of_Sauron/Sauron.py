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
import matplotlib.pyplot as plt
import sys
from ruamel.yaml import YAML
import os
plt.style.use('ggplot')


class Palantir(object):
    def __init__(self, data):
        self.df = data
        self.scenario = self.df[0].loc[0, 'scenario']

    def value_calculate(self):
        # define the mapping rule
        pass

    def value_transform(self):
        big_df = []
        for i in range(0, len(self.df)):
            slice_info = self.df[i].loc[0, ['Time', 'Bot']]
            big_df.append(slice_info)

        # choise by time

        return big_df
        pass

    def dealing(self):
        # return first_phase_reject, first_phase_accept, second_phase_reject, second_phase_accept
        # return
        slice_df = self.value_transform()
        plot_data = pd.DataFrame(slice_df)

        plt.figure(figsize=(10, 10))
        plt.scatter(range(0, len(plot_data)), plot_data['Bot'], marker='o',c='',edgecolors='green')
        if self.scenario == 0:
            plt.plot([0, len(plot_data)], [0.69, 0.69], c='red')
            plt.plot([0, len(plot_data)], [0.89623, 0.89623], c='red')
        else:
            plt.plot([0, len(plot_data)], [0.58, 0.58], c='red')
            plt.plot([0, len(plot_data)], [0.89623, 0.89623], c='red')
        plt.show()
        pass

    def mall(self):
        # fetch 4 zone data
        # transform the data
        #  call dealing
        pass

    def statistics_info(self):
        tmp_data = self.value_transform()
        plot_data = pd.DataFrame(tmp_data, index=None)
        plot_data[['Time', 'Bot']] = plot_data[['Time', 'Bot']].astype(float)
        bot_data = plot_data['Bot']

        if self.scenario == 0:
            accept_count = sum(plot_data['Bot'] < 0.691131498470948)
            reject_count = sum(plot_data['Bot'] > 0.691131498470948)
        else:
            accept_count = sum(plot_data['Bot'] < 0.58)
            reject_count = sum(plot_data['Bot'] > 0.58)
        pass_ratial = float(accept_count) / len(plot_data)
        less_than_4point = sum(plot_data['Bot'] == 0.89632)

        plt.figure(figsize=(6, 9))
        labels = ['Accept', 'Reject']
        sizes = [accept_count, reject_count]
        colors = ['yellowgreen', 'red']
        explode = (0, 0.02)
        patches, text1, text2 = plt.pie(sizes, explode=explode, labels=labels, colors=colors, labeldistance=1.2,
                                        autopct='%3.2f%%', shadow=False, startangle=90, pctdistance=0.6)
        plt.axis('equal')
        if self.scenario == 0:
            plt.title('Phase 1')
        else:
            plt.title("Phase 2")
        plt.legend()
        plt.show()


def main():
    # data
    test = Palantir(data)
    # test.value_transform()
    # plot
    test.dealing()
    pass


if __name__ == '__main__':
    pass
