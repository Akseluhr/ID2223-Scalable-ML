import pandas as pd
import requests
from datetime import datetime
from time import sleep, time
from concurrent.futures import ThreadPoolExecutor
import random
import hopsworks
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

project = hopsworks.login()
fs = project.get_feature_store()


# endpoint to get bitcoin price
binanceAPI = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
FREQUNCY = 1
dt = datetime.now()
ts = datetime.timestamp(dt)

data_dict = {"btc_price": 0,"event_time": ts}
blockchainAPI = "https://blockchain.info/q/hashrate"

btc_price = []
timestamp = []
df_initial = pd.DataFrame(columns=['btc_price', 'timestamp'])


def get_btc_price():
    while True:
        r = requests.get(binanceAPI)
        btc_price.append(float(r.json()['price']))
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        timestamp.append(ts)
       # df = pd.DataFrame(data_dict)
       # print(btc_price)
       # print(timestamp)
       # if (len(btc_price) >= 10):
       #     sleep(10) # Upload every 10 seconds 
       #     upload_to_hopsworks(btc_price, timestamp, True)
       # else:
       #     upload_to_hopsworks(btc_price, timestamp, False)
       # print(timestamp)
       # print(btc_price)

        sleep(1/FREQUNCY)

def upload_to_hopsworks(first=True):
    while True:
          
        btc_df = df_initial.append(pd.DataFrame(list(zip(btc_price, timestamp)), columns=['btc_price', 'timestamp']))

        # keeps the 50 most recent records
      #  if len(btc_df) > 20:
      #  btc_df = btc_df.drop(btc_df.index[0:len(btc_df)-20]).reset_index(drop=True)
    
        
        if len(btc_df) > 5:        
            btc_fg = fs.get_or_create_feature_group( # 
                   name="btc_modal",
                   version=1)
            btc_fg.insert(btc_df, storage="online", write_options={"wait_for_job": False})
        
        print(btc_df)
        
        # Every 60 seconds we upload our new DF to hopsworks
        sleep(5/FREQUNCY)
'''
def get_hash_rate():
	while True:
		r = requests.get(blockchainAPI)
		#rand_int = random.randint(-1000, 1000)		
		data_dict['hash_rate'] = float(r.json())
		sleep(10/FREQUNCY)
'''

if __name__ == "__main__":
    # Delete the most recent FG (outdated data)
    '''
    try:
        previous_btc_fg = fs.get_feature_group('btc_modal', version=1)
        previous_btc_fg.delete()
    except:
    '''

    executor = ThreadPoolExecutor(2)
    for func in [get_btc_price, upload_to_hopsworks]:
        executor.submit(func)
        
    executor.shutdown(wait=True)
