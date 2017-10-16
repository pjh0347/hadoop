# coding: utf-8
#!/bin/env python

"""
 Word counter exercise

 * outputMode
   complete : Result Table 모두 출력.
   update : Result Table 에서 업데이트된 Row 만 출력. 
            데이터 처리 소요 시간이 항상 일정하지 만은 않기 때문에, 
            데이터가 일정한 속도로 들어와도 매번 처리되는 데이터 건수는 다르다.
   append : Result Table 에 새로 추가된 Row 만 출력. 
            기존 Result Table Row 들을 업데이트 시키지 않는 경우에 사용해야 한다.
            윈도우 기반으로 워터마크를 이용하는 경우에 group by 같은 집계 연산이 가능하다.

 * 문제점
   아직 인터페이스가 깔끔하지 않다.
   경우에 따라서 지원되지 않는 연산이 많기 때문에 몇 가지 케이스들을 잘 숙지해야 한다!!!
   데이터 양이 많지 않은데도(예제 수준에서 돌려봐도) 속도가 느린데 원래 문제가 있는 것인지, 
   아니면 튜닝을 해야 하는것인지 알 수 없다. 즉, 아직 뭔가 어수선한 느낌이다.

"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
                    .master("spark://192.168.10.201:7077") \
                    .appName("wordcount exercise") \
                    .config("spark.submit.deployMode", "client") \
                    .config("spark.executor.memory", "1g") \
                    .getOrCreate()

lines = spark.readStream \
             .format('socket') \
             .option('host', 'node-201') \
             .option('port', 8440) \
             .option('includeTimestamp', 'true') \
             .load()

print "lines.isStreaming : ", lines.isStreaming
print "lines.printSchema()"
lines.printSchema()

words = lines.select(
	F.explode(F.split(lines.value, ' ')).alias('word'),
	lines.timestamp
)

# non-window based aggregation
counts = words.groupBy(words.word).count()
query = counts.writeStream \
              .outputMode("complete") \
              .format("console") \
              .start()

# window based aggregation
windowedCounts = words.groupBy(
    F.window(words.timestamp, '5 seconds', '2 seconds'),
    words.word
).count()
windowedQuery = windowedCounts.writeStream \
                              .outputMode("complete") \
                              .format("console") \
                              .start()

# window based aggregationi with watermark
windowedWithWatermarkCounts = words.withWatermark('timestamp', '5 seconds') \
                                   .groupBy(
                                       F.window(words.timestamp, '5 seconds', '2 seconds'), 
                                       words.word
                                   ).count()
windowedWithWatermarkQuery = windowedWithWatermarkCounts.writeStream \
                                                        .outputMode("complete") \
                                                        .format("console") \
                                                        .start()

query.awaitTermination()
windowedQuery.awaitTermination()
windowedWithWatermarkQuery.awaitTermination()

