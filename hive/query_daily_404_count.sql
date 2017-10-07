SELECT p_time, COUNT(1) FROM tbl_apache_access_log WHERE p_time BETWEEN '20151220' AND '20151231' AND status = '404' GROUP BY p_time ORDER BY p_time;
