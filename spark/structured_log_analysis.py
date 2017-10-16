# coding: utf-8

"""
 Analyzing apache access log using Spark Structured Streaming

 written by pjh0347
"""

###########################################################
# import modules
###########################################################
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import apache_access_log

###########################################################
# session
###########################################################
spark = SparkSession.builder \
                    .master("spark://192.168.10.201:7077") \
                    .appName("apache access log exercise") \
                    .config("spark.submit.deployMode", "client") \
                    .config("spark.executor.memory", "1g") \
                    .config("spark.driver.memory", "1g") \
                    .getOrCreate()

###########################################################
# loading
###########################################################

# Method 1: File system streaming
# could be tested by moving files into the monitored directory.
LOG_DIR_PATH = 'hdfs://node-201:9000/data/weblog/streaming/'
df = spark.readStream \
          .format("text") \
          .option("maxFilesPerTrigger", 1) \
          .load(LOG_DIR_PATH)

'''
# Method 2: TCP socket streaming
# could be tested by sending data using nc utility.
HOSTNAME = 'node-201'
PORT = 8440
df = spark.readStream \
          .format('socket') \
          .option('host', HOST) \
          .option('port', PORT) \
          .load()

# Method 3: Queue
# TBD
'''

print "df.isStreaming : ", df.isStreaming
print "df.printSchema()"
df.printSchema()

###########################################################
# transformations
###########################################################
# Streaming DataFrame 타입으로는 커스텀 로그 포멧을 제대로 파싱할 수 없다.
# RDD 로 변환해서 처리할 수도 없게 되어 있다.

###########################################################
# query
###########################################################
#counts = ...
#query = counts.writeStream \
#              .outputMode("complete") \
#              .format("console") \
#              .start()

###########################################################
# run
###########################################################
#query.awaitTermination()

###########################################################
# hdfs dfs -mkdir /data/weblog/streaming
# hdfs dfs -mv /data/weblog/2015-1k /data/weblog/streaming/2015-1k
# hdfs dfs -rm /data/weblog/streaming/2015-1k

