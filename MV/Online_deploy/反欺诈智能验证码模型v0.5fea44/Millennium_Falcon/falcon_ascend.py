# import numpy as np
# import pandas as pd

# from CCM.ccm import

message = {"scenario": -1, "terminal": -1, "success": -1}

# FIRST_STAGE_TRACE_NAME = ['Time', 'key_event_type', 'dialog_type', 'mouse_event_type', 'op_x', 'op_y', 'Action']
FIRST_STAGE_TRACE_NAME = ['Time',  'mouse_event_type', 'op_x', 'op_y', 'Action']

FIRST_STAGE_TRACE_INFORMARION_NAME = ["first_x", "first_y", "second_x", "second_y", 'Bot']

SECOND_STAGE_TRACE_NAME = ['Time', 'event_type', 'op_x', 'op_y', 'Action']
SECOND_STAGE_TRACE_INFORMATION_NAME = ['correct_x', 'correct_y', 'slidebarleft_x', 'slidebarleft_y',
                                       'slidebarright_x', 'slidebarright_y', 'Bot']


class MillenniumFalcon(object):
    def __init__(self, raw_dataframe, scenario):
        self.df = raw_dataframe
        # result 0 fail, 1 success
        self.result = 0
        self.message = {"scenario": -1, "terminal": -1, "success": -1}
        self.scenario = scenario

    # check data format
    def chewbacca_check(self):
        # self.df
        # print("chewbacca start check the Falcon")

        if len(self.df) <= 2:
            self.result = 0
        else:
            self.result = 1

        # print("chewbacca end check of Falcon")
        return self.result

    # check data length
    def solo_check(self):
        # solo use self.df to generlize what this data is ,
        # output 3 contents: 1. this data is which stage,  first, second
        #                    2. it's scenario, pc, mobile(only happen at second stage)
        #                    3. check result message
        #                    4. prepare dataframe
        # print("solo start check the Falcon")

        # columns_name = list(self.df.columns)
        # stage = -1
        if  self.scenario == 0:
            self.message["scenario"] = 0
            self.message["terminal"] = 0
            self.result = 1
        elif self.scenario == 1:
            self.message["scenario"] = 1
            self.message["terminal"] = 0
            self.result = 1
        else:
            print("wrong data type")
            self.result = 0

        # print("solo end check of Falcon")
        return self.result

    # dealing with missing data
    def quantum_prepare(self):
        # self.df
        # print("quantum start prepare the Falcon")

        if self.message['scenario'] == 0:
            # trace_information = self.df.loc[0, FIRST_STAGE_TRACE_INFORMARION_NAME]
            self.df = self.df.loc[0:, FIRST_STAGE_TRACE_NAME]
            self.message['success'] = 1
        elif self.message['scenario'] == 1:
            # trace_information = self.df.loc[0, SECOND_STAGE_TRACE_INFORMATION_NAME]
            self.df = self.df.loc[0:, SECOND_STAGE_TRACE_NAME]
            self.message['success'] = 1

        # print("quantum end prepare of Falcon")
        return self.df

    def ascend(self):
        # print("Millennium Falcon start to ascend")
        # if self.chewbacca_check() == 0:
        #     return self.result
        # elif self.solo_check() == 0:
        #     return self.result
        # else:
        #     preprocess_dataframe = self.quantum_prepare()
        #     return self.message, preprocess_dataframe
        preprocess_dataframe = self.quantum_prepare()
        return self.message, preprocess_dataframe


def main():
    # print("Millennium Falcon start to ascend")
    # track = millenniumFalcon(raw_dataframe).ascend()
    pass


if __name__ == '__main__':
    # main()
    pass