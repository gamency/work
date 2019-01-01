#-*- coding:utf-8 -*-
from pyspark import SparkContext, SparkConf
from pyspark.sql import Row, HiveContext


"""
1.输入本地ip文件路径将其转化成broadcast
2.通过sql取2015.9.20 － 2016.9.20期间activity特定字段的数据
3.使用mapPartion遍历每一个partitions
4.对个partitions进行以下处理：
	若trueipAddress 或 ipAddress 在broadcast的key中，则把该条记录加入到列表中

5.将数据以parquet保存到hdfs上

"""
def read_to_dict(infp):
	out = {}
	with open(infp, "r") as f:
		for line in f:
			line = line.replace("\n", "").strip()
			out[line] = 1
	return out

def apply_rows(rows, broadcast):
	out = []
	for row in rows:
		if row.ipAddress in broadcast.value:
			out_row = Row(
				ip = row.ipAddress,
				sequence_id = row.sequence_id,
				deviceId = row.deviceId,
				os = row.os,
				isp = get_isp(row.geoIp),
				ssid = row.ssid,
				bssid = row.bssid,
				partnerCode = row.partnerCode,
				eventType = row.eventType,
				accountMobile = row.accountMobile,
				eventOccurTime = row.eventOccurTime,
				appType = row.appType
			)
			out.append(out_row)
	return out
def get_isp(geoIp):
	isp = ''
	if geoIp:
		geoIp = eval(geoIp)
		isp = geoIp.get('isp', '')
	return isp

conf = SparkConf()
conf.setAppName("get_data_by_ip")
sc = SparkContext(conf=conf)
sqlContext = HiveContext(sc)

infp = "/home/zhen.wang/project/ip/ip15/data/adsl_ip.csv"
outfp = "ip/ip_category_1_5_mid"
ip = read_to_dict(infp)
ip = sc.broadcast(ip)

sql = """
	select  
		sequence_id,device_map.deviceId,device_map.os,
		device_map.geoIp,device_map.ssid,device_map.bssid,
		activity_map.partnerCode,activity_map.eventType,
		activity_map.accountMobile,activity_map.eventOccurTime,event_result_map.appType,
		geo_map.ipAddress 
	from activity 
	where year = 2016 and month <=9 and month >=4
"""

activity = sqlContext.sql(sql)
result = activity.mapPartitions(lambda rows: apply_rows(rows, ip))
result = result.toDF()
result.coalesce(1000).write.parquet(outfp)

