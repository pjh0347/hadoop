SELECT p_time, status, COUNT(1) FROM tbl_apache_access_log WHERE p_time BETWEEN '20151220' AND '20151231' GROUP BY p_time, status ORDER BY p_time, status;
