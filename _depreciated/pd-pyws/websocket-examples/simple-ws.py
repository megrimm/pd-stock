#!/usr/bin/env python3

from websocket import create_connection

import json

ws = create_connection('wss://ws-feed.exchange.coinbase.com')
sub = json.dumps({"type": "subscribe", "product_id": "BTC-USD"})
ws.send(sub)

while True:
	result = json.loads(ws.recv())
	print(result)

ws.close()