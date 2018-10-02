# ten_greatest_hitters_rdb.py

# Find the ten greatest hitters in the RDB.

# SQL implementation of ten greatest hitters algorithm provided by Prof F.

import RDBTable


connect_info = { 'host':'localhost', 'user':'root', 'password':'Jellybean128!', 'db':'Lahman2017'}
rdb = RDBTable.RDBTable("people", "Lahman2017", ["playerID"], connect_info)
print(rdb.ten_greatest_hitters())