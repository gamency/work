# -*- encoding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# get id_gender
def get_gender(uid):# 1为男性
    length = len(uid)
    if length == 18 and uid[16].isdigit():
        gender = int(uid[16]) % 2
    elif length == 15 and uid[14].isdigit():
        gender = int(uid[14]) % 2
    else:
        gender = -1111
    return gender

def get_province(uid):
    area_dic = {11: u'BJ', 12: u'TJ', 13: u'HE', 14: u'SX', 15: u'IM', 21: u'LN', 22: u'JL', 23: u'HL', 31: u'SH', 32: u'JS', 33: u'ZJ', 34: u'AH', 35: u'FJ',
            36: u'JX', 37: u'SD', 41: u'HA', 42: u'HB', 43: u'HN', 44: u'GD', 45: u'GX', 46: u'HI', 50: u'CQ', 51: u'SC', 52: u'GZ', 53: u'YN', 54: u'XZ',
            61: u'SN', 62: u'GS', 63: u'QH', 64: u'NX', 65: u'XJ', 71: u'TW', 81: u'HK', 82: u'MO'}
    if uid[:2].isdigit() and int(uid[:2]) in area_dic:
        province = area_dic[int(uid[:2])]
    else:
        province = -1111
    return province


    
# woe dict
WOE_dict_uid={
    'BAZZ01030010': {'(0.0,1.0)': 0.812799892785,
                     '(2.0,inf)': -1.552214107280},
    'EAZZ29000010': {'(0.0,0.0)': 0.736255075041,
                     '(1.0,2.0)': -0.936069166055,
                     '(3.0,inf)': -2.864537873270},
    'EBZZ26000010': {'(0.0,0.0)': 1.344810731880,
                     '(1.0,1.0)': -0.449021590798,
                     '(2.0,inf)': -1.872932310410},
    'id_age':{'(0.0,24.0)': -0.584240751000 ,
           '(25.0,31.0)': -0.099102664000 ,
           '(32.0,39.0)': 0.111707218000,
           '(40.0,49.0)': 0.484288576000,
           '(50.0,inf)': 0.909424168000},
    'id_gender':{'(1.0,1.0)': -0.212891680318,
              '(0.0,0.0)': 0.647969589484}
}


WOE_dict_mob={
    'GEZZ00000011': {'(-1111.0,-1111.0)': 2.747453058,
                     '(0.0,7.0)': 1.253878553,
                     '(8.0,15.0)': 0.512032064,
                     '(16.0,79.0)': -0.412041277,
                     '(79.0,inf)': -2.01312604},
    'BEAZ00100011': {'(0.0,0.0)': 1.635136087,
                     '(1.0,1.0)': 0.572107147,
                     '(2.0,2.0)': -0.918449228,
                     '(3.0,inf)': -2.249964237},
    'ACBZ03130011': {'(-1111.0,-1111.0)': 2.752983634,
                     '(0.0,0.0417)': 0.977235419,
                     '(0.0418,0.25)': -0.478911566,
                     '(0.2501,0.3333)': -0.718851291,
                     '(0.3334,1.0)': -1.567280519},
     'ABZZ05100011': {'(0.0,0.0)': 1.635178324,
                      '(1.0,1.0)': 0.358586611,
                      '(2.0,inf)': -1.921024965},
     'CHZZ04138011': {'(-1111.0,-1111.0)': 1.133660411,
                      '(0.0,0.0)': 0.389368914,
                      '(0.0001,inf)': -1.055865755},
     'EAZZ29000011': {'(0.0,0.0)': 0.876463767,
                      '(1.0,inf)': -1.259441002},
     'EBZZ25000011': {'(0.0,0.0)': 0.907879677,
                      '(1.0,inf)': -1.157807344},
     'ABZZ03008081': {'(0.0,0.0)': 0.65906324,
                      '(1.0,inf)': -0.966065267},
     'ACBZ03036011': {'(-1111.0,0.1667)': -0.234393448,
                      '(0.1668,0.4)': 0.882858537,
                      '(0.4001,1.0)': 1.797721963}}

# woe replace
def select_para_woe_uid(key, value):
    woe=0
    if key in WOE_dict_uid.keys():
        n = round(float(value),4)
        woe_map_list = WOE_dict_uid[key].keys()
        woe_map_list.sort()
        for t in woe_map_list:
            if 'inf' in t:
                if n >= float(t.replace('(','').replace(')','').split(',')[0]):
                    woe= float(WOE_dict_uid[key][t])
                    break
            else:    
                if eval(t)[0] <= n <= eval(t)[1]:
                    woe= float(WOE_dict_uid[key][t])
                    break
    return woe

def province2woe(x):
    if x in ['JS','HE','FJ','XJ','SD','SN','HL','NX','IM','JL','CQ']:
        return -0.373362605
    elif x in ['GS','SX','LN','SH','HA','GX','YN','TJ']:
        return -0.024217413
    elif x in ['HI','HN','AH','SC','HB']:
        return 0.167414649
    elif x in ['JX','GD','GZ']:
        return 0.309449282
    else:
        return 0.765823007



def select_para_woe_mob(key, value):
    woe=0
    if key in WOE_dict_mob.keys():
        n = round(float(value),4)
        woe_map_list = WOE_dict_mob[key].keys()
        woe_map_list.sort()
        for t in woe_map_list:
            if 'inf' in t:
                if n >= float(t.replace('(','').replace(')','').split(',')[0]):
                    woe= float(WOE_dict_mob[key][t])
                    break
            else:
                if eval(t)[0] <= n <= eval(t)[1]:
                    woe= float(WOE_dict_mob[key][t])
                    break
    return woe

# get score
def cuts(x,s1,s2):
    if x<=s1:
        return s1
    elif x>=s2:
        return s2
    else:
        return x

def get_score_uid(x):
    c1 = {
        'EBZZ26000010': -0.4110,
        'EAZZ29000010': -0.5857,
        'BAZZ01030010': -0.4767,
        'id_age': -0.0541,
        'id_gender': -0.5555,
        'id_province': -0.6357,
        'intercept': -2.9783
}
    woe=x
    woe['intercept'] = 1
    sum_score = 0
    for p in c1:
        if woe.get(p) is None:
            woe_score = 0
        else:
            woe_score = woe.get(p)
        sum_score += c1[p] * woe_score
    score = int(600 - 288.53900817779271 * sum_score)
    score1=cuts(score,1147,2038)
    score2=int(score1 * 0.6734006734006734 - 472.3905723905724)
    score_id=cuts(score2,300,900)
    return score_id


def get_score_mob(x):
    c1 = {
        'EBZZ25000011': -0.0297,
        'ACBZ03036011': -0.5749,
        'ABZZ05100011': -0.3885,
        'CHZZ04138011': -0.1565,
        'EAZZ29000011': -0.2016,
        'GEZZ00000011': -0.3132,
        'ACBZ03130011': -0.3068,
        'ABZZ03008081': -0.0484,
        'BEAZ00100011': -0.0205,
        'intercept': -2.8433
}
    woe=x
    woe['intercept'] = 1
    sum_score = 0
    for p in c1:
        if woe.get(p) is None:
            woe_score = 0
        else:
            woe_score = woe.get(p)
        sum_score += c1[p] * woe_score
    score = int(600 - 288.53900817779271 * sum_score)
    score1 = cuts(score,958,1795)
    score2 = int(1.0027 * score1 + 117.4865) # 线性拟合
    score3 = int(0.7151370679380215 * score2 - 470.91775923718717)
    score_mob=cuts(score3,300,900)
    return score_mob

def get_ori_score(params,uid,mob):
    params_id=[k for k in params if k in uid]
    params_mob = [k for k in params if k in mob]
    score={}
    result = {}
    # 获得初版模型分数，id_score & mobile_score
    if str(params['BAZZ01030010']) == '-999.0' or str(params['EAZZ29000010']) == '-999.0' or str(params['EBZZ26000010']) == '-999.0' or str(params['id_number']) == '' or str(params['id_age']) == '-999': 
       score['id_score']=-1
    else:
        params['id_gender']=get_gender(params['id_number'])
        params['id_province']=get_province(params['id_number'])
        for param in params_id:
            if param =='id_province':
                result[param] = province2woe(params[param])
            else:
                result[param] = select_para_woe_uid(param, params[param])
        score['id_score'] = get_score_uid(result)
    result_mob={}
    if str(params['GEZZ00000011']) == '-999.0' or str(params['BEAZ00100011']) == '-999.0' or str(params['ACBZ03130011']) == '-999.0' or str(params['ABZZ05100011']) == '-999.0' or str(params['CHZZ04138011']) == '-999.0' or str(params['EAZZ29000011']) == '-999.0' or str(params['EBZZ25000011']) == '-999.0' or str(params['ABZZ03008081']) == '-999.0' or str(params['ACBZ03036011']) == '-999.0': 
        score['mobile_score']=-1
    else:
        for param in params_mob:
            result_mob[param] = select_para_woe_mob(param, params[param])
        score['mobile_score'] = get_score_mob(result_mob)
    return score
    
def modify_ori_score(params,score):
    # 三方数据增加覆盖度
    if (str(params['y_latest_in_amt_min']) != '-999.0') & (score['id_score'] == -1):
        score['id_score'] = 666
    if str(params['assbalv9']) != '-999.0':
        if score['id_score'] == -1:
            score['id_score'] = 666
        if score['mobile_score'] == -1:
            score['mobile_score'] = 824
    
    # 黑灰名单增加覆盖度及高分调整
    if (str(params['ILZZ00000000']) == '1')|(str(params['ILZZ00000001']) == '1'):# 命中黑名单
        if (score['id_score'] >513)|(score['id_score']==-1):
            score['id_score'] = 513
        if (score['mobile_score']>642)|(score['mobile_score']==-1):
            score['mobile_score'] = 642
    elif (str(params['ILZZ01000000']) == '1') & (str(params['ILZZ01000001']) == '1'):# 非黑但灰
        if (score['id_score'] >666)|(score['id_score']==-1):
            score['id_score'] = 666
        if (score['mobile_score']>824)|(score['mobile_score']==-1):
            score['mobile_score'] = 824
    return score
    
def get_person_score(score):
    # id缺失，用mob分数
    if (score['id_score'] < 0) & (score['mobile_score'] > 0):
        score['person_score'] = score['mobile_score']
    if (score['id_score'] < 0) & (score['mobile_score'] < 0):
        score['person_score'] = 697 # 都缺失，用50%分位点分数
    if (score['id_score'] > 0) & (score['mobile_score'] < 0):
        score['person_score'] = score['id_score'] # mob缺失，用手机号分数
    if (score['id_score'] > 0) & (score['mobile_score'] > 0): # 都不缺失，加权
            score['person_score']=int(score['id_score']*0.8 + score['mobile_score']*0.2)
    return score

def modify_score(params,score):
    score1=get_person_score(score)
    # 内部数据减分
    if str(params['YLZZ02000000']) == '1':
        score1['person_score']=score1['person_score'] - 60
    if str(params['YLZZ01000000']) == '1':
        score1['person_score']=score1['person_score'] - 60
    if str(params['YLZZ03000000']) == '1':
        score1['person_score']=score1['person_score'] - 150
    if str(params['YLZZ04000000']) == '0':
        score1['person_score']=score1['person_score'] - 80
    score1['person_score'] = cuts(score1['person_score'],300,900)
    # 婚姻状况加分
    marriage_dict={u'未婚':12,u'已婚':36,u'离异':18,u'丧偶':24,u'其他':12}
    if params['marriage'] in marriage_dict:
        score1['person_score']=score1['person_score']+int(marriage_dict[params['marriage']])
    else:
        score1['person_score']=score1['person_score']+12 # 不在dict里面做其他处理
    return score1
    
    
def get_loan_score(params,score):
    score['loan_score'] = 300
    # 缺失返回-1
    if str(params['down_payment_percent'])=='-999.0' or str(params['balance_payment_percent'])=='-999.0' or str(params['loan_term'])=='-999.0':
        score['loan_score']=-1
    # 首付比例
    def get_down_payment(x):
        if x==0:
            return 34
        elif x<=0.1:
            return 102
        elif x<=0.2:
            return 170
        elif x<=0.3:
            return 272
        else:
            return 340
    score['loan_score']=score['loan_score'] + int(get_down_payment(params['down_payment_percent']))
    # 贷款期限
    def get_loan_term(loan_term,loan_term_unit): # 默认为MONTH，支持DAY
        if loan_term_unit=='DAY':
            if loan_term <= 360:
                return 136
            elif loan_term <= 540:
                return 102
            elif loan_term <= 720:
                return 68
            elif loan_term <= 1080:
                return 34
            else:
                return 0
        else:
            if loan_term <= 12:
                return 136
            elif loan_term <= 18:
                return 102
            elif loan_term <= 24:
                return 68
            elif loan_term <= 36:
                return 34
            else:
                return 0
    score['loan_score']=score['loan_score'] + int(get_loan_term(params['loan_term'],params['loan_term_unit']))
    # 尾款比例
    def get_balance_payment(x):
        if x==0:
            return 119
        elif x<=0.2:
            return 85
        elif x<=0.5:
            return 51
        else:
            return 0
    score['loan_score']=score['loan_score'] + int(get_balance_payment(params['balance_payment_percent']))
    if score['loan_score']<=334:
        score['loan_score'] = 300
    if score['loan_score']>=895:
        score['loan_score'] = 900
    # score['type_down_parment']=str(type(params['balance_payment_percent']))
    return score            
                
def get_car_score(params,score):
    score['car_score']=0
    params['car_index']=0 # 若不在list，按0类别（最低分，默认值）算
    # 品牌, 大众型-普通	3 大众型-豪华 2 小众-普通 1 小众-豪华 0
    brand_score_dict={3:360,2:240,1:120,0:120}
    # brand_dict={'Jeep':0,'WEY':0,u'宝骏':0,u'北汽道达':0,u'北汽幻速':0,u'北汽绅宝':0,u'北汽威旺':0,
    #    u'北汽新能源':0,u'北汽制造':0,u'奔腾':0,u'本田':0,u'比速汽车':0,u'比亚迪':0,u'标致':0,u'别克':0,
    #    u'昌河':0,u'成功汽车':0,u'大发':0,u'大众':0,u'电咖':0,u'东风':0,u'东风风度':0,u'东风风光':0,
    #    u'东风风行':0,u'东风风神':0,u'东风小康':0,u'东南':0,u'菲亚特':0,u'丰田':0,u'福特':0,u'福田':0,
    #    u'福田乘用车':0,u'观致':0,u'广汽传祺':0,u'广汽吉奥':0,u'国金汽车':0,u'哈飞':0,u'哈弗':0,u'海格':0,
    #    u'海马':0,u'汉腾汽车':0,u'恒天':0,u'红旗':0,u'华凯':0,u'华普':0,u'华骐':0,u'华颂':0,u'华泰':0,
    #    u'华泰新能源':0,u'黄海':0,u'吉利汽车':0,u'江淮':0,u'江铃':0,u'江铃集团轻汽':0,u'江铃集团新能源':0,
    #    u'金杯':0,u'金龙':0,u'金旅':0,u'九龙':0,u'君马汽车':0,u'卡威':0,u'开瑞':0,u'凯翼':0,u'康迪全球鹰':0,
    #    u'雷诺':0,u'理念':0,u'力帆汽车':0,u'莲花汽车':0,u'猎豹汽车':0,u'铃木':0,u'领克':0,u'陆风':0,u'马自达':0,
    #    u'南京金龙':0,u'欧宝':0,u'奇瑞':0,u'祺智':0,u'启辰':0,u'起亚':0,u'日产':0,u'荣威':0,u'瑞驰新能源':0,
    #    u'瑞麒':0,u'萨博':0,u'三菱':0,u'上汽大通':0,u'世爵':0,u'双环':0,u'双龙':0,u'思铭':0,u'斯巴鲁':0,u'斯柯达':0,
    #    u'沃尔沃':0,u'五菱汽车':0,u'五十铃':0,u'现代':0,u'雪佛兰':0,u'雪铁龙':0,u'一汽':0,u'依维柯':0,u'永源':0,
    #    u'宇通客车':0,u'驭胜':0,u'御捷':0,u'裕路':0,u'云度':0,u'长安':0,u'长安跨越':0,u'长安欧尚':0,u'长安轻型车':0,
    #    u'长城':0,u'之诺':0,u'知豆':0,u'中华':0,u'中兴':0,u'众泰':0,
    #    'GMC':1,'MINI':1,'smart':1,u'奥迪':1,u'宝马':1,u'宝沃':1,u'奔驰':1,u'悍马':1,u'捷豹':1,u'凯迪拉克':1,u'莱斯勒':1,
    #    u'雷克萨斯':1,u'林肯':1,u'路虎':1,u'讴歌':1,u'特斯拉':1,u'腾势':1,u'蔚来':1,u'英菲尼迪':1,
    #    'AC Schnitzer':2,'ALPINA':2,'ARCFOX':2,'DS':2,'Icona':2,'KTM':2,'LOCAL MOTORS':2,'Lorinser':2,u'SWM斯威汽车':2,
    #    u'阿尔法罗密欧':2,u'阿斯顿马丁':2,u'巴博斯':2,u'保时捷':2,u'宾利':2,u'布加迪':2,u'道奇':2,u'法拉利':2,u'福迪':2,
    #    u'福汽启腾':2,u'光冈':2,u'卡尔森':2,u'卡升':2,u'科尼赛克':2,u'兰博基尼':2,u'劳斯莱斯':2,u'陆地方舟':2,u'路特斯':2,
    #    u'玛莎拉蒂':2,u'迈巴赫':2,u'迈凯伦':2,u'名爵':2,u'摩根':2,u'纳智捷':2,u'欧朗':2,u'帕加尼':2,u'前途':2,u'庆铃汽车':2,
    #    u'如虎':2,u'赛麟':2,u'陕汽通家':2,u'斯达泰克':2,u'泰卡特':2,u'威麟':2,u'威兹曼':2,u'潍柴英致':2,u'西雅特':2,
    #    u'新凯':2,u'鑫源':2,u'野马汽车':2
# }
    #is_brand_popular={u'奥迪':1,u'宝马':1,u'保时捷':1,u'奔驰':1,u'本田':1,u'比亚迪':1,u'标致':1,u'别克':1,u'大众':1,u'东风':1,u'东风风度':1,
    #u'东风小康':1,u'菲亚特':1,u'丰田':1,u'福特':1,u'福田':1,u'哈弗':1,u'红旗':1,u'吉利':1,u'江淮':1,u'凯迪拉克':1,u'马自达':1,u'日产':1,u'荣威':1,u'斯巴鲁':1,
    #u'斯柯达':1,u'特斯拉':1,u'通用':1,u'蔚来':1,u'沃尔沃':1,u'五菱':1,u'西安奥拓':1,u'夏利':1,u'现代':1,u'雪佛兰':1,u'雪铁龙':1,   
    #'Alpina':0,'DS':0,'GMC':0,'Jeep':0,'MG':0,'MINI':0,'RUF':0,'Scion':0,'Smart':0,'SPRINGO':0,'WEY':0,u'阿尔法-罗密欧':0,u'阿斯顿马丁':0,u'安驰':0,
    #u'巴博斯':0,u'宝骏':0,u'宝龙':0,u'宝沃':0,u'保斐利':0,u'北京':0,u'北汽':0,u'奔腾':0,u'比速':0,u'宾利':0,u'布加迪':0,u'昌河':0,u'传祺':0,u'大迪':0,u'大发':0,u'大通':0,
    #u'大宇':0,u'道达':0,u'道奇':0,u'帝豪':0,u'东南':0,u'法拉利':0,u'风行':0,u'风神':0,u'福迪':0,u'富奇':0,u'观致':0,u'光冈':0,u'哈飞':0,u'海格':0,u'海马':0,u'汉腾':0,
    #u'悍马':0,u'黑豹':0,u'恒天':0,u'华北':0,u'华普':0,u'华骐':0,u'华颂':0,u'华泰':0,u'华阳':0,u'幻速':0,u'黄海':0,u'汇众':0,u'吉奥':0,u'佳星':0,u'江铃':0,u'江南':0,
    #u'捷豹':0,u'金杯':0,u'金程':0,u'九龙':0,u'君马':0,u'卡尔森':0,u'卡威':0,u'开瑞':0,u'凯翼':0,u'科尼赛克':0,u'克莱斯勒':0,u'兰博基尼':0,u'劳伦士':0,u'劳斯莱斯':0,
    #u'雷克萨斯':0,u'雷诺':0,u'理念':0,u'力帆':0,u'莲花':0,u'猎豹':0,u'林肯':0,u'铃木':0,u'领克':0,u'陆风':0,u'路虎':0,u'路特斯':0,u'罗孚':0,u'玛莎拉蒂':0,u'迈巴赫':0,
    #u'迈凯伦':0,u'美亚':0,u'纳智捷':0,u'讴歌':0,u'欧宝':0,u'欧朗':0,u'帕加尼':0,u'庞蒂克':0,u'奇瑞':0,u'祺智':0,u'启辰':0,u'启腾':0,u'起亚':0,u'庆铃':0,u'全球鹰':0,
    #u'瑞麒':0,u'萨博':0,u'赛宝':0,u'三菱':0,u'陕汽通家':0,u'绅宝':0,u'世爵':0,u'双环':0,u'双龙':0,u'思铭':0,u'斯威':0,u'腾势':0,u'天马':0,u'通田':0,u'万丰':0,u'威麟':0,
    #u'威旺':0,u'威兹曼':0,u'五十铃':0,u'西雅特':0,u'新凯':0,u'新雅途':0,u'扬子':0,u'野马':0,u'一汽':0,u'英菲尼迪':0,u'英伦':0,u'英致':0,u'永源':0,u'云度':0,u'云雀':0,
    #u'长安':0,u'长安商用':0,u'长城':0,u'之诺':0,u'知豆':0,u'中华':0,u'中欧':0,u'中顺':0,u'中兴':0,u'众泰':0
    #}
    #is_type_popular={'MPV':1,'SUV':1,u'货车':1,u'轿车':1,u'客车':1,u'敞篷SUV':0, u'敞篷轿车':0, u'敞篷轿跑车':0, u'敞篷跑车':0, u'敞篷越野车':0, u'房车':0, u'轿跑车':0, 
    #u'旅行车':0, u'跑车':0, u'皮卡':0, u'掀背轿车':0, u'掀背轿跑车':0, u'掀背跑车':0, u'越野车':0
    #}
    if params['is_car_popular'] == 1:
        params['car_index'] =params['car_index']+2 # 大众车+2
    if params['is_car_luxury'] == 0:
        params['car_index'] = params['car_index']+1 # 普通车+1
    score['car_score']=score['car_score']+int(brand_score_dict[params['car_index']]) # 若不在list，按0类别（最低分）算
    # 是否新能源
    if str(params['is_new_energy']) == '1':
        score['car_score']=score['car_score']+120
    else:
        score['car_score']=score['car_score']+60
    # 是否新车
    if str(params['is_new_car']) == '1':
        score['car_score']=score['car_score']+180
    else:
        score['car_score']=score['car_score']+60
    # 最终成交价格
    if params['deal_price']==-999.0:
        params['deal_price']=params['guide_price'] # 成交价格为空，用指导价格代替
    if params['deal_price'] <= 100000:
        score['car_score']=score['car_score']+240
    elif params['deal_price'] <= 200000:
        score['car_score']=score['car_score']+180
    elif params['deal_price'] <= 300000:
        score['car_score']=score['car_score']+120
    else:
        score['car_score']=score['car_score']+60
    return score
    
def modify_carfin_score(params,carfin_score):
    # 三方数据加分
    if (str(params['ILZZ00000000']) != '1') & (str(params['ILZZ00000001']) != '1'):
        if params['y_latest_in_amt_min'] >= 10:
            carfin_score = carfin_score + 120
        if params['assbalv9'] > 7:
            carfin_score = carfin_score + 100
    return carfin_score
        
    
#### 3.处理逻辑的入口方法
def handle(params):
    uid=['BAZZ01030010','EAZZ29000010','EBZZ26000010','id_province','id_age','id_gender'] # 实际用到的指标列表
    mob=['GEZZ00000011','BEAZ00100011','ACBZ03130011','ABZZ05100011','CHZZ04138011','EAZZ29000011','EBZZ25000011','ABZZ03008081','ACBZ03036011']
    score1=get_ori_score(params,uid,mob) # dict,['id_score','mobile_score']
    score2=modify_ori_score(params,score1) # dict,['id_score','mobile_score']
    score_person=modify_score(params,score2) # dict,['id_score','mobile_score','person_score'] # 300-900, 无缺失值
    score_loan=get_loan_score(params,score_person) # dict,['id_score','mobile_score','person_score','loan_score']
    score_car=get_car_score(params,score_loan) # dict,['id_score','mobile_score','person_score','loan_score','car_score']
    score_car['carfin_score1']=int(score_car['person_score']*0.5 + score_car['loan_score']*0.35 + score_car['car_score']*0.15)
    score_car['carfin_score2']=modify_carfin_score(params,score_car['carfin_score1'])
    score_car['carfin_score']=cuts(score_car['carfin_score2'],300,900)
    # 贷款结构和车辆信息必须非空，否则返回-1
    if params['down_payment_percent']==-999.0 or params['balance_payment_percent']==-999.0 or params['loan_term']==-999.0 or params['is_new_energy']==-999 or params['is_new_car']==-999 or (params['deal_price']==-999.0 and params['guide_price']==-999.0):
        score_car['carfin_score']=-1
    # ???
    # deal_price 限制严格大于0？
    
    # score_car['flag']=str(score_car['mobile_score'] > 0)
    # dict,['id_score','mobile_score','person_score','loan_score','car_score','carfin_score']
    return score_car
    