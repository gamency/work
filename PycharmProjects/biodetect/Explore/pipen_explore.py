# import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import time
import os
from Sauron.Eye_of_Sauron import eye

message = {"scenario": -1, "terminal": -1, "success": 1}
# FIRST_STAGE_TRACE_NAME = ['Time', 'key_event_type', 'dialog_type', 'mouse_event_type', 'op_x', 'op_y', 'Action']
FIRST_STAGE_TRACE_NAME = ['Time', 'mouse_event_type', 'op_x', 'op_y', 'Action']
# FIRST_STAGE_TRACE_NAME = ['c', 'y', 'p', 'u', 'k', 'o', 'n']
FIRST_STAGE_TRACE_INFORMARION_NAME = ["first_x", "first_y", "second_x", "second_y", "scenario", "terminal", 'Bot']

SECOND_STAGE_TRACE_NAME = ['Time', 'event_type', 'op_x', 'op_y', 'Action']
# SECOND_STAGE_TRACE_NAME = ['c', 'u', 'k', 'o', 'n']
SECOND_STAGE_TRACE_INFORMATION_NAME = ['correct_x', 'correct_y', 'slidebarleft_x', 'slidebarleft_y',
                                       'slidebarright_x', 'slidebarright_y', "scenario", "terminal", 'Bot']


def military_name():
    series = ['dx', 'tacc', 'cur', 'curroc']
    construction = ['tm', 'tra', 'tsk', 'tku', 'fshm', 'fshstd2', 'fshsk', 'fshku', 'fv', 'fsk', 'fkur']
    mn = []
    for i in series:
        for j in construction:
            mn.append(str(i + "_" + j))
    mn.append("hbc")
    mn.append("Bot")
    return mn


def fetch_file_name(file_dir):
    data_file_names = []
    for root, dirs, files in os.walk(file_dir):
        data_file_names = files.copy()
    if '.DS_Store' in data_file_names:
        data_file_names.remove('.DS_Store')
    return data_file_names


def colon_soldier(base_location):
    # read in files for colon
    data_file_names = fetch_file_name(base_location)

    # for every colon seed, calling lightsaber
    colon_collection = []
    for item in data_file_names:
        print("_____start____", item)
        colon_location = base_location + '/' + str(item)
        colon_seed = open(colon_location, 'r')

        colon_df = pd.read_csv(colon_seed)

        # visualize the data
        # eye(colon_df)

        # colon_item = lightsaber(colon_df)
        colon_collection.append(colon_df)

    print(colon_collection)
    print(len(colon_collection))

    return colon_collection


def pipen_travel(colon_collection):

    for i in range(0, len(colon_collection)):
        colon_seed = colon_collection[i]

        # method of explore


def main():
    print("come of jedi")
    start_time = time.time()
    # data = pd.read_csv("../Data/1515396437520_2_1_human.csv")
    # # data = pd.DataFrame()
    # result = lightsaber(data)
    # print("the final result is: ", result)

    # base_dir = "/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/First"

    # base_dir = "/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/FirstBig"
    # scenario = 0
    base_dir = "/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/secondBig"
    # base_dir = "/Users/kite/Desktop/Mobile_verify/Data/trainData/H5/SecondBig"
    # scenario = 1
    result = colon_soldier(base_dir)

    print("duration is: ", time.time() - start_time)


if __name__ == '__main__':
    main()
