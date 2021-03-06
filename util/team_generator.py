import json
import random
from basegame.basegame import *

team_names = [
	'👻 Netherlands Ghasts',
	'🍳 Glasgow Pans',
	'⚡ Paris Circuits',
	'🗝️ Berlin Keys',
	'🚕 Hamburg Taxis',
	'💿 Melbourne Discs',
	'🎈 York Ballons',
	'🐉 Roman Dragons',
	'🦊 Elysium Foxes',
	'🎷 Kimberley Saxophones',
	'⛓️ Rio Chains',
	'🪁 Catalonian Kites',
	'🥚 Vienna Eggs',
	'🔋 Sun City Batteries'
]

player_names = [
	'Penguin Pitch',
	'Jaxon Dry',
	'Ayla Wall',
	'Syllia Umeris',
	'Sibren Veenhuis',
	'Labyrinth Quinn',
	'Chaos Fade',
	'Echo Nox',
	'Charles Magnus',
	'Kaiser Drach',
	'Tretan Boradil',
	'Gacco Bi',
	'Violet Froid',
	'Pink Mechanical',
	'Jeanne Luna',
	'Shady Angel',
	'Skeletal Curator',
	'Royal Mandrake',
	'Brown Cobra',
	'Liang Huan',
	'Taute Wildmane',
	'Gwentin Tizwyn',
	'Nymph Wynter',
	'Mario Vogl',
	'Caspian Lyn',
	'Brodir Jonsson',
	'Kinesh Freiburg',
	'Omen Mask',
	'Lindsay Chalice',
	'Noël Clair',
	'Lydia Plouffe',
	'Gus Norman',
	'Hegel Beans'
]

print(len(player_names), len(team_names)*6)

'''
for team_name in team_names:
	players = []
	for i in range(6):
		if len(player_names) < 1:
			break
		else:
			p = random.choice(player_names)
		player_names.remove(p)
		stats = Player.random_stats()
		player = Player(p, stats)
		old_rating = player.rating()/5
		new_rating = sum([random.random() for i in range(4)])/4
		for key, value in player.stats.items():
			player.stats[key] = value/old_rating*new_rating
		players.append(player)

	team = Team(team_name, players)
	sum_stats = team.sum_stats()

	for player in team.players:
		for key, value in player.stats.items():
			player.stats[key] = value/sum_stats*42

	first_word = team_name.split(' ')[1]
	with open(f'data/teams/{first_word}.json', 'w+') as f:
		json.dump(team.export_team(), f, indent=4)
'''