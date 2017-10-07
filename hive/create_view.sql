
CREATE VIEW view_apache_access_log AS 
SELECT 
  host,
  identity,
  remote_user,
  CAST(FROM_UNIXTIME(UNIX_TIMESTAMP(time, 'dd/MMM/yyyy:HH:mm:ss Z')) AS TIMESTAMP) time,
  method,
  url,
  protocol,
  status,
  CAST(REGEXP_REPLACE(size, '-', '0') AS BIGINT) size,
  referer,
  agent
FROM 
  etbl_apache_access_log;

