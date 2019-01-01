# coding=utf-8
from pyspark.sql import HiveContext, SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as f
from datetime import datetime, timedelta
import sys


def create_time_agg(prefix=""):
    """
    构造时间相关的agg函数
    :param prefix:if to compute ip feature then prefix = "ip_"
    :return: the agg functions abount time
    """
    out = []
    time_section_cols = [
        'work_7_10', 'work_10_18', 'work_18_21', 'work_21_7',
        'rest_7_10', 'rest_10_18', 'rest_18_21', 'rest_21_7'
    ]
    for i in time_section_cols:
        f_days = f.countDistinct(i + "_days").alias("%s%s_days" % (prefix, i))
        out.append(f_days)

        f_devices = f.countDistinct(i + "_devices").alias("%s%s_devices" % (prefix, i))
        out.append(f_devices)
    return out


def create_basic_agg(prefix = ""):
    """
    构造基本字段的agg统计函数
    :param prefix: if to compute ip feature then prefix = "ip_"
    :return: the agg functions about basic cols
    """
    if prefix == "ip_":
        out = [
            f.countDistinct("occur_date").alias("ip_accum_days"),
            f.countDistinct("deviceid").alias("ip_device_cnt"),
            f.countDistinct("deviceid", "occur_date").alias("ip_device_days"),
            f.countDistinct("bssid").alias("ip_bssid_cnt"),
            f.countDistinct("bssid4").alias("ip_bssid4_cnt"),
            f.countDistinct("bssid3").alias("ip_bssid3_cnt"),
            f.countDistinct("ssid").alias("ip_ssid_cnt")
        ]
    else:
        out = [
            f.countDistinct("trueIp").alias("ip_cnt"),
            f.countDistinct("ip3").alias("ip3_cnt"),
            f.countDistinct("deviceid").alias("device_cnt"),
            f.countDistinct("occur_date").alias("accum_days"),
            f.countDistinct("deviceid", "occur_date").alias("device_days")
        ]
    return out

def create_extend_agg(prefix=""):
    """
    构造获取额外字段的agg函数
    :param prefix:if to compute ip feature then prefix = "ip_"
    :return:the agg functions about extend cols
    """
    if prefix == "ip_":
        out = []
    else:
        out = [
            f.last("ssid").alias("extend_ssid"),
            f.last("wifi_lat_long").alias("extend_wifi_lat_long"),
            f.last("wifi_accuracy").alias("extend_wifi_accuracy"),
            f.last("wifi_address").alias("extend_wifi_address"),
            f.max("occur_date").alias("extend_last_date"),
            f.last("trueIp").alias("trueIp")# to join for geting ip feature
        ]
    return out


def compute_feature(data, key, prefix=""):
    agg_func =  create_basic_agg(prefix) + create_time_agg(prefix) + create_extend_agg(prefix)
    feature = data.groupby(key).agg(*agg_func)
    feature = (
        feature
            .withColumn("%sdevice_days_mean" % prefix, f.col("%sdevice_days" % prefix) / f.col("%sdevice_cnt" % prefix))
            .drop("%sdevice_days" % prefix)
    )
    return feature
