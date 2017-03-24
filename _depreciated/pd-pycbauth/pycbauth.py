# Requires python-requests and the puredata external pyext

import json, hmac, hashlib, time, requests, base64, pyext, dateutil.parser
from requests.auth import AuthBase
from datetime import date, timedelta, datetime

# SANDBOX
#API_KEY = "key"
#API_SECRET = 'secret'
#API_PASS = 'pass'
#API_URLS = 'https://api-public.sandbox.exchange.coinbase.com/'

# GDAX
API_KEY = "key"
API_SECRET = 'secret'
API_PASS = 'pass'
API_URLS = 'https://api.gdax.com/'

# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = signature.digest().encode('base64').rstrip('\n')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

api_url = API_URLS
auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)

# Generates a hmac-sha256 hash
class cbauth(pyext._class):

    # number of inlets and outlets
    _inlets=1
    _outlets=1
    
    # Get Ticker
    def ticker_1(self):
        ticker = requests.get(api_url + 'products/BTC-USD/ticker', auth=auth).json()
        decode = json.dumps(ticker,indent=4)
        self._outlet(1,decode)

    #Get Stats
    def stats_1(self,args):
        stats = requests.get(api_url + 'products/BTC-USD/stats', auth=auth).json()
        #if str(args) == 'volume_30day':
        #    value = float(ticker["volume_30day"])
        #if str(args) == 'volume':
        #    value = float(ticker["volume"])
        decode = json.dumps(stats,indent=4)
        self._outlet(1,decode)

    #Get Time
    def time_1(self,args):
        time = requests.get(api_url + 'time', auth=auth).json()
        #if str(args) == 'iso':
        #    value = str(ticker["iso"])
        #if str(args) == 'epoch':
        #    value = float(ticker["epoch"])
        decode = json.dumps(time,indent=4)
        self._outlet(1,decode)

    # Get Accounts
    def accounts_1(self):
        accounts = requests.get(api_url + 'accounts/073247a4-0fab-42f9-89a2-c47ee0bcbdc4', auth=auth).json() # Need to change account ID to variable
        decode = json.dumps(accounts,indent=4)
        self._outlet(1,decode)

    # Get Candles
    def candles_1(self, start, end, granu):
        candles = {'start' : str(start), 'end' : str(end), 'granularity' : str(granu)}
        candles = requests.get(api_url + 'products/BTC-USD/candles', json=candles, auth=auth).json()
        decode = json.dumps(candles,indent=4)
        self._outlet(1,decode)

    '''
    def candles_1(self):
        time = requests.get(api_url + '/time').text
        time = json.loads(time)['iso']
        yesterday = date.today() - timedelta(days=1)
        yesterday = dateutil.parser.parse(str(yesterday))
        args = {'start' : yesterday.isoformat(), 'end' : time, 'granularity' : 60}
        r = requests.get(api_url + 'products/BTC-USD/candles', json=args, auth=auth).text
        #decode = json.dumps(r)
        self._outlet(1,str(r))
    '''


    # Create an Limit Order
    def limit_1(self, side, size, price, prod, post):
        limit = {'type': 'limit', 'side': str(side), 'size': str("%.3f" % size), 'price': str("%.3f" % price), 'product_id': str(prod), 'post_only': str(post)}
        limit = requests.post(api_url + 'orders', json=limit, auth=auth).json()
        decode = json.dumps(limit,indent=4)
        self._outlet(1,decode)

    # Create an Market Order
    def market_1(self, side, size, prod):
        market = {'type': 'market', 'side': str(side), 'size': str("%.3f" % size), 'product_id': str(prod)}
        market = requests.post(api_url + 'orders', json=market, auth=auth).json()
        decode = json.dumps(market,indent=4)
        self._outlet(1,decode)

    # Create an Stop Order
    def stop_1(self, side, size, prod):
        stop = {'type': 'market', 'side': str(side), 'size': str("%.3f" % size), 'product_id': str(prod)}
        stop = requests.post(api_url + 'orders', json=stop, auth=auth).json()
        decode = json.dumps(stop,indent=4)
        self._outlet(1,decode)

    # Get Open Orders
    def orders_1(self):
        orders = requests.get(api_url + 'orders', auth=auth).json() # Need to change account ID to variable
        decode = json.dumps(orders,indent=4)
        self._outlet(1,decode)

    def delorder_1(self,cancel):
        if str(cancel) == 'all':
            delorder = requests.delete(api_url + 'orders', auth=auth).json()
            decode = json.dumps(delorder,indent=4)
        else:
            #delorder = {str(cancel)}
            delorder = requests.delete(api_url + 'orders/' + str(cancel), auth=auth).json()
            decode = json.dumps(delorder,indent=4)
            print 'need variable here somewhere to reflect id'
        self._outlet(1,decode)
