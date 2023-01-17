import modal

LOCAL = False

def feature_daily():
    import hopsworks
    import datetime as dt
    from pandas_datareader import data as pdr
    import yfinance as yf

    # add the new data here.

if not LOCAL:
    stub = modal.Stub()
    image = modal.Image.debian_slim().apt_install(["libgomp1"]).pip_install([
        "hopsworks==3.0.4", "seaborn", "joblib", "scikit-learn==1.0.2", "xgboost==1.5", "dataframe-image", "pandas",
        "datetime", "requests", "python-dotenv", "yfinance", "pandas_datareader"])


    @stub.function(image=image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("HOPSWORKS_API_KEY"))
    # @stub.function(image=image, secret=modal.Secret.from_name("HOPSWORKS_API_KEY"))
    def modal_btc_feature_daily():
        feature_daily()


if __name__ == "__main__":
    if LOCAL:
        feature_daily()
    else:
        stub.deploy("btc_modal_feature_daily")