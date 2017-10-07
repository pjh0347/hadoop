
SET hive.exec.dynamic.partition.mode = nonstrict;
SET hive.exec.max.dynamic.partitions.pernode = 1000000;

INSERT OVERWRITE TABLE 
  tbl_apache_access_log 
PARTITION (p_time, p_host)
SELECT 
  host,
  identity,
  remote_user,
  CAST(FROM_UNIXTIME(UNIX_TIMESTAMP(time, 'dd/MMM/yyyy:HH:mm:ss Z')) AS TIMESTAMP),
  method,
  url,
  protocol,
  status,
  CAST(REGEXP_REPLACE(size, '-', '0') AS BIGINT) size,
  referer,
  agent,
  FROM_UNIXTIME(UNIX_TIMESTAMP(time, 'dd/MMM/yyyy:HH:mm:ss Z'), 'yyyyMMdd'),
  SUBSTR(host, -1, 1)
FROM 
  etbl_apache_access_log;

