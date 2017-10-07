
-- examples
load data inpath '</hdfs/path/file.txt>' into table test;
load data local inpath '</local/path/file.txt>' into table test;
load data inpath '</hdfs/path/file.txt>' overwrite into table test;
load data inpath '</hdfs/path/file.txt>' into table test partition (ts='2017-01-01');

