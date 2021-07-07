import schedule
import time
import random
import os
import json
import math

from datetime import datetime


from basegame import basegame
from util.config_handling import load_config
from util.webhook_handling import send_message

config = load_config()
DELAY = config['site']['match_tick']

def generate_teams():
    	

def now_string():
	now = datetime.now()
	return now.strftime('%Y.%m.%d_%H.%M.%S')


def match(team1, team2, save_path):

	with open(save_path, 'w+') as f:
		f.write('')

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
		if m.game is False:
			event['event'] = 'over'
		else:
			event = m.next()
			event['event'] = 'match'

		with open('data/current.json', 'w') as f:
			json.dump(event, f)

		with open(save_path, 'a+') as f:
			f.write(json.dumps(event) + '\n')

		time.sleep(DELAY)
		if event['event'] == 'over':
			break

	return m


def random_match():
	names = []
	for team in os.listdir('data/teams'):
		with open(os.path.join('data/teams', team)) as f:
			name = json.load(f)['name']
		names.append(name)


	t1 = random.choice(names)
	t2 = random.choice(names)
	while t2 == t1:
		t2 = random.choice(names)

	print('random match', t1, t2)
	match(t1, t2, f'data/replays/tests/{now_string()}_{t1.split()[1]}_{t2.split()[1]}')


def advance_tournament():
	with open('data/tournament.json') as f:
		tournament_data = json.load(f)['data']

	for i, r in enumerate(tournament_data):
		for j, m in enumerate(r):
			for k, team in enumerate(m):
				if team is None:
					if i == 0:
						raise Exception('Not enough teams')
					else:
						previous_match = (i - 1, j * 2 + k)
						pr_depth, pr_breadth = previous_match
						team1, team2 = tournament_data[pr_depth][pr_breadth]
						
						print('match', team1, team2)
						m = match(team1, team2, f'data/replays/tournament/{now_string()}_{team1.split()[1]}_{team2.split()[1]}')
						send_message(f'{team1} vs {team2} match starting!')
						winner = m.winner.name

						tournament_data[i][j][k] = winner
						tournament_data = {'data': tournament_data}

						with open('data/tournament.json', 'w') as f:
							json.dump(tournament_data, f, indent=4)
						return
			else:
				pass


schedule.every().day.at('13:29').do(random_match)

while True:
    schedule.run_pending()
    time.sleep(1)
