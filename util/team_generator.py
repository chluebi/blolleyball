import json
import random
from basegame.basegame import *


def generate_teams():
	cities = [
		'Amsterdam',
		'Glasgow',
		'Paris',
		'Berlin',
		'Hamburg',
		'Melbourne',
		'York',
		'Roman',
		'Elysium',
		'Kimberley',
		'Rio',
		'Barcelona',
		'Vienna',
		'Sun City',
		'Zurich',
		'British'
	]

	objects = [
		['👻', 'Ghasts'],
		['🍳', 'Pans'],
		['⚡', 'Circuits'],
		['🗝️', 'Keys'],
		['🚕', 'Taxis'],
		['💿', 'Discs'],
		['🎈', 'Ballons'],
		['🐉', 'Dragons'],
		['🦊', 'Foxes'],
		['🎷', 'Saxophones'],
		['⛓️', 'Chains'],
		['🪁', 'Kites'],
		['🥚', 'Eggs'],
		['🔋',  'Batteries'],
		['🎀', 'Ribbons'],
		['🧲', 'Magnets']
	]

	player_names = [
		'Penguin',
		'Pitch',
		'Jaxon',
		'Dry',
		'Ayla',
		'Wall',
		'Syllia',
		'Umeris',
		'Sibren',
		'Veenhuis',
		'Labyrinth',
		'Quinn',
		'Chaos',
		'Fade',
		'Echo',
		'Nox',
		'Charles',
		'Magnus',
		'Kaiser',
		'Drach',
		'Tretan' 
		'Boradil',
		'Gacco',
		'Bi',
		'Violet'
		'Froid',
		'Pink',
		'Mechanical',
		'Jeanne',
		'Luna',
		'Shady',
		'Angel',
		'Skeletal',
		'Curator',
		'Royal',
		'Mandrake',
		'Brown',
		'Cobra',
		'Liang',
		'Huan',
		'Taute',
		'Wildmane',
		'Gwentin',
		'Tizwyn',
		'Nymph',
		'Wynter',
		'Mario',
		'Vogl',
		'Caspian',
		'Lyn',
		'Brodir',
		'Jonsson',
		'Kinesh',
		'Freiburg',
		'Omen',
		'Mask',
		'Lindsay',
		'Chalice',
		'Noël',
		'Clair',
		'Lydia',
		'Plouffe',
		'Gus',
		'Norman',
		'Hegel',
		'Beans',
		'Forest',
		'Rock',
		'Tree',
		'River',
		'Hill',
		'House',
		'Rabbit',
		'Elbiranth',
		'Zanai',
		'Siaphas',
		'Xypais',
		'Camruss',
		'Brave',
		'Gifted',
		'True',
		'Crimson',
		'Angel',
		'Blind',
		'Yellow',
		'Adam',
		'Eren',
		'Nes',
		'Sunu',
		'Melon',
		'Jon',
		'Theobald',
		'Guinevere',
		'Maddock',
		'Eiriol',
		'Maddock',
		'Elin',
		'Glovruk',
		'Bobby',
		'Joe',
		'James',
		'Jon',
		'Garfield',
		'President',
		'Big',
		'Holy',
		'First',
		'Wraith',
		'Sparkling',
		'Joyce',
		'Barbara',
		'Theodore',
		'Ed',
		'Lela',
		'Beth',
		'Bri',
		'Gracy',
		'Dog',
		'Cat',
		'Rabbit',
		'Drake',
		'Bear',
		'Beaver',
		'Slayer',
		'Avenger',
		'Reaper',
		'Solver',
		'Finder',
		'Friend',
		'Gamer',
		'Black',
		'White',
		'Red',
		'Blue',
		'Purple',
		'Glass',
		'Stone',
		'Wood',
		'Roland',
		'Gnill',
		'Gnugg',
		'Tustran',
		'Caelvu',
		'Pumpblock',
		'Finebell',
		'Castfluke',
		'Niftyclock',
		'Singlefizz'
	]


	for k in range(16):
		players = []
		for i in range(6):
			if len(player_names) < 1:
				break
			else:
				first = random.choice(player_names)
				last = random.choice(player_names)

			stats = Player.random_stats()
			player = Player(f'{first} {last}', stats)
			old_rating = player.rating()/5
			new_rating = sum([random.random() for i in range(3)])/3
			for key, value in player.stats.items():
				player.stats[key] = value/old_rating*new_rating
			players.append(player)

		city = random.choice(cities)
		cities.remove(city)
		obj = random.choice(objects)
		objects.remove(obj)

		team = Team(f'{obj[0]} {city} {obj[1]}', players)
		sum_stats = team.sum_stats()

		for player in team.players:
			for key, value in player.stats.items():
				player.stats[key] = value/sum_stats*42

		first_word = city.split()[0]
		with open(f'data/teams/{first_word}.json', 'w+') as f:
			json.dump(team.export_team(), f, indent=4)