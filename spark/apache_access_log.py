import re
from dateutil import parser
from pyspark.sql import Row

APACHE_ACCESS_LOG_PATTERN = '^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+)? ?(\S+)? ?(\S+)?" (\d{3}) ([\d-]+) ?"?([^"]+)?"? ?"?([^"]+)?"?'
pattern = re.compile(APACHE_ACCESS_LOG_PATTERN)

def parse(line):
	row = None

	try:
		m = pattern.match(line)

		time = m.group(4)
		time = parser.parse(time.replace(':', ' ', 1))

		date = time.strftime('%Y%m%d')

		size = m.group(9)
		if size == '-': size = 0
		else: size = long(size)

		row = Row(host     = m.group(1),
			  identity = m.group(2),
			  user     = m.group(3),
			  time     = time,
			  method   = m.group(5),
			  url      = m.group(6),
			  protocol = m.group(7),
			  status   = m.group(8),
			  size     = size,
			  referer  = m.group(10),
			  agent    = m.group(11),
			  date     = date)
	except:
		print "apache access log parsing error : ", line

	return row

