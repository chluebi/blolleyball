import os
import json
import random

def populate_tournament():
	names = []
	for team in os.listdir('data/teams'):
		with open(os.path.join('data/teams', team)) as f:
			name = json.load(f)['name']
		names.append(name)

	with open('data/tournament.json') as f:
		data = json.load(f)

	for i in range(8):
		t1 = random.choice(names)
		names.remove(t1)
		t2 = random.choice(names)
		names.remove(t2)

		data['data'][0][i][0] = t1
		data['data'][0][i][1] = t2

	with open('data/tournament.json', 'w') as f:
		json.dump(data, f, indent=4)