# coding=utf-8
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as f
from datetime import datetime, timedelta
import sys
spark = SparkSession.builder.enableHiveSupport().getOrCreate()

rest_day = spark.read.csv("rest_day").rdd.collectAsMap()
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

def create_agg_func():
    """
    构造统计的agg函数
    :return: the agg functions
    """
    out = []
    time_section_cols = [
        'work_7_10', 'work_10_18', 'work_18_21', 'work_21_7',
        'rest_7_10', 'rest_10_18', 'rest_18_21', 'rest_21_7'
    ]
    for i in time_section_cols:
        f_days = f.countDistinct(i + "_days").alias(i + "_days")
        out.append(f_days)

    out.extend([
        f.countDistinct("occur_date").alias("accum_days"),
        f.last("ssid").alias("ssid"),
        f.last("wifi_lat_long").alias("wifi_lat_long"),
        f.last("wifi_accuracy").alias("wifi_accuracy"),
        f.last("wifi_address").alias("wifi_address"),
        f.max("occur_date").alias("last_date")
    ])
    return out

def prepare_data(data):
    split_time_udf = f.udf(split_time)
    data = (
        data
        .withColumn("occur_date_flag", split_time_udf(f.col("hour").cast("int"), "occur_date"))
    )

    time_section_cols = [
        'work_7_10', 'work_10_18', 'work_18_21', 'work_21_7',
        'rest_7_10', 'rest_10_18', 'rest_18_21', 'rest_21_7'
    ]
    for i in time_section_cols:
        data = data.withColumn(i + "_days", f.when(data.occur_date_flag == i, data['occur_date']).otherwise(None))
    return data

if len(sys.argv) == 2:
    dt = datetime.strptime(sys.argv[1],"%Y-%m-%d")  # specific date
else:
    dt = datetime.today()
dt_before120_str = (dt - timedelta(2)).strftime("%Y-%m-%d")
dt_str = dt.strftime("%Y-%m-%d")

filter_str = """
    occur_date >= '%s' and occur_date < '%s' and deviceid is not null and bssid is not null
""" % (dt_before120_str, dt_str)
data = spark.read.parquet("lbs/raw_data").filter(filter_str)
data = prepare_data(data)
agg_func = create_agg_func()
dev_wifi = data.groupby(["deviceid", "bssid"]).agg(*agg_func)
dev_wifi.repartition(100).write.parquet("lbs/model/dev_wifi", mode="overwrite")
