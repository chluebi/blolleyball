import os
import json


def load_game(replay_category, game):
    path = replay_category + '/' + game
    
    with open('data/replays/' + path, 'r') as f:
        lines = [json.loads(l) for l in f.readlines()]

    for line in lines:
        for key, value in line.items():
            if type(value) is str:
                line[key] = value.replace('\n', '<br>')

    data = {'data': lines}

    return json.dumps(data)
