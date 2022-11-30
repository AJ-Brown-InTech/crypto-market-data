#view market data in realtime
import asyncio
import websocket
import os
from dotenv import load_dotenv
import time
import math
import hmac
import hashlib  
import base64
import json 
websocket

#load .env file and GLOBAL vars
load_dotenv()
URL = os.getenv('BASE_URL')
KEY = os.getenv('KEY')
PORT = os.getenv('PORT')
PHRASE = os.getenv('PHRASE')
SECRET = os.getenv('SECRET')
TIMESTAMP =  math.ceil(time.time()/1000)
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
#this thing is the final signature used for all socket request but also REST api calls
final_sub = json.dumps(subscription)

#wss func to retrieve coin tickers(prices)/ connect to server
# async def wss_func():
#    wss_connector = await websockets.connect(URL)
#    await wss_connector.send(final_sub)
#    response = await websockets.recv()
#    print(response)
# asyncio.get_event_loop().run_until_complete(wss_func())

ws = create_connection(URL)
print (ws)
ws.send(final_sub)
print("Sent")
print("Receiving...")
result =  ws.recv()
print("Received '%s'" % result)
