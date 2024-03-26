import json
import sys
from websocket import create_connection

market = sys.argv[1]
api_data = {
    "type": "subscribe",
    "channel": "v4_orderbook",
    "id": market,
}
ws = create_connection('wss://indexer.v4testnet.dydx.exchange/v4/ws')
ws.send(json.dumps(api_data))
while True:
        try:
                api_data = ws.recv()
                api_data = json.loads(api_data)
                print(api_data)
        except KeyboardInterrupt:
                ws.close()
                sys.exit(0)
        except Exception as error:
                print(error)
                ws.close()
                sys.exit(0)
