import os
import json

from basegame import basegame

def load_teams():
	teams = []
	for file in os.listdir('data/teams'):
		with open(os.path.join('data/teams', file)) as f:
			data = json.load(f)
		teams.append(basegame.Team.load_team(data))

	teams_data = []
	for team in teams:
		data = {'name': team.name, 'players': []}
		for player in team.players:
			data['players'].append({'name': player.name, 'rating': round(player.rating()/0.5)*0.5})

		teams_data.append(data)

	return teams_data

def get_folder(path, folder_only=False):
	return [{'name': file.replace('_', ' ').capitalize(), 'link': file} for file in sorted(os.listdir(path)) if not folder_only or os.path.isdir(os.path.join(path, file))]


def json_load_teams():
	return json.dumps({'data': load_teams()})


def json_load_tournament():
	with open('data/tournament.json') as f:
		data = json.load(f)

	return json.dumps(data)