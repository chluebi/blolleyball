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

    data['data'] = [None for i in range(7)]

    data['data'][0] = [None for i in range(8)]

    for i in range(8):
        t1 = random.choice(names)
        names.remove(t1)
        t2 = random.choice(names)
        names.remove(t2)
        data['data'][0][i] =[t1, t2]

    for k in range(1, 4):
        data['data'][k] = [[] for i in range(8//2**k)]
        data['data'][k] = [[None, None] for match in data['data'][k]]

    data['data'][4] = [[None]]
    data['data'][5] = []
    data['data'][6] = []

    with open('data/tournament.json', 'w') as f:
        json.dump(data, f, indent=4)