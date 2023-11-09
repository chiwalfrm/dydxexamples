import websockets
import asyncio
import json
import sys

node_url = sys.argv[1]

async def test():
  async with websockets.connect(f'{node_url}/websocket') as websocket:
    #response = await websocket.recv()
    #print(response)
    await websocket.send('{ "jsonrpc": "2.0", "method": "subscribe", "params": ["tm.event=\'NewBlock\'"], "id": 1 }')
    while True:
      response = await websocket.recv()
      responseJson = json.loads(response)
      if 'data' in responseJson['result'] and 'value' in responseJson['result']['data']:
        print(f"{responseJson['result']['data']['value']['block']['header']['height']} {responseJson['result']['data']['value']['block']['header']['time']}")

asyncio.get_event_loop().run_until_complete(test())
