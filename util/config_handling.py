
import json
import os

def load_config():
	data = {}
	for file in os.listdir('configs'):
		with open('configs/' + file) as f:
			basename, _ = os.path.splitext(file)
			data[basename] = json.load(f)
	return data