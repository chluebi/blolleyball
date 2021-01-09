import asyncio
import websockets
import time
import json

from util.config_handling import load_config

config = load_config()

last_update = time.time()

ws = []
DELAY = config['site']['match_tick']

def get_next():
    with open('data/current.json') as f:
        data = json.load(f)
    return data

def replace_linebreaks(data):
    for key, value in data.items():
        if type(value) is dict:
            data[key] = replace_linebreaks(data[key])
        elif type(value) is list:
            data[key] = [e.replace('\n', '<br>') if type(str) is e else e for e in data[key]]
        elif type(value) is str:
            data[key] = data[key].replace('\n', '<br>')
        else:
            data[key] = data[key]
    return data

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
            events = get_next()
            msg = json.dumps(replace_linebreaks(events))

            for i, w in enumerate(ws):
                try:
                    await w.send(msg)
                except:
                    ws.remove(w)

start_server = websockets.serve(match, 'localhost', config['site']['websocket_port'])

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()