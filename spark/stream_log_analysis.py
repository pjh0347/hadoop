# coding: utf-8

"""
 Analyzing apache access log using Spark Streaming

 문제점)
 Spark Streaming 인터페이스는 데이터를 수신 받은 시각 기준으로 구현되어 있다.
 보통 로그 데이터는 최초 발생 이 후 수집/파싱/로딩/분석 등 여러 단계의 파이프라인을 
 거치게 되는데, 이 과정에서 과부하 또는 장애로 인해 지연 처리되는 상황이 발생한다.
 그래서 실제와 분석 결과 사이에 시간적인 갭이 발생할 수 있으며, 불규칙한 지연으로 인해
 실제와 분석 결과 사이에 오차도 들쭉날쭉 해질 수 도 있다.
 TODO : 이런 문제점이 Structured Streaming 에서 해결되는지 확인해 봐야...

 written by pjh0347
"""

###########################################################
# import modules
###########################################################
from pyspark import StorageLevel
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.streaming import StreamingContext
import apache_access_log

###########################################################
# session & context
###########################################################
spark = SparkSession.builder \
                    .master("spark://192.168.10.201:7077") \
                    .appName("apache access log exercise") \
                    .config("spark.submit.deployMode", "client") \
                    .config("spark.executor.memory", "1g") \
                    .config("spark.driver.memory", "1g") \
                    .getOrCreate()
sc = spark.sparkContext
ssc = StreamingContext(sc, batchDuration=1)
ssc.checkpoint("checkpoint")

###########################################################
# loading
###########################################################

# Method 1: File system streaming
# could be tested by moving files into the monitored directory.
LOG_DIR_PATH = 'hdfs://node-201:9000/data/weblog/streaming/'
lines = ssc.textFileStream(LOG_DIR_PATH)

'''
# Method 2: TCP socket streaming
# could be tested by sending data using nc utility.
HOSTNAME = 'node-201'
PORT = 8440
lines = ssc.socketTextStream(hostname=HOSTNAME, 
                             port=PORT, 
                             storageLevel=StorageLevel.MEMORY_ONLY)

# Method 3: Queue
# TBD
'''

###########################################################
# transformations
###########################################################
logs  = lines.map(apache_access_log.parse) \
             .filter(lambda x: x is not None) 

###########################################################
# query
###########################################################

print "pv per second"
logs.count().pprint()

print "uv per second"
logs.map(lambda x: x.host).countByValue().count().pprint()

print "status count per second"
logs.map(lambda x: x.status).countByValue().pprint()
#logs.map(lambda x: (x.status, 1)).reduceByKey(lambda a, b: a+b).pprint()

print "404 status count per second"
logs.filter(lambda x: x.status == '404').count().pprint()

print "response size per second"
def response_size_stat(time, rdd):
	if rdd.isEmpty(): return
	print "[response size] sum=%d, min=%d, max=%d, avg=%d, stddev=%f, variance=%f" % \
	      (rdd.sum(), rdd.min(), rdd.max(), rdd.mean(), rdd.stdev(), rdd.variance())
logs.map(lambda x: x.size).foreachRDD(response_size_stat)

print "top 5 urls per second"
logs.map(lambda x: (x.host, 1)) \
    .reduceByKey(lambda a, b: a+b) \
    .transform(lambda rdd: rdd.sortBy(lambda x: x[1], ascending=False)) \
    .pprint()

###########################################################
# run
###########################################################
ssc.start()
ssc.awaitTermination()

###########################################################
# hdfs dfs -mkdir /data/weblog/streaming
# hdfs dfs -mv /data/weblog/2015-1k /data/weblog/streaming/2015-1k
# hdfs dfs -rm /data/weblog/streaming/2015-1k

