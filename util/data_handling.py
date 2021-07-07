import os

def clear_tournament_replays():
    base_path = 'data/replays/tournament/'
    for file in os.listdir(base_path):
        os.remove(base_path + file)