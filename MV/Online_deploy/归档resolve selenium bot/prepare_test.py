#-*- coding:utf8 -*-
#### 1.所有编码格式统一为utf-8
import sys
import os
import execute_model
import xml.dom.minidom
import simplejson as json
import types

reload(sys)
sys.setdefaultencoding("utf-8")

#### 2.获取文件路径
filepath = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(filepath)

def read_xml():
    dom = xml.dom.minidom.parse(filepath+'/params_spec.xml')
    root = dom.documentElement
    inparams = root.getElementsByTagName("inparams")[0]
    argType = inparams.getAttribute("type")
    inparamList = inparams.getElementsByTagName("inparam")

    result={"type":argType}
    inputList=[]
    for inparam in inparamList:
        defaultValue = None
        if len(inparam.getElementsByTagName("defaultValue")) >0 :
            if len(inparam.getElementsByTagName("defaultValue")[0].childNodes)>0 :
                defaultValue =inparam.getElementsByTagName("defaultValue")[0].childNodes[0].nodeValue;
        inparamMap={"defaultValue":defaultValue,"name":inparam.getElementsByTagName("name")[0].childNodes[0].nodeValue,"datatype":inparam.getElementsByTagName("datatype")[0].childNodes[0].nodeValue}
        inputList.append(inparamMap)
    result["inputList"]=inputList
    return result

def transformParamData(inputValue,dataType,defalueValue):
    if "double" == dataType:
        try:
            return float(inputValue)
        except Exception, e:
            print "转化参数",inputValue,"出错",e.message
            try:
                return float(defalueValue)
            except Exception, e:
                return float(0)
    elif "int" == dataType:
        try:
            return int(float(inputValue))
        except Exception, e:
            print "转化参数",inputValue,"出错",e.message
            try:
                return int(float(defalueValue))
            except Exception, e:
                return int(0)
    elif "boolean" == dataType:
        try:
            return inputValue == str(True)
        except Exception, e:
            print "转化参数", inputValue, "出错", e.message
            try:
                return defalueValue == str(True)
            except Exception, e:
                return False
    else:
        try:
            if inputValue == None:
                return None
            return str(inputValue)
        except Exception, e:
            print "转化参数", inputValue, "出错", e.message
            try:
                if defalueValue == None:
                    return None
                return str(defalueValue)
            except Exception, e:
                print "转化参数", inputValue, "出错", e.message
                return None
def handle_test_data(inparam):
    inputMap = read_xml()
    argType=inputMap["type"]
    inputList =inputMap["inputList"]

    if "list" == argType:
        if len(inparam) != len(inputList):
            raise Exception("params_spec.xml文件中入参长度与实际测试入参长度不一致")

        if type(inparam) is not types.ListType:
            raise Exception("params_spec.xml文件中type类型为list，而实际测试入参不是list类型")
        for i in range(0,len(inparam)):
            # print inputList[i]["name"],inparam[i],transformParamData(inparam[i],inputList[i]["datatype"],inputList[i]["defaultValue"])
            inparam[i] = transformParamData(inparam[i],inputList[i]["datatype"],inputList[i]["defaultValue"])
    elif "map" == argType:
        if len(inparam) != len(inputList):
            raise Exception("params_spec.xml文件中入参长度与实际测试入参长度不一致")

        if type(inparam) is not types.DictType:
            raise Exception("params_spec.xml文件中type类型为map，而实际测试入参不是map类型")
        for input in inputList:
            if not inparam.has_key(input["name"]):
                raise Exception("params_spec.xml中inparam,name="+input['name']+"在测试入参中不存在")
            inputValue = inparam[input["name"]]
            inparam[input["name"]] = transformParamData(inputValue,input["datatype"],input["defaultValue"])
    else:
        raise Exception("params_spec.xml文件中type类型目前只支持map、list两种类型")
    return json.dumps(inparam)

if __name__ == "__main__":
    # 测试入参_
    # data = sys.argv[1]
    test_data = {"event_info": "{\"Action\":[\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"12\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"13\"],\"event_type\":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\"Time\":[1520589717344,1520589717360,1520589717377,1520589717393,1520589717427,1520589717461,1520589717477,1520589717494,1520589717510,1520589717527,1520589717543,1520589717561,1520589717576,1520589717593,1520589717610,1520589717626,1520589717767,1520589717777,1520589717794,1520589717810,1520589717827,1520589717843,1520589717859,1520589717961,1520589718010,1520589718027,1520589718043,1520589718061,1520589718081,1520589718093,1520589718111,1520589718126,1520589718143,1520589718160,1520589718209,1520589718277,1520589718293,1520589718310,1520589718327,1520589718343,1520589718359,1520589718377,1520589718393,1520589718411,1520589718460,1520589718491,1520589718593,1520589718596,1520589718610,1520589718610,1520589718627,1520589718628,1520589718643,1520589718645,1520589718660,1520589718661,1520589718677,1520589718678,1520589718693,1520589718694,1520589718709,1520589718711,1520589718727,1520589718728,1520589718744,1520589718745,1520589718894,1520589718894,1520589718910,1520589718910,1520589718928,1520589718929,1520589718943,1520589718944,1520589718977,1520589718977,1520589718993,1520589718994,1520589719011,1520589719011,1520589719043,1520589719044,1520589719076,1520589719079,1520589719179,1520589719183,1520589719227,1520589719228,1520589719277,1520589719278,1520589719310,1520589719311,1520589719327,1520589719328,1520589719344,1520589719345,1520589719360,1520589719361,1520589719377,1520589719378,1520589719394,1520589719394,1520589719410,1520589719411,1520589719428,1520589719431,1520589719938],\"op_x\":[295,295,295,295,295,295,296,297,301,308,321,339,363,388,401,404,408,420,436,471,497,517,528,536,538,543,548,560,569,574,578,580,580,581,580,579,578,576,573,570,569,568,566,566,565,565,566,566,570,570,580,580,593,593,611,611,632,632,648,648,665,665,673,673,679,679,683,683,688,688,693,693,701,701,710,710,711,711,711,711,712,712,713,713,714,714,715,715,716,716,717,717,718,718,719,719,720,720,721,721,722,722,724,724,725,725,725],\"op_y\":[1147,1146,1145,1144,1144,1143,1143,1141,1140,1136,1131,1127,1125,1124,1124,1124,1124,1124,1124,1124,1126,1130,1133,1137,1137,1139,1144,1155,1162,1168,1174,1177,1180,1181,1181,1181,1181,1181,1182,1182,1182,1182,1182,1182,1182,1182,1182,1182,1182,1182,1182,1182,1182,1182,1182,1182,1180,1180,1180,1180,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178,1178]}","true_info": "{\"correct_y\":986,\"correct_x\":708,\"scenario\":1,\"slidebarleft_x\":534,\"slidebarleft_y\":1162,\"slidebarright_y\":1202,\"terminal\":0,\"slidebarright_x\":576}"}
    inparams = handle_test_data(test_data)
    print "入参",inparams
    print "出参",execute_model.execute_model(inparams)