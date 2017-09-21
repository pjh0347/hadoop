
get 'apache_access_log', '<yyyyMMddHHmmss>-<client address>'
get 'apache_access_log', '<yyyyMMddHHmmss>-<client address>', { COLUMN => 'client' }
get 'apache_access_log', '<yyyyMMddHHmmss>-<client address>', { COLUMN => 'client:address' }
get 'apache_access_log', '<yyyyMMddHHmmss>-<client address>', { COLUMN => 'client:address', VERSIONS => 100 }
get 'apache_access_log', '<yyyyMMddHHmmss>-<client address>', { FILTER => "ValueFilter(=, 'binary:<any value>')" }
get 'apache_access_log', '<yyyyMMddHHmmss>-<client address>', { ROWPREFIXFILTER => '<yyyyMMddHHmmss>' }
get 'apache_access_log', '<yyyyMMddHHmmss>-<client address>', { ROWPREFIXFILTER => '<yyyyMMdd>' }
