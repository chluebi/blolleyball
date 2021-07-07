
import requests
import json

from util.config_handling import load_config

config = load_config()
webhook_url = config['site']['webhook_url'] + '?wait=true'
role_id = config['site']['webhook_mention_id']


def send_message(title):
	embed = {
		'title': 'Automatic Notification',
		'description' : f'<@&{role_id}> \n\n {title}'
	}

	message = {
		'embeds': [embed]
	}

	message = json.dumps(message)
	headers = {'Content-Type': 'application/json'}

	r = requests.post(webhook_url, data=message, headers=headers)