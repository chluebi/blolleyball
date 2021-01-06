from flask import Flask, render_template, url_for, request
from website.flasksite.util import *
from website.flasksite import replays
app = Flask(__name__, static_url_path='/blolleyball/static')


@app.route('/')
def home():
   return render_template('main.html')


@app.route('/teams')
def teams():
   return render_template('teams.html', teams=load_teams())

@app.route('/tournament')
def tournament():
	return render_template('tournament.html')


@app.route('/replays')
def replays_main():
	files = get_folder('data/replays', folder_only=True)
	return render_template('replays.html', files=files, path='replays')

@app.route('/replays/<replay_category>')
def replays_category(replay_category):
	files = get_folder(f'data/replays/{replay_category}', folder_only=False)
	return render_template('replays.html', files=files, path=f'replays/{replay_category}')

@app.route('/replays/<replay_category>/<game>')
def replays_game(replay_category, game):
	return render_template('replay.html', replay_category=replay_category, game=game)


@app.route('/api/replays/<replay_category>/<game>')
def api_replay(replay_category, game):
	return replays.load_game(replay_category, game)

@app.route('/api/teams')
def api_teams():
	return json_load_teams()

@app.route('/api/tournament')
def api_tournament():
	return json_load_tournament()



app.run(debug=True, port=37070, host='0.0.0.0')