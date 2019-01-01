# coding=utf-8
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as f
from datetime import datetime, timedelta
import sys

from tools import *

spark = SparkSession.builder.enableHiveSupport().getOrCreate()

if len(sys.argv) == 2:
    dt = datetime.strptime(sys.argv[1],"%Y-%m-%d")  # specific date
else:
    dt = datetime.today()
print dt

dt_str = dt.strftime("%Y-%m-%d")
wifi_sub_feature = spark.read.parquet("lbs/model/wifi_sub_feature").filter("accum_days > 2")
ip_feature = spark.read.parquet("lbs/model/wifi_ip_feature")
wifi_feature = wifi_sub_feature.join(ip_feature, on="trueIp")
wifi_feature = (
    wifi_feature
    .withColumn("all_7_10_days", f.col("work_7_10_days") + f.col("rest_7_10_days"))
    .withColumn("all_10_18_days", f.col("work_10_18_days") + f.col("rest_10_18_days"))
    .withColumn("all_18_21_days", f.col("work_18_21_days") + f.col("rest_18_21_days"))
    .withColumn("all_21_7_days", f.col("work_21_7_days") + f.col("rest_21_7_days"))
    .withColumn("device_days_rate", f.col("device_days_mean") / f.col("accum_days"))
    .withColumn("ip_bssid_per_ssid", f.col("ip_bssid_cnt") / f.col("ip_ssid_cnt"))
    .withColumn("ip_bssid_per_bssid4", f.col("ip_bssid4_cnt") / f.col("ip_ssid_cnt"))
    .withColumn("ip_device_cnt_per_bssid", f.col("ip_device_cnt") / f.col("ip_bssid_cnt"))
    .withColumn("ds", f.lit(dt_str))
)
from pyspark.sql import functions as f

wifi_feature = wifi_feature.withColumn("ds", f.lit(dt_str))
wifi_feature.write.partitionBy("ds").parquet("lbs/model/feature", mode="append")

