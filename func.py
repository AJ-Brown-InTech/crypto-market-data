import json, hmac, hashlib, time, base64
import asyncio
import time
import websockets
import sys
uri = "wss://ws-feed.prime.coinbase.com"
PASSPHRASE = "YOUR PASSWORD"
ACCESS_KEY = "YOUR ACCESS KEY"
SIGNING_KEY = "YOUR SIGNING KEY"
SVC_ACCOUNTID = "YOUR SERVICE ACCOUNT ID"
s = time.gmtime(time.time())
TIMESTAMP = time.strftime("%Y-%m-%dT%H:%M:%SZ", s)
async def sign(channel, key, secret, account_id, portfolio_id, product_ids):
    message = channel + key + account_id + TIMESTAMP + portfolio_id + product_ids
    print(message)
    signature = hmac.new(secret.encode('utf-8'), message.encode('utf-8'), digestmod=hashlib.sha256).digest()
    signature_b64 = base64.b64encode(signature).decode()
    print(signature_b64)
    return signature_b64
async def main_loop():
    async with websockets.connect(uri, ping_interval=None, max_size=None) as websocket:
        signature = await sign('l2_data', ACCESS_KEY, SIGNING_KEY, SVC_ACCOUNTID, "", "BTC-USD")
        print(signature)
        auth_message = json.dumps({
            "type": "subscribe",
            "channel": "l2_data",
            "access_key": ACCESS_KEY,
            "api_key_id": SVC_ACCOUNTID,
            "timestamp": TIMESTAMP,
            "passphrase": PASSPHRASE,
            "signature": signature,
            "portfolio_id": "",
            "product_ids": ["BTC-USD"]
        })
        
        await websocket.send(auth_message)
        try:
            processor = None
            while True:
                response = await websocket.recv()
                parsed = json.loads(response)
                print(parsed)
        except websockets.exceptions.ConnectionClosedError:
            print("Error caught")
            sys.exit(1)
if __name__ == '__main__':
    asyncio.run(main_loop())