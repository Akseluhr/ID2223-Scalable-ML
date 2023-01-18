import hopsworks
from pandas_datareader import data as pdr
import yfinance as yf
import pandas as pd

project = hopsworks.login()
fs = project.get_feature_store()

yf.pdr_override()
btc_df = pdr.get_data_yahoo('BTC-USD', start='2016-01-01')

btc_df.drop(columns=['Adj Close'], inplace=True)

btc_df['Dayofyear'] = btc_df.index.dayofyear
btc_df['Month'] = btc_df.index.month
btc_df['Year'] = btc_df.index.year
btc_df['Date'] = btc_df.index.strftime('%Y-%m-%d %H:%M:%S')
btc_df['Date'] = pd.to_datetime(btc_df['Date'])

btc_fg = fs.get_or_create_feature_group(
    name="btc_modal_2",
    version=1,
    primary_key=["Date"], #all but target
    description="yahoo btc dataset",
    event_time="Date")
btc_fg.insert(btc_df, write_options={"wait_for_job": False})