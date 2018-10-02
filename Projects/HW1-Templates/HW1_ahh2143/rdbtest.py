# rdbtest.py

# Test cases for RDBTable (SQL implementation)

import RDBTable

connect_info = { 'host':'localhost', 'user':'root', 'password':'Jellybean128!', 'db':'lahman2017'}

rdb1 = RDBTable.RDBTable("people", "lahman2017", ['playerID'], connect_info)
t = {'playerID':'ahh2143', 'birthYear':'1998', 'birthMonth':'8', 'birthDay':'13', 'birthCountry':'USA', 'nameLast':'Hwang', 'nameFirst':'Alyssa'}
print("Inserting {'playerID':'ahh2143', 'birthYear':'1998', 'birthMonth':'8', 'birthDay':'13', 'birthCountry':'USA', 'nameLast':'Hwang', 'nameFirst':'Alyssa'} to people table")
rdb1.insert(t)
print("done")

print("Finding what I just inserted")
print(rdb1.find_by_template(t, None))

print("Trying to insert the same thing--should result in error")
rdb1.insert(t)

print("Delete the record")
rdb1.delete(t)
print("done")

rdb2 = RDBTable.RDBTable("battingsmall", "lahman2017", ["playerID", "teamID", "yearID", "stint"], connect_info)
print("Try to insert batting record for Alyssa--should result in error")
r = {"playerID":"ahh2143", "yearID":"2018", "teamID":"YAN", "stint":"3"}
rdb2.insert(r)

print("Insert people record for Alyssa")
rdb1.insert(t)
print("done")

print("Try again to insert batting record for Alyssa")
rdb2.insert(r)
print("done")

print("Find what I just inserted")
print(rdb2.find_by_primary_key(["ahh2143", "YAN", "2018", "3"], None))

print("Delete batting record for Alyssa")
rdb2.delete(r)
print("Done")

print(rdb2)

