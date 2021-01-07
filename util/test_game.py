
import json

from basegame import basegame


with open('data/teams/Berlin.json', encoding='utf-8') as f:
    team1 = basegame.Team.load_team(json.load(f))

with open('data/teams/Netherlands.json', encoding='utf-8') as f:
    team2 = basegame.Team.load_team(json.load(f))

m = basegame.Match([team1, team2], 2)
m.print = True

#with open('data/replays/tests/Berlin_Keys_vs_Netherland_Ghasts', 'w+') as f:
		#f.write('')

for i in range(1000000):
	events = m.next()
	#with open('data/replays/tests/Berlin_Keys_vs_Netherland_Ghasts', 'a+') as f:
	#	f.write(json.dumps(events) + '\n')