from basegame.basegame import *
import json

'''
with open('data/teams/karasuno.json') as f:
	karasuno = Team.load_team(json.load(f))

with open('data/teams/nekoma.json') as f:
	nekoma = Team.load_team(json.load(f))
m = Match([karasuno, nekoma], 3)

m.debug = False
m.print = True
for i in range(10):
	events = m.next()
	if m.n is None:
		break
	if m.n[0] is None:
		break
	print(json.dumps(events))
'''
'''
with open('games/test_game.txt', 'w+', encoding='utf-8') as f:
	for entry in m.history:
		f.write(entry + '\n')$
'''

with open('data/teams/British.json') as f:
	british = Team.load_team(json.load(f))
	for player in british.players:
		print(player.name, player.rating())