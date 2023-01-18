import datetime

import modal

LOCAL = False


def feature_daily():
    import hopsworks
    from pandas_datareader import data as pdr
    import yfinance as yf

    # add the new data here.
    today_date = datetime.datetime.today()

    yf.pdr_override()
    btc_df = pdr.get_data_yahoo('BTC-USD', start=today_date)
    btc_df.drop(columns=['Adj Close'], inplace=True)

    btc_df['Dayofyear'] = btc_df.index.dayofyear
    btc_df['Month'] = btc_df.index.month
    btc_df['Year'] = btc_df.index.year
    btc_df['Date'] = btc_df.index.strftime('%Y-%m-%d %H:%M:%S')

    project = hopsworks.login()
    fs = project.get_feature_store()

    fg = fs.get_feature_group(name="btc_modal_2", version=1)
    fg.insert(btc_df, write_options={"wait_for_job": False})


if not LOCAL:
    stub = modal.Stub()
    image = modal.Image.debian_slim().pip_install(
        ["hopsworks==3.0.4", "joblib", "seaborn", "scikit-learn", "xgboost", "dataframe-image", "datetime",
         "yfinance", "pandas_datareader"])

    @stub.function(image=image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("HOPSWORKS_API_KEY"))
    # @stub.function(image=image, secret=modal.Secret.from_name("HOPSWORKS_API_KEY"))
    def modal_btc_feature_daily():
        feature_daily()

if __name__ == "__main__":
    if LOCAL:
        feature_daily()
    else:
        stub.deploy("btc_modal_2_feature_daily")
