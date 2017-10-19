
describe 'apache_access_log'

get 'apache_access_log', '<yyyyMMddHHmmss>-<client address>'
get 'apache_access_log', '<yyyyMMddHHmmss>-<client address>', { COLUMN => 'client' }
get 'apache_access_log', '<yyyyMMddHHmmss>-<client address>', { COLUMN => 'client:address' }
get 'apache_access_log', '<yyyyMMddHHmmss>-<client address>', { COLUMN => 'client:address', VERSIONS => 100 }
get 'apache_access_log', '<yyyyMMddHHmmss>-<client address>', { FILTER => "ValueFilter(=, 'binary:<any value>')" }

scan 'apache_access_log', ROWPREFIXFILTER => '<yyyyMMddHHmmss>'
scan 'apache_access_log', ROWPREFIXFILTER => '<yyyyMMddHHmmss>', COLUMNS => 'request'
scan 'apache_access_log', ROWPREFIXFILTER => '<yyyyMMddHHmmss>', COLUMNS => 'request:url'
scan 'apache_access_log', ROWPREFIXFILTER => '<yyyyMMddHHmmss>-<client address>', COLUMNS => 'request:url', VERSIONS => 1000
scan 'apache_access_log', ROWPREFIXFILTER => '<yyyyMMddHHmmss>', COLUMNS => 'request:url', VERSIONS => 1000, FILTER => "ValueFilter(=, 'substring:.jpg')"
