# coding=utf-8
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as f
from datetime import datetime, timedelta
import sys

from tools import *

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

def prepare_data(data):
    split_time_udf = f.udf(split_time)
    get_pre3_udf = f.udf(get_pre3)
    get_pre4_udf = f.udf(get_pre4)
    data = (
        data
            .withColumn("occur_date_flag", split_time_udf(f.col("hour").cast("int"), "occur_date"))
            .withColumn("ip3", get_pre3_udf("trueIp"))
            .withColumn("bssid3", get_pre3_udf("bssid"))
            .withColumn("bssid4", get_pre4_udf("bssid"))
    )

    time_section_cols = [
        'work_7_10', 'work_10_18', 'work_18_21', 'work_21_7',
        'rest_7_10', 'rest_10_18', 'rest_18_21', 'rest_21_7'
    ]
    for i in time_section_cols:
        data = data.withColumn(i + "_days", f.when(data.occur_date_flag == i, data['occur_date']).otherwise(None))
        data = data.withColumn(i + "_devices", f.when(data.occur_date_flag == i, data['deviceid']).otherwise(None))
    return data


if len(sys.argv) == 2:
    dt = datetime.strptime(sys.argv[1],"%Y-%m-%d")  # specific date
else:
    dt = datetime.today()
print dt

dt_before120_str = (dt - timedelta(120)).strftime("%Y-%m-%d")
dt_str = dt.strftime("%Y-%m-%d")
filter_str = "occur_date >= '%s' and occur_date < '%s' and %s is not null" % (dt_before120_str, dt_str, "trueIp")
data = spark.read.parquet("lbs/raw_data").filter(filter_str)
data = prepare_data(data)
feature = compute_feature(data, "trueIp", "ip_")
feature.repartition(200).write.parquet("lbs/model/wifi_ip_feature", mode="overwrite")
sqlContext.read.parquet("lbs/model/wifi_ip_feature")