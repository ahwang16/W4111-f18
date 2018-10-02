# csvtest.py

import CSVTable

csv1 = CSVTable.CSVTable("People", "People.csv", ['playerID'])
csv1.load()

t = {'playerID':'ahh2143', 'birthYear':'1998', 'birthMonth':'8', 'birthDay':'13', 'birthCountry':'USA', 'nameLast':'Hwang', 'nameFirst':'Alyssa'}
print("Inserting {'playerID':'ahh2143', 'birthYear':'1998', 'birthMonth':'8', 'birthDay':'13', 'birthCountry':'USA', 'nameLast':'Hwang', 'nameFirst':'Alyssa'} to people table")
csv1.insert(t)
print("done")

print("Finding what I just inserted")
print(csv1.find_by_template(t, None))

print("Trying to insert the same thing--should result in error")
try:
	csv1.insert(t)
except:
	print("Properly refused to insert invalid record")

print("Delete the record")
csv1.delete(t)
print("done")

print("Find what I just deleted--should be nothing")
print(csv1.find_by_primary_key(["ahh2143"], None))
print("done")

csv2 = CSVTable.CSVTable("Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"])
csv2.load()
print('Insert {"playerID": "dff1", "teamID": "BOS", "yearID": "2018", "stint": "1", "AB": "100", "H": "100"}')
print(csv2.insert({"playerID": "dff1", "teamID": "BOS", "yearID": "2018", "stint": "1", "AB": "100", "H": "100"}))

print("Find what I just inserted")
print(csv2.find_by_template({'playerID':'dff1'}))

print("Delete what I just inserted")
csv2.delete({"playerID": "dff1", "teamID": "BOS", "yearID": "2018", "stint": "1", "AB": "100", "H": "100"})
print("done")

# print("Find everyone born in August")
# print(csv1.find_by_template({"birthMonth":"8"}))

print("Insert without a primary key to people table: {'nameLast':'Hwang', 'birthMonth':'8'}--should be error")
try:
	csv1.insert({'nameLast':'Hwang', 'birthMonth':'8'})
except:
	print("Properly refused to insert invalid record")

print("Insert with invalid field: {'playerID':'ahh2143', 'college':'Columbia'}")
try:
	csv1.insert({'playerID':'ahh2143', 'college':'Columbia'})
except:
	print("Properly refused to insert invalid record")
