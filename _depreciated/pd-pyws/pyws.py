#!/usr/bin/env python3
from websocket import create_connection
from time import sleep
import json, pyext

class ws(pyext._class):

	# number of inlets and outlets
	_inlets=1
	_outlets=1

	sltime=0.2 # sleep time

	def open_1(self,feed):
		ws = create_connection(str(feed))
		sub = json.dumps({"type": "subscribe", "product_id": "BTC-USD"})

		ws.send(sub)
		while True:
			result = json.dumps(ws.recv())
			self._outlet(1,result)
			sleep(self.sltime)

	def close_1(self):
		ws.close()