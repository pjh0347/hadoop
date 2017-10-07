SELECT p_time, COUNT(DISTINCT host) FROM tbl_apache_access_log GROUP BY p_time ORDER BY p_time;
