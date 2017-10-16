from pyspark import StorageLevel
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext

spark = SparkSession.builder \
                    .master("spark://192.168.10.201:7077") \
                    .appName("wordcount exercise") \
                    .config("spark.submit.deployMode", "client") \
                    .config("spark.executor.memory", "1g") \
                    .getOrCreate()
ssc = StreamingContext(spark.sparkContext, batchDuration=1) # window_size = interval_size = 1
ssc.checkpoint("checkpoint")

lines = ssc.socketTextStream(hostname='node-201', 
                             port=8440, 
                             storageLevel=StorageLevel.MEMORY_ONLY)

words = lines.flatMap(lambda line: line.split(" "))
pairs = words.map(lambda word: (word, 1))
counts = pairs.reduceByKey(lambda a, b: a+b)
counts.pprint() # print word count every second. (t-1 ~ t)

def updateFunction(new_values, cur_value):
	return (cur_value or 0) + sum(new_values)
state = pairs.updateStateByKey(updateFunction)
state.pprint() # print accumulative word count every second. ( ~ t)

windowedWordCounts = pairs.reduceByKeyAndWindow(lambda a, b: a+b, 
                                                lambda a, b: a-b, 
                                                windowDuration=5, 
                                                slideDuration=2)
windowedWordCounts.pprint() # print word count once every two seconds. (t-4 ~ t)

ssc.start()
ssc.awaitTermination()

