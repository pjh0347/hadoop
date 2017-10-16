
$SPARK_HOME/bin/spark-submit \
    --master spark://192.168.10.201:7077 \
    --deploy-mode client \
    --conf "spark.executor.memory=1g" \
    --conf "spark.driver.memory=1g" \
    --py-files apache_access_log.py \
    spark_stream_analysis.py

