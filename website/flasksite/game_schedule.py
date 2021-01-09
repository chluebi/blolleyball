import schedule
import time
import random
import os
import json

from basegame import basegame
from util.config_handling import load_config

config = load_config()
DELAY = config['site']['match_tick']


def match(team1, team2):

	first_word = team1.split(' ')[1]
	with open(f'data/teams/{first_word}.json', encoding='utf-8') as f:
	    team1 = basegame.Team.load_team(json.load(f))

	first_word = team2.split(' ')[1]
	with open(f'data/teams/{first_word}.json', encoding='utf-8') as f:
	    team2 = basegame.Team.load_team(json.load(f))

	m = basegame.Match([team1, team2], 2)
	m.debug = False
	m.print = False

	while True:
		try:
			event = m.next()
			event['event'] = 'match'
		except Exception as e:
			event['event'] = 'over'

		with open('data/current.json', 'w') as f:
			json.dump(event, f)

		time.sleep(DELAY)
		if event['event'] == 'over':
			break


def random_match():
	names = ['0 Berlin Keys', '0 British \"People\"', '0 Glasgow Pans', '0 Hamburg Taxis']
	'''
	for team in os.listdir('data/teams'):
		with open(os.path.join('data/teams', team)) as f:
			name = json.load(f)['name']
		names.append(name)
	'''

	t1 = random.choice(names)
	t2 = random.choice(names)
	while t2 == t1:
		t2 = random.choice(names)

	print('random match', t1, t2)
	match(t1, t2)



schedule.every().day.at('19:00').do(random_match)

while True:
    schedule.run_pending()
    time.sleep(1)