import hopsworks
import datetime as dt
from pandas_datareader import data as pdr
import yfinance as yf


project = hopsworks.login()
fs = project.get_feature_store()

crypto_currency = 'BTC'
against_currency = 'USD'

start_date = dt.datetime(2020,1,1)
end_date = dt.datetime.now()

yf.pdr_override()
btc_df = pdr.get_data_yahoo('BTC', start='2016-1-1')

# data.head(5)
# data.describe()
# print(data.dtypes)

btc_df.reset_index(inplace=True)
# data.head(5)

# print(data['Close'].corr(data['Volume']))
btc_df.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'])
# data.head(5)

titanic_fg = fs.get_or_create_feature_group(
    name="btc_modal",
    version=1,
    primary_key=["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"],
    description="yahoo btc dataset")
titanic_fg.insert(btc_df, write_options={"wait_for_job": False})
