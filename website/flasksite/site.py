from flask import Flask, render_template, url_for
from website.flasksite.util import *
app = Flask(__name__, static_url_path='/static')


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
def replays():
	return render_template('replays.html')


@app.route('/api/teams')
def api_teams():
	return json_load_teams()

@app.route('/api/tournament')
def api_tournament():
	return json_load_tournament()



app.run(debug=True, port=37070, host='0.0.0.0')