import asyncio
import websockets
import time
import json

from basegame import basegame

ws = []

DELAY = 3

with open('data/teams/Berlin.json', encoding='utf-8') as f:
    team1 = basegame.Team.load_team(json.load(f))

with open('data/teams/Netherlands.json', encoding='utf-8') as f:
    team2 = basegame.Team.load_team(json.load(f))

m = basegame.Match([team1, team2], 2)
m.debug = False
m.print = False

events = m.next()
last_update = time.time()

async def match(websocket, path):
    global ws

    global events
    global last_update
    global m

    ws.append(websocket)
    print('concurrent connections', len(ws))

    for timestep in range(10**6):
        await asyncio.sleep(DELAY)

        if time.time() - last_update > DELAY:
            last_update = time.time()
            events = m.next()

            if m.n is None:
                events = {'event': 'over'}
                return
            elif m.n[0] is None:
                events = {'event': 'over'}
                return

            for i, w in enumerate(ws):
                events['event'] = 'match'
                for key, value in events.items():
                    if type(value) is str:
                        events[key] = value.replace('\n', '<br>')

                msg = json.dumps(events)
                try:
                    await w.send(msg)
                except:
                    ws.remove(w)

start_server = websockets.serve(match, "0.0.0.0", 36960)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()