import hopsworks
from pandas_datareader import data as pdr
import yfinance as yf


project = hopsworks.login()
fs = project.get_feature_store()

yf.pdr_override()
btc_df = pdr.get_data_yahoo('BTC-USD', start='2016-01-01')

btc_df.drop(columns=['Adj Close'], inplace=True)


titanic_fg = fs.get_or_create_feature_group(
    name="btc_modal_2",
    version=1,
    primary_key=["Open", "High", "Low", "Close", "Volume"],
    description="yahoo btc dataset")
titanic_fg.insert(btc_df, write_options={"wait_for_job": False})