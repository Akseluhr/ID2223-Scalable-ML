import gradio as gr

import hopsworks
import joblib
import datetime
import yfinance as yf
from pandas_datareader import data as pdr

project = hopsworks.login()
fs = project.get_feature_store()

mr = project.get_model_registry()
model = mr.get_model("btc_model", version=1)
model_dir = model.download()
model = joblib.load(model_dir + "/btc_model.pkl")


def predict():
    today = get_date()

    yf.pdr_override()
    btc_df = pdr.get_data_yahoo('BTC-USD', start=today)
    btc_df.drop(columns=['Adj Close'], inplace=True)

    btc_df['Dayofyear'] = btc_df.index.dayofyear
    btc_df['Month'] = btc_df.index.month
    btc_df['Year'] = btc_df.index.year
    # btc_df['Date'] = btc_df.index.strftime('%Y-%m-%d %H:%M:%S')
    price = model.predict(btc_df.drop(columns=['Close']))[0]
    return [today, price]


def get_date():
    today = datetime.datetime.today()
    return today.date()


demo = gr.Interface(
    fn=predict,
    title="Bitcoin Closing Price Prediction",
    description="Daily Bitcoin closing price prediction",
    allow_flagging="never",
    inputs=[],
    outputs=[
        gr.Textbox(label="Date"),
        gr.Textbox(label="Predicted Closing price"),
    ]
)

demo.launch()
