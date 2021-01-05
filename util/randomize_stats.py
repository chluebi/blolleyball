import json
import random

file = 'British.json'

with open(f'{file}', encoding='utf-8') as f:
    team = json.load(f)

for player in team['players']:
	for key, value in player['stats'].items():
		player['stats'][key] = random.random()

with open(f'{file}', 'w', encoding='utf-8') as f:
	json.dump(team, f, indent=4)