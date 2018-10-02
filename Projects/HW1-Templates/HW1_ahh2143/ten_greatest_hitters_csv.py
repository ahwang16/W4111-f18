# ten_greatest_hitters_csv.py

from CSVTable import CSVTable

csvb = CSVTable("Batting", "Batting.csv", ['playerID', 'yearID'])
csvp = CSVTable("People", "People.csv", ['playerID'])

csvb.load()
csvp.load()


batting = {}

# batting records after 1960
for y in range(1960, 2019):
    results = csvb.find_by_template({'yearID': str(y)}, ['playerID', 'yearID', 'AB', 'H'])

    # Compute average batting score for every player year by year --> update existing players or add a new one
    # batting average = H / AB --> hits / at bats
    for result in results:
        player = result['playerID']

        if player in batting.keys():
            batting[player]['total_AB'] += int(result['AB'])
            batting[player]['total_H'] += int(result['H'])

            if batting[player]['total_AB'] > 0:
                batting[player]['average'] = batting[player]['total_H'] / batting[player]['total_AB']
        else:
            batting[player] = {
	            'total_AB':int(result['AB']),
	            'total_H':int(result['H'])
	        }

            if batting[player]['total_AB'] > 0:
                batting[player]['average'] = batting[player]['total_H'] / batting[player]['total_AB']
            else:
            	batting[player]['average'] = 0

batting2 = {}

for player in batting:
    if batting[player]['total_AB'] > 200:
        batting2[player] = batting[player]

people = {}

for player in batting2:
    result = csvp.find_by_template({'playerID': player}, ['nameFirst', 'nameLast'])[0]
    people[player] = {
	    'average':batting2[player]['average'],
	    'nameFirst':result['nameFirst'],
	    'nameLast':result['nameLast']
    }

players = sorted(people.items(), key=lambda k: k[1]['average'], reverse=True)
print(players[:10])