# coding=utf-8
from pyspark.sql import  SparkSession
from pyspark.sql.types import *
from datetime import datetime, timedelta
import sys
import re

spark = SparkSession.builder.enableHiveSupport().getOrCreate()
rest_day = spark.read.csv("rest_day").rdd.collectAsMap()

def get_pre3(col):
    subcol=None
    if col:
        subcol = ":".join(col.split(":")[:3])
    return subcol

def get_pre4(col):
    subcol=None
    if col:
        subcol = ":".join(col.split(":")[:4])
    return subcol


def split_time(hour, occur_date):
    """
    分时间段
    :param hour: 小时
    :param dayofweek: 星期， 周日=7
    :return:
    """
    flag = None
    is_rest_day = occur_date in rest_day
    if not is_rest_day and hour >= 7 and hour < 10:
        flag = "work_7_10"
    elif not is_rest_day and hour >= 10 and hour < 18:
        flag = "work_10_18"
    elif not is_rest_day and hour >= 18 and hour < 21:
        flag = "work_18_21"
    elif not is_rest_day and (hour >=21 or hour < 7):
        flag = "work_21_7"
    elif is_rest_day and hour >= 7 and hour < 10:
        flag = "rest_7_10"
    elif is_rest_day and hour >= 10 and hour < 18:
        flag = "rest_10_18"
    elif is_rest_day and hour >= 18 and hour < 21:
        flag = "rest_18_21"
    elif is_rest_day and (hour >=21 or hour < 7):
        flag = "rest_21_7"
    return flag

def repair_bssid(bssid):
    """
    修复bssid
    :param bssid:
    :return:
    """
    new_bssid = []
    try:
        for i in bssid.split(":"):
            if len(i) == 1:
                i = "0" + i
            new_bssid.append(i)
    except Exception,e:
        pass
    new_bssid = ":".join(new_bssid)
    p = '^([0-9a-fA-F]{1,2})(:[0-9a-fA-F]{1,2}){5}$'
    if new_bssid in ('00:02:00:00:00:00', 'ff:ff:ff:ff:ff:ff', '00:00:00:00:00:00') or not re.match(p,new_bssid):
        new_bssid = None
    return new_bssid

def extract_lat_long(lbs_json, is_gps=False):
    """
    提取基站／wifi／gps 定位中的经纬度，
    :param lbs_json: 基站／wifi／gps 位置的json串
    :param is_gps:  是否解析gpsjson串
    :return: [纬度,经度]
    """
    try:
        if is_gps:
            lat = "lat"
            long = "long"
        else:
            lat = "latitude"
            long = "longitude"

        lat_long = eval(lbs_json)
        out = [lat_long[lat], lat_long[long]]
    except Exception:
        out = None
    return out
def extract_address(lbs_json):
    """
    提取出 wifi定位和基站定位地址
    :return: addrees, string
    """
    out = None
    if lbs_json:
        try:
            lbs = eval(lbs_json)
            out = lbs.get('geo', {}).get('address', None)

        except Exception :
            pass
    return out

def extract_accuracy(lbs_json):
    """
    提取出 wifi定位和基站定位的精度
    :return: array
    """
    out = None
    if lbs_json:
        try:
            lbs = eval(lbs_json)
            out = lbs['accuracy']
        except Exception :
            pass
    return out

spark.udf.register("extract_lat_long",extract_lat_long, ArrayType(DoubleType()))
spark.udf.register("extract_accuracy", extract_accuracy, IntegerType())
spark.udf.register("extract_address", extract_address, StringType())
spark.udf.register("repair_bssid", repair_bssid, StringType())


def prepare_data(year, month, day):
    sql = """
      select
            deviceid,
            from_unixtime(gmtcreate / 1000, 'yyyy-MM-dd') as occur_date,
            from_unixtime(gmtcreate / 1000, 'HH') as hour,
            repair_bssid(deviceinfo.bssid) as bssid,
            deviceinfo.ssid, deviceinfo.trueIp,
            extract_lat_long(deviceinfo.locationOfWifi) as wifi_lat_long,
            extract_accuracy(deviceinfo.locationOfWifi) as wifi_accuracy,
            extract_address(deviceinfo.locationOfWifi) as wifi_address
      from fp
      where
            year=%s and month=%s and day=%s
    """ % (year, month, day)
    data = spark.sql(sql)
    data = data.groupby(data.columns).count().drop("count")
    return data


def run_history(month, start_day, end_day):
    year = 2017
    for day in range(start_day, end_day + 1):
        print year, month ,day
        data = prepare_data(year, month, day)
        data.repartition(200).write.partitionBy("occur_date").parquet("lbs/raw_data", mode="append")


if __name__ == '__main__':

    if len(sys.argv) == 2:
        dt = datetime.strptime(sys.argv[1], '%Y-%m-%d') # specific date
    else:
        dt = datetime.today() - timedelta(1) # yesterday

    print "daily: ", dt
    data = prepare_data(dt.year, dt.month, dt.day)
    data.repartition(200).write.partitionBy("occur_date").parquet("lbs/raw_data", mode = "append")
    # print "history"
    #run_history(7, 1, 2)

