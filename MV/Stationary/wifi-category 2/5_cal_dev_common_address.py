# coding=utf-8
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as f
from datetime import datetime, timedelta
import sys
spark = SparkSession.builder.enableHiveSupport().getOrCreate()

wifi_type = spark.sql("select * from afraudtech.wifi_category_all")
dev_wifi = spark.read.parquet("lbs/model/dev_wifi")

dev_wifi_common = dev_wifi.join(wifi_type, on="bssid", how="left")
col_selected = [
    "deviceid",
    "bssid",
    "accum_days",
    "wifi_lat_long as lat_long",
    "wifi_accuracy as accuracy",
    "pred as address_category",
    "last_date"
]
def list2str(col):
    return ",".join([str(i) for i in col])

list2str_udf = f.udf(list2str)
dev_wifi_common = (
    dev_wifi_common.selectExpr(col_selected)
    .filter("lat_long is not null")
    .withColumn("lat_long", list2str_udf(f.col("lat_long")))
    .fillna({"address_category":"home"})
)

dev_wifi_common.createOrReplaceTempView("dev_wifi_common")
spark.sql("insert overwrite table afraudtech.dev_common_address select * from dev_wifi_common")
# dev_wifi_common.coalesce(200).write.parquet("lbs/model/dev_common_address", mode="overwrite")
