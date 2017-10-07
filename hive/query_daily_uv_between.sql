SELECT p_time, COUNT(DISTINCT host) FROM tbl_apache_access_log WHERE p_time BETWEEN '20151201' AND '20151231' GROUP BY p_time ORDER BY p_time;
