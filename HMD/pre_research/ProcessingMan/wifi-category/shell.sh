#!/bin/bash
/usr/install/spark2-yarn/bin/pyspark \
--conf spark.ui.port=8259 \
--conf spark.sql.autoBroadcastJoinThreshold=-1 \
--conf spark.driver.maxResultSize=8g \
--driver-memory 8g \
--conf  spark.sql.shuffle.partitions=6000 \
--conf  spark.sql.adaptive.enabled=false \
