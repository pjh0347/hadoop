# coding: utf-8

"""
 Analyzing apache access log using Spark SQL/RDD/DataFrame

 RDD vs DataFrame
  - RDD       : provide low level control
  - DataFrame : provide high level interface

 written by pjh0347
"""

###########################################################
# import modules
###########################################################
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark import StorageLevel
import apache_access_log

###########################################################
# session & context
###########################################################
spark = SparkSession.builder \
                    .master("spark://192.168.10.201:7077") \
                    .appName("apache access log exercise") \
                    .config("spark.submit.deployMode", "client") \
                    .config("spark.executor.memory", "1g") \
                    .enableHiveSupport() \
                    .getOrCreate()
sc = spark.sparkContext

###########################################################
# loading
###########################################################
LOG_FILE_PATH = 'hdfs://node-201:9000/data/weblog/2015'
rdd = sc.textFile(LOG_FILE_PATH) \
        .map(apache_access_log.parse) \
        .filter(lambda x: x is not None) 
df = spark.createDataFrame(rdd)

###########################################################
# partition
###########################################################
print "rdd.getNumPartitions() : %s" % rdd.getNumPartitions()
print "rdd.repartition(10)"
rdd = rdd.repartition(10)
print "rdd.getNumPartitions() : %s" % rdd.getNumPartitions()

###########################################################
# temporary view
###########################################################
'''
########################################################################################
# pyspark 쉘을 이용할때 보통 global_temp 데이터베이스를 찾을 수 없다고 Warning 이 뜬다.
# 이런 문제로 인해 global 임시 뷰는 동작하지 않는다.
# 인터넷 검색해 보아도 질문만 있고 솔루션은 없다.
########################################################################################
# lifetime : Spark application
df.createGlobalTempView('apache_access_log_table')
print "spark.sql('select * from global_temp.apache_access_log_table limit 10').collect()"
print spark.sql('select * from global_temp.apache_access_log_table limit 10').collect()
spark.catalog.dropGlobalTempView('apache_access_log_table')
'''

# lifetime : SparkSession
df.createTempView('apache_access_log_table')
print "spark.sql('select * from apache_access_log_table limit 10').collect()"
print spark.sql('select * from apache_access_log_table limit 10').collect()
spark.catalog.dropTempView('apache_access_log_table')

###########################################################
# database, table and view
###########################################################
spark.sql('show databases').show()
spark.sql('show tables').show()

###########################################################
# persist & cache
###########################################################
print "df.storageLevel : %s" % df.storageLevel
print "df.persist(StorageLevel.MEMORY_ONLY) : %s" % df.persist(StorageLevel.MEMORY_ONLY) # same with df.cache()
print "df.storageLevel : %s" % df.storageLevel

print "rdd.getStorageLevel() : %s" % rdd.getStorageLevel()
print "rdd.persist(StorageLevel.MEMORY_AND_DISK) : %s" % rdd.persist(StorageLevel.MEMORY_AND_DISK) # default value
print "rdd.getStorageLevel() : %s" % rdd.getStorageLevel()

print "rdd.getStorageLevel() : %s" % rdd.getStorageLevel()
print "rdd.persist(StorageLevel.MEMORY_ONLY) : %s" % rdd.persist(StorageLevel.MEMORY_ONLY) # same with rdd.cache()
print "rdd.getStorageLevel() : %s" % rdd.getStorageLevel()

print "rdd.getStorageLevel() : %s" % rdd.getStorageLevel()
print "rdd.persist(StorageLevel.DISK_ONLY) : %s" % rdd.persist(StorageLevel.DISK_ONLY)
print "rdd.getStorageLevel() : %s" % rdd.getStorageLevel()

###########################################################
# inspection
###########################################################
print "rdd.take(10) : %s" % rdd.take(10)
print "rdd.count() : %s" % rdd.count()

print "df.take(10) : %s" % df.take(10)
print "df.count() : %s" % df.count()
print "df.printSchema()"
df.printSchema()
print "df.columns : %s" % df.columns
print "df.describe() : %s" % df.describe()
print "df.describe(['size']).show()"
df.describe(['size']).show()
print "df.explain(extended=True)"
df.explain(extended=True)

###########################################################
# select
###########################################################
print "df.select('method', 'url', 'status').head()"
print df.select('method', 'url', 'status').head()

print "df.select(df.method, df.url, df.status).first()"
print df.select(df.method, df.url, df.status).first()

df = df.alias('log')
print "df.select('log.method', 'log.url', 'log.status').first()"
print df.select('log.method', 'log.url', 'log.status').first()

###########################################################
# aggregate
###########################################################
print "df.agg({'size' : 'max'}).show()"
df.agg({'size' : 'max'}).show()

print "df.groupBy().agg({'size' : 'max'}).show()"
df.groupBy().agg({'size' : 'max'}).show()

print "df.agg(F.max(df.size)).show()"
df.agg(F.max(df.size)).show()

print "df.agg(F.min(df.size), F.avg(df.size), F.max(df.size)).show()"
df.agg(F.min(df.size), F.avg(df.size), F.max(df.size)).show()

print "df.groupBy(['method', df.status]).count().show()"
df.groupBy(['method', df.status]).count().show()

###########################################################
# query
###########################################################
print "total pv"
print df.count()
spark.sql("select count(1) from apache_access_log_table").show()

print "daily pv"
df.groupBy('date').count().sort('date').show()
spark.sql("select date, count(1) from apache_access_log_table group by date order by date").show()

print "daily status count"
df.groupBy('date', 'status').count().sort('date', 'status').show()
spark.sql("select date, status, count(1) from apache_access_log_table group by date, status order by date, status").show()

print "daily uv"
df.agg(F.countDistinct('date', 'host')).show()
spark.sql("select date, count(distinct host) from apache_access_log_table group by date order by date").show()

print "daily uv (between 20151201 ~ 20151231)"
df.filter(df.date.between('20151201', '20151231')).agg(F.countDistinct('date', 'host').alias('uv')).sort('uv').show()
spark.sql("select date, count(distinct host) from apache_access_log_table where date between '20151201' and '20151231' group by date order by date").show()

print "daily 404 status count"
df.filter(df.status == '404').groupBy('date').count().sort('date').show()
spark.sql("select date, count(1) from apache_access_log_table where status = '404' group by date order by date").show()

###########################################################
# UDF
###########################################################
def slen(s): return len(s)

spark.udf.register('slen', slen)
spark.sql("select slen(url) from apache_access_log_table").show()

slen_udf = F.udf(slen)
df.select(slen_udf(df.url)).show()

###########################################################
# join
###########################################################
df2 = spark.createDataFrame([('200', 'OK'), ('304', 'Not Modified')], ['code', 'desc'])
df3 = df.join(df2, on=df.status==df2.code, how='left_outer')
df3.show()

###########################################################
# write
###########################################################
path = 'hdfs://node-201:9000/data/weblog/2015-1k-transformed'
mode = 'overwrite'
df3.coalesce(1).write.csv(path=path, mode=mode, header=True)

