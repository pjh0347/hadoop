hadoop jar hbase-loader-0.0.1-SNAPSHOT-jar-with-dependencies.jar \
    com.coreaos.hbase.loader.HBaseLoader \
    -D hbase.loader.tableName=<HBase Table Name> \
    -D hbase.loader.inputPath=<HDFS file path> \
    -D hbase.loader.hFilePath=<Temporary HFile path> \
    -D hbase.loader.serverAddress=<Server Host>