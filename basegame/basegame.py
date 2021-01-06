import random
import collections
import copy
import json
import tqdm


class Player:

	@staticmethod
	def random_stats():
		return {
			'height': random.random(),

			'constitution': random.random(),
			'agility': random.random(),
			'jump': random.random(),
			'intelligence': random.random(),
			'reflexes': random.random(),

			'serve_strength': random.random(),
			'serve_precision': random.random(),

			'spike_strength': random.random(),
			'spike_precision': random.random(),

			'overhand_strength': random.random(),
			'overhand_precision': random.random(),

			'dig_precision': random.random(),

			'block_precision': random.random()
		}

	def __init__(self, name, stats):
		self.name = name
		self.stats = stats

	def __repr__(self):
		if hasattr(self, 'number'):
			return f'#{self.number} {self.name}'
		else:
			return f'P[{self.name}'

	def sum_stats(self):
		return sum([value for name, value in self.stats.items()])

	def rating(self):
		return 5*sum([value for name, value in self.stats.items()])/sum([1 for name, value in self.stats.items()])


class Team:

	@staticmethod
	def load_team(data):
		players = []
		for p in data['players']:
			player = Player(p['name'], p['stats'])
			players.append(player)

		team = Team(data['name'], players)
		return team

	def export_team(self):
		data = {}
		data['name'] = self.name
		data['players'] = []
		for player in self.players:
			data['players'].append({'name': player.name, 'stats': player.stats})
		return data

	def __init__(self, name, players):
		self.name = name
		self.players = players
		self.rotation = self.players

		for i, player in enumerate(self.players):
			player.number = i+1

	def __repr__(self):
		return 'The {0}'.format(self.name, '\n'.join([player.name for player in self.rotation]))

	def rotate(self):
		copied_rotation = self.rotation.copy()
		for i in range(6):
			self.rotation[(i+1) % 6] = copied_rotation[i]

	def sum_stats(self):
		stats = []
		for player in self.players:
			for stat, value in player.stats.items():
				stats.append(value)
		return sum(stats)

	def overview_stats(self):
		stats = {}
		for player in self.players:
			for stat, value in player.stats.items():
				if stat in stats:
					stats[stat] += value
				else:
					stats[stat] = value

		return stats

	def ratings(self):
		stats = {}
		for player in self.players:
			stats[str(player)] = player.rating()

		return stats


def flip(x):
	return 1 - x

def deviate(x):
	return x + (random.random()-0.5)*x

def wrap(x, lower, upper):
	if x < lower:
		return upper - (lower - x) + 1
	elif x > upper:
		return lower + (x - upper) - 1
	else:
		return x

def mirror(x):
	if x == 0:
		return 2
	if x == 1:
		return 1
	if x == 2:
		return 0
	if x == 3:
		return 5
	if x == 4:
		return 4
	if x == 5:
		return 3
	return 0


def bar(text, upper, value):
	empty = '▢'
	full = '■'
	overfull = '▶'
	endstring = text
	endstring += ' ['
	amount = int(value//(upper/10))
	for i in range(min(10, amount)):
		endstring += full
	if (10-amount) > 0:
		for i in range(10-amount):
			endstring += empty
		endstring += ']'
	else:
		for i in range(amount-10):
			endstring += overfull
		endstring += ']'
	return endstring

def front(x):
	if x in [0, 5]:
		return 5
	if x in [1, 4]:
		return 4
	if x in [2, 3]:
		return 3

def back(x):
	if x in [0, 5]:
		return 0
	if x in [1, 4]:
		return 1
	if x in [2, 3]:
		return 2

class Match:

	def __init__(self, teams, win_sets):
		self.teams = teams
		self.win_sets = win_sets

		self.set_count = 0
		self.score = []
		self.set_score = [0, 0]
		self.history = []
		
		self.debug = False
		self.print = False

		self.n = [self.start, []]

		self.last = {'events': [],
					'stats': '',
					'field': '',
					'touches': 0}

	def next(self):
		self.n = self.n[0](*self.n[1])
		last = self.last.copy()

		last['set_score'] = self.set_score
		last['score'] = self.score
		last['teams'] = [team.name for team in self.teams]
		self.last['events'] = []

		return last

	def render(self):
		ball_side = self.ball[0]
		ball_slot = self.ball[1]
		ball_status = self.ball[2]

		f = [[['    ' for i in range(2)] for j in range(7)] for k in range(2)]

		if ball_status in ['receive']:
			ball_x = 1
			ball_y = random.randint(0, 1)
		elif ball_status in ['pass']:
			ball_x = 1
			ball_y = random.randint(0, 1)
		elif ball_status in ['set', 'spike', 'block']:
			ball_x = 3
			ball_y = ball_side
		elif ball_status in ['serve']:
			ball_x = 1
			ball_y = 0
		else:
			ball_x = 0
			ball_y = -1

		ball_sum_pos = ball_x + ball_y * 4
		
		for j, side in enumerate(f):

			for i, slot in enumerate(side):
				if i < 6:
					p_num = self.teams[j].rotation[i].number
				else:
					p_num = self.teams[j].rotation[0].number

				if ball_side != j and ball_status in ['block'] and i in [3, 4, 5]:
					blockers = self.ball[3] # val, p_id, stats
					number_b = sum([1 for e in blockers if e[0]])

					ball_pos = ball_slot * 2 + ball_y
					ball_pos = 17 - ball_pos

					def get_pos(right):
						return ((6 + right) // 2, (6 + right) % 2)
					
					if blockers[i-3][0]:
						s = f'   {p_num}' if j == 0 else f'{p_num}   '
						if ball_pos == 6:
							pos = [get_pos(0), get_pos(1), get_pos(2)][i-3]
						elif ball_pos == 7:
							pos = [get_pos(0), get_pos(1), get_pos(2)][i-3]
						elif ball_pos == 8:
							pos = [get_pos(1), get_pos(2), get_pos(3)][i-3]
						elif ball_pos == 9:
							pos = [get_pos(2), get_pos(3), get_pos(4)][i-3]
						elif ball_pos == 10:
							pos = [get_pos(3), get_pos(4), get_pos(5)][i-3]
						elif ball_pos == 11:
							pos = [get_pos(3), get_pos(4), get_pos(5)][i-3]
						else:
							raise Exception('Unknown ball_pos')

						player_slot = pos[0]
						player_y = pos[1]

						f[j][player_slot][player_y] = s
					else:
						player_x = ball_x - 1
						player_y = ball_y

						player_s = [[' ' for _ in range(4)] for __ in range(2)]
						player_s[player_y][player_x] = str(p_num)

						if j == 1:
							player_s = [e[::-1] for e in player_s]

						if i == 6:
							player_s = [player_s[0][0] + player_s[0][1]]

						f[j][i] = [''.join(e) for e in player_s]

				else:
					if ball_side == j and ball_slot == i:
						if ball_status in ['receive', 'pass', 'point']:
							player_x = ball_x - 1
							player_y = ball_y
						elif ball_status in ['set', 'spike', 'block']:
							player_x = ball_x - 1
							player_y = ball_y
						elif ball_status in ['serve']:
							player_x = 0
							player_y = 0
						else:
							raise Exception(f'unknown ball status {ball_status}')
					else:
						player_x = random.randint(1, 2)
						player_y = flip(j)

					player_s = [[' ' for _ in range(4)] for __ in range(2)]
					player_s[player_y][player_x] = str(p_num)
					

					if ball_side == j and ball_slot == i and ball_sum_pos > -1:
						player_s[ball_y][ball_x] = '@'

					if i == 6:
						if player_s[0][0] == str(7):
							player_s = [str(p_num) + player_s[0][1]]
						else:
							player_s = ['  ']

					if j == 1:
						player_s = [e[::-1] for e in player_s]

					f[j][i] = [''.join(e) for e in player_s]
				


		return f'''   _ _ _ _   _ _ _ _
  |{f[0][2][0]}{f[0][3][0]}|{f[1][5][1]}{f[1][0][1]}|  
  |{f[0][2][1]}{f[0][3][1]}|{f[1][5][0]}{f[1][0][0]}|  
  |{f[0][1][0]}{f[0][4][0]}|{f[1][4][1]}{f[1][1][1]}|  
{f[0][6][0]}|{f[0][1][1]}{f[0][4][1]}|{f[1][4][0]}{f[1][1][0]}|{f[1][6][0]}
  |{f[0][0][0]}{f[0][5][0]}|{f[1][3][1]}{f[1][2][1]}|  
  |{f[0][0][1]}{f[0][5][1]}|{f[1][3][0]}{f[1][2][0]}|  
  |_ _ _ _ |_ _ _ _ |'''

		f'''
		  _ _ _ _   _ _ _ _
		 |        |        | 
		 | 2   3  |  5   0 |
		 |        |        | 
		0| 1   4  |  4   1 |0
		 |        |        | 
		 | 0   5  |  3   2 | 
		 |_ _ _ _ |_ _ _ _ |
		'''
		return f'''   _ _ _ _   _ _ _ _
  |        |        |
  | {t1[2]}{b1[2]}  {t1[3]}{b1[3]} | {b2[5]}{t2[5]}  {b2[0]}{t2[0]} |
  |        |        |
{t1[6]}{b1[6]}| {t1[1]}{b1[1]}  {t1[4]}{b1[4]} | {b2[4]}{t2[4]}  {b2[1]}{t2[1]} |{b2[6]}{t2[6]}
  |        |        |
  | {t1[0]}{b1[0]}  {t1[5]}{b1[5]} | {b2[3]}{t2[3]}  {b2[2]}{t2[2]} |
  |_ _ _ _ |_ _ _ _ |'''

	def start(self):
		return [self.determine_start, []]

	def event(self, text, field=True, stat=False):
		if self.print:
			print(text)

		self.history.append(text)


		if hasattr(self, 'touches'):
			self.last['touches'] = self.touches

		if stat:
			self.last['stats'] = text
		else:
			self.last['events'].append(text)

		if field:
			if hasattr(self, 'touches'):
				if self.touches > 0:
					if self.print:
						print(f'touches: {self.touches}')

					self.history.append(f'touches: {self.touches}')

			if self.print:
				print(self.render())
			self.history.append(self.render())
			self.last['field'] = self.render()

	def full_history(self):
		return '\n'.join(self.history)

	def start_set(self):
		self.set_count += 1
		self.score.append([0, 0])
		self.last_point = None

		if self.set_count % 2 == 1:
			self.ball = [self.first_serve, 6, 'serve']

			server = self.teams[self.first_serve].rotation[0]
			self.event(f'{server} is serving for {self.teams[self.first_serve]}', field=True)
			
			return [self.serve, [self.first_serve]]
		else:
			self.ball = [flip(self.first_serve), 6, 'serve']

			server = self.teams[flip(self.first_serve)].rotation[0]
			self.event(f'{server} is serving for {self.teams[flip(self.first_serve)]}', field=True)
			
			return [self.serve, [flip(self.first_serve)]]

	def point(self, team_id):
		team = self.teams[team_id]
		self.score[-1][team_id] += 1
		self.ball = [team_id, 6, 'serve']
		self.touches = 0

		if False:
			raise Exception('Not implemented the final fifth set yet')
		else:
			if self.score[-1][team_id] > 24:
				if self.score[-1][team_id] > self.score[-1][flip(team_id)] + 1:
					if self.set_score[team_id]+1 < self.win_sets:
						self.event(f'{team} has won set #{self.set_count}: {self.score[-1][0]}-{self.score[-1][1]}')
						self.set_score[team_id] += 1
						return [self.start_set, []]
					else:
						self.set_score[team_id] += 1
						self.event('{0} has won the match!\n[{2[0]}-{2[1]}]\n{1}'.format(team, '\n'.join([f'{i}:{j}' for i, j in self.score]), self.set_score))
						return [None, []]
				else:
					return [self.serve, [team_id]]

			else:
				self.event(f'Set #{self.set_count}: {self.score[-1][0]}-{self.score[-1][1]}')
				if self.last_point is not None:
					if self.last_point != team_id:
						self.teams[team_id].rotate()
						self.event(f'{self.teams[team_id]} rotates', field=False)
						self.last_point = team_id
				else:
					self.last_point = team_id

		server = self.teams[team_id].rotation[0]
		self.event(f'{server} is serving for {self.teams[team_id]}', field=True)
		return [self.serve, [team_id]]

	def determine_start(self):
		self.first_serve = random.randint(0, 1)
		self.event(f'{self.teams[self.first_serve]} will have the first serve', field=False)
		return [self.start_set, []]

	def serve(self, team_id):
		self.ball = [team_id, 6, 'serve']
		server = self.teams[team_id].rotation[0]
		#self.event(f'{server} is serving for {self.teams[team_id]}')
		serve_type = ''

		if server.stats['serve_precision'] < 0.3 or server.stats['agility'] < 0.6 or server.stats['jump'] < 0.4:
			serve_type = 'normal standing serve'
			ball_precision = server.stats['serve_precision']*0.7 + server.stats['intelligence'] * 0.5
			ball_strength = server.stats['serve_strength']*0.5
		elif server.stats['serve_precision'] > 0.7 and server.stats['jump'] < 0.4:
			serve_type = 'jump float serve'
			ball_precision = server.stats['jump']*0.3 + server.stats['serve_precision'] * 0.7 + server.stats['intelligence'] * 0.4
			ball_strength = server.stats['jump']*0.3 + server.stats['serve_strength']*0.5
		else:
			serve_type = 'jump serve'
			ball_precision = server.stats['jump']*0.3 + server.stats['serve_precision'] * 0.7 + server.stats['intelligence'] * 0.4
			ball_strength = server.stats['jump']*0.4 + server.stats['serve_strength'] * 0.8

		ball_precision = deviate(ball_precision)
		ball_strength = deviate(ball_strength)

		

		if ball_precision < 0.1:
			self.event(f'{server} failed the {serve_type}', field=False)
			return [self.point, [flip(team_id)]]
		elif ball_strength < 0.1:
			self.event(f'{server} has not made it over the net with {serve_type}', field=False)
			return [self.point, [flip(team_id)]]
		elif ball_precision*3 < ball_strength:
			self.event(f'{server} has hit the ball into the out with {serve_type}', field=False)
			return [self.point, [flip(team_id)]]
		else:
			if ball_strength > 0.8:
				other_p = random.choice([0, 1, 2])
			else:
				other_p = random.choice([3, 4, 5])

			self.ball = [flip(team_id), other_p, 'receive']
			other_player = self.teams[flip(team_id)].rotation[other_p]
			self.event(f'{server} makes a {serve_type} towards {other_player}')
			self.touches = 0

			if self.debug:
				self.event('ball ' + str((ball_precision, ball_strength)), field=False)
			else:
				endstring = '[Serve]\n'
				endstring += bar('Precision', 1.4, ball_precision) + '\n'
				endstring += bar('Strength', 1.2, ball_precision)
				self.event(endstring, field=False, stat=True)

			return [self.receive, [flip(team_id), other_p, ball_precision, ball_strength, ball_strength-1]]

	def receive(self, team_id, p, ball_precision, ball_strength, ball_speed):
		self.touches += 1
		player = self.teams[team_id].rotation[p]
		team = self.teams[team_id]
		
		receive_agility = deviate(player.stats['agility']*0.75 + player.stats['intelligence']*0.25 + player.stats['reflexes']*1.25)
		receive_constitution = deviate(player.stats['constitution']*1.5 + player.stats['intelligence']*0.25)

		receive_precision = 0

		if ball_speed > player.stats['reflexes']*3 + receive_agility/2:
			self.event(f'{player} is too slow to react', field=False)
			return [self.point, [flip(team_id)]]
		if receive_agility**3 < ball_precision*ball_strength*ball_speed:
			self.event(f'{player} fails to receive the ball', field=False)
			return [self.point, [flip(team_id)]]
		elif receive_constitution*2.5 < ball_strength:
			self.event(f'{player} fails to stop the force of the ball', field=False)
			return [self.point, [flip(team_id)]]
		elif receive_constitution < ball_strength:
			receive_precision = player.stats['dig_precision'] * 0.5 + player.stats['reflexes'] * 0.3
			self.event(f'{player} barely manages to dig out the ball', field=False)
		elif ball_strength + ball_precision + ball_speed < receive_constitution:
			receive_precision = player.stats['overhand_precision'] * 2
			self.event(f'{player} manages to receive the ball in overhand', field=False)
		else:
			receive_precision = player.stats['dig_precision'] + (player.stats['reflexes'] - ball_speed) * 0.5
			self.event(f'{player} digs out the ball', field=False)

		if self.debug:
			self.event('receive ' + str((receive_agility, receive_constitution)), field=False)
		else:
			endstring = '[Receive]\n'
			endstring += bar('Agility', 2.5, receive_agility) + '\n'
			endstring += bar('Constitution', 2.5, receive_constitution)
			self.event(endstring, field=False, stat=True)

		receive_precision = deviate(receive_precision)

		def info():
			if self.debug:
				self.event('receive precision ' + str(receive_precision), field=False)
			else:
				endstring = '[Pass]\n'
				endstring += bar('Precision', 2, receive_precision)
				self.event(endstring, field=False, stat=True)

		if receive_precision < 0.1:
			if self.touches < 3:
				other_p = wrap(p + random.choice([-1, 1]), 0, 5)
				other_player = self.teams[team_id].rotation[other_p]
				self.ball = [team_id, other_p, 'receive']
				self.event(f'{player} fails to properly pass the ball and the ball goes to {other_player}')
				info()
				return [self.receive, [team_id, other_p, ball_precision*0.7, ball_strength*0.5, 1-deviate(receive_precision)]]
			else:
				self.event(f'{player} fails to properly pass the ball and the ball stays on the side of {team}')
				info()
				return [self.point, [flip(team_id)]]
		elif (receive_precision < 0.6 and ball_strength > 0.4) or self.touches > 2:
			self.touches = 0
			other_p = random.randint(0, 5)
			self.ball = [flip(team_id), other_p, 'receive']
			self.event(f'{player} passes the ball to the other side of the net')
			info()
			return [self.receive, [flip(team_id), other_p, receive_precision, 0, -1]]
		elif receive_precision < 0.8 and self.touches > 1:
			self.touches -= 1
			self.event(f'{player} prepares to make an emergency set')
			return [self.set, [team_id, p, receive_precision*0.3]]
		elif self.touches > 1:
			self.touches -= 1
			self.event(f'{player} prepares to directly set the ball', field=False)
			return [self.set, [team_id, p, receive_precision*0.5]]
		else:
			possibles = [num for num in range(0, 6) if num != p]
			# bias in favour of front setters
			for i in range(15):
				possibles += [num for num in range(4, 6) if num != p]

			other_p = random.choice(possibles)
			other_player = self.teams[team_id].rotation[other_p]

			self.ball = [team_id, other_p, 'pass']
			self.event(f'{player} passes the ball to {other_player}')
			info()
			return [self.set, [team_id, other_p, receive_precision]]

	def set(self, team_id, p, pass_precision):
		self.touches += 1
		player = self.teams[team_id].rotation[p]
		team = self.teams[team_id]

		possibles = [num for num in range(0, 6) if num != p]
		# bias in favour of front spikers
		for i in range(20):
			possibles += [num for num in range(3, 6) if num != p]

		other_p = random.choice(possibles)
		other_player = self.teams[team_id].rotation[other_p]
		self.ball = [team_id, other_p, 'set']

		set_speed = player.stats['overhand_strength']
		set_precision = player.stats['overhand_precision']

		if pass_precision + player.stats['agility'] < 0.2 or (pass_precision + player.stats['agility'] < 0.5 and self.touches > 2):
			self.event(f'{player} fails to touch the passed ball')
			return [self.point, [flip(team_id)]]
		elif self.touches > 2 or deviate(pass_precision) > 2.5:
			self.touches -= 1
			self.event(f'{player} jumps for setter drop', field=False)
			return [self.spike, [team_id, p, max(0.5, pass_precision), 2]]
		elif pass_precision + player.stats['agility'] < 0.5:
			other_p = wrap(p + random.choice([-1, 1]), 0, 5)
			other_player = self.teams[team_id].rotation[other_p]
			self.ball = [team_id, other_p, 'receive']
			self.event(f'{player} fails to touch the ball and the ball goes to {other_player}')
			return [self.receive, [team_id, other_p, deviate(2), deviate(0.2), 1-deviate(pass_precision)]]
		if deviate(pass_precision) + player.stats['jump'] > 2:
			self.event(f'{player} manages to jump set to {other_player}')
			set_speed = player.stats['overhand_strength'] * 1.2 + player.stats['jump'] * 0.5 + player.stats['height'] * 0.2
			set_precision = pass_precision * 0.6 + player.stats['overhand_precision'] + player.stats['intelligence'] * 0.3
		else:
			self.event(f'{player} sets the ball for {other_player}')
			set_speed = player.stats['overhand_strength'] * 1.5
			set_precision = pass_precision * 0.4 + player.stats['overhand_precision'] * 1.2 + player.stats['intelligence'] * 0.3

		speed_cat = random.randint(1, 3)
		set_speed = set_speed * speed_cat
		set_precision = set_precision / max(1, speed_cat - player.stats['overhand_precision']*2)

		if self.debug:
			self.event('set' + str((set_speed, set_precision)), field=False)
		else:
			endstring = '[Set]\n'
			endstring += bar('Precision', 1.7, set_precision) + '\n'
			endstring += bar('Speed', 1.7, set_speed)
			self.event(endstring, field=False, stat=True)

		return [self.spike, [team_id, other_p, set_precision, set_speed]]

	def spike(self, team_id, p, set_precision, set_speed):
		self.touches += 1
		player = self.teams[team_id].rotation[p]
		team = self.teams[team_id]

		spike_precision = set_precision
		spike_strength = set_speed
		spike_speed = set_speed
		spike_height = player.stats['height']

		if set_precision*3 - set_speed + deviate(player.stats['reflexes']*8) < 2.5:
			self.event(f'{player} fails to hit the ball for a spike', field=False)
			return [self.point, [flip(team_id)]]
		elif set_precision*3 - set_speed + player.stats['reflexes']*2 < 2.5:
			other_p = mirror(p)
			other_player = self.teams[flip(team_id)].rotation[other_p]

			self.touches = 0
			self.ball = [flip(team_id), other_p, 'receive']
			self.event(f'{player} misses the spike, barely hitting the ball to the other side to {other_player}')
			return [self.receive, [flip(team_id), other_p, player.stats['reflexes']*0.5, player.stats['spike_strength']*0.1, set_speed-0.5]]
		else:
			spike_precision = set_precision * 0.7 + player.stats['spike_precision'] * 1.5 + player.stats['agility']*0.2
			spike_strength = set_precision * 0.5 + player.stats['spike_strength'] * 2
			spike_speed = set_speed + player.stats['reflexes']*0.2
			spike_height = player.stats['height'] + player.stats['jump']*1.5 + player.stats['agility']*0.2
			spike_intelligence = player.stats['intelligence']*0.8 + player.stats['spike_precision']*0.2

		spike_precision = deviate(spike_precision)
		spike_strength = deviate(spike_strength)
		spike_speed = deviate(spike_speed)
		spike_height = deviate(spike_height)
		spike_intelligence = deviate(spike_intelligence)

		if p in [0, 1, 2]:
			# backrow spike
			if spike_height + spike_precision*0.3 < 0.8:
				self.event(f'{player} hits the ball into the net', field=False)
				return [self.point, [flip(team_id)]]
			else:
				other_p = random.randint(0, 2)
				other_player = self.teams[flip(team_id)].rotation[other_p]
		else:
			# frontrow spike
			if spike_height + spike_precision*0.1 < 0.5:
				self.event(f'{player} hits the ball into the net', field=False)
				return [self.point, [flip(team_id)]]
			else:
				spike_speed = spike_speed - 1
				other_p = random.randint(0, 5)
				other_player = self.teams[flip(team_id)].rotation[other_p]

		self.touches = 0
		self.event(f'{player} spikes the ball', field=False)
		self.ball = [team_id, p, 'spike']

		if self.debug:
			self.event(f'spike' + str((spike_precision, spike_strength, spike_speed, spike_height, spike_intelligence)), field=False)
		else:
			endstring = '[Spike]\n'
			endstring += bar('Precision', 3, spike_precision) + '\n'
			endstring += bar('Strength', 3, spike_strength) + '\n'
			endstring += bar('Speed', 3, spike_speed+1) + '\n'
			endstring += bar('Height', 3, spike_height) + '\n'
			endstring += bar('Intelligence', 1, spike_intelligence)
			self.event(endstring, field=False, stat=True)

		return [self.block_prepare, [flip(team_id), other_p, mirror(front(p)), spike_precision, spike_strength, spike_speed, spike_intelligence, spike_height]]


	def block_prepare(self, team_id, target, pos, ball_precision, ball_strength, ball_speed, ball_intelligence, ball_height):
		target_player = self.teams[team_id].rotation[target]

		def b_speed(player):
			return max(player.stats['reflexes']*0.5 + player.stats['height'] + player.stats['jump'] * 0.3, player.stats['intelligence'] - ball_intelligence*0.5 + player.stats['height'] + player.stats['jump'] * 0.3)

		block_pos = 'side' if pos in [3, 5] else 'mid'

		blockers_pos = [3, 4, 5]
		blockers = [self.teams[team_id].rotation[p] for p in blockers_pos]

		def get_stats(b_player, p_pos, b_pos):
			stats = {}
			stats['block_precision'] = b_player.stats['block_precision']*0.7 + b_player.stats['reflexes']*0.3
			stats['block_constitution'] = b_player.stats['constitution']*0.9 + b_player.stats['reflexes']*0.1
			stats['block_speed'] = b_speed(b_player) - 0.5 * abs(p_pos - b_pos)
			stats['block_height'] = b_player.stats['height'] + b_player.stats['jump']*0.5
			return stats

		blocker_stats = [get_stats(p, blockers_pos[i], pos) for i, p in enumerate(blockers)]

		active_blockers = [[True, p, blocker_stats[i]] if blocker_stats[i]['block_speed'] > ball_speed else [False, p, blocker_stats[i]] for i, p in enumerate(blockers)]
		active_blockers_listed = [p for i, p in enumerate(blockers) if active_blockers[i][0]]

		if target in blockers_pos:
			target = back(target)

		if active_blockers[0] is False and random.randint(0, 1) == 1:
			active_blockers[0], active_blockers[1], active_blockers[2] = active_blockers[1], active_blockers[2], active_blockers[0]
		elif active_blockers[2] is False and random.randint(0, 1) == 1:
			active_blockers[0], active_blockers[1], active_blockers[2] = active_blockers[2], active_blockers[0], active_blockers[1]

		self.ball = [flip(team_id), mirror(pos), 'block', active_blockers]

		s = ''
		if len(active_blockers_listed) == 0:
			s = 'No blocker is able to react to block the ball'
		elif len(active_blockers_listed) == 1:
			player_str = str(active_blockers_listed[0])
			s = '{0} jumps to block the ball'.format(player_str)
		elif len(active_blockers_listed) == 2:
			player_str = str(active_blockers_listed[0]) + ' and ' + str(active_blockers_listed[1])
			s = '{0} jump to block the ball'.format(player_str)
		elif len(active_blockers_listed) == 3:
			player_str = str(active_blockers_listed[0]) + ', ' + str(active_blockers_listed[1]) + ' and ' + str(active_blockers_listed[2])
			s = '{0} jump to block the ball'.format(player_str)
		else:
			print('something has gone horribly wrong')

		self.event(s, field=True)

		return [self.block, [team_id, target, pos, active_blockers, ball_precision, ball_strength, ball_speed, ball_intelligence, ball_height]]


	def block(self, team_id, target, pos, active_blockers, ball_precision, ball_strength, ball_speed, ball_intelligence, ball_height):
		block_pos = 'side' if pos in [3, 5] else 'mid'
		active_blockers_value = [p[0] for p in active_blockers]
		active_blockers_player = [p[1] for p in active_blockers]
		active_blockers_pos = list(range(3, 5))
		active_blockers_stats = [p[2] for p in active_blockers]

		profit = [(abs(pos - p), p) if active_blockers_value[i] else (abs(pos - p) + 3, p) for i, p in enumerate(active_blockers_pos)]
		best = max(profit, key=lambda x: x[0])
		best_pos = profit[profit.index(best)][1]

		if ball_intelligence > 0.6 and ball_precision > 1.6:
			attack = best_pos - 3
		elif ball_precision > 1.3:
			attack = random.randint(0, 2)
		else:
			attack = pos - 3

		blocker_pos = attack + 3
		blocker_id = attack

		p = blocker_id
		blockers = active_blockers_stats
		blocker = blockers[p]

		blocker_player = self.teams[team_id].rotation[blocker_pos]

		if self.debug:
			# nobody uses this
			pass
			#self.event(f'spike' + str((spike_precision, spike_strength, spike_speed, spike_height, spike_intelligence)), field=False)
		else:
			endstring = ''
			p = attack
			endstring += f'[Block]\n'
			endstring += bar('Precision', 1, blockers[p]['block_precision']) + '\n'
			endstring += bar('Constitution', 0.8, blockers[p]['block_constitution']) + '\n'
			endstring += bar('Speed', 1.6, blockers[p]['block_speed']) + '\n'
			endstring += bar('Height', 1, blockers[p]['block_height']) + '\n'
			endstring = endstring[:-1]
			self.event(endstring, field=False, stat=True)


		if active_blockers_value[p] is False:
			if True in active_blockers_value:
				active_b = active_blockers_player[active_blockers_value.index(True)]
				if pos == 4:
					target = back(pos)
					target_player = self.teams[team_id].rotation[target]
					self.ball = [team_id, target, 'receive']
					self.event(f'The ball flies by {active_b} towards {target_player}')
					return [self.receive, [team_id, mirror(back(pos)), ball_precision, ball_strength, ball_speed]]
				elif pos == p:
					target = back(pos)
					target_player = self.teams[team_id].rotation[target]
					self.ball = [team_id, target, 'receive']
					self.event(f'The ball flies by {active_b} in a straight spike towards {target_player}')
					return [self.receive, [team_id, back(pos), ball_precision, ball_strength, ball_speed]]
				else:
					target = mirror(back(pos))
					target_player = self.teams[team_id].rotation[target]
					self.ball = [team_id, target, 'receive']
					self.event(f'The ball flies by {active_b} in a cross-court spike towards {target_player}')
					return [self.receive, [team_id, mirror(back(pos)), ball_precision, ball_strength, ball_speed]]
			else:
				target = back(random.randint(0, 5))
				target_player = self.teams[team_id].rotation[target]
				self.ball = [team_id, target, 'receive']
				self.event(f'The ball is spiked towards {target_player}')

			return [self.receive, [team_id, target, ball_precision, ball_strength, ball_speed]]

		elif blocker['block_height'] < ball_height * 0.2:
			self.ball = [team_id, target, 'receive']
			self.event(f'The spike is too high for {blocker_player} and flies directly over the block', field=False)
			return [self.receive, [team_id, target, ball_precision, ball_strength, ball_speed]]
		elif blocker['block_constitution'] < ball_strength * 0.1:
			self.ball = [team_id, back(pos), 'receive']
			self.event(f'The spike breaks through the block of {blocker_player}', field=False)
			return [self.receive, [team_id, back(pos), ball_precision+1, ball_strength - blocker['block_constitution']*2, ball_speed+1]]
		elif blocker['block_height'] < ball_height*0.2 and ball_intelligence < 0.6:
			target = back(pos)
			target_player = self.teams[team_id].rotation[target]
			self.ball = [team_id, target, 'receive']
			self.event(f'The spike ricochets off of the hands of {blocker_player} to {target_player}')
			return [self.receive, [team_id, target, ball_precision-0.5, ball_strength/3, ball_speed-0.5]]
		elif blocker['block_height'] < ball_height*0.4:
			self.event(f'The ball ricochets off of the hands of {blocker_player} into the out')
			return [self.point, [flip(team_id)]]
		else:
			self.ball = [flip(team_id), back(mirror(pos)), 'receive']
			self.event(f'{blocker_player} blocks the ball and it falls back to the other side')
			if ball_strength > 0.8:
				new = back(mirror(pos))
			else:
				new = front(mirror(pos))
			return [self.receive, [flip(team_id), new, ball_precision+1, ball_strength-0.4, ball_speed+1]]