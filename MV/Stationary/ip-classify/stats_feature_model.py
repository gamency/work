#!/usr/bin/python
# -*- coding:utf-8 -*-
from pyspark import SparkContext, SparkConf
from pyspark.sql import Row, HiveContext
from datetime import datetime
import numpy
from collections import defaultdict

conf = SparkConf()
conf.setAppName("get_model_data")
sc = SparkContext(conf=conf)
sqlContext = HiveContext(sc)

def apply_row(x, timetype_dict):
	"""
	  计算每个ip及对应的指标
	  返回格式：(ip,指标（列表表示）)
	"""
	ip = x[0]
	rows = x[1]
	out = []
	#将数据聚合
	device_set = set()
	device_pc_set = set() 
	device_mobile_set = set()
	device_unknow_set = set()
	partnerCode_set = set()
	eventType_set = set()
	bssid_set = set()
	ssid_set = set()
	bssid_ssid_set = set()
	accountMobile_set = set()
	partnerCode_device = defaultdict(set)
	eventType_device = defaultdict(set)
	timetype_device = defaultdict(set)
	timetype_sid = defaultdict(set)
	for row in rows:
		sequence_id = row['sequence_id']
		deviceId = row['deviceId']
		os = row['os']
		appType = row['appType']
		accountMobile = row['accountMobile']
		bssid = row['bssid']
		ssid = row['ssid']
		partnerCode = row['partnerCode']
		eventType = row['eventType']
		eventOccurTime = float(row['eventOccurTime']) / 1000
		day_hour = get_weekday_hour_type(eventOccurTime)
		timetype = timetype_dict[day_hour]
		if deviceId:
			device_set.add(deviceId)
			device_type = judge_device_type(os, appType)
			if device_type == 'pc':
				device_pc_set.add(deviceId)
			elif device_type == 'mobile':
				device_mobile_set.add(deviceId)
			else:
				device_unknow_set.add(deviceId)
			partnerCode_device[deviceId].add(partnerCode)
			eventType_device[deviceId].add(eventType)
			timetype_device[timetype].add(deviceId)
		timetype_sid[timetype].add(sequence_id)
		partnerCode_set.add(partnerCode)
		eventType_set.add(eventType)

		if bssid:
			bssid_set.add(bssid)
		if ssid:
			ssid_set.add(ssid)
		if bssid and ssid:
			bssid_ssid = bssid + ";" + ssid.replace(",", " ").replace("|", " ").replace(";", "")
			bssid_ssid_set.add(bssid_ssid)
		if accountMobile:
			accountMobile_set.add(accountMobile)
	#统计指标
	event_cnt = len(rows)
	device_cnt = len(device_set) #关联设备数量
	device_pc_cnt = len(device_pc_set) #关联设备为pc端的数量
	device_mobile_cnt = len(device_mobile_set) #关联设备为移动端的数量
	device_unknow_cnt = len(device_unknow_set) #关联设备未知类型的数量

	bssid_cnt = len(bssid_set) #关联的bssid数量
	ssid_cnt = len(ssid_set)

	accountMobile_cnt = len(accountMobile_set) #关联的手机号数

	partner_cnt = len(partnerCode_set) #关联的合作方数量
	if partnerCode_device:
		partnerCode_device_len = [len(i) for i in partnerCode_device.values()]
		partner_device_median = numpy.median(partnerCode_device_len) #关联的每台设备平均合作方数
		partner_device_std = numpy.std(partnerCode_device_len) #关联的每台设备合作方数波动
	else:
		partner_device_median = 0
		partner_device_std = 0

	eventType_cnt = len(eventType_set) # 关联的事件类型数
	if eventType_device:
		eventType_device_len = [len(i) for i in eventType_device.values()] 
		eventType_device_median = numpy.median(eventType_device_len) # 关联的每台设备平均事件类型数
		partner_device_std = numpy.std(eventType_device_len) # 关联的每台设备事件类型数分布
	else:
		eventType_device_median = 0
		partner_device_std = 0
	timetype_device_features = stats_with_time(timetype_device) #统计每个时段内关联设备数相关指标
	timetype_sid_features = stats_with_time(timetype_sid) #统计每个时段内事件数相关指标

	feature = [
		event_cnt, device_cnt, device_pc_cnt, device_mobile_cnt, device_unknow_cnt,
		bssid_cnt, ssid_cnt, accountMobile_cnt,
		partner_cnt, partner_device_median, partner_device_std,
		eventType_cnt, eventType_device_median, partner_device_std,
	]

	extend_bssid_ssid = "|".join(bssid_ssid_set)
	feature = feature + timetype_device_features + timetype_sid_features 
	out = (ip, feature, extend_bssid_ssid)
	return out

def stats_with_time(timetype_filed):
	"""统计各个时段field（设备数/事件数)相关指标,返回33个指标
	"""
	week11_filed_cnt = len(timetype_filed.get('week11', [])) #周一时段1内field的去重数量 
	week12_filed_cnt = len(timetype_filed.get('week12', [])) #周一时段2内field的去重数量 
	week13_filed_cnt = len(timetype_filed.get('week13', [])) #周三时段3内field的去重数量 
	week21_filed_cnt = len(timetype_filed.get('week21', [])) #周二时段1内field的去重数量
	week22_filed_cnt = len(timetype_filed.get('week22', [])) 
	week23_filed_cnt = len(timetype_filed.get('week23', []))
	week31_filed_cnt = len(timetype_filed.get('week31', []))
	week32_filed_cnt = len(timetype_filed.get('week32', []))
	week33_filed_cnt = len(timetype_filed.get('week33', []))
	week41_filed_cnt = len(timetype_filed.get('week41', []))
	week42_filed_cnt = len(timetype_filed.get('week42', []))
	week43_filed_cnt = len(timetype_filed.get('week43', []))
	week51_filed_cnt = len(timetype_filed.get('week51', []))
	week52_filed_cnt = len(timetype_filed.get('week52', []))
	week53_filed_cnt = len(timetype_filed.get('week53', []))
	week61_filed_cnt = len(timetype_filed.get('week61', []))
	week62_filed_cnt = len(timetype_filed.get('week62', []))
	week63_filed_cnt = len(timetype_filed.get('week63', []))
	week71_filed_cnt = len(timetype_filed.get('week71', []))
	week72_filed_cnt = len(timetype_filed.get('week72', []))
	week73_filed_cnt = len(timetype_filed.get('week73', []))

	work1_filed_list = [week11_filed_cnt, week21_filed_cnt, week31_filed_cnt,
		 					week41_filed_cnt, week51_filed_cnt]
	work2_filed_list = [week12_filed_cnt, week22_filed_cnt, week32_filed_cnt,
		 					week42_filed_cnt, week52_filed_cnt] 
	work3_filed_list = [week13_filed_cnt, week23_filed_cnt, week33_filed_cnt,
		 					week43_filed_cnt, week53_filed_cnt]

	weekend1_filed_list = [week61_filed_cnt, week71_filed_cnt]
	weekend2_filed_list = [week62_filed_cnt, week72_filed_cnt]
	weekend3_filed_list = [week63_filed_cnt, week73_filed_cnt]

	time1_filed_list = work1_filed_list + weekend1_filed_list
	time2_filed_list = work2_filed_list + weekend2_filed_list
	time3_filed_list = work3_filed_list + weekend3_filed_list

	work1_filed_mean = numpy.mean(work1_filed_list) #工作日时段1内平均field去重数
	work2_filed_mean = numpy.mean(work2_filed_list) #工作日时段2内平均field去重数
	work3_filed_mean = numpy.mean(work3_filed_list) #工作日时段3内平均field去重数

	weekend1_filed_mean = numpy.mean(weekend1_filed_list) #周末时段1内平均field去重数
	weekend2_filed_mean = numpy.mean(weekend2_filed_list) #周末时段2内平均field去重数
	weekend3_filed_mean = numpy.mean(weekend3_filed_list) #周末时段3内平均field去重数

	time1_filed_mean = numpy.mean(time1_filed_list) #时段1内平均field去重数
	time2_filed_mean = numpy.mean(time2_filed_list) #时段2内平均field去重数
	time3_filed_mean = numpy.mean(time3_filed_list) #时段3内平均field去重数

	time1_filed_std = numpy.std(time1_filed_list) #时段1内field去重数波动
	time2_filed_std = numpy.std(time2_filed_list) #时段2内field去重数波动
	time3_filed_std = numpy.std(time3_filed_list) #时段3内field去重数波动

	out = [
		week11_filed_cnt, week12_filed_cnt, week13_filed_cnt, 
		week21_filed_cnt, week22_filed_cnt, week23_filed_cnt, 
		week31_filed_cnt, week32_filed_cnt, week33_filed_cnt, 
		week41_filed_cnt, week42_filed_cnt, week43_filed_cnt, 
		week51_filed_cnt, week52_filed_cnt, week53_filed_cnt, 
		week61_filed_cnt, week62_filed_cnt, week63_filed_cnt, 
		week71_filed_cnt, week72_filed_cnt, week73_filed_cnt, 
		work1_filed_mean, work2_filed_mean, work3_filed_mean, 
		weekend1_filed_mean, weekend2_filed_mean, weekend3_filed_mean, 
		time1_filed_mean, time2_filed_mean, time3_filed_mean,
		time1_filed_std, time2_filed_std, time3_filed_std
	]
	return out

def tolower(s):
	if s:
		s = s.lower()
	else:
		s = ''
	return s

def judge_device_type(os, appType):
	"""
	  根据os和appType判断设备是移动端、pc端还是未知。
	"""
	os = tolower(os)#统一转成小写判定
	appType = tolower(appType)
	if 'android' in os or 'ios' in os or 'linux' in 'os' or 'windows phone' in os \
		or 'android' in appType or 'ios' in appType:
		flag = 'mobile'
	elif 'windows' in os or 'mac os' in os:
		flag = 'pc'
	else:
		flag = 'unknow'
	return flag

def get_weekday_hour_type(timestamp):
	"""
	  获得星期、时段
	  返回(7,1)表示星期天时段1 
	"""
	dt = datetime.fromtimestamp(timestamp)
	weekday = dt.weekday() + 1
	hour_type = get_hour_type(dt.hour)
	out = (weekday, hour_type)
	return out

def get_hour_type(hour):
	"""
	  获得时间对应的时段
	"""
	if hour >= 7 and hour < 18:
		hour_type = 1
	elif hour >= 18 and hour < 22:
		hour_type = 2
	else:
		hour_type = 3
	return hour_type

def create_timetype_dict():
	"""
	  生成时段类型，week11表示周一时段一
	"""
	out = {}
	for i in range(1, 8):
		for j in range(1, 4):
			out[(i, j)] = "week%s%s" %(i, j)
	return out

infp = "ip/ip_category_1_5_mid"
# infp = "ip/ip_category_1_5_mid/part-r-00999-b82dfb51-7cb7-42cf-9eaa-84b461fa4938.gz.parquet"
outfp = "ip/ip_category_1_5_feature"
df = sqlContext.read.parquet(infp)
df = df.map(lambda x : (x.ip, x))
df = df.combineByKey(
	lambda value : [value],
	lambda x, value : x + [value],
	lambda x, y : x + y
)
timetype_dict = create_timetype_dict()
result = df.map(lambda x : apply_row(x, timetype_dict))
result.coalesce(10).saveAsTextFile(outfp)
