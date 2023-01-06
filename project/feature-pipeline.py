import pandas as pd
import requests
import datetime
from time import sleep, time
from concurrent.futures import ThreadPoolExecutor
import random




# endpoint to get bitcoin price
binanceAPI = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
FREQUNCY = 1
data_dict = {"btc_price": 0,"event_time": datetime.datetime.now()}
blockchainAPI = "https://blockchain.info/q/hashrate"


def get_btc_price():
    while True:
        r = requests.get(binanceAPI)
        data_dict['btc_price'] = float(r.json()['price'])
        data_dict['event_time'] = datetime.datetime.now()
        print(data_dict)
        sleep(1/FREQUNCY)

'''
def get_hash_rate():
	while True:
		r = requests.get(blockchainAPI)
		#rand_int = random.randint(-1000, 1000)		
		data_dict['hash_rate'] = float(r.json())
		sleep(10/FREQUNCY)
'''

if __name__ == "__main__":
	executor = ThreadPoolExecutor(3)
	for func in [get_btc_price]:
		executor.submit(func)

	executor.shutdown(wait=True)
