# coding=utf-8
from pyspark.sql import  SparkSession
from pyspark.sql import functions as f
from datetime import datetime, timedelta
import sys
from sklearn.externals import joblib
import pandas as pd
spark = SparkSession.builder.enableHiveSupport().getOrCreate()

model = joblib.load("model/lbs_cate_v1_20170705.model")
inputX = [i.strip() for i in file("model/lbs_cate_v1_20170705.inputX")]

#
# def myencode(x):
#     import sys
#     reload(sys)
#     sys.setdefaultencoding("utf-8")
#     return x.replace("\"", "").replace(",", "").encode("raw_unicode_escape").decode() if x else None
# encode_udf = f.udf(myencode)

def apply_predict(rows):
    """
    预测
    :param rows:数据
    :return:味数据打上标记
    """
    data = pd.DataFrame([i.asDict() for i in rows]).set_index("bssid")
    # [cols]
    X = data[inputX].dropna()

    pred = model.predict(X)
    X['pred'] = pred
    out = X.loc[:,['pred',]].reset_index()
    # data['pred'] = pred
    return out.values.tolist()

if len(sys.argv) == 2:
    dt = datetime.strptime(sys.argv[1],"%Y-%m-%d")  # specific date
else:
    dt = datetime.today()

print dt

dt_str = dt.strftime("%Y-%m-%d")
feature = spark.read.parquet("lbs/model/feature").filter("ds = '%s' and accum_days >=3 " % dt_str)

feature_pred = feature.repartition(1000).rdd.mapPartitions(lambda p: apply_predict(p)).toDF(['bssid','pred' ])  # 预测
feature_pred.createOrReplaceTempView("wifi_pred")
spark.sql("insert overwrite table afraudtech.wifi_category_all select * from wifi_pred")
# dev_wifi_common.coalesce(200).write.parquet("lbs/model/dev_common_address", mode="overwrite")
# feature_pred.repartition(100).write.parquet("lbs/model/wifi_category", mode="overwrite")
