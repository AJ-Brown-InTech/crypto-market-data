#view market data in realtime
import asyncio
import websockets
import os
from dotenv import load_dotenv
import time
import hmac
import hashlib  
import base64
import json 
import sys

#load .env file and GLOBAL vars
load_dotenv()
URL = os.getenv('BASE_URL')
URI = os.getenv('URI')
KEY = os.getenv('KEY')
PORT = os.getenv('PORT')
PHRASE = os.getenv('PHRASE')
SECRET = os.getenv('SECRET')
s = time.gmtime(time.time())
TIMESTAMP = time.strftime("%Y-%m-%dT%H:%M:%SZ", s)
CURRENCY_LIST = ["BTC-USD", "ETH-USD", "USDT-USD", "ADA-USD"]
'''
=======REST  API HEADER========
# request.headers.update({
#     'CB-ACCESS-SIGN': signature_b64,
#     'CB-ACCESS-TIMESTAMP': timestamp,
#     'CB-ACCESS-KEY': self.api_key,
#     'CB-ACCESS-PASSPHRASE': self.api_pass,
#     'Content-Type': 'application/json'
# })
=======WEBSOCKET AUTH SUBSCRIPTION ========
{
    "type": "subscribe",
    "product_ids": [
        "BTC-USD"
    ],
    "channels": [
        "full"
    ],
    "signature": "...",
    "key": "...",
    "passphrase": "...",
    "timestamp": "..."
}
'''
#signature hash
#signature = hmac.new(bytes(SECRET , 'utf-8'), msg = bytes(SECRET , 'utf-8'), digestmod = hashlib.sha256).hexdigest().upper()
message = str(TIMESTAMP) + 'GET' + URL + 'accounts' + ''
sign = bytes(message, 'UTF-8')
hmac_key = base64.b64decode(SECRET)
signature = hmac.new(hmac_key, sign, hashlib.sha256)
socket_signature = base64.b64encode(signature.digest()).decode('utf-8')

subscription= {
    "type": "subscribe",
    "product_ids": CURRENCY_LIST,
    "channels": [
        "full"
    ],
    "signature": f"{socket_signature}",
    "key": f"{KEY}",
    "passphrase": f"{PHRASE}",
    "timestamp": f"{TIMESTAMP}"
}

final_sub = json.dumps(subscription)

async def wss_connector():        
    async with websockets.connect(URI, ping_interval=None, max_size=None) as ws:
        await ws.send(final_sub)
        try:
            processor = None
            while True:
                response = await ws.recv()
                parsed = json.loads(response)
                print(parsed)
        except websockets.exceptions.ConnectionClosedError:
            print("Error caught")
            sys.exit(1)
if __name__ == '__main__':
    asyncio.run(wss_connector())      

