#!/bin/bash
datetime=`date "+%Y%m%d"`
nohup /usr/install/spark2-yarn/bin/spark-submit \
--conf spark.ui.port=8259 \
--conf spark.sql.autoBroadcastJoinThreshold=-1 \
--executor-memory 16g \
--conf spark.driver.maxResultSize=8g \
--driver-memory 8g \
$1 $2 > "${datetime}_$2" &

