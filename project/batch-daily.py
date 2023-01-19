import modal

LOCAL = False


def batch_btc():
    import matplotlib.pyplot as plt
    import pandas as pd
    import datetime
    from sklearn.metrics import mean_absolute_error
    import hopsworks
    import joblib
    import os
    from pandas_datareader import data as pdr
    import yfinance as yf
    import math
    import dataframe_image as dfi

    project = hopsworks.login()
    fs = project.get_feature_store()

    feature_group = fs.get_feature_group(name="btc_modal_2", version=1)

    # get model and make prediction for latest instance
    mr = project.get_model_registry()
    model = mr.get_model("btc_model", version=1)
    model_dir = model.download()
    model = joblib.load(model_dir + "/btc_model.pkl")
    
    start = datetime.datetime.today() - datetime.timedelta(days=9)

    yf.pdr_override()
    btc_df = pdr.get_data_yahoo('BTC-USD', start=start)
    
    actual_values = btc_df['Close']
    offset = 10
    X_pred = feature_group.read()
    
    X_pred = X_pred.sort_values(by=["date"], ascending=[True]).reset_index(drop=True)
    X_pred = X_pred.tail(offset)

    # predict and get latest (daily) feature
    y_pred = model.predict(X_pred.drop(columns=['close', 'date']))
    
    prices_df = pd.DataFrame(actual_values)
    prices_df['Prediction'] = y_pred
    
    err = mean_absolute_error(actual_values, y_pred)
    rmse = math.sqrt(err)
    print("RMSE: ", rmse)
    now = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    data = {
    'RMSE': [rmse],
    'date': [now],
    }
    monitor_df = pd.DataFrame(data)
    
    # create monitoring FG
    monitor_fg = fs.get_or_create_feature_group(name="rmse_history",
                                                version=1,
                                                primary_key=["date"],
                                                description="History of rmse")
    
    monitor_fg.insert(monitor_df, write_options={"wait_for_job": False})
    
    
    history_df = monitor_fg.read()
    
    dataset_api = project.get_dataset_api()
    dfi.export(history_df.tail(5), './df_btc_recent.png', table_conversion='matplotlib')
    dataset_api.upload("./df_btc_recent.png", "Resources/images", overwrite=True)
    
    ax = prices_df[['Close']].plot(figsize=(15,5))
    prices_df['Prediction'].plot(ax=ax)
    plt.legend(['Actual Data', 'Predictions'])
    ax.set_title('Actual Data and Predictions')
    plt.savefig("./df_btc_prediction.png")
    dataset_api.upload("./df_btc_prediction.png", "Resources/images", overwrite=True)


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