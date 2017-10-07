
CREATE INDEX idx_apache_access_log_01 ON TABLE tbl_apache_access_log (status) AS 'COMPACT' WITH DEFERRED REBUILD;
ALTER INDEX idx_apache_access_log_01 ON tbl_apache_access_log REBUILD;
-- SHOW FORMATTED INDEX ON tbl_apache_access_log;
-- DROP INDEX idx_apache_access_log_01 ON tbl_apache_access_log;

