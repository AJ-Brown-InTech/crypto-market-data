#view market data in realtime
import asyncio
import websockets
import os
from dotenv import load_dotenv

#load .env file and utilize vars
load_dotenv()
URL = os.getenv('BASE_URL')
KEY = os.getenv('KEY')
PORT = os.getenv('PORT')
PHRASE = os.getenv('PHRASE')

#wss func to retrieve coin tickers(prices)
async def wss_func():
   wss_connector = await websockets.connect(URL)
   print(wss_connector.recv())
   
asyncio.get_event_loop().run_until_complete(wss_func())
    
    
 
   
