import modal

LOCAL = True


def batch_btc():
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    from datetime import datetime
    from sklearn.metrics import mean_absolute_error
    import dataframe_image as dfi
    import hopsworks
    import joblib
    import os
    from pandas_datareader import data as pdr
    import yfinance as yf

    project = hopsworks.login()
    fs = project.get_feature_store()

    feature_group = fs.get_feature_group(name="btc_modal_2", version=1)

    # get model and make prediction for latest instance
    mr = project.get_model_registry()
    model = mr.get_model("btc_model", version=1)
    model_dir = model.download()
    model = joblib.load(model_dir + "/btc_model.pkl")

    offset = 5
    X_pred = feature_group.read().tail(offset)
    print("5 days instance: \n{}".format(X_pred))

    # predict and get latest (daily) feature
    y_pred = model.predict(X_pred.drop(columns=['close', 'date']))
    print("Prediction: {}".format(y_pred[0]))

    prediction_date = X_pred.iloc[0]['date']
    prediction_date = prediction_date.date()
    print("Prediction date: {}".format(prediction_date))

if not LOCAL:
    stub = modal.Stub()
    image = modal.Image.debian_slim().pip_install(
        ["hopsworks==3.0.4", "joblib", "seaborn", "scikit-learn", "xgboost", "dataframe-image", "datetime",
         "yfinance", "pandas_datareader", "numpy", "pandas", "matplotlib"])


    @stub.function(image=image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("HOPSWORKS_API_KEY"))
    # @stub.function(image=image, secret=modal.Secret.from_name("HOPSWORKS_API_KEY"))
    def modal_batch_btc():
        batch_btc()

if __name__ == "__main__":
    if LOCAL:
        batch_btc()
    else:
        stub.deploy("btc_modal_2_batch")
