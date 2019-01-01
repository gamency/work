#!/bin/bash
nohup /usr/install/spark2-yarn/bin/spark-submit \
--conf spark.ui.port=8259 \
--conf spark.sql.autoBroadcastJoinThreshold=-1 \
--conf spark.driver.maxResultSize=8g \
--driver-memory 8g \
--conf  spark.sql.shuffle.partitions=6000 \
--conf  spark.sql.adaptive.enabled=false \
$1 $2 > "logs/$1_${datetime}_$2" &
