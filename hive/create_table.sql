
-- external table
CREATE EXTERNAL TABLE etbl_apache_access_log (
  host STRING,
  identity STRING,
  remote_user STRING,
  time STRING,
  method STRING,
  url STRING,
  protocol STRING,
  status STRING,
  size STRING,
  referer STRING,
  agent STRING)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
WITH SERDEPROPERTIES (
  "input.regex" = "^(\\S+) (\\S+) (\\S+) \\[([\\w:/]+\\s[+\\-]\\d{4})\\] \"(\\S+)? ?(\\S+)? ?(\\S+)?\" (\\d{3}) ([\\d-]+) ?\"?([^\"]+)?\"? ?\"?([^\"]+)?\"?",
  "columns.types" = "string,string,string,string,string,string,string,string,string,string,string"
)
STORED AS TEXTFILE
LOCATION '<HDFS directory path>';

-- managed table
CREATE TABLE tbl_apache_access_log (
  host STRING,
  identity STRING,
  remote_user STRING,
  time TIMESTAMP,
  method STRING,
  url STRING,
  protocol STRING,
  status STRING,
  size BIGINT,
  referer STRING,
  agent STRING)
PARTITIONED BY (p_time STRING, p_host STRING)
STORED AS TEXTFILE;

