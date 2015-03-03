'''
#file: example.conf

[DEFAULT]
conn_str = %(dbn)s://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s
dbn = mysql
user = root
host = localhost
port = 3306
[db1]
user = aaa
pw = ppp
db = example
[db2]
host = 192.168.0.1
pw = www
db = example
'''

import ConfigParser
conf = ConfigParser.ConfigParser()
conf.read('format.conf')
print conf.get('db1','conn_str')
print conf.get('db2','conn_str')
