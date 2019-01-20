from pyspark.sql import SparkSession
# import pandas as pd
# import numpy as np


def pirates():
    spark = SparkSession.builder.appName("tt").enableHiveSupport().getOrCreate()
    select_df = spark.sql('''select get_json_object(rqst_other_fields, '$.mouseMoving) msg, 
    get_json_object(rqst_other_fields, '$.botProbability) prob, month, day from bigdata.raw_activity_flat 
    where year=2018 and month in(2,3) and event='verification' ''')

    df = select_df.toPandas()

    return df
