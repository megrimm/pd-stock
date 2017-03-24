from modules.GDAX import GDAX
import pyext

class ws(pyext._class):

	# number of inlets and outlets
	_inlets=1
	_outlets=1
    
        def open_1(self):
            # Paramters are optional
            wsClient = GDAX.WebsocketClient(ws_url="wss://ws-feed.gdax.com", product_id=["BTC-USD", "ETH-USD"])

        def close_1(self):
            # Do other stuff...
            wsClient.close()