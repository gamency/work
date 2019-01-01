# -*- coding: utf-8 -*-
# __author__ = "chao.fang"
from __future__ import unicode_literals, division
import json
import pandas as pd
import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
filepath = os.path.split(os.path.realpath(__file__))[0]


# def numeric_binning(s, val):
#     if (s == u"-999" or s == -999) and val == -999:
#         return True
#     if (s == u"-1" or s == -1) and val == -1:
#         return True
#     if (s == u"-1" or s == -1) and val != -1:
#         return False
#     s = s.strip(" ")
#     _ele = []
#     _ele.append(s[0])  # ["["]
#     _ele.append(s[len(s) - 1])  # ["[","]"]
#     flag = 0
#     val = round(val, 3)
#     if s.find('+') >= 0:
#         _ele.append(float(s[1:len(s) - 1].replace(' ', '').split(",")[0]))
#         if _ele[0] == "(" and _ele[2] < val:
#             flag += 2
#         elif _ele[0] == "[" and _ele[2] <= val:
#             flag += 2
#     elif s.find('+') < 0:
#         _ele.extend([float(x) for x in s[1:len(s) - 1].replace(' ', '').split(",")])
#         if _ele[0] == "(" and _ele[2] < val:
#             flag += 1
#         elif _ele[0] == "[" and _ele[2] <= val:
#             flag += 1
#         if _ele[1] == ")" and _ele[3] > val:
#             flag += 1
#         elif _ele[1] == "]" and _ele[3] >= val:
#             flag += 1
#     if flag == 2:
#         return True
#     else:
#         return False


# def categorical_binning(s, val):
#     # s = s.strip(" ")
#     s = s.strip().split("|")
#     if val in s:
#         return True
#     # elif val == s:
#     #     return True
#     else:
#         return False


# def binning(df_, val):
#     import copy
#     df = copy.copy(df_)
#     var_name = df.iloc[0].tolist()
#     df.index = [x for x in range(df.shape[0])]
#     df = df.drop(0)
#     df.columns = var_name
#     label_ = -1
#     range_ = ''
#     score_ = 0
#
#     # if type(val) == type('') or type(val) == type(u''):
#     if isinstance(val, (str, unicode, bytes)):
#         # 对于有数字的分类信息，如渤海的y_latest_in_amt_min是否有可能有误?
#         # 判断在哪个bin
#         for i in range(len(df)):
#             # if categorical_binning(df.iloc[i][1], val) == True:
#             if categorical_binning(df.iloc[i][1], val):
#                 # 输出label，range和score
#                 label_ = df.iloc[i][0]
#                 range_ = df.iloc[i][1]
#                 score_ = df.iloc[i][2]
#                 return label_, range_, score_
#     # elif type(val) == type(1.0) or type(val) == type(1):
#     elif isinstance(val, (float, int)):
#         for i in range(len(df)):
#             # if numeric_binning(df.iloc[i][1], val) == True:
#             if numeric_binning(df.iloc[i][1], val):
#                 # 输出label，range和score
#                 label_ = df.iloc[i][0]
#                 range_ = df.iloc[i][1]
#                 score_ = df.iloc[i][2]
#                 return label_, range_, score_
#     return label_, range_, score_
def judge_sdf_and_value(value, sdf):
    if isinstance(value, (str, unicode, bytes)):
        # if type(value) in [str, unicode]:
        sdf = sdf.strip(" ")
        if value in sdf:
            return True
        elif value == sdf:
            return True
        else:
            return False
    if isinstance(value, (float, int)):
        # if type(value) in [float, int]:
        value = float(value)
        try:
            sdf = float(sdf)
            return value == sdf
        except ValueError:
            front_boundary = sdf[0]#(
            end_boundary = sdf[-1]#}
            sdf_arr = sdf[1: len(sdf) - 1].split(',') #[-,-1]
            if str(sdf_arr[0]) == '-' or (front_boundary == '(' and value > float(sdf_arr[0])) or \
                    (front_boundary == '[' and value >= float(sdf_arr[0])):
                if sdf_arr[1].strip() == '+' :
                    return True
                else:
                    if (end_boundary == ')' and value < float(sdf_arr[1])) \
                            or (end_boundary == ']' and value <= float(sdf_arr[1])):
                        return True
    return False


def binning(df_, val):
    import copy
    df = copy.copy(df_)
    var_name = df.iloc[0].tolist()
    df.index = [x for x in range(df.shape[0])]
    df = df.drop(0)
    df.columns = var_name
    for i in range(len(df)):
        sdf = df.iloc[i][1]
        if judge_sdf_and_value(val, sdf):
            return df.iloc[i][0], df.iloc[i][1], df.iloc[i][2]

    return -1, '', 0

df_all = pd.read_excel(os.path.join(filepath + "/shoujidai.xlsx"), header=None)

def handle(params):
    import math

    result = {"credit_score": 0}

    df_all[3] = df_all[3].fillna("NaN").map(lambda _: _.upper())

    if params['eazz28000010'] == '-999' or params['eazz28000010'] == -999 \
            or params['gcaz11000011'] == '-999' or params['gcaz11000011'] == -999:
        result['r_eazz28000010'] = ''
        result['r_chzz05001050'] = ''
        result['r_acbz03238011'] = ''
        result['r_gcaz11000011'] = ''
        result['r_bebz00001101'] = ''
        result['r_acbz03001011'] = ''
        result['r_gazz11000040'] = ''
        result['r_chzz04001050'] = ''
        result['r_abzz03132010'] = ''
        result['r_ebzz35000070'] = ''
        result['r_chzz05138061'] = ''
        result['ext_r_ebzz2000005x'] = ''
        result['ext_r_abzz0313202y'] = ''
        result['ext_r_ebzz3900001x'] = ''
        result['r_eazz43000011'] = ''
        result['credit_score'] = 0
        return result
    # df_all[3] = [x.upper() if type(x) == type(u'') else x for x in df_all[3].tolist()]

    #var1:
    df_tmp = df_all[df_all[3] == "eazz28000010".upper()]
    label, range_, score_ = binning(df_tmp, params['eazz28000010'])
    result['r_eazz28000010'] = range_
    result["credit_score"] += score_

    #var2:
    df_tmp = df_all[df_all[3] == "chzz05001050".upper()]
    label, range_, score_ = binning(df_tmp, params['chzz05001050'])
    result['r_chzz05001050'] = range_
    result["credit_score"] += score_

    #var3:
    df_tmp= df_all[df_all[3] == "acbz03238011".upper()]
    label, range_, score_ = binning(df_tmp, params['acbz03238011'])
    result['r_acbz03238011'] = range_
    result["credit_score"] += score_

    #var4:
    df_tmp= df_all[df_all[3] == "gcaz11000011".upper()]
    label, range_, score_ = binning(df_tmp, params['gcaz11000011'])
    result['r_gcaz11000011'] = range_
    result["credit_score"] += score_

    #var5:
    df_tmp = df_all[df_all[3] == "bebz00001101".upper()]
    label, range_, score_ = binning(df_tmp, params['bebz00001101'])
    result['r_bebz00001101'] = range_
    result["credit_score"] += score_

    #var6:
    df_tmp = df_all[df_all[3] == "acbz03001011".upper()]
    label, range_, score_ = binning(df_tmp, params['acbz03001011'])
    result['r_acbz03001011'] = range_
    result["credit_score"] += score_

    #var7:
    df_tmp = df_all[df_all[3] == "gazz11000040".upper()]
    label, range_, score_ = binning(df_tmp, params['gazz11000040'])
    result['r_gazz11000040'] = range_
    result["credit_score"] += score_

    #var8:
    df_tmp = df_all[df_all[3] == "chzz04001050".upper()]
    label, range_, score_ = binning(df_tmp, params['chzz04001050'])
    result['r_chzz04001050'] = range_
    result["credit_score"] += score_

    #var9:
    df_tmp = df_all[df_all[3] == "abzz03132010".upper()]
    label, range_, score_ = binning(df_tmp, params['abzz03132010'])
    result['r_abzz03132010'] = range_
    result["credit_score"] += score_


    #var10:
    df_tmp = df_all[df_all[3] == "ebzz35000070".upper()]
    label, range_, score_ = binning(df_tmp, params['ebzz35000070'])
    result['r_ebzz35000070'] = range_
    result["credit_score"] += score_

    #var11:
    df_tmp = df_all[df_all[3] == "chzz05138061".upper()]
    label, range_, score_ = binning(df_tmp, params['chzz05138061'])
    result['r_chzz05138061'] = range_
    result["credit_score"] += score_

    #var 12: max(params['ebzz20000050'], params['ebzz20000051'])
    if params['ebzz20000050'] == -1111.0 and params['ebzz20000051'] != -1111.0:
        EBZZ2000005X_max = params['ebzz20000051']
    elif params['ebzz20000050'] != -1111.0 and params['ebzz20000051'] == -1111.0:
        EBZZ2000005X_max = params['ebzz20000050']
    else:
        EBZZ2000005X_max = max(params['ebzz20000050'], params['ebzz20000051'])
    # return EBZZ2000005X_max

    df_tmp = df_all[df_all[3] == "ebzz20000050".upper()]
    label, range_, score_ = binning(df_tmp, EBZZ2000005X_max)
    result['ext_r_ebzz2000005x'] = range_
    result["credit_score"] += score_

    #var 13: params['abzz03132020'] - params['abzz03132021']
    if params['abzz03132020'] == -1111.0 or params['abzz03132021'] == -1111.0:
        ABZZ0313202Y = -1111.0
    else:
        ABZZ0313202Y = params['abzz03132020'] - params['abzz03132021']
    # return ABZZ0313202Y

    df_tmp = df_all[df_all[3] == "abzz0313202y".upper()]
    label, range_, score_ = binning(df_tmp, ABZZ0313202Y)
    result['ext_r_abzz0313202y'] = range_
    result["credit_score"] += score_

    #var 14: max(params['ebzz39000010'], params['ebzz39000011'])
    if params['ebzz39000010'] == -1111.0 and params['ebzz39000011'] != -1111.0:
        EBZZ3900001X_max = params['ebzz39000011']
    elif params['ebzz39000010'] != -1111.0 and params['ebzz39000011'] == -1111.0:
        EBZZ3900001X_max = params['ebzz39000010']
    else:
        EBZZ3900001X_max = max(params['ebzz39000010'], params['ebzz39000011'])
    # return EBZZ3900001X_max

    df_tmp = df_all[df_all[3] == "ebzz39000010".upper()]
    label, range_, score_ = binning(df_tmp, EBZZ3900001X_max)
    result['ext_r_ebzz3900001x'] = range_
    result["credit_score"] += score_

    #var 15:
    df_tmp = df_all[df_all[3] == "eazz43000011".upper()]
    label, range_, score_ = binning(df_tmp, params['eazz43000011'])
    result['r_eazz43000011'] = range_
    result["credit_score"] += score_


    return result

